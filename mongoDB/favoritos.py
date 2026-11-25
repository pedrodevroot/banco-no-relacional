from bson import ObjectId
from db import conectar_mongo

from produto import mostrarTodosProdutos
from usuario import mostrarTodosUsuarios
 
db = conectar_mongo()

colecao_favorito = db.favorito
colecao_produto = db.produto
colecao_usuario = db.usuario

def atualizarusuarioFavoritos(favorito):

    query_filter_usuario = {'_id': ObjectId(favorito["usuario"]["_id"])}

    usuario_favoritos = list(colecao_favorito.find({'usuario._id': favorito["usuario"]["_id"]}))
    novos_favoritos = [fav["produto"] for fav in usuario_favoritos]

    update_operacao_usuario = { "$set": {"favoritos": novos_favoritos}}

    result_usuario = colecao_usuario.update_one(query_filter_usuario, update_operacao_usuario)

    if result_usuario.modified_count > 0:
        print(f"Lista de favoritos do usuario atualizada com sucesso!")
    else:
        print("Nenhuma alteração da lista de favortios do usuario")

def mostrarTodosFavortios():
    print("\nLista de favoritos")
    favoritos = list(colecao_favorito.find({}))

    for index, favorito in enumerate(favoritos):
        print(f"{index} - {favorito['produto']['nome']} de {favorito['usuario']['nome']}")

def listarFavoritoDict(favorito_dict):
    for key in favorito_dict:
        if(key == "produto"): 
            print('-- Informações do produto')
            for produto_key in favorito_dict["produto"]:
                if(produto_key == "vendedor"): 
                    print(f'{produto_key}: {favorito_dict[key][produto_key]["nome"]}')
                    continue
                print(f'{produto_key}: {favorito_dict[key][produto_key]}')
            continue
        if(key == "usuario"): 
            print('-- Informações do usuário')
            for usuario_key in favorito_dict["usuario"]:
                if(usuario_key == "favoritos"): continue
                print(f'{usuario_key}: {favorito_dict[key][usuario_key]}')
            continue
        print(f'{key}: {favorito_dict[key]}')

def criarFavorito():
    print("\n======== Inserindo um novo favorito ========")

    print("Escolha um produto para favoritar: ")
    mostrarTodosProdutos()

    opcao_produto = int(input("Escolha o index do produto desejado: "))
    produtos = list(colecao_produto.find({}))

    try:
        produto_escolhido = produtos[opcao_produto]
    except IndexError:
        print("Opção não encontrada!")
        return

    print("Escolha um usuario: ")

    mostrarTodosUsuarios()

    usuario_opcao = int(input("Index do usuario escolhido: "))
    usuarios = list(colecao_usuario.find({}))

    try:
        usuario_escolhido = usuarios[usuario_opcao]
    except IndexError:
        print("Opção não encontrada!")
        return

    favorito = {
        "usuario": usuario_escolhido,
        "produto": produto_escolhido
    }

    doc = colecao_favorito.insert_one(favorito)
    print("Documendo inserido com ID ", doc.inserted_id)

    query_filter = {"_id": ObjectId(usuario_escolhido["_id"])}
    update_operacao = { "$push": {"favoritos": favorito["produto"]}}

    result = colecao_usuario.update_one(query_filter, update_operacao)
    if result.modified_count > 0:
        print(f"Favorito adicionado ao usuário com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique os dados.")

def editarFavorito():
    print("\n======== Editar um favorito ========")

    mostrarTodosFavortios()

    opcao = int(input("Escolha o index: "))

    favoritos = list(colecao_favorito.find({}))
    try:
        favorito_escolhido = favoritos[opcao]
    except IndexError:
        print("Opção não encontrada!")
        return

    query_filter = {"_id": ObjectId(favorito_escolhido["_id"])}

    print("Escolha um novo produto para o favoritar :")
    mostrarTodosProdutos()

    opcao_produto = int(input("Escolha o index: "))
    produtos = list(colecao_produto.find({}))

    try:
        produto_escolhido = produtos[opcao_produto]
    except IndexError:
        print("Opção não encontrada!")
        return

    favorito_escolhido["produto"] = produto_escolhido

    update_operecao = { '$set': {'produto': produto_escolhido}}

    result = colecao_favorito.update_one(query_filter, update_operecao)

    if result.modified_count > 0:
        print(f"favorito atualizado com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique os dados.")

    atualizarusuarioFavoritos(favorito_escolhido)

def deletarFavorito():
    print("\n======== Remover um Favorito ========")

    mostrarTodosFavortios()

    opcao = int(input("escolha o index: "))

    favoritos = list(colecao_favorito.find({}))
    try:
        favorito_escolhido = favoritos[opcao]
    except IndexError:
        print("Opção não encontrada!")
        return

    query_filter = {"_id": ObjectId(favorito_escolhido["_id"])}

    result = colecao_favorito.delete_one(query_filter)

    if result.deleted_count > 0:
        print("favorito deletado com sucesso!")
        atualizarusuarioFavoritos(favorito_escolhido)
    else:
        print("Nenhuma alteraçao realizada, verifique os dados")

def listarFavorito():
    print("\n======== Listar um favorito ========")

    mostrarTodosFavortios()

    opcao = int(input("Escolha um index: "))

    favoritos = list(colecao_favorito.find({}))
    try:
        favorito_escolhido = favoritos[opcao]
    except IndexError:
        print("Opção não encontrada! verifique os dados")
        return

    query_filter = {"_id": ObjectId(favorito_escolhido["_id"])}

    result = colecao_favorito.find_one(query_filter)

    print("\n")
    listarFavoritoDict(result)

def listarTodosFavoritos():
    print("\n======== Listar todos favoritos ========")
    favoritos = list(colecao_favorito.find({}))

    for favorito in favoritos:
        print("------------------------------------------------------")
        listarFavoritoDict(favorito)


        
    