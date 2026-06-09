from datetime import datetime
from util.conexao import Conexao
from flask import Flask, request, jsonify

from repositorio.hospede_repositorio_mysql  import HospedeRepositorioMySQL
from repositorio.quarto_repositorio_mysql   import QuartoRepositorioMySQL
from repositorio.reserva_repositorio_mysql  import ReservaRepositorioMySQL
from repositorio.usuario_repositorio_mysql  import UsuarioRepositorioMySQL
from command.criar_quarto_command           import CriarQuartoCommand
from controles.hospede_controle             import HospedeControle
from controles.quarto_controle              import QuartoControle
from controles.reserva_controle             import ReservaControle
from controles.autenticacao_controle        import AutenticacaoControle
from servico.servico_reserva                import ReservaServico
from servico.servico_validacao             import ValidacaoServico
from decorator.reserva_basica             import ReservaBasica
from decorator.servicos_extras            import CafeDaManha, Estacionamento, LateCheckout, TransferAeroporto

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response

@app.route("/", defaults={"path": ""}, methods=["OPTIONS"])
@app.route("/<path:path>", methods=["OPTIONS"])
def options_handler(path):
    return jsonify({}), 200



hospede_repo     = HospedeRepositorioMySQL()
quarto_repo      = QuartoRepositorioMySQL()
reserva_repo     = ReservaRepositorioMySQL()
usuario_repo     = UsuarioRepositorioMySQL()

criar_quarto_cmd = CriarQuartoCommand(quarto_repo)
reserva_servico  = ReservaServico(hospede_repo, quarto_repo, reserva_repo)

hospede_controle       = HospedeControle(hospede_repo)
quarto_controle        = QuartoControle(criar_quarto_cmd, quarto_repo)
reserva_controle       = ReservaControle(reserva_repo, reserva_servico, hospede_repo, quarto_repo)
autenticacao_controle  = AutenticacaoControle(usuario_repo)

print("API INICIOU")


@app.route("/hospedes", methods=["GET"])
def listar_hospedes():
    hospedes = hospede_controle.listar_hospedes()
    return jsonify([_hospede_dict(h) for h in hospedes])


@app.route("/hospedes", methods=["POST"])
def criar_hospede():
    d = request.json
    try:
        hospede = hospede_controle.criar_hospede(
            d["nome"], d["documento"], d["email"], d["telefone"],
            d["endereco"], d["cidade"], d["estado"], d["cep"],
            d["nacionalidade"], d["data_nascimento"]
        )
        senha = d.get("senha", "")
        if senha:
            import hashlib
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            from util.conexao import Conexao
            conn = Conexao.conectar()
            cur  = conn.cursor()
            cur.execute(
                """INSERT IGNORE INTO usuario
                   (nome, documento, email, senha, role, telefone, endereco,
                    cidade, estado, cep, nacionalidade, data_nascimento)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (d["nome"], d["documento"], d["email"], senha_hash, "hospede",
                 d.get("telefone",""), d.get("endereco",""), d.get("cidade",""),
                 d.get("estado",""), d.get("cep",""),
                 d.get("nacionalidade",""), d.get("data_nascimento",None))
            )
            conn.commit(); cur.close(); conn.close()
        return jsonify({"ok": True, "id": hospede.id})
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)}), 400


@app.route("/hospedes/<int:id>", methods=["PUT"])
def atualizar_hospede(id):
    d = request.json
    try:
        hospede_controle.atualizar_hospede(
            id,
            novo_email         = d.get("email"),
            novo_telefone      = d.get("telefone"),
            novo_endereco      = d.get("endereco"),
            novo_nome          = d.get("nome"),
            nova_cidade        = d.get("cidade"),
            novo_estado        = d.get("estado"),
            novo_cep           = d.get("cep"),
            nova_nacionalidade = d.get("nacionalidade"),
        )
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)}), 400


@app.route("/hospedes/<int:id>", methods=["DELETE"])
def deletar_hospede(id):
    try:
        hospede_controle.deletar_hospede(id)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)}), 400



@app.route("/quartos", methods=["GET"])
def listar_quartos():
    quartos = quarto_controle.listar_quartos()
    return jsonify([_quarto_dict(q) for q in quartos])




@app.route("/reservas", methods=["GET"])
def listar_reservas():
    reservas = reserva_controle.listar_reservas()
    return jsonify([_reserva_dict(r) for r in reservas])


@app.route("/reservas", methods=["POST"])
def criar_reserva():
    d = request.json
    try:
        check_in  = datetime.strptime(d["check_in"],  "%Y-%m-%d").date()
        check_out = datetime.strptime(d["check_out"], "%Y-%m-%d").date()

        servicos = d.get("servicos_extras", [])
        reserva = reserva_controle.criar_reserva(
            d["hospede_id"], d["quarto_id"],
            check_in, check_out,
            d.get("observacao", ""),
            d.get("forma_pagamento", "PIX")
        )
        if servicos:
            reserva_repo.atualizar_servicos(reserva.id, servicos)
        return jsonify({"ok": True, "id": reserva.id})
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"ok": False, "erro": str(e)}), 400


@app.route("/reservas/<int:id>", methods=["PUT"])
def atualizar_reserva(id):
    d = request.json
    try:
        check_in  = datetime.strptime(d["check_in"],  "%Y-%m-%d").date() if d.get("check_in")  else None
        check_out = datetime.strptime(d["check_out"], "%Y-%m-%d").date() if d.get("check_out") else None
        reserva_controle.atualizar_reserva(
            id,
            quarto_id     = d.get("quarto_id"),
            check_in      = check_in,
            check_out     = check_out,
            total_diarias = d.get("total_diarias"),
            valor_total   = d.get("valor_total"),
        )
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)}), 400


@app.route("/reservas/<int:id>", methods=["DELETE"])
def cancelar_reserva(id):
    try:
        reserva_controle.cancelar_reserva(id)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)}), 400



@app.route("/login", methods=["POST"])
def login():
    d = request.json
    try:
        usuario = autenticacao_controle.login(d["email"], d["senha"])
        hospede = hospede_repo.encontrar_por_email(d["email"]) if hasattr(hospede_repo, "encontrar_por_email") else None
        if not hospede:
            hospede = next((h for h in hospede_repo.listar() if h.email == d["email"]), None)
        hospede_id = hospede.id if hospede else None
        return jsonify({
            "ok": True,
            "id": hospede_id if hospede_id and usuario.role == "hospede" else usuario.id,
            "hospede_id": hospede_id,
            "nome": usuario.nome,
            "documento": usuario.documento,
            "email": usuario.email,
            "role": usuario.role,
            "telefone": usuario.telefone,
            "endereco": usuario.endereco,
            "cidade": usuario.cidade,
            "estado": usuario.estado,
            "cep": usuario.cep,
            "nacionalidade": usuario.nacionalidade,
            "data_nascimento": str(usuario.data_nascimento) if usuario.data_nascimento else ""
        })
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)}), 401


def _hospede_dict(h):
    return {
        "id": h.id, "nome": h.nome, "documento": h.documento,
        "email": h.email, "telefone": h.telefone, "endereco": h.endereco,
        "cidade": h.cidade, "estado": h.estado, "cep": h.cep,
        "nacionalidade": h.nacionalidade, "data_nascimento": str(h.data_nascimento)
    }

def _quarto_dict(q):
    return {
        "id": q.id, "numero": q.numero, "tipo": q.tipo_quarto.name,
        "preco": q.preco, "capacidade": q.capacidade,
        "descricao": q.descricao, "andar": q.andar,
        "tem_varanda": q.tem_varanda, "tem_banheira": q.tem_banheira,
        "area_m2": q.area_m2, "amenidades": q.amenidades
    }

def _reserva_dict(r):
    return {
        "id": r.id,
        "hospede_id": r.hospede.id, "hospede_nome": r.hospede.nome,
        "hospede_email": r.hospede.email or "",
        "hospede_telefone": r.hospede.telefone or "",
        "hospede_documento": r.hospede.documento or "",
        "hospede_endereco": r.hospede.endereco or "",
        "hospede_cidade": r.hospede.cidade or "",
        "hospede_estado": r.hospede.estado or "",
        "hospede_cep": r.hospede.cep or "",
        "hospede_nacionalidade": r.hospede.nacionalidade or "",
        "hospede_data_nascimento": str(r.hospede.data_nascimento) if r.hospede.data_nascimento else "",
        "quarto_id": r.quarto.id,   "quarto_numero": r.quarto.numero,
        "check_in": str(r.check_in), "check_out": str(r.check_out),
        "status": r.status.value,
        "total_diarias": r.total_diarias,
        "valor_total": float(r.valor_total),
        "observacao": r.observacao,
        "forma_pagamento": r.forma_pagamento,
        "servicos_extras": getattr(r, "_servicos_extras", [])
    }



@app.route("/validar/hospede", methods=["POST"])
def validar_hospede():
    erros = ValidacaoServico.validar_hospede(request.json or {})
    if erros:
        return jsonify({"ok": False, "erros": erros}), 400
    return jsonify({"ok": True})


@app.route("/validar/reserva", methods=["POST"])
def validar_reserva():
    erros = ValidacaoServico.validar_reserva(request.json or {})
    if erros:
        return jsonify({"ok": False, "erros": erros}), 400
    return jsonify({"ok": True})


@app.route("/calcular/diarias", methods=["POST"])
def calcular_diarias():
    d = request.json or {}
    try:
        ci = datetime.strptime(d["check_in"],  "%Y-%m-%d").date()
        co = datetime.strptime(d["check_out"], "%Y-%m-%d").date()
        noites = (co - ci).days
        if noites <= 0:
            return jsonify({"ok": False, "erro": "Check-out deve ser após o check-in"}), 400
        preco = float(d.get("preco_noite", 0))
        return jsonify({"ok": True, "noites": noites, "total": noites * preco})
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)}), 400


@app.route("/reservas/com-hospede", methods=["POST"])
def criar_reserva_com_hospede():
    d = request.json or {}
    try:
        erros_h = ValidacaoServico.validar_hospede(d.get("hospede", {}))
        if erros_h:
            return jsonify({"ok": False, "erros": erros_h}), 400

        hospede = hospede_controle.criar_hospede(
            d["hospede"]["nome"],        d["hospede"]["documento"],
            d["hospede"]["email"],       d["hospede"]["telefone"],
            d["hospede"]["endereco"],    d["hospede"]["cidade"],
            d["hospede"]["estado"],      d["hospede"]["cep"],
            d["hospede"]["nacionalidade"], d["hospede"]["data_nascimento"]
        )

        check_in  = datetime.strptime(d["check_in"],  "%Y-%m-%d").date()
        check_out = datetime.strptime(d["check_out"], "%Y-%m-%d").date()
        reserva = reserva_controle.criar_reserva(
            hospede.id, d["quarto_id"],
            check_in, check_out,
            d.get("observacao", ""),
            d.get("forma_pagamento", "PIX")
        )
        return jsonify({"ok": True, "hospede_id": hospede.id, "reserva_id": reserva.id})
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)}), 400


SERVICOS_DISPONIVEIS = {
    "cafe_da_manha":     {"decorator": CafeDaManha,       "descricao": "Café da manhã",    "preco": 50.0},
    "estacionamento":    {"decorator": Estacionamento,    "descricao": "Estacionamento",   "preco": 30.0},
    "late_checkout":     {"decorator": LateCheckout,      "descricao": "Late check-out",   "preco": 80.0},
    "transfer_aeroporto":{"decorator": TransferAeroporto, "descricao": "Transfer aeroporto","preco": 120.0},
}


@app.route("/servicos/disponiveis", methods=["GET"])
def listar_servicos():
    """Retorna os serviços extras disponíveis para decorar uma reserva."""
    return jsonify([
        {"id": k, "descricao": v["descricao"], "preco": v["preco"]}
        for k, v in SERVICOS_DISPONIVEIS.items()
    ])


@app.route("/reservas/<int:reserva_id>/calcular-servicos", methods=["POST"])
def calcular_servicos(reserva_id):
    reserva = reserva_controle.buscar_por_id(reserva_id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    servicos_selecionados = request.json.get("servicos", [])

    pedido = ReservaBasica(reserva)

    for s in servicos_selecionados:
        if s in SERVICOS_DISPONIVEIS:
            decorator_class = SERVICOS_DISPONIVEIS[s]["decorator"]
            pedido = decorator_class(pedido)

    return jsonify({
        "reserva_id":  reserva_id,
        "descricao":   pedido.get_descricao(),
        "custo_total": pedido.custo(),
        "servicos_aplicados": servicos_selecionados
    })


@app.route("/reservas/<int:reserva_id>/servicos", methods=["PUT"])
def atualizar_servicos_reserva(reserva_id):
    
    reserva = reserva_repo.encontrar_por_id(reserva_id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    servicos = request.json.get("servicos", [])


    pedido = ReservaBasica(reserva)
    for s in servicos:
        if s in SERVICOS_DISPONIVEIS:
            pedido = SERVICOS_DISPONIVEIS[s]["decorator"](pedido)
                
    reserva_repo.atualizar_servicos(reserva_id, servicos, novo_valor_total=pedido.custo())



    custo_total = pedido.custo()


    return jsonify({
        "ok": True,
        "reserva_id": reserva_id,
        "servicos": servicos,
        "descricao": pedido.get_descricao(),
        "custo_total": pedido.custo()
    })


if __name__ == "__main__":
    print("API rodando em http://localhost:5000")
    app.run(debug=True, port=5000)
