# Окунев Степан 181-351
# ЯП - python
# нумерация букв в алфавите с 0
alf='абвгдежзийклмнопрстуфхцчшщъыьэюя' # алфавит
alf1='абвгдеёжзийклмнопрстуфхцчшщъыьэюя' # алфавит с Ё
magma_table=['0123456789abcdef',
            'c462a5b9e8d703f1',
            '68239a5c1e47bd0f',
            'b3582fade174c960',
            'c821d4f670a53e9b',
            '7f5a816d093eb42c',
            '5df692cab78143e0',
            '8e25691cf4b0da37',
            '17ed05834fa69cb2',]
# ГОСТ 28147-89 простая замена 
def gost28147_89_ez(n1, n2, x, k):
    for i in range(32):
        if i<24:
            newn1=( (x[i%8]+int(n1, 2)) % 2**32)
        else:
            newn1=( (x[(31-i)%8]+int(n1, 2)) % 2**32)
        newn1=hex(newn1)[2:]      # 16-чный результат сложения куска ключа с n1
        n = 0
        re_newn1=''
        for b in newn1:
            re_newn1 += k[(n % 8) + 1][k[0].find(b)] # добавление шифрбуквы из n-й строки таблицы магмы (K)
            n += 1
        bin_re_newn1=bin(int(re_newn1, 16))[2:]
        bin_re_newn1='0'*(32-len(bin_re_newn1))+bin_re_newn1
        bin_re_newn1=bin_re_newn1[11:]+bin_re_newn1[:11]           #  циклически сдвигается на одиннадцать шагов в сторону старших разрядов
        n12=bin(int(bin_re_newn1, 2)^int(n2, 2))               # сложение по модулю 2 зашифр n1 с n2
        n12='0'*(32-len(n12[2:]))+n12[2:]
        n2=n1
        n1=n12
    return n1, n2   

# ГОСТ 28147-89 генератор гаммы и сумматор гаммы с текстом/шифром в 16-чной системе
def gost28147_89_gum_builder(text, key, hsinh):
    c1='0x1010104'
    c2='0x1010101'
    x=[]                    # ключевые куски в 2-чной
    xd=[]                   # ключевые куски в 10-чной
    text2=''                      # результат суммы с гаммой текста/шифра в 16-чном формате
    binkey=bin(int(key, 16))[2:]     # ключ в двоичном варианте
    sinh=bin(int(hsinh,16))[2:]      # синхропосылка в двоичном варианте
    sinh='0'*(64-len(sinh))+sinh     # добавление 0 впереди для получения 64х бит если их было меньше
    n1=sinh[:32][::-1]
    n2=sinh[32:][::-1]
    for i in range(8):
        x.append(binkey[i*32:(i+1)*32])
        x[i]=x[i][::-1]
        xd.append(int(x[i], 2))
    n3, n4 = gost28147_89_ez(n1, n2, xd, magma_table)    # шифровка n1 и n1 в режиме простой замены
    print(n3, n4)
    M=len(text)//16              # количество блоков текста/шифра и гаммы
    if len(text)%16!=0:
        M+=1
    gs=[]  # блоки гаммы
    for i in range(M):
        # перемножение n4 с С1 и n3 c С2
        n3=bin((int(n3,2)+int(c2, 16))%(2**32))
        n4=bin((int(n4,2)+int(c1, 16))%(2**32-1))
        n1='0'*(32-len(n3[2:]))+n3[2:]
        n2='0'*(32-len(n4[2:]))+n4[2:]
        gs.append(gost28147_89_ez(n1, n2, xd, magma_table)[0]+gost28147_89_ez(n1, n2, xd, magma_table)[1])
        if (i+1)*16<=len(text):
            block=hex(int(gs[i], 2)^int(text[i*16:(i+1)*16], 16))[2:] # поразрядное сложение блока текста/шифра и гаммы
            text2+='0'*(16-len(block))+block
        else:
            a=int(gs[i][:len(text[i*16:])], 2)
            block=hex(a^int(text[i*16:], 16))[2:] # поразрядное сложение блока текста/шифра и гаммы
            text2+=block
    return text2

# ГОСТ 28147-89 в режиме гаммирования заш
def gost28147_89_gum(text, key, hsinh):
    hextext= bytes(text, 'utf-8').hex()  # перевод текста в 16й формат
    crtext=gost28147_89_gum_builder(hextext, key, hsinh)
    return crtext

# ГОСТ 28147-89 в режиме гаммирования расш
def gost28147_89_gum_re(crtext, key, hsinh):
    hextext=gost28147_89_gum_builder(crtext, key, hsinh)
    text = bytearray.fromhex(hextext).decode('utf-8')     # перевод из 16-го формата    
    return text


#text='цепьнекрепчесвоегосамогослабогозвенатчк'
#key=72345685785694856938472093870387203438431598682347032641234568578569483404012
#print(key.bit_length())
#hk='9ff23502eb846903d9f0cfce0c0655cdc74f4f569bd2045152eb7e78d4fd42ec'
#print(bin(key),bin(int(hk, 16)))
#hs='ab771aa5b5554353'
#s='1010101101110111000110101010010110110101010101010100001101010011'
#print(hk, hs)
#d=gost28147_89_gum(text, hk, hs)
#print(d)
#print(gost28147_89_gum_re(d, hk, hs))


# a=int('0b101010',2)
# b=int('0b11011',2)
# c=bin(a^b)
# print(c)
# c='0'*(32-len(c[2:]))+c[2:]
# print(c)
# a=1
# c=5
# m=len(alf1)
# en=shenon(alf1, text, a, c, m, 5)
# print(en)
# print(shenon_re(alf1, en, a, c, m, 5))




# СТАРАЯ ВЕРСИЯ (МОЖЕТ ПРИГОДИТСЯ)

# def gost28147_89_ez(n1, n2, x, k):
#     for i in range(32):
#         if i<24:
#             newn1=( (x[i%8]+int(n1, 2)) % 2**32)
#             #print(x[i%8], n1, newn1)
#         else:
#             newn1=( (x[(31-i)%8]+int(n1, 2)) % 2**32)
#             #print(x[(31-i)%8], n1, newn1)
#         #print(newn1.bit_length())
#         newn1=hex(newn1)[2:]      # 16-чный результат сложения куска ключа с n1
#         #print(newn1)
#         n = 0
#         re_newn1=''
#         for b in newn1:
#             re_newn1 += k[(n % 8) + 1][k[0].find(b)] # добавление шифрбуквы из n-й строки таблицы магмы (K)
#             n += 1
#         #print(len(re_newn1), len(n2))
#         bin_re_newn1=bin(int(re_newn1, 16))[2:]
#         bin_re_newn1='0'*(32-len(bin_re_newn1))+bin_re_newn1
#         #print('before',bin_re_newn1, len(bin_re_newn1))
#         bin_re_newn1=bin_re_newn1[11:]+bin_re_newn1[:11]           #  циклически сдвигается на одиннадцать шагов в сторону старших разрядов
#         #print('after',bin_re_newn1,len(bin_re_newn1))
        
#         n12=bin(int(bin_re_newn1, 2)^int(n2, 2))               # сложение по модулю 2 зашифр n1 с n2
#         #print(n12, len(n12))
#         n12='0'*(32-len(n12[2:]))+n12[2:]
#         #print(n12)
#         n2=n1
#         n1=n12
#     return n1, n2   


# # ГОСТ 28147-89 в режиме гаммирования заш
# def gost28147_89(text, key, hsinh):
#     crtext=''
#     c1='0x1010101'
#     c2='0x1010104'
#     x=[]                    # ключевые куски в 2-чной
#     xd=[]                   # ключевые куски в 10-чной
#     hextext= bytes(text, 'utf-8').hex()  # перевод текста в 16й формат
#     #print(hextext)
#     M=len(hextext)//16              # количество блоков текста и гаммы
#     if len(hextext)%16!=0:
#         M+=1
#     binkey=bin(int(key, 16))[2:]     #ключ в двоичном варианте
#     sinh=bin(int(hsinh,16))[2:]
#     n1=sinh[:32][::-1]
#     n2=sinh[32:][::-1]
#     for i in range(8):
#         x.append(binkey[i*32:(i+1)*32])
#         x[i]=x[i][::-1]
#         xd.append(int(x[i], 2))
    
#     n3, n4 = gost28147_89_ez(n1, n2, xd, magma_table)
#     #print(len(n3),len(n4))
#     gs=[]  # блоки гаммы
#     for i in range(M):
#         # перемножение с С1 и С2
#         n3=bin((int(n3,2)+int(c2, 16))%(2**32))
#         n4=bin((int(n4,2)+int(c1, 16))%(2**32-1))
#         n1='0'*(32-len(n3[2:]))+n3[2:]
#         n2='0'*(32-len(n4[2:]))+n4[2:]
#         gs.append(gost28147_89_ez(n1, n2, xd, magma_table)[0]+gost28147_89_ez(n1, n2, xd, magma_table)[1])
#         #print(len(gs[i]))
#         if (i+1)*16<=len(hextext):
#             block=hex(int(gs[i], 2)^int(hextext[i*16:(i+1)*16], 16))[2:]
#             #print(len(block), block, i)
#             crtext+='0'*(16-len(block))+block
#         else:
#             #print(gs[i][:len(hextext[i*16:])], i, len(gs[i][:len(hextext[i*16:])]))
#             a=int(gs[i][:len(hextext[i*16:])], 2)
#             block=hex(a^int(hextext[i*16:], 16))[2:]
#             #print(len(block))
#             crtext+=block
    
#     return crtext

# # ГОСТ 28147-89 в режиме гаммирования расш
# def gost28147_89_re(crtext, key, hsinh):
#     text=''
#     c1='0x1010101'
#     c2='0x1010104'
#     x=[]                    # ключевые куски в 2-чной
#     xd=[]                   # ключевые куски в 10-чной
#     hextext=''                 # открытый текст в 16-чном формате
#     M=len(crtext)//16              # количество блоков текста и гаммы
#     if len(crtext)%16!=0:
#         M+=1
#     binkey=bin(int(key, 16))[2:]     # ключ в двоичном варианте
#     sinh=bin(int(hsinh,16))[2:]      # синхропосылка в двоичном варианте
#     n1=sinh[:32][::-1]
#     n2=sinh[32:][::-1]
#     for i in range(8):
#         x.append(binkey[i*32:(i+1)*32])
#         x[i]=x[i][::-1]
#         xd.append(int(x[i], 2))
    
#     n3, n4 = gost28147_89_ez(n1, n2, xd, magma_table)
#     #print(len(n3),len(n4))
#     gs=[]  # блоки гаммы
#     for i in range(M):
#         # перемножение с С1 и С2
#         n3=bin((int(n3,2)+int(c2, 16))%(2**32))
#         n4=bin((int(n4,2)+int(c1, 16))%(2**32-1))
#         n1='0'*(32-len(n3[2:]))+n3[2:]
#         n2='0'*(32-len(n4[2:]))+n4[2:]
#         gs.append(gost28147_89_ez(n1, n2, xd, magma_table)[0]+gost28147_89_ez(n1, n2, xd, magma_table)[1])
#         if (i+1)*16<=len(crtext):
#             block=hex(int(gs[i], 2)^int(crtext[i*16:(i+1)*16], 16))[2:]
#             hextext+='0'*(16-len(block))+block
#         else:
#             #print(gs[i][:len(crtext[i*16:])], i)
#             a=int(gs[i][:len(crtext[i*16:])], 2)
#             block=hex(a^int(crtext[i*16:], 16))[2:]
#             hextext+=block
#     #print(hextext)
#     text = bytearray.fromhex(hextext).decode('utf-8')     # перевод из 16-го формата    
#     return text
