#!/usr/bin/python3

try:
    import requests as req, os, time
    from multiprocessing import Process as pro
except Exception as ex:
    exit(f"Module '{ex.name}' belum terinstall")

w = tuple([chr(27)+'[1;0m'] + list(chr(27)+'[1;3'+str(x)+'m' for x in range(1,7)))
url = 'https://api.kawalcorona.com/'
commands = (
        'q', 'exit',
        'ls',
        'cls',
        'status',
        'h', 'help',
        'total'
        )

def help():
    a, b = w[2], w[3]
    print(f'\t{a}- q, exit\n\t{b}- h, help\n\t{a}- cls -> hapus screen\n\t{b}- ls -> list negara/provinsi\n\t{a}- status -> status corona\n\t{b}- total -> total kasus keseluruhan')

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

def total():
    g = req.get(url).json()
    positif = 0
    sembuh = 0
    mati = 0
    for x in g:
        data = x['attributes']
        positif += data['Confirmed']
        sembuh += data['Recovered']
        mati += data['Deaths']
        if data['Country_Region'] == 'Indonesia':
            idih = g.index(x)
    idn = g[idih]['attributes']
    cls()
    print(f'''{w[5]}Global:
\t{w[2]}Positif: {positif:,d}
\t{w[3]}Sembuh: {sembuh:,d}
\t{w[2]}Meninggal: {mati:,d}
{w[5]}Indonesia:
\t{w[2]}Positif: {idn["Confirmed"]:,d}
\t{w[3]}Sembuh: {idn["Recovered"]:,d}
\t{w[2]}Meninggal: {idn["Deaths"]:,d}''')

total()
def status():
    x,y,z = getter()
    if x == None: return
    a = input(f'{w[0]}Masukkan no urut {z}[1-{len(x)}]\n> ')
    if a.isnumeric() and -1 < int(a)-1 < len(x):
        cls()
        data = x[int(a)-1]['attributes']
        if z == 'negara':
            print(f'''\t{w[2]}Nama {z}: {data["Country_Region"]}
\t{w[3]}terakhir update: {data["Last_Update"]}
\t{w[2]}Garis lintang: {data["Lat"]}
\t{w[3]}Garis Bujur: {data["Long_"]}
\t{w[2]}Aktif: {data["Active"]}
\t{w[3]}Positif: {data["Confirmed"]:,d}
\t{w[2]}Sembuh: {data["Recovered"]:,d}
\t{w[3]}Meninggal: {data["Deaths"]:,d}''')
        elif z == 'provinsi':
            print(f'''\t{w[2]}Nama {z}: {data["Provinsi"]}
\t{w[3]}Positif: {data["Kasus_Posi"]:,d}
\t{w[2]}Sembuh: {data["Kasus_Semb"]:,d}
\t{w[3]}Meninggal: {data["Kasus_Meni"]:,d}''')

cls()
while True:
    cmd = input(w[0]+'$ ')
    if cmd in commands:
        exec(cmd+'()')
    else:
        print(f'\x1b[7;31mtidak ada command "{cmd}"{w[0]}') if cmd != '' else None
