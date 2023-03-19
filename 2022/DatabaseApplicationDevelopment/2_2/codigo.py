import csv
import json

# Definição de constantes
NOME_ARQUIVO_CSV = "_2Semestre2CheckpointDBApp.csv"
NOME_ARQUIVO_JSON = "_2Semestre2CheckpointDBApp.json"


def ler_csv() -> list:
    """Retorna o conteudo de um arquivo CSV."""

    with open(NOME_ARQUIVO_CSV, "r", newline="", encoding="UTF-8") as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")
        colunas = next(leitor)
        linhas = list(leitor)
        estrutura = [colunas, linhas]
    return estrutura


def escrever_csv(linha: list) -> None:
    """Escreve uma lista de linhas no arquivo CSV."""

    print(f"📝 Dados escritos em {NOME_ARQUIVO_CSV}")
    with open(NOME_ARQUIVO_CSV, "a", newline="", encoding="UTF-8") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(linha)


def imprimir_tabela(colunas: list, linhas: list) -> None:
    """Formata a tabela para ser exibida no terminal."""

    # Adicionar coluna indice e preencher linhas com 0 até len(linhas).

    # Ordenar com base no nome do tutor.
    linhas.sort(key=lambda x: x[1])

    colunas.insert(0, "Indice")
    for i in range(len(linhas)):
        linhas[i].insert(0, i + 1)

    # Ajuste automático do tamanho das colunas baseado no maior valor de cada celula.
    tamanho = max(len(str(celula)) for linha in linhas for celula in linha) + 2

    # Imprimir cabeçalho.
    print("┌" + "┬".join("─" * tamanho for _ in colunas) + "┐")
    print("│" + "│".join(str(celula).center(tamanho)
                         for celula in colunas) + "│")
    print("├" + "┼".join("─" * tamanho for _ in colunas) + "┤")

    # Imprimir linhas.
    for linha in linhas:
        if linha:  # Ignora linhas vazias.
            print("│" +
                  "│".join(str(celula).center(tamanho)
                           for celula in linha) + "│")
            if not linha == linhas[-1]:  # Ignora a última linha.
                print("├" + "┼".join("─" * tamanho for _ in colunas) + "┤")

    # Imprimir rodapé.
    print("└" + "┴".join("─" * tamanho for _ in colunas) + "┘")


def listar():
    """Lista todos os registros do arquivo."""

    colunas, linhas = ler_csv()
    imprimir_tabela(colunas, linhas)


def cadastrar(nome_pet: str = None,
              tutor: str = None,
              especie: str = None,
              idade: int = None) -> None:
    """Cadastra um novo registro no arquivo CSV."""

    if not nome_pet:
        nome_pet = input("🐶🐱 Nome do pet: ")
    if len(nome_pet) < 3 or len(nome_pet) > 30:
        print("🟥 Nome do pet precisa ter de 3 a 30 caracteres.")
        return cadastrar()

    if not tutor:
        tutor = input("👨👩 Nome do tutor(a): ")
    if len(tutor) < 3 or len(tutor) > 30:
        print("🟥 Nome do tutor precisa ter de 3 a 30 caracteres.")
        return cadastrar(nome_pet=nome_pet)

    if not especie:
        especie = input("🧬 Espécie: ")
    if len(especie) < 3 or len(especie) > 30:
        print("🟥 Especie precisa ter de 3 a 30 caracteres.")
        return cadastrar(nome_pet=nome_pet, tutor=tutor)

    if not idade:
        idade = input("⌛ Idade: ")
    if not idade.isnumeric():
        print("🟥 Idade precisa ser um número.")
        return cadastrar(nome_pet=nome_pet, tutor=tutor, especie=especie)
    elif int(idade) < 0 or int(idade) > 100:
        print("🟥 Idade precisa ser de 0 a 100 anos.")
        return cadastrar(nome_pet=nome_pet, tutor=tutor, especie=especie)

    return escrever_csv([nome_pet, tutor, especie, int(idade)])


def main():
    """Função principal."""

    while True:

        # Processador de comandos.
        comando = input(
            "🤖 O que deseja? [sair/listar/cadastrar/json]\n>>> ").lower()

        if comando == "sair":
            break

        elif comando == "listar":
            listar()

        elif comando == "cadastrar":
            cadastrar()

        elif comando == "json":
            with open(NOME_ARQUIVO_JSON, "w",
                      encoding="UTF-8") as arquivo_json:
                colunas, linhas = ler_csv()

                # Cria um JSON com as colunas como chaves e as linhas como valores.
                javascriptobject = []
                for linha in linhas:
                    dicionario = {}
                    for i in range(len(colunas)):
                        dicionario[colunas[i]] = linha[i]
                    javascriptobject.append(dicionario)

                json.dump(javascriptobject, arquivo_json, indent=4)

            print(f"🟩 Arquivo {NOME_ARQUIVO_JSON} criado com sucesso!")

            if "s" in input("❓ Deseja inspecionar o arquivo? [s/n] ").lower():
                with open(NOME_ARQUIVO_JSON, "r",
                          encoding="UTF-8") as arquivo_json:
                    conteudo = json.load(arquivo_json)
                    print(json.dumps(conteudo, indent=4))

        else:
            print("🟥 Comando inválido.")


main()