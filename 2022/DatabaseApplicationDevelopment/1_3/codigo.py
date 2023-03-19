titulo = '\nCampanha de adoção de gatos PetShop PuppyBel!\n'

def formatar_nome(texto):
    linha = '#'*(len(texto)+4)
    linha += f'\n# {texto} #\n'
    linha += '#'*(len(texto)+4)
    return linha

while input("\nHá gatos a serem adotados? -> ").lower() in ("s", "y", "sim", "yes"):
    cliente_nome = input("Nome do cliente: ")
    cliente_cpf = input("CPF do cliente: ")
    gato_nome = input("Nome do gato: ")
    gato_idade = input("Idade do gato: ")
    gato_sexo = input("Sexo do gato: ")
    cuidados_medicos = input("Cuidados médicos: ")
    
    certificado = \
f"""
{formatar_nome(gato_nome)}
Nome do dono: {cliente_nome},
CPF do dono: {cliente_cpf},
Idade: {gato_idade} anos,
Sexo: {gato_sexo},
Cuidados médicos: {cuidados_medicos}
"""

    print(certificado)

print("Campanha encerrada!")