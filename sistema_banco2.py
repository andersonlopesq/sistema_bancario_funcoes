def main():
    print("\nSeja bem-vindo!")

    usuarios = []
    contas = []

    while True:
        opcao = input("\n[nu] Novo Usuário\n[nc] Nova Conta\n[lc] Listar Contas\n[op] Operações Bancárias\n[q] Sair\n=> ")

        if opcao == "nu":
            cadastrar_usuario(usuarios)
        elif opcao == "nc":
            cadastrar_conta_bancaria(usuarios, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "op":
            if contas:
                numero_conta = int(input("Informe o número da conta para realizar operações: "))
                conta_selecionada = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)

                if conta_selecionada:
                    nome_usuario = conta_selecionada['usuario']['nome']
                    print(f"\nSeja bem-vindo, {nome_usuario}!")
                    operacoes(conta_selecionada)
                else:
                    print("Conta não encontrada.")
            else:
                print("Nenhuma conta cadastrada.")
        elif opcao == "q":
            break
        else:
            print("Operação inválida. Selecione novamente a operação desejada.")

def operacoes(conta):
    saldo = conta.get('saldo', 0)
    extrato = conta.get('extrato', "")
    limite = 500
    numero_saques = conta.get('numero_saques', 0)
    LIMITE_SAQUES = 3

    menu = """
    [d] Depósito
    [s] Saque
    [e] Extrato
    [q] Sair

    => """

    while True:
        opcao = input(menu)

        if opcao == "d":
            valor = float(input("Valor do depósito: "))
            saldo, extrato = depositar(valor, saldo, extrato)  # Passando argumentos por posição
            conta['saldo'] = saldo
            conta['extrato'] = extrato

        elif opcao == "s":
            valor = float(input("Valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                valor=valor, saldo=saldo, extrato=extrato,
                limite=limite, numero_saques=numero_saques,
                LIMITE_SAQUES=LIMITE_SAQUES)
            conta['saldo'] = saldo
            conta['extrato'] = extrato
            conta['numero_saques'] = numero_saques

        elif opcao == "e":
            exibir_extrato(conta)

        elif opcao == "q":
            break

        else:
            print("Operação inválida. Selecione novamente a operação desejada.")

def depositar(valor, saldo, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito ------- (+)R$ {valor:.2f}\n"
    else:
        print("O valor informado é inválido.")
    return saldo, extrato

def sacar(*, valor, saldo, extrato, limite, numero_saques, LIMITE_SAQUES):
    saldo_excedido = valor > saldo
    limite_excedido = valor > limite
    saque_excedido = numero_saques >= LIMITE_SAQUES

    if saldo_excedido:
        print("Não há saldo disponível para esta operação. Consulte seu extrato.")
    elif limite_excedido:
        print("O valor máximo por saque é de R$ 500,00.")
    elif saque_excedido:
        print("Você já atingiu o limite de 03 saques diários.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque ---------- (-)R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("O valor informado é inválido.")
    return saldo, extrato, numero_saques

def exibir_extrato(conta):
    print("\n~~~~~~~~~~ EXTRATO ~~~~~~~~~~")
    print("Você ainda não realizou nenhuma operação." if not conta.get('extrato') else conta['extrato'])
    print(f"Saldo ------------- R$ {conta.get('saldo', 0):.2f}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_usuario(cpf, usuarios):
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    
    logradouro = input("Informe o logradouro: ")
    numero = input("Informe o número: ")
    bairro = input("Informe o bairro: ")
    cidade = input("Informe a cidade: ")
    estado = input("Informe o estado (UF): ")
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário cadastrado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def cadastrar_conta_bancaria(usuarios, contas):
    cpf = input("Informe o CPF do usuário (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        numero_conta = len(contas) + 1
        contas.append({"agencia": "0001", "numero_conta": numero_conta, "usuario": usuario, "saldo": 0, "extrato": "", "numero_saques": 0})
        print(f"Conta cadastrada com sucesso para {usuario['nome']}! Número da conta: {numero_conta}")
    else:
        print("Usuário não encontrado. Cadastre o usuário primeiro.")

def listar_contas(contas):
    if contas:
        for conta in contas:
            usuario = conta['usuario']
            endereco = usuario['endereco']
            print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}, Usuário: {usuario['nome']}, CPF: {usuario['cpf']}, Data de")
    else:
        print("Nenhuma conta cadastrada.")

main()