# SistemaDeAdocaoDeAnimais CLI

Este repositório contém a modelagem e implementação orientada a objetos do **Sistema de Adoção de Animais**, desenvolvido para automatizar e organizar os processos de triagem, reserva e adoção em abrigos de animais.

---

## 🎯 Objetivos do Projeto

- **Organização do Fluxo de Adoção:** Gerenciar desde o cadastro do animal até a emissão do contrato final.
- **Modelagem Orientada a Objetos:** Aplicar conceitos fundamentais de POO (Abstração, Encapsulamento, Herança, Polimorfismo e Composição/Mixins).
- **Garantia de Regras de Negócio:** Validar a elegibilidade de adotantes e controlar prazos de reserva e status dos animais.

---
 
## ▶️ Como executar
 
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 adocao.py seed              # cria dados de exemplo em data/
python3 adocao.py --help
pytest -v
```
 
Opções globais (antes do subcomando):
 
| Opção | Padrão | Descrição |
|---|---|---|
| `--dados` | `data` | pasta onde ficam os arquivos JSON |
| `--settings` | `settings.json` | arquivo de configurações |
 
> O arquivo de configurações fica em `src/settings.json`. Como o padrão procura `settings.json` na raiz, use `--settings src/settings.json` para carregá-lo. Se o arquivo não for encontrado, o sistema usa valores padrão equivalentes.
 
---
 
## 💻 Comandos
 
```bash
python3 adocao.py listar [--status DISPONIVEL]
python3 adocao.py cadastrar-animal --tipo cachorro --nome Bidu --sexo MACHO --idade-meses 18 --porte M --raca SRD --passeio media
python3 adocao.py cadastrar-animal --tipo gato --nome Mia --sexo FEMEA --idade-meses 10 --porte P --independencia 4
python3 adocao.py cadastrar-adotante --nome Carlos --idade 40 --moradia casa --area 120 --experiencia
python3 adocao.py atualizar-animal --id 1 --nome Rex --idade-meses 30 --porte G
python3 adocao.py excluir-animal --id 1
python3 adocao.py reservar --animal 1 --adotante 1
python3 adocao.py fila --animal 1 --adotante 2
python3 adocao.py adotar --animal 1 --adotante 1
python3 adocao.py devolver --animal 1 --motivo "mudança de cidade" --problema-saude
python3 adocao.py reavaliar --animal 1 --status DISPONIVEL
python3 adocao.py rodar-expiracao
python3 adocao.py relatorio top     # disponiveis | top | taxas | tempo | devolucoes
```
 
Fluxo típico: `cadastrar` → `reservar` → `adotar` → (se necessário) `devolver` → `reavaliar`.
 
---
 
## 🏗️ Arquitetura e organização
 
```text
.
├── adocao.py                  # ponto de entrada
├── cli.py                     # subcomandos (argparse)
├── models/                    # domínio orientado a objetos
│   ├── pessoa.py              # Pessoa (abstrata)
│   ├── adotante.py            # Adotante
│   ├── animal.py              # Animal (abstrata), StatusAnimal, SexoAnimal, TRANSICOES
│   ├── cachorro.py            # Cachorro
│   ├── gato.py                # Gato
│   ├── mixins.py              # VacinavelMixin, AdestravelMixin
│   └── excecoes.py            # exceções do domínio
├── services/                  # regras de negócio
│   ├── servico.py             # AdocaoService e Reserva
│   ├── politicas.py           # validação de elegibilidade
│   ├── compatibilidade.py     # pontuação adotante-animal (0-100)
│   ├── fila.py                # FilaEspera e EntradaFila
│   ├── taxas.py               # Strategy de taxas
│   ├── relatorios.py          # relatórios
│   └── config.py              # Settings
├── repositories/
│   └── repositorio_json.py    # persistência em JSON
├── src/
│   ├── seed.py                # dados de exemplo
│   └── settings.json          # políticas configuráveis
├── tests/                     # testes com pytest
├── docs/UML.md                # diagramas (Mermaid)
├── pytest.ini
├── requirements.txt
└── .gitignore
```
 
Fluxo geral: `CLI → AdocaoService → (modelos, política, fila, taxas) → RepositorioJSON`.
 
### Entidades do domínio
 
- **`Pessoa` (abstrata)** → **`Adotante`**: perfil (moradia, área útil, experiência, crianças e outros animais em casa) e vínculo com os animais adotados (`vincular_animal` / `desvincular_animal`).
- **`Animal` (abstrata)** → **`Cachorro`** e **`Gato`**: dados básicos, status, data de entrada, histórico de eventos e o método abstrato `descrever_necessidades()`.
- **Mixins:** `VacinavelMixin` (registro de vacinas, usado por `Cachorro` e `Gato`) e `AdestravelMixin` (nível de adestramento de 0 a 5, só para `Cachorro`).
- **`Reserva`** (em `services/servico.py`): bloqueio temporário de um animal por um adotante, com `criada_em` e `expira_em`.
- **Contrato de adoção:** não é uma classe. `AdocaoService.adotar()` gera o texto do contrato com animal, adotante, data e taxa.
### Ciclo de vida do animal
 
| De | Para |
|---|---|
| `DISPONIVEL` | `RESERVADO`, `INADOTAVEL` |
| `RESERVADO` | `ADOTADO`, `DISPONIVEL` (quando a reserva expira) |
| `ADOTADO` | `DEVOLVIDO` |
| `DEVOLVIDO` | `QUARENTENA`, `DISPONIVEL`, `INADOTAVEL` |
| `QUARENTENA` | `DISPONIVEL`, `INADOTAVEL` |
| `INADOTAVEL` | — (estado final) |
 
Transições fora dessa tabela levantam `TransicaoDeEstadoInvalidaError`.
 
---
 
## 📏 Regras de negócio
 
- **Elegibilidade** (`services/politicas.py`): o adotante precisa ter a idade mínima configurada (18 anos) e, para animais de porte **G**, morar em **casa** com área útil de pelo menos 50 m².
- **Reserva:** só para animais `DISPONIVEL` e sem reserva ativa. Dura 48 horas por padrão (`reserva_horas`).
- **Adoção:** exige reserva ativa e não expirada em nome do adotante.
- **Fila de espera:** ordenada pela pontuação de compatibilidade (maior primeiro) e, em empate, por quem entrou antes. Ao expirar uma reserva, o próximo da fila é notificado (Observer).
- **Compatibilidade (0-100):** média ponderada de porte x moradia, idade x energia, experiência e crianças em casa. Os pesos ficam no `settings.json`.
- **Taxas** (Strategy): padrão R$ 100; sênior (96 meses ou mais) R$ 50; filhote (menos de 12 meses) R$ 150; cuidados especiais (evento de tratamento no histórico) R$ 250.
- **Devolução:** com `--problema-saude`, o animal vai direto para `QUARENTENA`. A reavaliação leva a `DISPONIVEL` ou `INADOTAVEL`.
### Configurações (`src/settings.json`)
 
| Chave | Significado |
|---|---|
| `idade_minima` | idade mínima do adotante |
| `area_minima_porte_g` | área mínima (m²) para animais de porte G |
| `reserva_horas` | duração da reserva |
| `taxa_padrao` | estratégia de taxa padrão |
| `pesos` | pesos dos critérios de compatibilidade |
 
---
 
## 🧩 Decisões de design
 
- **State/Enum:** `StatusAnimal` e o dicionário `TRANSICOES` validam as mudanças de status. Além do fluxo básico, `RESERVADO → DISPONIVEL` existe para a expiração da reserva.
- **Strategy:** `BaseFeeStrategy`, `SeniorFee`, `PuppyFee` e `SpecialCareFee`.
- **Repository:** `RepositorioJSON` isola a persistência do domínio, com gravação atômica.
- **Observer:** o serviço notifica os inscritos quando o próximo da fila é avisado.
- **Herança múltipla:** `Cachorro` e `Gato` usam mixins cooperativos (`super()`).
- **Estado entre comandos:** reservas e filas são salvas em `data/estado.json`.
- **Tempo injetável:** os métodos do serviço aceitam `agora`, o que facilita testar expiração.
---
 
## 📊 Diagramas UML
 
Os diagramas de classes (domínio e serviços) e o de estados do animal estão em Mermaid:
 
**[Ver UML completo](./docs/UML.md)**
 
---
 
## ✅ Testes
 
```bash
pytest -v
```
 
Cobrem validações e métodos especiais, transições de estado, políticas, reserva e expiração, fila, compatibilidade, taxas, devolução, reavaliação, persistência JSON, relatórios e a CLI.
 

reserva e expiração (com tempo injetado), fila, compatibilidade, taxas, devolução,
reavaliação, persistência JSON, relatórios e a CLI.
