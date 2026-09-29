# Diagrama de Classes UML - Sistema de Adoção de Animais

```mermaid
classDiagram
    class StatusAnimal {
        <<enumeration>>
        DISPONIVEL
        RESERVADO
        ADOTADO
        DEVOLVIDO
        QUARENTENA
        INADOTAVEL
    }

    class SexoAnimal {
        <<enumeration>>
        MACHO
        FEMEA
    }

    class Pessoa {
        <<abstract>>
        #nome: String
        #idade: int
    }

    class Adotante {
        -moradia: String
        -area_util: float
        -experiencia_pets: bool
        -criancas_em_casa: bool
        -outros_animais: bool
        +validar_elegibilidade() bool
    }

    class Animal {
        <<abstract>>
        #id_animal: int
        #nome: String
        #sexo: SexoAnimal
        #idade_meses: int
        #porte: String
        #temperamento: List~String~
        #status: StatusAnimal
        +alterar_status(novo_status: StatusAnimal) void
    }

    class VacinavelMixin {
        -historico_vacinas: List~String~
        +vacinar(vacina: String) void
    }

    class AdestravelMixin {
        -nivel_adestramento: int
        +treinar() void
    }

    class Cachorro {
        -necessidade_passeio: String
        -raca: String
        -adestrado: bool
        
    }

    class Gato {
        -nivel_independencia: int
    }

    class Reserva {
        -data_criacao: DateTime
        -expirada: bool
        +verificar_expiracao() bool
    }

    class ContratoAdocao {
        -data_adocao: DateTime
        -taxa_aplicada: float
        -termos: String
        +gerar_contrato() String
    }

    %% Heranças
    Pessoa <|-- Adotante
    Animal <|-- Cachorro
    Animal <|-- Gato

    %% Mixins (Herança Múltipla)
    VacinavelMixin <|-- Cachorro
    AdestravelMixin <|-- Cachorro
    VacinavelMixin <|-- Gato

    %% Relacionamentos e Associações
    Animal "1" --> "1" StatusAnimal : possui
    Animal "1" --> "1" SexoAnimal : possui
    Reserva "*" --> "1" Adotante : realizada por
    Reserva "1" --> "1" Animal : reserva
    ContratoAdocao "*" --> "1" Adotante : assinado por
    ContratoAdocao "1" --> "1" Animal : refere-se a
```
