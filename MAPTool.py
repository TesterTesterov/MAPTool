import struct

separator = '===SEP===\n'
encoding = "utf-16le"

def disassemble_file(MAP_file, txt_file):
    in_file = open(MAP_file, 'rb')
    strings_number = struct.unpack('I', in_file.read(4))[0]
    strings_offset_lib = []
    for i in range(strings_number):
        in_file.read(4)
        strings_offset_lib.append(struct.unpack('I', in_file.read(4))[0])
    out_file = open(txt_file, 'w', encoding=encoding)
    for offset in strings_offset_lib:
        in_file.seek(offset, 0)
        all_byter = b''
        while True:
            new_bytes = in_file.read(2)
            if (new_bytes == b'\x00\x00'):
                break
            all_byter += new_bytes
        out_file.write(all_byter.decode(encoding))
        out_file.write('\n')
        out_file.write(separator)
    in_file.close()
    out_file.close()
def assemble_file(MAP_file, txt_file):
    in_file = open(txt_file, 'r', encoding=encoding)
    line = in_file.readline()
    counter = 0
    while (line != ''):
        counter += 1
        line = in_file.readline()
    counter //= 2
    in_file.close()
    out_file = open(MAP_file, 'wb')
    out_file.write(struct.pack('I', counter))
    this_case = 4
    this_case += 8*counter
    in_file = open(txt_file, 'r', encoding=encoding)
    for i in range(counter):
        out_file.write(struct.pack('I', i))
        out_file.write(struct.pack('I', this_case))
        ze_line = ''
        new_line = in_file.readline()
        while (new_line != separator):
            ze_line += new_line
            new_line = in_file.readline()
        ze_line = ze_line.rstrip('\n')
        bytez = ze_line.encode(encoding)
        this_case += len(bytez)
        this_case += 2
    in_file.close()
    in_file = open(txt_file, 'r', encoding=encoding)
    for i in range(counter):
        ze_line = ''
        new_line = in_file.readline()
        while (new_line != separator):
            ze_line += new_line + '\n'
            new_line = in_file.readline()
        ze_line = ze_line.rstrip('\n')
        bytez = ze_line.encode(encoding)
        out_file.write(bytez)
        out_file.write(b'\x00\x00')
    in_file.close()
    out_file.close()

#disassemble_file("S03_06_CT.MAP", 'S03_06_CT.TXT')
#assemble_file("S03_06_CT.MAP", 'S03_06_CT.TXT')

test_flag = False

if (test_flag):
    zlo = open("en._bsi", 'rb')
    dobro = open("en_._bsi", 'rb')
    one = zlo.read(1)
    two = dobro.read(1)
    count = 0
    while ((one != b'') and (two != b'')):
        if (one != two):
            print(count)
            break
        one = zlo.read(1)
        two = dobro.read(1)
        count += 1
    zlo.close()
    dobro.close()
    exit()

Mode = 0
try:
    Mode = int(input("Декодировать (0), кодировать (1):/Decode (0), encode (1): "))
    if ((Mode != 0) and (Mode != 1)):
        raise Exception("Караул!")
except:
    print("Ошибка! Некорректное значение!/Error! Incorrect value!")
    input()
    exit()

FileMAP = input("Введите название файла MAP:/Input the MAP file name: ")
FileTXT = input("Введите название файла txt:/Input the txt file name: ")
if (Mode == 0):
    disassemble_file(FileMAP, FileTXT)
else:
    assemble_file(FileMAP, FileTXT)