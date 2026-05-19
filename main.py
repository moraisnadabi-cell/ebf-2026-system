from cadastro import (
    cadastrar_crianca,
    listar_criancas,
    total_inscritos,
    buscar_crianca,
    filtrar_por_igreja,
    editar_cadastro,
    remover_cadastro
)

while True:

    print('\n=== SISTEMA EBF ===')
    print('1 - Cadastrar criança')
    print('2 - Listar crianças')
    print('3 - Ver total de inscritos')
    print('4 - Buscar criança')
    print('5 - Filtrar por igreja')
    print('6 - Editar cadastro')
    print('7 - Remover cadastro')
    print('8 - Sair')

    opcao = input('Escolha uma opção: ')

    if opcao == '1':
        cadastrar_crianca()

    elif opcao == '2':
        listar_criancas()

    elif opcao == '3':
        total_inscritos()

    elif opcao == '4':
        buscar_crianca()

    elif opcao == '5':
        filtrar_por_igreja()

    elif opcao == '6':
        editar_cadastro()

    elif opcao == '7':
        remover_cadastro()

    elif opcao == '8':
        print('Sistema encerrado.')
        break

    else:
        print('Opção inválida.')