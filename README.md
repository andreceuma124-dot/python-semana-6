# Sistema Bancário Orientado a Objetos (Semana 06 - Desafio Sprint 6)

Este projeto foi desenvolvido para a disciplina de **Desenvolvimento em Python** (Universidade CEUMA)[cite: 42], aplicando os pilares fundamentais da Programação Orientada a Objetos (POO): **Abstração, Encapsulamento, Herança e Polimorfismo**.

---

## 📐 Diagrama de Classes (Mermaid)

```mermaid
classDiagram
    class Cliente {
        -str _nome
        -str _email
        -str _cpf
        +nome() str
        +email() str
        +cpf() str
    }

    class Conta {
        <<Abstract>>
        -int _numero
        -Cliente _cliente
        -float _saldo
        +depositar(valor: float)
        +sacar(valor: float)
        +calcular_rendimento()* float
    }

    class ContaCorrente {
        +float taxa_manutencao
        +calcular_rendimento() float
        +descontar_taxa()
    }

    class ContaPoupanca {
        +float taxa_juros
        +calcular_rendimento() float
        +aplicar_rendimento()
    }

    Conta <|-- ContaCorrente : Herança
    Conta <|-- ContaPoupanca : Herança
    Conta "1" o-- "1" Cliente : Composição ("Tem um")
