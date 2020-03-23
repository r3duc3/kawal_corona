#!/usr/bin/python3

try:
    import requests as req, os
except Exception as ex:
    exit(f"Module '{ex.name}' belum terinstall")

w = tuple([chr(27)+'[1;0m'] + list(chr(27)+'[1;3'+str(x)+'m' for x in range(1,7)))
url = 'https://api.kawalcorona.com/'
commands = (
        'q', 'exit',
        'ls',
        'cls',
        'status',
        'h', 'help'
        )

def help():
    a, b = w[2], w[3]
    print(f'\t{a}- q, exit\n\t{b}- h, help\n\t{a}- cls -> hapus screen\n\t{b}- ls -> list negara/provinsi\n\t{a}- status -> status corona')

def h(): help()

def q(): exit()

def getter():
    x = input(w[0]+'\t1. Global\n\t2. Lokal\n> ')
    if x == '2':
        return req.get(url+'indonesia/provinsi/').json(), 'Provinsi', 'provinsi'
    elif x == '1':
        return req.get(url).json(), 'Country_Region', 'negara'
    else:
        return None, None, x

def ls():
    a,b,c = getter()
    if a == None: return
    lines = os.get_terminal_size().lines
    line = 1
    try:
        for y in a:
            print(f'\t{w[3]}{a.index(y)+1}. {w[2]}{y["attributes"][b]}')
            line += 1
            if line == lines:
                line = 1
                input(w[0]+'Enter untuk lanjut')
                cls()
    except:
        cls()
        return

def cls():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(w[6]+''' ______________
< Kawal corona >
 --------------
  \\
   \\
       ___
     {~._.~}
      ( Y )
     ()~*~()
     (_)-(_)
api: '''+url)

def status():
    x,y,z = getter()
    a = input(f'{w[0]}Masukkan no urut {z}[1-{len(x)}]\n> ')
    if a.isnumeric() and -1 < int(a)-1 < len(x):
        data = x[int(a)-1]['attributes']
        if z == 'negara':
            print(f'''\t{w[2]}Nama {z}: {data["Country_Region"]}
\t{w[3]}terakhir update: {data["Last_Update"]}
\t{w[2]}Garis lintang: {data["Lat"]}
\t{w[3]}Garis Bujur: {data["Long_"]}
\t{w[2]}Dikonfirmasi: {data["Confirmed"]}x
\t{w[3]}Positif: {data["Active"]}
\t{w[2]}Sembuh: {data["Recovered"]}
\t{w[3]}Meninggal: {data["Deaths"]}''')
        elif z == 'provinsi':
            print(f'''\t{w[2]}Nama {z}: {data["Provinsi"]}
\t{w[3]}Positif: {data["Kasus_Posi"]}
\t{w[2]}Sembuh: {data["Kasus_Semb"]}
\t{w[3]}Meninggal: {data["Kasus_Meni"]}''')

cls()
while True:
    cmd = input(w[0]+'$ ')
    if cmd in commands:
        exec(cmd+'()')
    else:
        print(f'\x1b[7;31mtidak ada command "{cmd}"{w[0]}') if cmd != '' else None
