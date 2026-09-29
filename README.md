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
