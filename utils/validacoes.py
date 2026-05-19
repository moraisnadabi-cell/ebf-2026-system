def validar_idade(idade):

    if idade.isdigit():

        idade = int(idade)

        if idade > 0 and idade < 18:
            return True

    return False


def validar_texto(texto):

    if texto.strip() == '':
        return False

    return True


def validar_telefone(telefone):

    telefone = telefone.replace(' ', '')
    telefone = telefone.replace('-', '')
    telefone = telefone.replace('(', '')
    telefone = telefone.replace(')', '')

    return telefone.isdigit()