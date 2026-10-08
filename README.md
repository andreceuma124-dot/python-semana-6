# Sistema Bancário Orientado a Objetos (Semana 06 - Desafio Sprint 6)

Este projeto foi desenvolvido para a disciplina de **Desenvolvimento em Python** (Universidade CEUMA), aplicando os conceitos fundamentais do paradigma de Programação Orientada a Objetos (POO): **Abstração, Encapsulamento, Herança e Polimorfismo**.

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


📌 Justificativa das Decisões de ModelagemHerança vs.
Composição:ContaCorrente e ContaPoupanca herdam de Conta: Aplicação da relação "é uma". Ambas partilham atributos comuns de saldo, número, depósito e levantamento.
  Conta é composta por Cliente: Aplicação da relação "tem um" (Composição). Uma conta possui um titular do tipo Cliente, mantendo as responsabilidades bem separadas e coesas.
  Classe Abstrata (ABC):A classe Conta utiliza o módulo abc e define o método abstrato @abstractmethod def calcular_rendimento().
Isto garante que nenhuma conta genérica seja instanciada diretamente e obriga as subclasses a implementarem a sua própria regra de rendimento.
🔐 Encapsulamento e Validações
 (@property)E-mail: Validado por Expressão Regular (Regex) no setter correspondente para garantir o formato correto (utilizador@dominio.com).
  CPF: Validado por Regex para respeitar o padrão de formatação (000.000.000-00).
  Saldo e Saque: O saldo inicial e as operações de levantamento validam restrições de valores negativos ou saldos insuficientes, disparando exceções controladas (ValueError).   
