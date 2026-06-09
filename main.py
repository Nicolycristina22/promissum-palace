from datetime import datetime


from repositorio.hospede_repositorio_mysql import HospedeRepositorioMySQL
from repositorio.quarto_repositorio_mysql import QuartoRepositorioMySQL
from repositorio.reserva_repositorio_mysql import ReservaRepositorioMySQL


from command.criar_quarto_command import CriarQuartoCommand

from controles.hospede_controle import HospedeControle
from controles.quarto_controle import QuartoControle
from controles.reserva_controle import ReservaControle

from servico.servico_reserva import ReservaServico



hospede_repo  = HospedeRepositorioMySQL()
quarto_repo   = QuartoRepositorioMySQL()
reserva_repo  = ReservaRepositorioMySQL()

criar_quarto_cmd = CriarQuartoCommand(quarto_repo)

reserva_servico = ReservaServico(hospede_repo, quarto_repo, reserva_repo)

hospede_controle = HospedeControle(hospede_repo)
quarto_controle  = QuartoControle(criar_quarto_cmd, quarto_repo)
reserva_controle = ReservaControle(reserva_repo, reserva_servico, hospede_repo, quarto_repo)



def menu():
    print("\n╔══════════════════════════════╗")
    print("║      PROMISSUM PALACE        ║")
    print("╠══════════════════════════════╣")
    print("║  HÓSPEDES                    ║")
    print("║   1 - Cadastrar hóspede      ║")
    print("║   2 - Buscar hóspede por ID  ║")
    print("║   3 - Atualizar hóspede      ║")
    print("║   4 - Deletar hóspede        ║")
    print("║   5 - Listar hóspedes        ║")
    print("╠══════════════════════════════╣")
    print("║  QUARTOS                     ║")
    print("║   6 - Cadastrar quarto       ║")
    print("║   7 - Buscar quarto por ID   ║")
    print("║   8 - Atualizar quarto       ║")
    print("║   9 - Deletar quarto         ║")
    print("║  10 - Listar quartos         ║")
    print("╠══════════════════════════════╣")
    print("║  RESERVAS                    ║")
    print("║  11 - Criar reserva          ║")
    print("║  12 - Buscar reserva por ID  ║")
    print("║  13 - Cancelar reserva       ║")
    print("║  14 - Deletar reserva        ║")
    print("║  15 - Listar reservas        ║")
    print("║  16 - Reservas por hóspede   ║")
    print("╠══════════════════════════════╣")
    print("║   0 - Sair                   ║")
    print("╚══════════════════════════════╝")



while True:
    menu()
    opcao = input("\nEscolha uma opção: ").strip()

    try:


        if opcao == "1":
            print("\n── Cadastrar Hóspede ──")
            nome            = input("Nome completo: ")
            documento       = input("CPF (000.000.000-00) ou CNPJ: ")
            email           = input("E-mail: ")
            telefone        = input("Telefone: ")
            endereco        = input("Endereço (rua e número): ")
            cidade          = input("Cidade: ")
            estado          = input("Estado (UF): ")
            cep             = input("CEP: ")
            nacionalidade   = input("Nacionalidade: ")
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")

            hospede = hospede_controle.criar_hospede(
                nome, documento, email, telefone,
                endereco, cidade, estado, cep,
                nacionalidade, data_nascimento
            )
            print(f"\n✔ Hóspede cadastrado! ID: {hospede.id}")

        elif opcao == "2":
            print("\n── Buscar Hóspede por ID ──")
            hid = input("ID do hóspede: ")
            h = hospede_controle.buscar_por_id(hid)
            print(f"\n  ID: {h.id}")
            print(f"  Nome: {h.nome}")
            print(f"  Documento: {h.documento}")
            print(f"  E-mail: {h.email}")
            print(f"  Telefone: {h.telefone}")
            print(f"  Endereço: {h.endereco}")
            print(f"  Cidade/UF: {h.cidade} - {h.estado}")
            print(f"  CEP: {h.cep}")
            print(f"  Nacionalidade: {h.nacionalidade}")
            print(f"  Nascimento: {h.data_nascimento}")

        elif opcao == "3":
            print("\n── Atualizar Hóspede ──")
            hid = input("ID do hóspede: ")
            print("(Deixe em branco para não alterar)")
            novo_email    = input("Novo e-mail: ").strip() or None
            novo_telefone = input("Novo telefone: ").strip() or None
            novo_endereco = input("Novo endereço: ").strip() or None
            hospede_controle.atualizar_hospede(hid, novo_email, novo_telefone, novo_endereco)
            print("✔ Hóspede atualizado com sucesso!")

        elif opcao == "4":
            print("\n── Deletar Hóspede ──")
            hid = input("ID do hóspede: ")
            hospede_controle.deletar_hospede(hid)
            print("✔ Hóspede deletado com sucesso!")

        elif opcao == "5":
            hospedes = hospede_controle.listar_hospedes()
            print(f"\n── Hóspedes cadastrados ({len(hospedes)}) ──")
            if not hospedes:
                print("  Nenhum hóspede cadastrado.")
            for h in hospedes:
                print(f"  [{h.id}] {h.nome} | {h.documento} | {h.email} | {h.cidade}-{h.estado}")


        elif opcao == "6":
            print("\n── Cadastrar Quarto ──")
            numero       = int(input("Número do quarto: "))
            tipo         = input("Tipo (STANDARD / LUXO / SUITE): ").strip().upper()
            preco        = float(input("Preço por noite (R$): "))
            capacidade   = int(input("Capacidade (pessoas): "))
            descricao    = input("Descrição: ")
            andar        = int(input("Andar: "))
            tem_varanda  = input("Tem varanda? (s/n): ").strip().lower() == "s"
            tem_banheira = input("Tem banheira? (s/n): ").strip().lower() == "s"
            area_m2      = float(input("Área (m²): "))
            amenidades   = input("Amenidades (ex: Wi-Fi, TV, Frigobar): ")

            quarto = quarto_controle.criar_quarto(
                numero, tipo, preco, capacidade, descricao,
                andar, tem_varanda, tem_banheira, area_m2, amenidades
            )
            print(f"\n✔ Quarto cadastrado! ID: {quarto.id}")

        elif opcao == "7":
            print("\n── Buscar Quarto por ID ──")
            qid = input("ID do quarto: ")
            q = quarto_controle.buscar_por_id(qid)
            print(f"\n  ID: {q.id}")
            print(f"  Número: {q.numero} | Andar: {q.andar}")
            print(f"  Tipo: {q.tipo_quarto.value}")
            print(f"  Preço: R$ {q.preco:.2f}/noite")
            print(f"  Capacidade: {q.capacidade} pessoa(s)")
            print(f"  Área: {q.area_m2} m²")
            print(f"  Varanda: {'Sim' if q.tem_varanda else 'Não'} | Banheira: {'Sim' if q.tem_banheira else 'Não'}")
            print(f"  Descrição: {q.descricao}")
            print(f"  Amenidades: {q.amenidades}")

        elif opcao == "8":
            print("\n── Atualizar Quarto ──")
            qid = input("ID do quarto: ")
            print("(Deixe em branco para não alterar)")
            novo_preco_str = input("Novo preço (R$): ").strip()
            nova_descricao = input("Nova descrição: ").strip() or None
            novo_preco = float(novo_preco_str) if novo_preco_str else None
            quarto_controle.atualizar_quarto(qid, novo_preco, nova_descricao)
            print("✔ Quarto atualizado com sucesso!")

        elif opcao == "9":
            print("\n── Deletar Quarto ──")
            qid = input("ID do quarto: ")
            quarto_controle.deletar_quarto(qid)
            print("✔ Quarto deletado com sucesso!")

        elif opcao == "10":
            quartos = quarto_controle.listar_quartos()
            print(f"\n── Quartos cadastrados ({len(quartos)}) ──")
            if not quartos:
                print("  Nenhum quarto cadastrado.")
            for q in quartos:
                print(f"  [{q.id}] Nº{q.numero} | {q.tipo_quarto.value} | R${q.preco:.2f}/noite | {q.area_m2}m² | Cap:{q.capacidade}")


        elif opcao == "11":
            print("\n── Criar Reserva ──")
            hospede_id     = input("ID do hóspede: ")
            quarto_id      = input("ID do quarto: ")
            check_in       = datetime.strptime(input("Check-in (AAAA-MM-DD): "), "%Y-%m-%d").date()
            check_out      = datetime.strptime(input("Check-out (AAAA-MM-DD): "), "%Y-%m-%d").date()
            observacao     = input("Observação (opcional): ").strip()
            forma_pagamento = input("Forma de pagamento (PIX / Cartão / Dinheiro) [PIX]: ").strip() or "PIX"

            reserva = reserva_controle.criar_reserva(
                hospede_id, quarto_id, check_in, check_out,
                observacao, forma_pagamento
            )
            print(f"\n✔ Reserva criada! ID: {reserva.id}")
            print(f"   Diárias: {reserva.total_diarias} | Total: R$ {reserva.valor_total:.2f}")

        elif opcao == "12":
            print("\n── Buscar Reserva por ID ──")
            rid = input("ID da reserva: ")
            r = reserva_controle.buscar_por_id(rid)
            print(f"\n  ID: {r.id}")
            print(f"  Hóspede: [{r.hospede.id}] {r.hospede.nome}")
            print(f"  Quarto: [{r.quarto.id}] Nº{r.quarto.numero} - {r.quarto.tipo_quarto.value}")
            print(f"  Check-in: {r.check_in}  →  Check-out: {r.check_out}")
            print(f"  Diárias: {r.total_diarias} | Valor total: R$ {r.valor_total:.2f}")
            print(f"  Forma de pagamento: {r.forma_pagamento}")
            print(f"  Observação: {r.observacao or '—'}")
            print(f"  Status: {r.status.value}")

        elif opcao == "13":
            print("\n── Cancelar Reserva ──")
            rid = input("ID da reserva: ")
            reserva_controle.cancelar_reserva(rid)
            print("✔ Reserva cancelada!")

        elif opcao == "14":
            print("\n── Deletar Reserva ──")
            rid = input("ID da reserva: ")
            reserva_controle.deletar_reserva(rid)
            print("✔ Reserva deletada com sucesso!")

        elif opcao == "15":
            reservas = reserva_controle.listar_reservas()
            print(f"\n── Todas as Reservas ({len(reservas)}) ──")
            if not reservas:
                print("  Nenhuma reserva cadastrada.")
            for r in reservas:
                print(f"  [{r.id}] {r.hospede.nome} | Qto Nº{r.quarto.numero} | "
                      f"{r.check_in} → {r.check_out} | "
                      f"R${r.valor_total:.2f} | {r.forma_pagamento} | {r.status.value}")

        elif opcao == "16":
            print("\n── Reservas por Hóspede (1:N) ──")
            hid = input("ID do hóspede: ")
            h = hospede_controle.buscar_por_id(hid)
            reservas = reserva_controle.listar_reservas_por_hospede(hid)
            print(f"\n  Hóspede: {h.nome}")
            print(f"  Total de reservas: {len(reservas)}")
            if not reservas:
                print("  Nenhuma reserva encontrada.")
            for r in reservas:
                print(f"    [{r.id}] Qto Nº{r.quarto.numero} | {r.check_in} → {r.check_out} | "
                      f"R${r.valor_total:.2f} | {r.status.value}")

        elif opcao == "0":
            print("\nEncerrando o sistema. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")

    except Exception as e:
        print(f"\n✖ Erro: {e}")
