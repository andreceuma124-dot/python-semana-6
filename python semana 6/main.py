from abc import ABC, abstractmethod
import re


# ==========================================
# 1. CLASSE CLIENTE
# ==========================================
class Cliente:
    """Representa um cliente do banco."""

    def __init__(self, nome: str, email: str, cpf: str):
        self.nome = nome
        self.email = email
        self.cpf = cpf

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("O nome do cliente não pode estar vazio.")
        self._nome = valor.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(padrao, valor.strip()):
            raise ValueError(f"Formato de e-mail inválido: '{valor}'")
        self._email = valor.strip()

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, valor: str):
        padrao = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
        if not re.match(padrao, valor.strip()):
            raise ValueError(f"Formato de CPF inválido: '{valor}' (Esperado: 000.000.000-00)")
        self._cpf = valor.strip()

    def __str__(self) -> str:
        return f"{self.nome} (CPF: {self.cpf}, E-mail: {self.email})"

    def __repr__(self) -> str:
        return f"Cliente(nome={self.nome!r}, email={self.email!r}, cpf={self.cpf!r})"


# ==========================================
# 2. CLASSE ABSTRATA CONTA (CLASSE MÃE)
# ==========================================
class Conta(ABC):
    """Classe abstrata que serve de base para os tipos de conta bancária."""

    def __init__(self, numero: int, cliente: Cliente, saldo_inicial: float = 0.0):
        self.numero = numero
        self.cliente = cliente
        self.saldo = saldo_inicial  # Usa o setter para validar

    @property
    def numero(self) -> int:
        return self._numero

    @numero.setter
    def numero(self, valor: int):
        if valor <= 0:
            raise ValueError("O número da conta deve ser um valor positivo.")
        self._numero = valor

    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float):
        if valor < 0:
            raise ValueError("O saldo inicial não pode ser negativo.")
        self._saldo = float(valor)

    def depositar(self, valor: float):
        """Deposita um valor positivo na conta."""
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser maior que zero.")
        self._saldo += valor

    def sacar(self, valor: float):
        """Realiza o saque respeitando o saldo disponível."""
        if valor <= 0:
            raise ValueError("O valor do saque deve ser maior que zero.")
        if valor > self._saldo:
            raise ValueError(f"Saldo insuficiente na conta {self.numero}. Saldo atual: R$ {self._saldo:.2f}")
        self._saldo -= valor

    @abstractmethod
    def calcular_rendimento(self) -> float:
        """Método abstrato obrigatoriamente sobrescrito pelas subclasses."""
        pass

    def __str__(self) -> str:
        return f"Conta Nº {self.numero} | Titular: {self.cliente.nome} | Saldo: R$ {self.saldo:.2f}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(numero={self.numero!r}, cliente={self.cliente!r}, saldo={self.saldo!r})"

    def __eq__(self, outro) -> bool:
        if not isinstance(outro, Conta):
            return False
        return self.numero == outro.numero

    def __lt__(self, outro) -> bool:
        if not isinstance(outro, Conta):
            return NotImplemented
        return self.saldo < outro.saldo


# ==========================================
# 3. SUBCLASSE CONTA CORRENTE
# ==========================================
class ContaCorrente(Conta):
    """Representa uma Conta Corrente sujeita a taxa de manutenção."""

    def __init__(self, numero: int, cliente: Cliente, saldo_inicial: float = 0.0, taxa_manutencao: float = 15.0):
        super().__init__(numero, cliente, saldo_inicial)
        self.taxa_manutencao = taxa_manutencao

    def calcular_rendimento(self) -> float:
        """Conta corrente possui rendimento nulo (0.0)."""
        return 0.0

    def descontar_taxa(self):
        """Deduz a taxa mensal de manutenção do saldo."""
        self.sacar(self.taxa_manutencao)

    def __str__(self) -> str:
        return f"[Conta Corrente] {super().__str__()} | Taxa Mensal: R$ {self.taxa_manutencao:.2f}"


# ==========================================
# 4. SUBCLASSE CONTA POUPANÇA
# ==========================================
class ContaPoupanca(Conta):
    """Representa uma Conta Poupança que rende juros mensais."""

    def __init__(self, numero: int, cliente: Cliente, saldo_inicial: float = 0.0, taxa_juros: float = 0.005):
        super().__init__(numero, cliente, saldo_inicial)
        self.taxa_juros = taxa_juros

    def calcular_rendimento(self) -> float:
        """Calcula o rendimento mensal baseado na taxa de juros."""
        return self.saldo * self.taxa_juros

    def aplicar_rendimento(self):
        """Aplica o rendimento calculado diretamente ao saldo."""
        rendimento = self.calcular_rendimento()
        self.depositar(rendimento)

    def __str__(self) -> str:
        return f"[Conta Poupança] {super().__str__()} | Taxa Juros: {self.taxa_juros * 100:.1f}%"


# ==========================================
# DEMONSTRAÇÃO E TESTES COMPLETO
# ==========================================
if __name__ == "__main__":
    print("=" * 65)
    print("      SISTEMA BANCÁRIO ORIENTADO A OBJETOS - SPRINT 6")
    print("=" * 65 + "\n")

    # --- Criando Instâncias de Clientes ---
    c1 = Cliente("Ana Silva", "ana@email.com", "123.456.789-00")
    c2 = Cliente("Bruno Souza", "bruno@email.com", "987.654.321-11")
    c3 = Cliente("Carla Lima", "carla@empresa.com", "456.789.123-22")
    c4 = Cliente("Diego Costa", "diego@email.com", "789.123.456-33")

    # --- Criando Instâncias de Contas (Mais de 10 objetos no total) ---
    cc1 = ContaCorrente(101, c1, 1500.0)
    cc2 = ContaCorrente(102, c2, 500.0)
    cc3 = ContaCorrente(103, c3, 3000.0)

    cp1 = ContaPoupanca(201, c1, 2000.0, taxa_juros=0.01)
    cp2 = ContaPoupanca(202, c2, 10000.0, taxa_juros=0.008)
    cp3 = ContaPoupanca(203, c4, 150.0, taxa_juros=0.005)

    # --- Demonstrando Polimorfismo e Iteração ---
    contas = [cc1, cc2, cc3, cp1, cp2, cp3]

    print(">>> 1. LISTAGEM E POLIMORFISMO (Método __str__ e calcular_rendimento):")
    for conta in contas:
        print(f"{conta} | Rendimento Previsto: R$ {conta.calcular_rendimento():.2f}")
    print("\n" + "-" * 65 + "\n")

    # --- Demonstrando Métodos Dunder (__eq__ e __lt__) ---
    print(">>> 2. COMPARAÇÕES DUNDER (__lt__ para saldo e __eq__ para número):")
    print(f"cc1 < cp2? {cc1 < cp2} (R$ {cc1.saldo} vs R$ {cp2.saldo})")
    print(f"cp3 < cc2? {cp3 < cc2} (R$ {cp3.saldo} vs R$ {cc2.saldo})")
    outra_cc1 = ContaCorrente(101, c4, 0.0)
    print(f"cc1 == outra_cc1 (mesmo número 101)? {cc1 == outra_cc1}\n")
    print("-" * 65 + "\n")

    # --- Testes de Tratamento de Exceções ---
    print(">>> 3. TESTE DE VALIDAÇÕES E TRATAMENTO DE EXCEÇÕES:")

    # Teste 1: E-mail Inválido
    try:
        print("Tentando criar cliente com e-mail inválido...")
        Cliente("Ernesto", "email_invalido", "000.111.222-33")
    except ValueError as e:
        print(f"[EXCEÇÃO CAPTURADA] {e}")

    # Teste 2: CPF Inválido
    try:
        print("Tentando criar cliente com CPF fora do padrão...")
        Cliente("Fernanda", "nanda@email.com", "12345678900")
    except ValueError as e:
        print(f"[EXCEÇÃO CAPTURADA] {e}")

    # Teste 3: Saldo Negativo
    try:
        print("Tentando criar Conta Poupança com saldo negativo...")
        ContaPoupanca(204, c3, saldo_inicial=-200.0)
    except ValueError as e:
        print(f"[EXCEÇÃO CAPTURADA] {e}")

    # Teste 4: Saque Indevido (Saldo Insuficiente)
    try:
        print(f"Tentando sacar R$ 5000.00 da cc2 (Saldo atual: R$ {cc2.saldo:.2f})...")
        cc2.sacar(5000.0)
    except ValueError as e:
        print(f"[EXCEÇÃO CAPTURADA] {e}")

    print("\n" + "=" * 65)
    print("      EXECUÇÃO E DEMONSTRAÇÃO CONCLUÍDAS COM SUCESSO!")
    print("=" * 65)