from typing import Any, Union, Collection
from dataclasses import dataclass
import unicodedata
import re


@dataclass(frozen=True)
class Cliente(object):
    nome: str
    email: str
    cpf: str

    def __iter__(self):
        return iter([self.nome, self.email, self.cpf])

    def __repr__(self) -> str:
        return f"Nome: {self.nome}, e-mail: {self.email}, CPF: {self.cpf}"


@dataclass(frozen=True)
class Produto(object):
    id: int
    nome: str
    descricao: str
    preco: float

    def __iter__(self):
        # Método especial definido para imprimir com formatação nas tabelas.
        return iter(
            [
                self.id,
                self.nome,
                self.descricao,
                self.preco
            ]
        )

    def __repr__(self) -> str:
        # Geralmente descrição é um texto maior, portanto opto por quebrar a linha.
        return f"ID: {self.id}, nome: {self.nome}, preço: {self.preco},\nDescrição: {self.descricao}"


def remover_acentos(s: str) -> str:
    """
    Remove os acentos de uma dada string.

    Parâmetros:
        s (str): String qual será processada.

    Retorna:
        String formatada.
    """

    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def validar_cpf(cpf: str) -> bool:
    """
    Valida o CPF inserido.

    Parâmetros:
        cpf (str): O CPF a ser validado.

    Retorna:
        True se o CPF for valido e False caso não seja.
    """

    # Remove os pontos e traço do CPF
    cpf = re.sub("[^0-9]", "", cpf)

    # Calcula o primeiro dígito verificador
    def digito1(cpf) -> int:
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resultado = (soma * 10) % 11
        if resultado == 10:
            resultado = 0
        return resultado

    # Calcula o segundo dígito verificador
    def digito2(cpf) -> int:
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resultado = (soma * 10) % 11
        if resultado == 10:
            resultado = 0
        return resultado

    # Verifica se o CPF é válido
    if len(cpf) == 11 and cpf.isdigit():
        if int(cpf[9]) == digito1(cpf) and int(cpf[10]) == digito2(cpf):
            return True

    return False


def construir_cliente(
    nome: str, email: str, cpf: str, validador: bool = False
) -> Cliente:
    """
    Cria um objeto Cliente com as informações passadas como argumento.

    Parâmetros:
        nome (str): Nome do cliente.
        email (str): Endereço de email do cliente.
        cpf (str): CPF do cliente, no formato "xxx.xxx.xxx-xx".
        validador (bool): Indica se deve validar o CPF.

    Retorna:
        Cliente ou None: Retorna um objeto Cliente caso as informações sejam válidas, ou None caso ocorra algum erro.

    Exemplo:
        construir_cliente("João da Silva", "joao@gmail.com", "123.456.789-10")
        # Retorna um objeto Cliente com nome "João da Silva", email "joao@gmail.com" e CPF 
        # "123.456.789-10", ou None caso ocorra algum erro.
    """

    if ("" in (nome, email, cpf)) or ("@" not in email):
        raise Exception("Dados inconsistentes.")

    nome = nome.strip()
    nome = nome.capitalize()
    email = email.strip()
    cpf = cpf.strip()

    padrao_cpf = re.compile(r"\d{3}\.\d{3}\.\d{3}-\d{2}")

    if not padrao_cpf.match(cpf):
        raise Exception(
            f'Formato de CPF incorreto: {[cpf]}, use: "xxx.xxx.xxx-xx".')

    if validador:
        if not validar_cpf(cpf):
            raise Exception("CPF inválido.")

    return Cliente(nome=nome, email=email, cpf=cpf)


def construir_produto(
    id: int, nome: str, descricao: str, preco: Union[str, float]
) -> Produto:
    """
    Cria um objeto Produto com as informações passadas como argumento.

    Parâmetros:
        id (int): Identificador único do produto.
        nome (str): Nome do produto.
        descricao (str): Descrição do produto.
        preco (Union[str, float]): Preço do produto, como string ou float.

    Retorna:
        Produto ou None: Retorna um objeto Produto caso as informações sejam válidas, ou None caso ocorra algum erro.
    """

    if "" in (nome, descricao, preco):
        raise Exception("Dados inconsistentes.")

    nome = nome.strip()
    nome = nome.capitalize()
    preco = str(preco).strip()

    try:
        # Converter preço
        preco = preco.replace(",", ".")
        preco = float(preco)

    except ValueError as e:
        print(e)

    return Produto(id=id, nome=nome, descricao=descricao, preco=preco)


def para_tabela(
    lista: list[Union[Cliente, Produto]]
) -> tuple[list[str], list[list[Any]]]:
    """
    Converte uma lista de clientes ou produtos em colunas e linhas.

    Parâmetros:
        lista (list[Union[Cliente, Produto]]): Lista de clientes ou produtos.

    Retorna:
        Colunas e linhas.
    """

    colunas = list(type(lista[0]).__dataclass_fields__.keys())
    linhas = []

    for item in lista:
        linhas.append([*item])

    return colunas, linhas


def dicionario_para_tabela(
    dicionario: dict[Any, Any], colunas: list[str]
) -> tuple[list[str], list[list[Any]]]:
    """
    Converte um dicionário para um formato de linhas e colunas.

    Parâmetros:
        dicionario (dict[Any, Any]): Dicionário que será convertido.
        colunas (list[str]):         Nome das colunas.

    Retorna:
        Colunas e linhas dentro de uma tupla.
    """
    linhas = [[chave] + list(valor) for chave, valor in dicionario.items()]
    return colunas, linhas


def imprime_tabela(colunas: list[str], linhas: list[Collection], indice=False) -> None:
    """
    Formata a tabela para ser exibida no terminal.

    Parâmetros:
        colunas (list[str]): Nome das colunas da tabela.
        linhas (list[Collection]): Lista contendo as células de cada linha.

    Retorna:
        None

    Exemplo:
        >>> imprime_tabela(
                colunas = ['Coluna 1', 'Coluna 2', 'Coluna 3'],
                linhas = [
                    ['a', 'b', 'c'],
                    ['d', 'e', 'f'],
                    ['g', 'h', 'i'],
                    ['j', 'k', 'l']
                ]
            )

        ┌──────────┬──────────┬──────────┐
        │ Coluna 1 │ Coluna 2 │ Coluna 3 │
        ├──────────┼──────────┼──────────┤
        │    a     │    b     │    c     │
        ├──────────┼──────────┼──────────┤
        │    d     │    e     │    f     │
        ├──────────┼──────────┼──────────┤
        │    g     │    h     │    i     │
        ├──────────┼──────────┼──────────┤
        │    j     │    k     │    l     │
        └──────────┴──────────┴──────────┘
    """

    # Adicionar coluna indice e preencher linhas com 0 até len(linhas).
    if indice:
        colunas.insert(0, "Indice")
        for i in range(len(linhas)):
            linhas[i].insert(0, i + 1)

    # Ajuste automático do tamanho das colunas baseado no maior valor de cada celula.
    tamanho_c = max(len(str(celula))
                    for linha in linhas for celula in linha) + 2

    # Ajuste automático do tamanho das linhas baseado no maior valor de cada coluna.
    tamanho_l = max(len(coluna) for coluna in colunas for celula in coluna) + 2
    tamanho = tamanho_c if tamanho_c > tamanho_l else tamanho_l

    # Imprimir cabeçalho.
    print("┌" + "┬".join("─" * tamanho for _ in colunas) + "┐")
    print("│" + "│".join(str(celula).center(tamanho)
          for celula in colunas) + "│")
    print("├" + "┼".join("─" * tamanho for _ in colunas) + "┤")

    # Imprimir linhas.
    for linha in linhas:
        if linha:  # Ignora linhas vazias.
            print("│" + "│".join(str(celula).center(tamanho)
                  for celula in linha) + "│")
            if not linha == linhas[-1]:  # Ignora a última linha.
                print("├" + "┼".join("─" * tamanho for _ in colunas) + "┤")

    # Imprimir rodapé.
    print("└" + "┴".join("─" * tamanho for _ in colunas) + "┘")


def tabela(c: Collection[Any], i: bool = False) -> None:
    """
    'Macro' para imprimir diretamente.

    Parâmetros:
        c (Collection[Any]): Coleção contendo qualquer tipo de dado, essa coleção será desempacotada após ser processada por para_tabela().
        i (bool):            Habilita ou desabilita a inserção de índice.

    Retorna:
        None
    """

    imprime_tabela(*para_tabela(c), indice=i)


def cadastrar_produto(
    lista_de_produtos: list[Produto], produto: Produto = None
) -> None:
    """
    Cadastra um novo produto na lista de produtos.

    Parâmetros:
        lista_de_produtos (list[Produto]): Lista de produtos já cadastrados.

    Retorna:
        None
    """

    id = lista_de_produtos[-1].id + 1 if len(lista_de_produtos) else 0
    nome = input("Nome do produto: ")
    descricao = input("Descrição do produto: ")
    preco = input("Preço do produto: ")

    try:
        novo_produto = construir_produto(
            id=id, nome=nome, descricao=descricao, preco=preco
        )
        lista_de_produtos.append(novo_produto)
        print("Produto cadastrado.")
        print(novo_produto)

    except Exception as e:
        print(e)


def cadastrar_venda(
    vendas: dict[int, tuple[str, int]],
    lista_de_clientes: list[Cliente],
    lista_de_produtos: list[Produto],
    validador: bool = False,
) -> None:
    """
    Registra uma nova venda a partir do CPF do comprador e do ID do produto.

    Parâmetros:
        vendas (dict[str, int]): Um dicionário que armazena as vendas registradas.
            Cada chave é um número de venda e cada valor é uma tupla com o CPF do comprador e o ID do produto.
        lista_de_clientes (list[Cliente]): Uma lista com os clientes cadastrados.
        lista_de_produtos (list[Produto]): Uma lista com os produtos cadastrados.
        validador (bool, optional): Uma flag que indica se o CPF deve ser validado. O padrão é False.

    Retorna:
        None

    Exemplo:
        >>> cadastrar_venda({}, [Cliente(nome="João", email="joao@gmail.com", cpf="111.111.111-11")],
        ...                  [Produto(id=1, nome="Produto 1", descricao="Descrição do Produto 1", preco=10.0)], validador=False)
        Informe o CPF do comprador: 111.111.111-11
        Informe o ID do produto: 1
        Venda concluída.

    """

    # Auto incremento
    quantidade_de_vendas = len(vendas)
    numero_da_venda = 0 if quantidade_de_vendas else quantidade_de_vendas

    cpf = input("Informe o CPF do comprador: ")
    id = input("Informe o ID do produto: ")

    id = id.strip()
    cpf = cpf.strip()

    padrao_cpf = re.compile(r"\d{3}\.\d{3}\.\d{3}-\d{2}")

    if not padrao_cpf.match(cpf):
        print(f'Formato de CPF incorreto: {[cpf]}, use: "xxx.xxx.xxx-xx".')
        return

    if not id.isnumeric():
        print(f'O ID precisa ser um número, ID: "{id}".')
        return

    id = int(id)

    if validador:
        if not validar_cpf(cpf):
            print("CPF inválido.")
            return

    # Checar se ID e CPF existem na base.
    checagem = 0
    for cliente in lista_de_clientes:
        if cliente.cpf == cpf:
            checagem += 1

    for produto in lista_de_produtos:
        if produto.id == id:
            checagem += 1

    if checagem == 2:
        vendas[numero_da_venda] = (cpf, id)
        print("Venda concluída.")

    elif checagem > 2:
        print("Existem clientes ou produtos duplicados.")
        print("Venda cancelada.")

    else:
        print("Cliente ou produto não encontrado na base de dados.")


def cadastrar_cliente(
    lista_de_clientes: list[Cliente], validador: bool = False
) -> None:
    """
    Adiciona um novo cliente à lista de clientes.

    Parâmetros:
        lista_de_clientes (list[Cliente]): Lista de clientes já cadastrados.
        validador (bool): Indica se deve validar o CPF.

    Retorna:
        None: Não retorna nenhum valor.

    Exemplo:
        clientes = []
        cadastrar_cliente(clientes)
        # Adiciona um novo cliente à lista de clientes.

    """

    nome = input("Nome do cliente: ")
    email = input("E-mail do cliente: ")
    cpf = input("CPF do cliente: ")

    novo_cliente = construir_cliente(nome, email, cpf, validador)

    try:
        for cliente in lista_de_clientes:
            if cliente.email == email or cliente.cpf == cpf:
                print("CPF ou e-mail já cadastrados.")
                return

        lista_de_clientes.append(novo_cliente)
        print("Cadastro concluido.")
        print(novo_cliente)

    except Exception as e:
        print(e)


def ver_todos_os_objetos(
    lista_de_objetos: list[Union[Cliente, Produto]], indice: bool = False
) -> None:
    """
    Exibe todos os objetos (Cliente ou Produto) em formato de tabela.

    Parâmetros:
        lista_de_objetos (list[Union[Cliente, Produto]]): Lista de clientes ou produtos.
        indice           (bool): True para inserir índice e False para não inserir.

    Retorna:
        None
    """

    tabela(lista_de_objetos, indice)


def buscar_por_atributo(
    dado: str, nome_do_atributo: str, lista_de_objetos: list[object]
) -> tuple[list[object]]:
    """
    Busca um dado dentre os atributos dos objetos listados.

    Parâmetros:
        dado (str): Dado que se quer buscar.
        nome_do_atributo (str): Nome do atributo onde se deve procurar o dado.
        lista_de_objetos (list[object]): Lista de objetos onde se deve buscar o dado.

    Retorna:
        tuple[list[object], str]: Lista de objetos que contém o dado e uma string indicando se foi encontrado exatamente ("Encontrado"),
        se há sugestões de resultados ("Sugestão") ou se não foi encontrado ("Não encontrado").
    """

    dado = remover_acentos(dado)

    def jaccard(string_1: str, string_2: str) -> float:
        """
        Calcula a similaridade entre duas strings.

        Parâmetros:
            string_1 (str): Primeira string.
            string_2 (str): Segunda string.

        Retorna:
            Similaridade de 0.0 até 1.0.

        Exemplo:
            >>> jaccard('João', 'Jooã')
            1.0
            >>> jaccard("Vinicius", "Vini")
            0.5
        """
        # https://en.wikipedia.org/wiki/Jaccard_index

        conjunto_1 = set(string_1.capitalize())
        conjunto_2 = set(string_2.capitalize())

        interseccao = len(conjunto_1 & conjunto_2)
        uniao = len(conjunto_1 | conjunto_2)

        return interseccao / uniao

    if not hasattr(lista_de_objetos[0], nome_do_atributo):
        raise Exception(
            f'Objeto {objeto} não possui o atributo "{nome_do_atributo}".')

    objetos_corretos = []
    objetos_proximos = []

    for objeto in lista_de_objetos:
        atributo = getattr(objeto, nome_do_atributo)
        atributo = remover_acentos(atributo)

        if atributo == dado:
            objetos_corretos.append(objeto)

        elif (similaridade := jaccard(dado, atributo)) <= 0.5:
            continue

        else:
            # Só adiciona caso a similidaridade seja igual ou superior a 50%
            objetos_proximos.append((objeto, similaridade))

    objetos_proximos = sorted(
        objetos_proximos, key=lambda x: x[1], reverse=True)

    objetos_proximos = list(map(lambda x: x[0], objetos_proximos))

    if objetos_corretos:
        return objetos_corretos, "Encontrado"

    elif objetos_proximos:
        return objetos_proximos, "Sugestão"

    else:
        return None, "Não encontrado"


def ver_cliente(lista_de_clientes: list[Cliente]) -> None:
    """
    Permite a busca de clientes a partir do seu nome, e-mail ou CPF e exibe os resultados na forma de uma tabela.

    Parâmetros:
        lista_de_clientes (list[Cliente]): Lista de objetos da classe Cliente.

    Retorna:
        None
    """

    dado = input("Dê algum dado do cliente [Nome/e-mail/CPF]: ")

    dado = dado.strip()

    # Somente CPF termina com digito
    cpf = dado[-1].isdigit()

    # Somente e-mail tem @.
    email = "@" in dado

    # Se não for e-mail e CPF é nome.
    nome = not cpf and not email

    if nome:
        dado = dado.capitalize()
        nomes, tipo = buscar_por_atributo(dado, "nome", lista_de_clientes)
        if tipo == "Encontrado":
            tabela(nomes)
        elif tipo == "Não encontrado":
            print(tipo)
        else:
            possiveis_resultados = len(nomes)
            if possiveis_resultados > 1:
                texto = f'"{dado.capitalize()}" não encontrado, exibir outros {len(nomes)} possíveis resultados? S(im)/[N(ão)]: '
            else:
                texto = f"Você quis dizer {nomes[0].nome}? S(im)/[N(ão)]: "
            confirmacao = input(texto)
            if "s" in confirmacao.lower():
                tabela(nomes)
            else:
                print("Nenhum resultado encontrado.")

    elif email:
        emails, tipo = buscar_por_atributo(dado, "email", lista_de_clientes)
        if tipo == "Encontrado":
            tabela(emails)
        elif tipo == "Não encontrado":
            print(tipo)
        else:
            possiveis_resultados = len(emails)
            if possiveis_resultados > 1:
                texto = f'"{dado.capitalize()}" não encontrado, exibir outros {len(emails)} possíveis resultados? S(im)/[N(ão)]: '
            else:
                texto = f"Você quis dizer {emails[0].email}? S(im)/[N(ão)]: "
            confirmacao = input(texto)
            if "s" in confirmacao.lower():
                tabela(emails)
            else:
                print("Nenhum resultado encontrado.")

    else:
        for cliente in lista_de_clientes:
            if cliente.cpf == dado:
                tabela([cliente])
                return


def ver_produto(lista_de_produtos: list[Produto]) -> None:
    """
    Permite a busca de produtos a partir do seu nome ou ID e exibe os resultados na forma de uma tabela.

    Parâmetros:
        lista_de_produtos (list[Produto]): Lista de objetos da classe Produto.

    Retorna:
        None
    """
    dado = input("Dê algum dado do produto [ID/nome]: ")
    dado = dado.strip().lower()

    # Se dado é numérico, é considerado como ID.
    if dado.isnumeric():
        id_produto = int(dado)
        for produto in lista_de_produtos:
            if produto.id == id_produto:
                tabela([produto])
                return
        print("Produto não encontrado.")

    # Caso contrario é nome.
    else:
        nomes, tipo = buscar_por_atributo(dado, "nome", lista_de_produtos)
        if tipo == "Encontrado":
            tabela(nomes)
        elif tipo == "Não encontrado":
            print(tipo)
        else:
            possiveis_resultados = len(nomes)
            if possiveis_resultados > 1:
                texto = f'"{dado.capitalize()}" não encontrado ou duplicado, exibir outros {len(nomes)} possíveis resultados? S(im)/[N(ão)]: '
            else:
                texto = f"Você quis dizer {nomes[0].nome}? S(im)/[N(ão)]: "
            confirmacao = input(texto)
            if "s" in confirmacao.lower():
                tabela(nomes)
            else:
                print("Nenhum resultado encontrado.")


def ver_vendas(vendas: dict[str, int]) -> None:
    """
    Exibe todas as vendas.

    Parâmetros:
        vendas (dict[str, int]): Dicionário que usa o número da venda para armazenar uma tupla contendo o CPF do cliente e o ID do produto.

    Retorna:
        None
    """

    imprime_tabela(
        *dicionario_para_tabela(vendas, ["Número da venda", "CPF", "ID do produto"])
    )


def atualizar_cliente(lista_de_clientes: list[Cliente]) -> None:
    """
    Atualiza as informações de um cliente em uma lista de clientes.

    Parâmetros:
        lista_de_clientes (list[Cliente]): Uma lista de clientes para atualizar.

    Retorna:
        None

    Exemplo:
        Para atualizar as informações de um cliente em uma lista de clientes:

        >>> clientes = [Cliente("João", "joao@gmail.com", "123.456.789-00"),
                        Cliente("Maria", "maria@gmail.com", "987.654.321-00")]

        >>> atualizar_cliente(clientes)
        Digite o CPF do cliente: 123.456.789-00
        Atualizando cliente: João.
        Digite os dados solicitados, deixe em vazio caso não queira alterar.
        Nome:
        E-mail:
        CPF:

        >>> clientes
        [Cliente(nome='João', email='joao@gmail.com', cpf='123.456.789-00'),
         Cliente(nome='Maria', email='maria@gmail.com', cpf='987.654.321-00')]
    """

    cpf = input("Digite o CPF do cliente: ")

    for i, cliente in enumerate(lista_de_clientes):
        if cliente.cpf == cpf:
            print(f"Atualizando cliente: {cliente.nome}.")
            print(
                "Digite os dados solicitados, deixe em vazio caso não queira alterar."
            )

            # input() antes do "or" garante que cliente.* só será atribuído caso o retorno do input() seja vazio.
            novo_nome = input("Nome: ") or cliente.nome
            novo_email = input("E-mail: ") or cliente.email
            novo_cpf = input("CPF: ") or cliente.cpf

            try:
                novo_cliente = construir_cliente(
                    novo_nome, novo_email, novo_cpf)
                lista_de_clientes[i] = novo_cliente
                print("Cliente atualizado com sucesso.")
                return

            except Exception:
                print("Algo falhou.")
                return

    print("Nenhum cliente com esse CPF encontrado.")


def atualizar_produto(lista_de_produtos: list[Produto]) -> None:
    """
    Atualiza as informações de um produto em uma lista de produtos.

    Parâmetros:
        lista_de_produtos (list[Produto]): Uma lista de produtos para atualizar.

    Retorna:
        None


    Exemplo:
        Para atualizar as informações de um produto em uma lista de produtos:

        >>> produtos = [Produto("Celular", "Um celular moderno", 1500),
                        Produto("Notebook", "Um notebook rápido", 2500)]

        >>> atualizar_produto(produtos)
        Digite o ID do produto: 1
        Atualizando produto: Celular.
        Digite os dados solicitados, deixe em vazio caso não queira alterar.
        Nome:
        Descrição:
        Preço:

        >>> produtos
        [Produto(nome='Celular', descricao='Um celular moderno', preco=1500),
         Produto(nome='Notebook', descricao='Um notebook rápido', preco=2500)]
    """

    id = input("Digite o ID do produto: ")
    try:
        id = int(id)
    except ValueError:
        print("ID não encontrado.")
        return

    for i, produto in enumerate(lista_de_produtos):
        if produto.id == id:
            print(f"Atualizando produto: {produto.nome}.")
            print(
                "Digite os dados solicitados, deixe em vazio caso não queira alterar."
            )

            # input() antes do "or" garante que cliente.* só será atribuído caso o retorno do input() seja vazio.
            novo_nome = input("Nome: ") or produto.nome
            nova_descricao = input("Descrição: ") or produto.descricao
            novo_preco = input("Preço: ") or produto.preco

            try:
                novo_produto = construir_produto(
                    id, novo_nome, nova_descricao, novo_preco)
                lista_de_produtos[i] = novo_produto
                print("Produto atualizado com sucesso.")
                return

            except Exception as e:
                print(e)
                print("Algo falhou.")
                return

    print("Nenhum produto com esse ID encontrado.")


def main() -> None:
    validador = (
        "s" in input(
            "Deseja ativar o validador de CPF? S(im)/[N(ão)]: ").lower()
    )

    menu = """
========= MENU =========
[0]  Cadastrar cliente
[1]  Ver dados de um cliente específico
[2]  Visualizar todos os dados dos clientes cadastrados
[3]  Cadastrar produto
[4]  Ver dados de um produto específico
[5]  Visualizar todos os dados dos produtos cadastrados
[6]  Efetuar uma venda
[7]  Visualizar vendas
[8]  Sair
[9]  Atualizar dados de um cliente específico
[10] Atualizar dados de um produto específico
[?]  Exibe o menu
=========================
"""

    lista_de_clientes: list[Cliente] = []
    lista_de_produtos: list[Produto] = []
    vendas: dict[int, tuple[str, int]] = {}

    print(menu)
    while True:
        # Limpar sujeiras nas listas e dicionários.
        for i in range(len(lista_de_clientes)):
            if type(lista_de_clientes[i]) == None:
                del lista_de_clientes[i]

        for i in range(len(lista_de_produtos)):
            if type(lista_de_produtos[i]) == None:
                del lista_de_produtos[i]

        try:
            opcao = input("[0/1/2/3/4/5/6/7/8/9/10/?]\n>>> ")
            if opcao == "0":
                cadastrar_cliente(lista_de_clientes, validador)
            elif opcao == "1":
                ver_cliente(lista_de_clientes)
            elif opcao == "2":
                ver_todos_os_objetos(lista_de_clientes, indice=True)
            elif opcao == "3":
                cadastrar_produto(lista_de_produtos)
            elif opcao == "4":
                ver_produto(lista_de_produtos)
            elif opcao == "5":
                ver_todos_os_objetos(lista_de_produtos)
            elif opcao == "6":
                cadastrar_venda(vendas, lista_de_clientes,
                                lista_de_produtos, validador)
            elif opcao == "7":
                ver_vendas(vendas)
            elif opcao == "8":
                print("Saindo.")
                break
            elif opcao == "9":
                atualizar_cliente(lista_de_clientes)
            elif opcao == "10":
                atualizar_produto(lista_de_produtos)
            elif opcao == "?":
                print(menu)
            else:
                print(f'Opção inválida: "{opcao}".')

        except Exception as e:
            print(f"Erro: {e}")


main()
