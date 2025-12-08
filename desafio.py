# argumentos apenas por nome --> ao chamar deve ter nome da var + valor (saldo = x, ...)
# Sugestões:
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):

    return saldo, extrato


def depositar(cpf, valor, /):
    contas_cliente = []
    numeros_contas = []
    for conta in contas:
        if conta['cpf'] == cpf:
            contas_cliente.append(conta)
            numeros_contas.append(conta['nro'])
    
    print("Contas que o cliente possui: ", numeros_contas)
    conta_alvo = input("Informe o nro da conta que receberá o deposito: ")

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
            conta['extrato'] += f"Depósito: R$ {valor:.2f}\n"

            print(f"""Operação realizada com sucesso!\n
                Novo saldo: {conta['saldo']}\n
                Extrato: \n
                {conta['extrato']}
            """)

# Argumento saldo posicional
# Argumento extrato por nome
def extrato():

    return


def cadastrar_cliente(nome, data_nascimento, cpf, endereco):
    novo_cliente = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }

    clientes.append(novo_cliente)


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

        if ano < 1900 or ano > 2010:
            print("Novos clientes não podem ter menos de 16 anos ou terem nascido antes de 1900!")
            return None

        if not (1 <= mes <= 12):
            print(aux[1],"não é um mês válido.")
            data_nascimento = input("Digite a data de nascimento do cliente no formato DD/MM/AAAA: ")
            continue

        if not (1 <= dia <= 31):
            print(aux[0],"não é um dia válido.")
            data_nascimento = input("Digite a data de nascimento do cliente no formato DD/MM/AAAA: ")
            continue
        
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


clientes = []
contas = []

nro_conta = 1
NRO_AGENCIA = '0001'
extrato = ""


menu = """

[1] Cadastrar cliente
[2] Criar conta
[3] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """



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
        print('Cliente cadastrado com sucesso!')

    elif opcao == '2':
        cpf = input("Informe o CPF do cliente: ")

        if consultar_cpf(cpf) == False:
            print("CPF inválido ou não cadastrado!")
            continue

        criar_conta_corrente(NRO_AGENCIA, str(nro_conta), cpf)
        nro_conta += 1
        print('Conta criada com sucesso!')
    
    elif opcao == "3":
        cpf = input("Informe o CPF do cliente: ")

        if consultar_cpf(cpf) == False:
            print("CPF inválido ou não cadastrado!")
            continue

        valor = float(input("Informe o valor do depósito: "))

        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
        else:
            depositar(cpf, valor)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")