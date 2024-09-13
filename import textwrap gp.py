import textwrap
from datetime import datetime

MENU = """\n
=============== MENU ================
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuário
[q] Sair
=> """

LIMITE_TRANSACOES = 10
LIMITE_SAQUES = 3
AGENCIA = "0001"
LIMITE_SAQUE_VALOR = 500

def menu():
    return input(MENU)

def registrar_transacao(tipo, valor, extrato):
    agora = datetime.now()
    timestamp = agora.strftime("%d/%m/%Y %H:%M:%S")
    extrato.append(f"{tipo}:\tR$ {valor:.2f} em {timestamp}")
    return extrato

def contar_transacoes_hoje(extrato):
    hoje = datetime.now().strftime("%d/%m/%Y")
    transacoes_hoje = [linha for linha in extrato if hoje in linha]
    return len(transacoes_hoje)

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato = registrar_transacao("Depósito", valor, extrato)
        print("=== Depósito realizado com sucesso! ===")
    else:
        print("@@@ Operação falhou! Valor inválido. @@@")
    return saldo, extrato

def sacar(saldo, valor, extrato, numero_saques):
    if valor > saldo:
        print("@@@ Saldo insuficiente. @@@")
    elif valor > LIMITE_SAQUE_VALOR:
        print(f"@@@ Valor do saque excede o limite de R$ {LIMITE_SAQUE_VALOR}. @@@")
    elif numero_saques >= LIMITE_SAQUES:
        print("@@@ Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato = registrar_transacao("Saque", valor, extrato)
        numero_saques += 1
        print("=== Saque realizado com sucesso! ===")
    else:
        print("@@@ Valor inválido. @@@")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n========== EXTRATO ==========")
    if not extrato:
        print("Nenhuma movimentação.")
    else:
        for linha in extrato:
            print(linha)
    print(f"Saldo:\t\tR$ {saldo:.2f}")
    print("=============================")

def criar_usuario(usuarios):
    cpf = input("CPF (somente número): ")
    if filtrar_usuario(cpf, usuarios):
        print("@@@ Usuário já cadastrado. @@@")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("@@@ Usuário não encontrado. @@@")

def listar_contas(contas):
    for conta in contas:
        print(f"\nAgência: {conta['agencia']}\nC/C: {conta['numero_conta']}\nTitular: {conta['usuario']['nome']}")
        print("=" * 40)

def main():
    saldo = 0
    extrato = []
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if contar_transacoes_hoje(extrato) >= LIMITE_TRANSACOES:
            print("\n@@@ Limite de 10 transações diárias atingido! @@@")
            continue

        if opcao == "d":
            valor = float(input("Valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Valor do saque: "))
            saldo, extrato, numero_saques = sacar(saldo, valor, extrato, numero_saques)

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Opção inválida!")

main()
