from bson import ObjectId
from db import conectar_mongo

db = conectar_mongo()

colecao_vendedor = db.vendedor
colecao_produto = db.produto

def atualizarProduto(vendedor):
    vendedor_att = colecao_vendedor.find_one({'_id': ObjectId(vendedor['_id'])})


    query_filter_produto = {'vendedor._id': vendedor['_id']}
    update_operation_usuario = { '$set': {'vendedor': vendedor_att}}

    result = colecao_produto.update_many(query_filter_produto, update_operation_usuario)

    if result.modified_count > 0:
        print(f"Proddutos do vendedor atualizado com sucesso!")
    else:
        print("Nenhuma alteração nos produtos do vendedor.")

def mostrarTodosVendedores():
    print("\nListagem de vendedores")
    vendedores = list(colecao_vendedor.find({}))

    for index, vendedor in enumerate(vendedores):
        print(f"{index} - {vendedor['nome']}")

def listarVendedorDict(vendedor_dict):
    for key in vendedor_dict:
        if(key == "endereco"):
            print(f'{key}: {vendedor_dict[key]["rua"]}, {vendedor_dict[key]["bairro"]}, {vendedor_dict[key]["cidade"]}, {vendedor_dict[key]["estado"]}, {vendedor_dict[key]["cep"]}')
            continue
        print(f'{key}: {vendedor_dict[key]}')

def criarVendedor():
    print("\n======== Inserindo um novo vendedor ========")

    nome = input("Nome: ")
    dataNas = input("Data de Nascimento: ")
    telefone = input("Telefone: ")
    email = input("Email: ")
    senha = input("Senha: ")
    cnpj = input("CNPJ: ")

    rua = input("Rua: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("Cep: ")

    vendedor = {
        "nome": nome,
        "dataNascimento": dataNas,
        "telefone": telefone,
        "email": email,
        "senha": senha,
        "cnpj": cnpj,
        "endereco": {
            "rua": rua,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
    }

    doc = colecao_vendedor.insert_one(vendedor)
    print("Documento inserido com ID ", doc.inserted_id)

def editarVendedor():
    print("\n======== Editar um vendedor ========")

    mostrarTodosVendedores()

    opcao = int(input("Escolha uma opção: "))

    vendedores = list(colecao_vendedor.find({}))
    try:
        vendedor_escolhido = vendedores[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(vendedor_escolhido['_id'])}

    nome = input("Nome: ")
    dataNas = input("Data de Nascimento: ")
    telefone = input("Telefone: ")
    email = input("Email: ")
    senha = input("Senha: ")
    cnpj = input("CNPJ: ")

    rua = input("Rua: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("Cep: ")

    vendedor = {
        "nome": nome if nome else vendedor_escolhido["nome"],
        "dataNascimento": dataNas if dataNas else vendedor_escolhido["dataNascimento"],
        "telefone": telefone if telefone else vendedor_escolhido["telefone"],
        "email": email if email else vendedor_escolhido["email"],
        "senha": senha if senha else vendedor_escolhido["senha"],
        "cnpj": cnpj if cnpj else vendedor_escolhido["cnpj"],
        "endereco": {
            "rua": rua if rua else vendedor_escolhido["endereco"]["rua"],
            "bairro": bairro if bairro else vendedor_escolhido["endereco"]["bairro"],
            "cidade": cidade if cidade else vendedor_escolhido["endereco"]["cidade"],
            "estado": estado if estado else vendedor_escolhido["endereco"]["estado"],
            "cep": cep if cep else vendedor_escolhido["endereco"]["cep"]
        }
    }

    update_operation = { '$set' : vendedor }

    result = colecao_vendedor.update_one(query_filter, update_operation)

    if result.modified_count > 0:
        print("Vendedor atualizado com sucesso!")
        atualizarProduto(vendedor_escolhido)
    else:
        print("Nenhuma alteração realizada. Verifique o ID ou dados. ")

def deletarVendedor():
    print("\n======== Remover um vendedor ========")

    mostrarTodosVendedores()

    opcao = int(input("Escolha uma opção: "))

    vendedores = list(colecao_vendedor.find({}))
    try:
        vendedor_escolhido = vendedores[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(vendedor_escolhido['_id'])}

    result = colecao_vendedor.delete_one(query_filter)

    if result.deleted_count > 0:
        print("Vendedor deletado com sucesso!")
        atualizarProduto(vendedor_escolhido)
    else:
        print("Nenhuma alteração realizada. Verifique o ID.")

def listarVendedor():
    print("\n======== Listar um vendedor ========")

    mostrarTodosVendedores()

    opcao = int(input("Escolha uma opção: "))

    vendedores = list(colecao_vendedor.find({}))
    try:
        vendedor_escolhido = vendedores[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(vendedor_escolhido['_id'])}

    result = colecao_vendedor.find_one(query_filter)

    listarVendedorDict(result)


def listarTodosVendedores():
    print("\n======== Listar todos vendedores ========")
    vendedores = list(colecao_vendedor.find({}))
    
    for vendedor in vendedores:
        print("------------------------------------------------------")
        listarVendedorDict(vendedor)