clientes = []
contas = []

nro_conta = 1
NRO_AGENCIA = '0001'

menu = """
[1] Cadastrar cliente
[2] Criar conta
[3] Depositar
[4] Sacar
[5] Extrato
[0] Sair

=> """

def sacar(*, cpf, valor):
    contas_cliente = []
    numeros_contas = []
    for conta in contas:
        if conta['cpf'] == cpf:
            contas_cliente.append(conta)
            numeros_contas.append(conta['nro'])
    
    if numeros_contas:
        print("Contas que o cliente possui: ", numeros_contas)
        conta_alvo = input("Informe o nro da conta para o saque: ")
    else:
        print("Cliente ainda não possui uma conta cadastrada!")
        return

    while(1):
        if conta_alvo not in numeros_contas:
            print('Opção inválida. Contas que o cliente possui: ', numeros_contas)
            conta_alvo = input("Informe o nro da conta que receberá saque: ")
            continue
        else:
            break
    
    for conta in contas_cliente:
        if conta_alvo == conta['nro']:
            excedeu_saldo = valor > conta['saldo']
            excedeu_limite = valor > conta['limite']
            excedeu_saques = conta['numero_saques'] >= conta['limite_saques']

            if excedeu_saldo:
                print("Operação falhou! Conta sem saldo suficiente.")
                break
            elif excedeu_limite:
                print("Operação falhou! O valor excede o limite permitido para saques.")
            elif excedeu_saques:
                print("Operação falhou! Número máximo de saques excedido.")
            else:
                conta['saldo'] -= valor
                conta['extrato'] += f"- Saque R$ {valor:.2f}\n"
                conta['numero_saques'] += 1

                print("Operação realizada com sucesso!\n")
                print(f"Novo saldo: {conta['saldo']}")
                print(f"Extrato: ")
                print(conta['extrato'])


def depositar(cpf, valor, /):
    contas_cliente = []
    numeros_contas = []
    for conta in contas:
        if conta['cpf'] == cpf:
            contas_cliente.append(conta)
            numeros_contas.append(conta['nro'])
    
    if numeros_contas:
        print("Contas que o cliente possui: ", numeros_contas)
        conta_alvo = input("Informe o nro da conta para o depósito: ")
    else:
        print("Cliente ainda não possui uma conta cadastrada!")
        return

    while(1):
        if conta_alvo not in numeros_contas:
            print('Opção inválida. Contas que o cliente possui: ', numeros_contas)
            conta_alvo = input("Informe o nro da conta que receberá o deposito: ")
            continue
        else:
            break
    
    for conta in contas_cliente:
        if conta_alvo == conta['nro']:
            conta['saldo'] += valor
            conta['extrato'] += f"- Depósito R$ {valor:.2f}\n"

            print("Operação realizada com sucesso!\n")
            print(f"Novo saldo: {conta['saldo']}")
            print(f"Extrato: ")
            print(conta['extrato'])


def extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def cadastrar_cliente(nome, data_nascimento, cpf, endereco):
    novo_cliente = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }

    clientes.append(novo_cliente)
    print('Cliente cadastrado com sucesso!')


def criar_conta_corrente(agencia, nro_conta, cpf):
    nova_conta = {
        "agencia": agencia,
        "nro": nro_conta,
        "cpf": cpf,
        "saldo": 0,
        "limite": 500,
        "numero_saques": 0,
        "limite_saques": 3,
        "extrato": ''
    }
    
    contas.append(nova_conta)
    print('Conta criada com sucesso!')
    

def definir_nascimento():
    data_nascimento = input("Informe a data de nascimento do cliente no formato DD/MM/AAAA: ")
        
    while(1):
        aux = []
        aux = data_nascimento.split('/')

        if not len(aux) == 3:
            data_nascimento = input("Data inválida. Digite a data de nascimento do cliente no formato DD/MM/AAAA: ")
            continue

        erro = False
        for item in aux:
            if not item.isdigit():
                print(item, "não é um valor válido para datas.")
                erro = True
                break
        
        if erro:
            data_nascimento = input("Digite a data de nascimento do cliente no formato DD/MM/AAAA: ")
            continue
        
        dia = int(aux[0])
        mes = int(aux[1])
        ano = int(aux[2])

        if not (1 <= dia <= 31):
            print(aux[0],"não é um dia válido.")
            data_nascimento = input("Digite a data de nascimento do cliente no formato DD/MM/AAAA: ")
            continue

        if not (1 <= mes <= 12):
            print(aux[1],"não é um mês válido.")
            data_nascimento = input("Digite a data de nascimento do cliente no formato DD/MM/AAAA: ")
            continue

        if ano < 1900 or ano > 2010:
            print("Novos clientes não podem ter menos de 16 anos ou terem nascido antes de 1900!")
            return None
        
        break

    return data_nascimento


def definir_cpf():
    cpf = input("Informe o CPF do cliente (apenas números): ")

    while(1):

        if not cpf.isdigit():
            cpf = input('Digite apenas números para o CPF. Tente novamente: ')
            continue

        if len(cpf) != 11:
            cpf = input('O CPF deve conter 11 dígitos. Tente novamente: ')
            continue

        if consultar_cpf(cpf):
            cpf = input('Já existe um cliente cadastrado com o CPF informado. Tente novamente: ')
            continue

        break
    return cpf


def consultar_cpf(cpf):

    if len(clientes) == 0:
        return False
    
    for item in clientes:
        if item['cpf'] == cpf:
            return True
        
    return False


while True:

    opcao = input(menu)

    if opcao == '1':
        endereco = ''
        nome = input("Informe o nome do cliente: ")
        data_nascimento = definir_nascimento()
        
        if data_nascimento is None:
            continue

        cpf = definir_cpf()
        endereco += input('Informe o logradouro do cliente: ')
        endereco += ', ' + input('Informe o número da casa do cliente: ')
        endereco += ' - ' + input('Informe a cidade do cliente: ')
        endereco += '/' + input('Informe a sigla do estado: ')

        cadastrar_cliente(nome, data_nascimento, cpf, endereco)

    elif opcao == '2':
        cpf = input("Informe o CPF do cliente: ")

        if consultar_cpf(cpf) == False:
            print("CPF inválido ou não cadastrado!")
            continue

        criar_conta_corrente(NRO_AGENCIA, str(nro_conta), cpf)
        nro_conta += 1
    
    elif opcao == "3":
        cpf = input("Informe o CPF do cliente: ")

        if consultar_cpf(cpf) == False:
            print("CPF inválido ou não cadastrado!")
            continue

        while(1):
            try:
                valor = float(input("Informe o valor do depósito: "))
                if valor > 0:
                    depositar(cpf, valor)
                    break
                else:
                    print("O valor deve ser maior que zero.")
            except ValueError:
                print("Operação falhou! O valor informado é inválido! Digite apenas números e separe casa decimal com ponto (ex.: 1150.50)")

    elif opcao == "4":
        cpf = input("Informe o CPF do cliente: ")

        if consultar_cpf(cpf) == False:
            print("CPF inválido ou não cadastrado!")
            continue

        while(1):
            try:
                valor = float(input("Informe o valor do saque: "))
                if valor > 0:
                    sacar(cpf = cpf, valor = valor)
                    break
                else:
                    print("O valor deve ser maior que zero.")
            except ValueError:
                print("Operação falhou! O valor informado é inválido! Digite apenas números e separe casa decimal com ponto (ex.: 500.00)")

    elif opcao == "5":
        cpf = input("Informe o CPF do cliente: ")

        if consultar_cpf(cpf) == False:
            print("CPF inválido ou não cadastrado!")
            continue

        contas_cliente = []
        numeros_contas = []
        for conta in contas:
            if conta['cpf'] == cpf:
                contas_cliente.append(conta)
                numeros_contas.append(conta['nro'])
        
        if numeros_contas:
            print("Contas que o cliente possui: ", numeros_contas)
            conta_alvo = input("Informe o nro da conta que deseja ver o extrato: ")
        else:
            print("Cliente ainda não possui uma conta cadastrada!")
            continue

        while(1):
            if conta_alvo not in numeros_contas:
                print('Opção inválida. Contas que o cliente possui: ', numeros_contas)
                conta_alvo = input("Informe o nro da conta que deseja ver o extrato: ")
                continue
            else:
                break

        for conta in contas_cliente:
            if conta_alvo == conta['nro']:
                extrato(conta['saldo'], extrato = conta['extrato'])

    elif opcao == "0":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")