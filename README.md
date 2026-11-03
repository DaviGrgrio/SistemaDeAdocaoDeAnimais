# SistemaDeAdocaoDeAnimais CLI

Este repositório contém a modelagem e implementação orientada a objetos do **Sistema de Adoção de Animais**, desenvolvido para automatizar e organizar os processos de triagem, reserva e adoção em abrigos de animais.

---

## 🎯 Objetivos do Projeto

- **Organização do Fluxo de Adoção:** Gerenciar desde o cadastro do animal até a emissão do contrato final.
- **Modelagem Orientada a Objetos:** Aplicar conceitos fundamentais de POO (Abstração, Encapsulamento, Herança, Polimorfismo e Composição/Mixins).
- **Garantia de Regras de Negócio:** Validar a elegibilidade de adotantes e controlar prazos de reserva e status dos animais.

---

## 🏗️ Estrutura de Classes e Arquitetura

O sistema é construído a partir das seguintes entidades principais:

- **`Pessoa` (Classe Abstrata):** Base para entidades humanas no sistema.
  - **`Adotante`:** Herda de `Pessoa`. Armazena dados de perfil (tipo de moradia, presença de crianças, outros animais) e contém o método `validar_elegibilidade()`.
- **`Animal` (Classe Abstrata):** Base para todos os animais do abrigo.
  - Atributos principais: `id_animal`, `nome`, `sexo` (`SexoAnimal`), `idade_meses`, `porte`, `temperamento` e `status` (`StatusAnimal`).
  - Subclasses concretas: **`Cachorro`** e **`Gato`**.
- **Mixins (Comportamentos Reutilizáveis):**
  - **`VacinavelMixin`:** Adiciona histórico e métodos de vacinação (`Cachorro` e `Gato`).
  - **`AdestravelMixin`:** Adiciona gestão de nível de adestramento e treino (exclusivo para `Cachorro`).
- **`Reserva`:** Representa o bloqueio temporário de um animal por um adotante antes do contrato final.
- **`ContratoAdocao`:** Formaliza o processo de adoção, registrando datas, termos e taxas aplicadas.

---

## 📂 Organização do Repositório

```text
.
├── docs/
│   └── UML.md         # Diagrama de classes formal em sintaxe Mermaid
├── models/            # Módulo contendo as classes e domínio OO
│   ├── __init__.py
│   ├── pessoa.py
│   ├── animal.py
│   ├── adotante.py
│   ├── cachorro.py
│   ├── gato.py
│   └── mixins.py
├── .gitignore         
└── README.md          # Documentação principal
```

---

## 📊 Diagrama UML

O diagrama de classes completo do sistema está documentado utilizando o padrão Mermaid.js.

**[UML Completo](./docs/UML.md)**
---

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Modelagem:** UML 2.5 / Mermaid.js
- **Controle de Versão:** Git / GitHub


## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 adocao.py seed          # dados de exemplo em data/
python3 adocao.py --help
pytest -v
```

## Comandos

```bash
python3 adocao.py listar
python3 adocao.py cadastrar-animal --tipo cachorro --nome Bidu --sexo MACHO --idade-meses 18 --porte M --raca SRD --passeio media
python3 adocao.py cadastrar-adotante --nome Carlos --idade 40 --moradia casa --area 120 --experiencia
python3 adocao.py reservar --animal 1 --adotante 1
python3 adocao.py fila --animal 1 --adotante 2
python3 adocao.py adotar --animal 1 --adotante 1
python3 adocao.py devolver --animal 1 --motivo "mudança de cidade" --problema-saude
python3 adocao.py reavaliar --animal 1 --status DISPONIVEL
python3 adocao.py rodar-expiracao
python3 adocao.py relatorio top        # disponiveis | top | taxas | tempo | devolucoes
```

## Estrutura

```
adocao.py, cli.py        entrada e subcomandos da CLI
servico.py               regras de negócio (reserva, adoção, fila, devolução)
config.py, settings.json políticas configuráveis
politicas.py             validação de elegibilidade
compatibilidade.py       pontuação adotante-animal (0-100)
taxas.py                 Strategy de taxas
fila.py                  fila de espera priorizada
relatorios.py            relatórios
seed.py                  dados de exemplo
models/                  Animal, Cachorro, Gato, Pessoa, Adotante, mixins, exceções
repositories/            persistência em JSON
tests/                   testes com pytest
```

## Diagrama simples

```
Animal (abstrata) <- Cachorro (+VacinavelMixin, AdestravelMixin)
                  <- Gato (+VacinavelMixin)
Pessoa <- Adotante  (Adotante 1 --- * Animal)
AdocaoService --usa--> Settings, FilaEspera, BaseFeeStrategy, RepositorioJSON
```

## Decisões de design

- **State/Enum**: `StatusAnimal` + dicionário `TRANSICOES` validam as mudanças de status.
  Além das transições do enunciado, `RESERVADO -> DISPONIVEL` existe para a expiração da reserva.
- **Strategy**: `BaseFeeStrategy`, `SeniorFee`, `PuppyFee`, `SpecialCareFee`.
- **Repository**: `RepositorioJSON` isola a persistência do domínio (gravação atômica).
- **Observer**: o serviço notifica observadores quando o próximo da fila é avisado ao expirar uma reserva.
- **Fila de espera**: prioridade por pontuação de compatibilidade e, em empate, por tempo de espera.
- **Estado entre comandos**: reservas e filas são salvas em `data/estado.json`.
- **Herança múltipla**: `Cachorro` e `Gato` usam mixins cooperativos (`super()`).

## Testes

`pytest -v` cobre: validações e métodos especiais, transições de estado, políticas,
reserva e expiração (com tempo injetado), fila, compatibilidade, taxas, devolução,
reavaliação, persistência JSON, relatórios e a CLI.
