from usuario import criarUsuario, editarUsuario, deletarUsuario, listarUsuario, listarTodosUsuarios

print('-------- MongoDB -----------')

def menuAcoes():
    print('\nEscolha uma opção: ')
    print('''
        1 - Criar
        2 - Atualizar
        3 - Deletar
        4 - Listar um em especifico
        5 - Listar  todos
        0 - Sair
    ''')
    escolha = int(input("Opção escolhida: "))
    return escolha

while True:
    print('\nQual coleção deseja gerenciar?')
    print('''
        1 - Usuário
        2 - Vendedor
        3 - Produto
        4 - Compra
        5 - Favorito
        0 - Sair
    ''')

    escolha = int(input("Opção escolhida: "))

    match escolha:
        case 1:
            acao = menuAcoes()
            match acao:
                case 1:
                    criarUsuario()
                case 2:
                    editarUsuario()
                case 3:
                    deletarUsuario()
                case 4:
                    listarUsuario()
                case 5:
                    listarTodosUsuarios()
        case 2:
            acao = menuAcoes()
            match acao:
                case 1:
                    criarVendedor()
                case 2:
                    editarVendedor()
                case 3:
                    deletarVendedor()
                case 4:
                    listarVendedor()
                case 5:
                    listarTodosVendedores()
        case 3:
            acao = menuAcoes()
            match acao:
                case 1:
                    criarProduto()
                case 2:
                    editarProduto()
                case 3:
                    deletarProduto()
                case 4:
                    listarProduto()
                case 5:
                    listarTodosProdutos()
        case 4:
            acao = menuAcoes()
            match acao:
                case 1:
                    criarCompra()
                case 2:
                    editarCompra()
                case 3:
                    deletarCompra()
                case 4:
                    listarCompra()
                case 5:
                    listarTodasCompras()
        case 5:
            acao = menuAcoes()
            match acao:
                case 1:
                    criarFavorito()
                case 2:
                    editarFavorito()
                case 3:
                    deletarFavorito()
                case 4:
                    listarFavorito()
                case 5:
                    listarTodosFavoritos()
        case 0:
            break
        case _:
            print('Opção não invalida!')