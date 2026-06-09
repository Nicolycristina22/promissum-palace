import re
from datetime import datetime


class ValidacaoServico:

    @staticmethod
    def validar_email(email: str) -> bool:
        return bool(re.match(r'^[\w\.\-]+@[\w\.\-]+\.\w+$', email.strip()))

    @staticmethod
    def validar_documento(documento: str) -> bool:
        apenas_digitos = re.sub(r'[.\-/]', '', documento)
        return apenas_digitos.isdigit() and len(apenas_digitos) in (11, 14)

    @staticmethod
    def validar_data_nascimento(data: str) -> bool:
        for fmt in ('%d/%m/%Y', '%Y-%m-%d'):
            try:
                dt = datetime.strptime(data.strip(), fmt)
                return 1900 <= dt.year <= datetime.now().year
            except ValueError:
                continue
        return False

    @staticmethod
    def validar_cep(cep: str) -> bool:
        return bool(re.match(r'^\d{5}-?\d{3}$', cep.strip()))

    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        return len(re.sub(r'\D', '', telefone)) >= 8

    @staticmethod
    def validar_hospede(dados: dict) -> list:
        erros = []
        nome = dados.get('nome', '').strip()
        if not nome or len(nome) < 3:
            erros.append('Nome deve ter no mínimo 3 caracteres')
        if not ValidacaoServico.validar_documento(dados.get('documento', '')):
            erros.append('Documento inválido: CPF (11 dígitos) ou CNPJ (14 dígitos)')
        if not ValidacaoServico.validar_email(dados.get('email', '')):
            erros.append('E-mail inválido')
        if not ValidacaoServico.validar_telefone(dados.get('telefone', '')):
            erros.append('Telefone inválido: mínimo 8 dígitos')
        end = dados.get('endereco', '').strip()
        if not end or len(end) < 3:
            erros.append('Endereço muito curto')
        cidade = dados.get('cidade', '').strip()
        if not cidade or len(cidade) < 2:
            erros.append('Cidade inválida')
        estado = dados.get('estado', '').strip()
        if not estado or len(estado) != 2:
            erros.append('Estado inválido: use a sigla UF (ex: SP)')
        if not ValidacaoServico.validar_cep(dados.get('cep', '')):
            erros.append('CEP inválido: use o formato 00000-000')
        nac = dados.get('nacionalidade', '').strip()
        if not nac or len(nac) < 2:
            erros.append('Nacionalidade inválida')
        if not ValidacaoServico.validar_data_nascimento(dados.get('data_nascimento', '')):
            erros.append('Data de nascimento inválida')
        return erros

    @staticmethod
    def validar_reserva(dados: dict) -> list:
        erros = []
        ci = dados.get('check_in', '')
        co = dados.get('check_out', '')
        if not ci:
            erros.append('Data de check-in obrigatória')
        if not co:
            erros.append('Data de check-out obrigatória')
        if ci and co:
            try:
                dt_ci = datetime.strptime(ci, '%Y-%m-%d')
                dt_co = datetime.strptime(co, '%Y-%m-%d')
                if dt_co <= dt_ci:
                    erros.append('Check-out deve ser após o check-in')
            except ValueError:
                erros.append('Formato de data inválido: use AAAA-MM-DD')
        if not dados.get('hospede_id'):
            erros.append('Hóspede obrigatório')
        if not dados.get('quarto_id'):
            erros.append('Quarto obrigatório')
        return erros
