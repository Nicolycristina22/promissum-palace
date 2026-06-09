# 🏨 Promissum Palace — Hotel Management System

> Sistema de gerenciamento hoteleiro desenvolvido como projeto final da disciplina **Padrões de Projeto (PP) — 5B Engenharia de Software**.  
> Aplica os padrões **Builder, Factory, Command e Decorator**, os princípios **SOLID/DIP/Liskov**, arquitetura em camadas e REST API com Flask + MySQL.

---

## 📑 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Padrões de Projeto Aplicados](#-padrões-de-projeto-aplicados)
- [Princípios SOLID](#-princípios-solid)
- [Arquitetura em Camadas](#-arquitetura-em-camadas)
- [Entidades e Relacionamentos](#-entidades-e-relacionamentos)
- [Funcionalidades](#-funcionalidades)
- [API REST — Endpoints](#-api-rest--endpoints)
- [Diagramas](#-diagramas)
- [Testes Automatizados](#-testes-automatizados)
- [Como Executar](#-como-executar)
- [Tecnologias](#-tecnologias)
- [Integrantes do Grupo](#-integrantes-do-grupo)

---

## 🎯 Sobre o Projeto

O **Promissum Palace** é um sistema web completo de gerenciamento hoteleiro que permite:

- Cadastrar e gerenciar **hóspedes**, **quartos** e **reservas**
- Aplicar **serviços extras** à reserva via padrão Decorator (café da manhã, estacionamento, late check-out, transfer)
- Autenticação de usuários com **hash SHA-256** (sem bibliotecas externas)
- Verificação de **disponibilidade de quartos** em tempo real
- Interface web integrada (HTML + CSS + JS vanilla) consumindo a API Flask

---

## 🧩 Padrões de Projeto Aplicados

### 1. Builder
Utilizado para construção de objetos complexos com validação centralizada. Impede instanciação direta das entidades de domínio.

| Builder | Cria |
|---|---|
| `HospedeBuilder` | `Hospede` — valida CPF/CNPJ, e-mail, telefone, campos obrigatórios |
| `QuartoBuilder` | `Quarto` — valida número, tipo, preço, área |
| `ReservaBuilder` | `Reserva` — calcula total de diárias e valor automaticamente |

```python
# Exemplo de uso do HospedeBuilder
hospede = (
    HospedeBuilder()
    .set_nome("João Silva")
    .set_documento("123.456.789-09")
    .set_email("joao@email.com")
    .set_telefone("(11) 99999-0000")
    .set_cidade("São Paulo")
    .set_estado("SP")
    .set_cep("01310-100")
    .set_nacionalidade("Brasileiro")
    .set_data_nascimento("1990-05-15")
    .build()   # lança ValueError se qualquer validação falhar
)
```

### 2. Factory
`ReservaFactory` centraliza a criação de reservas, calculando automaticamente o número de diárias e o valor total com base no preço do quarto.

```python
reserva = ReservaFactory.criar_reserva(
    hospede, quarto,
    check_in=date(2025, 6, 10),
    check_out=date(2025, 6, 15),
    forma_pagamento="PIX"
)
# valor_total calculado automaticamente: 5 diárias × preço do quarto
```

### 3. Command
Padrão Command aplicado à criação de quartos. `QuartoCommand` é a interface abstrata; `CriarQuartoCommand` é o executor concreto que recebe o repositório por injeção de dependência.

```
QuartoCommand  (ABC)
    └── CriarQuartoCommand
            ├── validar parâmetros
            ├── criar Quarto via Quarto._criar(...)
            └── persistir via quarto_repo.salvar(quarto)
```

### 4. Decorator ⭐ (obrigatório)
Implementado **sem uso de pacotes de linguagem**, exatamente conforme o padrão estudado em sala.  
Permite adicionar serviços extras a uma reserva de forma composicional, alterando descrição e custo total.

```
ServicoReserva          ← Component (interface/ABC)
    ├── ReservaBasica   ← ConcreteComponent
    └── ServicoDecorator  ← Decorator (ABC)
            ├── CafeDaManha       (+R$ 50,00)
            ├── Estacionamento    (+R$ 30,00)
            ├── LateCheckout      (+R$ 80,00)
            └── TransferAeroporto (+R$120,00)
```

```python
# Composição de serviços extras — padrão Decorator em ação
servico = ReservaBasica(reserva)
servico = CafeDaManha(servico)
servico = Estacionamento(servico)
servico = LateCheckout(servico)

print(servico.get_descricao())
# "Quarto 101 (3 diária(s)), Café da manhã, Estacionamento, Late check-out"
print(servico.custo())
# valor_base + 50 + 30 + 80
```

---

## 🔷 Princípios SOLID

| Princípio | Onde é aplicado |
|---|---|
| **S** — Single Responsibility | Cada classe tem uma única responsabilidade: `Hospede` só representa dados; `HospedeControle` só orquestra; `HospedeRepositorioMySQL` só persiste |
| **O** — Open/Closed | Novos serviços extras são adicionados criando um novo Decorator, sem alterar os existentes |
| **L** — Liskov | `HospedeRepositorioMySQL` é substituível por qualquer outra implementação de `HospedeRepositorioInterface` sem quebrar o sistema |
| **I** — Interface Segregation | Interfaces separadas por entidade: `HospedeRepositorioInterface`, `QuartoRepositorioInterface`, `ReservaRepositorioInterface`, `UsuarioRepositorioInterface` |
| **D** — Dependency Inversion | Controles e serviços dependem das **interfaces**, não das implementações concretas MySQL |

---

## 🏗️ Arquitetura em Camadas

```
promissum/
│
├── dominio/                  ← Entidades de negócio (Hospede, Quarto, Reserva, Usuario)
├── interfaces/               ← Contratos / Interfaces dos repositórios (DIP)
├── repositorio/              ← Implementações MySQL (HospedeRepositorioMySQL, ...)
├── servico/                  ← Regras de negócio (ReservaServico, AutenticacaoServico)
├── controles/                ← Orquestração: recebem dados, chamam serviços (Flask glue)
├── builder/                  ← Padrão Builder (HospedeBuilder, QuartoBuilder, ReservaBuilder)
├── factory/                  ← Padrão Factory (ReservaFactory)
├── command/                  ← Padrão Command (QuartoCommand, CriarQuartoCommand)
├── decorator/                ← Padrão Decorator (ServicoReserva, ReservaBasica, extras)
├── util/                     ← Utilitários (Conexao MySQL)
├── tests/                    ← Testes automatizados (pytest)
├── Front/                    ← Frontend (index.html, styles.css, script.js)
├── api.py                    ← Servidor Flask / REST API
├── banco.sql                 ← Script de criação do banco de dados
└── main.py                   ← Entrypoint alternativo / demonstração em console
```

---

## 🗂️ Entidades e Relacionamentos

### Hospede (11 atributos)
`id`, `nome`, `documento`, `email`, `telefone`, `endereco`, `cidade`, `estado`, `cep`, `nacionalidade`, `data_nascimento`

### Quarto (11 atributos)
`id`, `numero`, `tipo_quarto` (Standard/Luxo/Suíte), `preco`, `capacidade`, `descricao`, `andar`, `tem_varanda`, `tem_banheira`, `area_m2`, `amenidades`

### Reserva (10 atributos)
`id`, `hospede_id`, `quarto_id`, `check_in`, `check_out`, `status`, `total_diarias`, `valor_total`, `observacao`, `forma_pagamento`

### Usuario (13 atributos)
`id`, `nome`, `documento`, `email`, `senha_hash`, `role`, `telefone`, `endereco`, `cidade`, `estado`, `cep`, `nacionalidade`, `data_nascimento`


---

## ⚙️ Funcionalidades

| Funcionalidade | Entidade | Padrão |
|---|---|---|
| Cadastrar hóspede | Hospede | Builder |
| Atualizar hóspede | Hospede | — |
| Deletar hóspede | Hospede | — |
| Listar hóspedes | Hospede | — |
| Criar quarto | Quarto | Command |
| Listar quartos | Quarto | — |
| Criar reserva | Reserva | Factory |
| Atualizar reserva | Reserva | — |
| Cancelar/deletar reserva | Reserva | — |
| Listar reservas | Reserva | — |
| Calcular serviços extras | Reserva | **Decorator** |
| Salvar serviços na reserva | Reserva | **Decorator** |
| Login com hash SHA-256 | Usuario | — |
| Validar dados de hóspede | — | Serviço de validação |
| Calcular total de diárias | — | Factory automática |
| Verificar disponibilidade de quarto | Reserva | Serviço de negócio |

---

## 🌐 API REST — Endpoints

### Hóspedes
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/hospedes` | Listar todos os hóspedes |
| `POST` | `/hospedes` | Cadastrar hóspede |
| `PUT` | `/hospedes/<id>` | Atualizar hóspede |
| `DELETE` | `/hospedes/<id>` | Deletar hóspede |

### Quartos
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/quartos` | Listar todos os quartos |

### Reservas
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/reservas` | Listar todas as reservas |
| `POST` | `/reservas` | Criar reserva |
| `PUT` | `/reservas/<id>` | Atualizar reserva |
| `DELETE` | `/reservas/<id>` | Cancelar/deletar reserva |
| `POST` | `/reservas/com-hospede` | Criar hóspede e reserva num único fluxo |
| `POST` | `/reservas/<id>/calcular-servicos` | Calcular custo com Decorator |
| `PUT` | `/reservas/<id>/servicos` | Salvar serviços extras da reserva |

### Autenticação e Utilitários
| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/login` | Login (SHA-256, sem JWT externo) |
| `POST` | `/validar/hospede` | Validar dados de hóspede |
| `POST` | `/validar/reserva` | Validar datas de reserva |
| `POST` | `/calcular/diarias` | Calcular número de diárias |
| `GET` | `/servicos/disponiveis` | Listar serviços extras disponíveis |

---

## 📐 Diagramas

Os diagramas estão disponíveis no arquivo [`diagrama_promissum.drawio`](diagrama_promissum.drawio) (abrível em [draw.io](https://app.diagrams.net/)) e contêm:

- **Diagrama de Classes** — todas as classes, atributos, métodos e relacionamentos organizados por camada
- **Diagrama de Sequência — Criar Reserva** — fluxo completo desde o usuário até o banco de dados
- **Diagrama de Sequência — Login** — fluxo de autenticação com hash SHA-256

---

## 🧪 Testes Automatizados

Testes implementados com **pytest**, cobrindo os três padrões principais:

```
tests/
├── test_builder.py                  ← HospedeBuilder e QuartoBuilder
├── test_decorator.py                ← Decorator: CafeDaManha, Estacionamento, LateCheckout, Transfer
└── test_factory_e_autenticacao.py   ← ReservaFactory e AutenticacaoServico
```

Para executar todos os testes:

```bash
pytest tests/ -v
```

Exemplos de casos cobertos:
- Builder rejeita dados inválidos (CPF com formato errado, e-mail sem @, etc.)
- Decorator acumula corretamente custo e descrição em qualquer ordem de composição
- Factory calcula valor total corretamente com base nas diárias
- Autenticação rejeita senha incorreta e aceita senha correta (SHA-256)

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- MySQL (porta padrão 3306 ou 3309)
- pip

### 1. Clonar o repositório

```bash
git clone https://github.com/<seu-usuario>/promissum-palace.git
cd promissum-palace
```

### 2. Instalar dependências

```bash
pip install flask mysql-connector-python pytest
```

### 3. Configurar o banco de dados

```bash
# Abrir o MySQL e executar o script:
mysql -u root -p < banco.sql
```

> Credenciais padrão do banco estão em `util/conexao.py`.  
> Edite `host`, `user`, `password` e `port` conforme seu ambiente.

### 4. Iniciar a API

```bash
python api.py
```

A API estará disponível em `http://localhost:5000`.

### 5. Abrir o frontend

Abra o arquivo `Front/index.html` diretamente no navegador.  
O frontend faz chamadas para `http://localhost:5000`.

### 6. Usuários de teste (já inseridos pelo `banco.sql`)

| E-mail | Senha | Role |
|---|---|---|
| `gerente@promissum.com` | `1234` | gerente |
| `funcionario@promissum.com` | `1234` | funcionario |

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python 3, Flask |
| Banco de dados | MySQL |
| Frontend | HTML5, CSS3, JavaScript  |
| Testes | pytest |
| Diagramas | draw.io |
| Versionamento | Git / GitHub |

---

