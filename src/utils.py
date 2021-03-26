from src.algorythms import algos
from src.crypto.models import Algorythm, Alphabet
from src.crypto.serializers import ActionSerializer


def replace_symbols(message:str):
    return message.upper().replace(
        ' ', ''
    ).replace(
        '.', 'ТЧК'
    ).replace(
        ',', 'ЗПТ'
    ).replace(
        '!', 'ВСКЛ',
    ).replace(
        '-', ''
    ).replace(
        '?', 'ВПРС'
    ).replace(
        '1', 'один'
    ).replace(
        '2', 'два'
    ).replace(
        '3', 'три'
    ).replace(
        '4', 'четыре'
    ).replace(
        '5', 'пять'
    ).replace(
        '6', 'шесть'
    ).replace(
        '7', 'семь'
    ).replace(
        '8', 'восемь'
    ).replace(
        '9', 'девять'
    ).replace(
        '0', 'ноль'
    ).replace(
        '\n', ''
    ).replace(
        'Ё', 'Е'
    )


def do_action(data):
    if data.get('alphabet'):
        alphabet = Alphabet.objects.get(id=data['alphabet']).value
    else:
        alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    algo_from_db = Algorythm.objects.get(id=data['algorythm'])
    algorythm = getattr(algos, algo_from_db.class_name)(keys=data['keys'], alph=alphabet)
    if not algo_from_db.no_alphabet:
        data['text'] = replace_symbols(data['text']).upper()
    if (data['action'] == ActionSerializer.ENCRYPT):
        result = algorythm.encrypt(data['text'])
    else:
        result = algorythm.decrypt(data['text'])

    response = {}
    if isinstance(result, str):
        response = {'result': result}
    else:
        response = {
            'result': result['result'],
            'info': result['info'],
        }
    return response
