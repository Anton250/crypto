def square_hash(mes: list, module: int):
    result = 0
    for l in mes:
        result = (result + l)**2 % module
    return result