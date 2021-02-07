import random
import sqlite3
from sqlite3 import Error

try:
    conn = sqlite3.connect('words.s3db')
except Error as e:
    print(e)
cur = conn.cursor()

try:
    cur.execute('CREATE TABLE passwords(name text, login text, password text)')
except:
    pass
conn.commit()

cur.execute('select * from passwords')
all_passwords = cur.fetchall()
conn.commit()

def pass_generate(name, login, liczba_znaków, liczba_dużych, liczba_specjalnych, liczba_cyfr):
    global all_passwords
    liczba_specjalnych = int(liczba_specjalnych)
    liczba_cyfr = int(liczba_cyfr)
    liczba_dużych = int(liczba_dużych)
    liczba_znaków = int(liczba_znaków)
    liczba_zwykłych = int(liczba_znaków) - (liczba_cyfr + liczba_specjalnych + liczba_dużych)

    password = []
    znaki_spec = list("!@#$%^&*()_-,./?\|;:[]{}'\"")
    duże_litery = list('QWERTYUIOPASDFGHJKLZXCVBNM')
    cyfry = list('123456789')
    znaki = list('qwertyuiopasdfghjklzxcvbnm')


    for i in range(liczba_znaków):
       zrobione = False
       while zrobione == False:
            x = random.randint(1, 4)

            if liczba_dużych > 0 and x == 1:
                password.append(random.choice(duże_litery))
                liczba_dużych -= 1
                zrobione = True

            elif liczba_specjalnych > 0 and x == 2:
                password.append(random.choice(znaki_spec))
                liczba_specjalnych -= 1
                zrobione = True

            elif liczba_cyfr > 0 and x == 3:
                password.append(random.choice(cyfry))
                liczba_cyfr -= 1
                zrobione = True

            elif liczba_zwykłych > 0 and x == 4:
                password.append(random.choice(znaki))
                liczba_zwykłych -= 1
                zrobione = True

    password = "".join(password)
    print("|||{}|||".format(name,))
    print("Twój login to: {} a hasło: {}".format(login, password))
    cur.execute('insert into passwords (name, login, password) Values(?,?,?)',(name,login,password))
    conn.commit()
    cur.execute('select * from passwords')
    all_passwords = cur.fetchall()

def print_password():
    xx = 0
    for lol in range(len(all_passwords)):
        xd = all_passwords[xx]
        print('''|||{}|||
        Twój login to: {} a hasło: {}'''.format(xd[0], xd[1], xd[2]))
        xx += 1

def delete_passwor(delete_name):
    global all_passwords
    cur.execute('DELETE FROM passwords where name = ?',(delete_name,))
    print('''
    hasło |||{}||| zostało usunięte pomyślnie
    '''.format(delete_name,))
    conn.commit()
    cur.execute('select * from passwords')
    all_passwords = cur.fetchall()

def menu():
    print("1.Generuj hasło")
    print("2.Pokaż hasła")
    print('0.Wyjście')
    print('')
    x = input()
    if x == '1':
        while True:
            name = input('''Wpisz nazwe:                              Wpisz "0" żeby wyjść
            ''')
            if name == '0':
                break
            cur.execute('select login from passwords where name = ?', (name,))

            if cur.fetchone() == None:

                login = input('''Wpisz login:                              Wpisz "0" żeby wyjść
                ''')
                if login == '0':
                    break
                a = input('''Wpisz liczbę znaków:                              Wpisz "0" żeby wyjść
                ''')
                if a == '0':
                    break
                b = input('Wpisz liczbę dużych liter:                              Wpisz "0" żeby wyjść')
                if b == '0':
                    break
                c = input('''Wpisz liczbę znaków specjalnych:                              Wpisz "0" żeby wyjść
                ''')
                if c == '0':
                    break
                d = input('''Wpisz liczbę cyfr:                              Wpisz "0" żeby wyjść
                ''')
                if d == '0':
                    break
                pass_generate(name, login, a, b, c ,d)
                break
            else:
                print('''Podana nazwa juz istnieje. Wybierz inną                              Wpisz "0" żeby wyjść
                ''')

    elif x == '2':
        while True:
            print_password()
            if print_password() == None:
                print('Nie masz żadnych zapisanych Haseł')
                break
            print('1.Usuń hasło')
            print('0.Wyjscie')
            see_int = input()
            if see_int == '1':
                del_pas = input('''Wpisz nazwe hasła, które chcesz usunąc:                              Wpisz "0" żeby wyjść
                ''')
                if del_pas == '0':
                    break
                delete_passwor(del_pas)
            elif see_int == '0':
                break
    elif x == '0':
        exit()

while True:
    menu()
