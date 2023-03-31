# CP1 - Revisão de Python

## [10 pontos] Crie um sistema em Python que contenha pelo menos duas classes: Produto e Cliente.

* O sistema deve permitir criar um cadastro de clientes e produtos.

* Os atributos de Cliente são: Nome, email e CPF. Os atributos do Produto são: ID, nome, preço e descrição.

* O cadastro é uma função que armazena objetos da classe Cliente em uma lista de clientes e objetos da classe Produto em uma lista de produtos.


## O sistema deve exibir um menu com as seguintes opções:

* Digite a opção desejada:
* [0] Cadastrar cliente
* [1] Ver dados de um cliente específico
* [2] Visualizar todos os dados dos clientes cadastrados
* [3] Cadastrar produto
* [4] Ver dados de um produto específico
* [5] Visualizar todos os dados dos produtos cadastrados
* [6] Efetuar uma venda
* [7] Visualizar vendas
* [8] Sair


## Entendendo as opções:

* Na opção [0] o usuário deverá fornecer os dados para cadastrar o objeto da Classe Cliente e este objeto deverá ser armazenado na lista de  clientes.

* Na opção [1] o usuário poderá fornecer o CPF de um cliente e o sistema deve devolver o nome e email.

* Na opção [2] o sistema deverá exibir todos os dados de todos os clientes cadastrados.

* Na opção [3] o usuário deverá fornecer os dados para cadastrar o objeto da Classe Produto e este objeto deverá ser armazenado na lista de produtos.

* Na opção [4] o usuário poderá fornecer o ID de um produto e o sistema deve
devolver o preço, descrição e nome daquele produto.

* Na opção [5] o sistema deverá exibir todos os dados de todos os produtos cadastrados.

* Na opção [6] o sistema deverá armazenar nas chaves de um dicionário “vendas” o número da venda feita (auto incrementada) e nos valores armazenar uma tupla contendo o CPF do cliente e o ID do produto.

* Na opção [7] o sistema deve exibir todos os dados do dicionário “vendas”.

* O sistema só deve encerrar quando o usuário digitar “8”.

## [2 pontos de Bônus] Implemente também as opções de alterar os dados dos clientes e produtos:

* [9] Atualizar dados de um cliente específico.

* [10] Atualizar dados de um produto.

## Nestas opções o usuário poderá alterar qualquer atributo dos objetos das classes Cliente e Produto.