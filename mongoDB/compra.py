from bson import ObjectId
from db import conectar_mongo

from produto import mostrarTodosProdutos
from usuario import mostrarTodosUsuarios

db = conectar_mongo()

colecao_compra = db.compra

colecao_usuario = db.usuario
colecao_produto = db.produto

def mostrarTodasCompras():
    print("\nListagem de Compras")
    compras = list(colecao_compra.find({}))

    for index, compra in enumerate(compras):
        print(f"{index} - {compra['usuario']['nome']} - {compra['data']}: R${compra['valor']}")

def listarCompraDict(compra_dict):
    for key in compra_dict:
        if(key == "produtos"): 
            print("-- Produtos: ")
            for item_compra in compra_dict["produtos"]:
                print(f"> {item_compra['produto']['nome']} | Quantidade: {item_compra['quantidade']} | Subtotal: {item_compra['subtotal']}")
            continue
        if(key == "usuario"):
            print(f"{key}: {compra_dict[key]['nome']}")
            continue
        print(f'{key}: {compra_dict[key]}')

def criarCompra():
    print("\n======== Inserindo uma nova compra ========")

    data = input("Data: ")

    print("Escolha os produtos e suas quantidades: ")
    itens = []

    while True:
        mostrarTodosProdutos()

        opcao_produto = int(input("Escolha uma opção: "))
        produtos = list(colecao_produto.find({}))

        try:
            produto_escolhido = produtos[opcao_produto]
        except IndexError:
            print("Índice não encontrado! Por favor, escolha um índice válido.")
            return

        while True:
            quantidade = int(input(f"Quantidade (disponivel: {produto_escolhido['quantidade']}): "))

            if(quantidade > int(produto_escolhido['quantidade'])):
                print(f"Quantidade indisponível.")
            else:
                break

        item_compra = {
            "produto": produto_escolhido,
            "quantidade": quantidade,
            "subtotal": float(produto_escolhido['preco']) * quantidade
        }

        itens.append(item_compra)
        
        escolha = input("Deseja adicionar mais produtos? [S/N] ")
        if escolha.lower() in ['n', 'nao', 'não']: break

    print('Associe essa compra a um usuário: ')
    mostrarTodosUsuarios()

    usuario_opcao = int(input("Index da opção escolhida: "))
    usuarios = list(colecao_usuario.find({}))

    try:
        usuario_escolhido = usuarios[usuario_opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return
    
    total_sugerido = 0
    for item in itens:
        total_sugerido += item['subtotal']

    valor = float(input(f"Valor total (calculado: {total_sugerido}): "))
    
    compra = {
        "data": data,
        "valor": valor,
        "produtos": itens,
        "usuario": usuario_escolhido
    }

    doc = colecao_compra.insert_one(compra)
    print("Documento inserido com ID ",doc.inserted_id)
 
    for item in itens:
        query_filter = {'_id': ObjectId(item['produto']['_id'])}
        update_operation = { '$set' : {'quantidade': int(item['produto']['quantidade']) - int(item['quantidade'])} }

        result = colecao_produto.update_one(query_filter, update_operation)
        if result.modified_count > 0:
            print(f"Quantidade do produto {item['produto']['nome']} atualizado com sucesso!")
        else:
            print("Nenhuma alteração realizada. Verifique o ID ou os dados.")

def editarCompra():
    print("\n======== Editar uma compra ========")


    mostrarTodasCompras()

    opcao_compra = int(input("Index da compra escolhida: "))
    compras = list(colecao_compra.find({}))

    try:
        compra_escolhida = compras[opcao_compra]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    print(f"\nProdutos da compra:")
    for idx, item in enumerate(compra_escolhida['produtos']):
        print(f"{idx} - {item['produto']['nome']} | Quantidade: {item['quantidade']} | Subtotal: {item['subtotal']}")

    print("\nDeseja editar algum produto dessa compra? [S/N]")
    escolha_produto = input().lower()
    
    if escolha_produto in ['s', 'sim']:
        while True:
            produto_idx = int(input("Escolha o produto para editar: "))
            produto = compra_escolhida['produtos'][produto_idx]
            produto_escolhido = produto['produto']

            quantidade_nova = int(input(f"Nova quantidade para {produto_escolhido['nome']} (disponível: {produto_escolhido['quantidade']}): "))
            if quantidade_nova > int(produto_escolhido['quantidade']):
                print(f"Quantidade indisponível. Tente novamente.")
            else:
                subtotal = quantidade_nova * float(produto_escolhido['preco'])
                produto['quantidade'] = quantidade_nova
                produto['subtotal'] = subtotal
                print(f"Produto {produto_escolhido['nome']} atualizado.")

            continuar = input("Deseja editar outro produto? [S/N]").lower()
            if continuar not in ['s', 'sim']:
                break

    data = input(f"Data (atual: {compra_escolhida['data']}): ")
    valor_total = float(input(f"Valor total (atual: {compra_escolhida['valor']}): "))

    mostrarTodosUsuarios()
    usuario_opcao = int(input("Index da opção escolhida para o usuário: "))
    usuarios = list(colecao_usuario.find({}))

    try:
        usuario_escolhido = usuarios[usuario_opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    compra = {
        "data": data if data else compra_escolhida['data'],
        "valor": valor_total if valor_total else compra_escolhida['valor'],
        "produtos": compra_escolhida['produtos'],  
        "usuario": usuario_escolhido
    }

    query_filter = {'_id': ObjectId(compra_escolhida['_id'])}
    update_operation = {'$set': compra}

    result = colecao_compra.update_one(query_filter, update_operation)

    if result.modified_count > 0:
        print(f"Compra atualizada com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique o ID ou os dados.")

def deletarCompra():
    print("\n======== Remover uma Compra ========")

    mostrarTodasCompras()

    opcao = int(input("Index da opção escolhida: "))

    compras = list(colecao_compra.find({}))
    try:
        compras_escolhida = compras[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(compras_escolhida['_id'])}

    result = colecao_compra.delete_one(query_filter)

    if result.deleted_count > 0:
        print("Compra deletada com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique o ID.")

def listarCompra():
    print("\n======== Listar uma compra ========")

    mostrarTodasCompras()

    opcao = int(input("Index da opção escolhida: "))

    compras = list(colecao_compra.find({}))
    try:
        compra_escolhida = compras[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(compra_escolhida['_id'])}

    result = colecao_compra.find_one(query_filter)

    listarCompraDict(result)


def listarTodasCompras():
    print("\n======== Listar todas compras ========")
    compras = list(colecao_compra.find({}))
    
    for compra in compras:
        print("------------------------------------------------------")
        listarCompraDict(compra)






