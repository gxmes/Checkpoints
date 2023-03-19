import random


# Definição de funções e variáveis globais
clientes = {}


def cadastrar_cliente(nome: str, cpf: str, valor_gasto: float, produtos: int) -> bool:
    if cpf in clientes:
        return False
    else:
        clientes[len(clientes)] = {
            "nome": nome,
            "cpf": cpf,
            "valor_gasto": valor_gasto,
            "produtos": produtos,
        }
        return True


def ranking_clientes() -> list:
    # Ordena os clientes de acordo com o valor gasto
    clientes_ordenados = sorted(
        clientes.items(), key=lambda x: x[1]["valor_gasto"], reverse=True
    )
    return clientes_ordenados


def ticket_medio(faturamento_mensal: float, numero_de_pedidos: int) -> float:
    return faturamento_mensal / float(numero_de_pedidos)


def relatorio_clientes() -> None:
    # Imprime um ranking dos clientes com maior ticket médio
    clientes_ordenados = ranking_clientes()
    faturamento_mensal = 0.0
    numero_de_pedidos = 0.0
    for cliente in clientes_ordenados:
        faturamento_mensal += cliente[1]["valor_gasto"]
        numero_de_pedidos += cliente[1]["produtos"]
    ticket_medio_mensal = ticket_medio(faturamento_mensal, numero_de_pedidos)
    print("============== Relatório ==============")
    print(f"Ticket médio mensal TOTAL: {ticket_medio_mensal}")
    print("Ranking de clientes com maior ticket médio:")
    # Ordenar os clientes de acordo com o ticket médio
    ticket_medio_por_cliente = []
    for cliente in clientes_ordenados:
        ticket_medio_cliente = ticket_medio(
            cliente[1]["valor_gasto"], cliente[1]["produtos"]
        )
        ticket_medio_por_cliente.append(
            (ticket_medio_cliente, cliente[1]["nome"], cliente[1]["cpf"])
        )
    ticket_medio_por_cliente.sort(reverse=True)
    ranking = 1
    for cliente in ticket_medio_por_cliente:
        print(
            f"{ranking}º lugar:\nNome: {cliente[1]} - CPF: {cliente[2]} - Ticket médio: {round(cliente[0], 2)}"
        )
        ranking += 1


# Cadastro
while True:
    indice = len(clientes) + 1
    print(f"Cadastro do cliente {indice}")
    nome = input(f"[{indice}] Digite o nome do cliente: ")
    cpf = input(
        f"[{indice}] Digite o CPF do cliente (Pressione ENTER para gerar um automaticamente): "
    )
    if not cpf or len(cpf) != 11:
        # Gera um CPF aleatório
        cpf = str(random.randint(10000000000, 99999999999))
        print(f"[{indice}] CPF gerado: {cpf}")
    valor_gasto = float(
        input(f"[{indice}] Digite o valor em reais gasto no ultimo mês pelo cliente: ")
    )
    produtos = int(
        input(f"[{indice}] Digite o número de produtos/serviços consumidos: ")
    )

    if cadastrar_cliente(nome, cpf, valor_gasto, produtos):
        print(f"[{indice}] Cliente cadastrado com sucesso!")
    else:
        print(f"[{indice}] Cliente já cadastrado!")

    if len(clientes) >= 3:
        if input(f"[{indice}] Deseja continuar? (s/n) ").lower() == "n":
            break

# Relatório
relatorio_clientes()
