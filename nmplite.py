#!/usr/bin/env python3

import os
import sys
import time
import datetime
import sqlite3

banner = '''
888b    888                        888      d8b 888            
8888b   888                        888      Y8P 888            
88888b  888                        888          888            
888Y88b 888 88888b.d88b.  88888b.  888      888 888888 .d88b.  
888 Y88b888 888 "888 "88b 888 "88b 888      888 888   d8P  Y8b 
888  Y88888 888  888  888 888  888 888      888 888   88888888 
888   Y8888 888  888  888 888 d88P 888      888 Y88b. Y8b.     
888    Y888 888  888  888 88888P"  88888888 888  "Y888 "Y8888  
                          888                                  
                          888                                  
                          888                                  
'''

conn = sqlite3.connect('db/nmplite.db')
c = conn.cursor()
c.execute('''SELECT * FROM saves''')

def chose():
    if menu == '1':
        save()

    if menu == 'h':
        print('Help is on the way...')
        time.sleep(1)
        main()

    if menu == '0' or menu == 'x' or menu == 'X':
        print('Godspeed')
        sys.exit()

    else:
        error()

def save():
    print('\n[+] scan with nmap and save in sqlite3')
    print('[?] do you want to save the scan?')
    save = input(str('\nNmpLite >>> Save [y/n]: '))

    if save == 'y':
        scan_with_save()

    if save == 'n':
        scan_no_save()

    else:
        error()

#__      __  ___  __ ___   _____ 
#\ \ /\ / / / __|/ _` \ \ / / _ \
# \ V  V /  \__ \ (_| |\ V /  __/
#  \_/\_/___|___/\__,_| \_/ \___|
#      |_____|                   
#

def scan_with_save():
    conn = sqlite3.connect('db/nmplite.db', timeout = 5)
    #conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    c.execute('''SELECT * FROM saves''')

    last = c.execute('''SELECT id FROM saves ORDER BY id DESC LIMIT 1''')
    last = c.fetchall()
    print(str(last))

    if last == []:
        ajdi = 0

    else:
        ajdi = last[0] + 1
        print(ajdi)

    unix = time.time()
    dt = str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%Y/%H:%M:%S'))
    print(dt)

    y = input(str('NmpLite >>> [+] Enter name of your scan: '))
    #conn.row_factory = lambda cursor, row: row[2]
    pr = c.execute('''SELECT * FROM saves WHERE name = ?''', (y,))
    pr = list(c.fetchall())
    print(pr)

    if y in pr:
        print('Saved scan with that name already exists in db!!!')
        time.sleep(1)
        main()

    else:
        pass

    print(
            '''
            [ 1 ] -sC: equivalent to --script=default
            [ 2 ] -sV: Probe open ports to determine service/version info
            [ 3 ] -p-: Scann all 65535 ports
            ''')
    flag = input(str('NmpLite >>> [+] Enter options: '))

    fl = ''
    if '1' in flag:
        fl = fl + '-sC '

    if '2' in flag:
        fl = fl + '-sV '

    if '3' in flag:
        fl = fl + '-p- '

    else:
        pass

    ip = input('NmpLite >>> [+] Enter ip addres: ')
    if ip == '':
        print("You didn't enter ip addr")
        time.sleep(1)
        main()

    #conn = sqlite3.connect('db/nmplite.db', timeout = 5)
    c.execute('''INSERT INTO saves (id, date, name) VALUES (?, ?, ?)''',
            (ajdi, dt, y))

    conn.commit()
    #conn.close()
    # Making variable for bash to start executing nmap
    scan = (f'nmap {fl}{ip} >> scans/{y}')
    print(f'[===== {scan} =====]')
    s = (f'touch scans/{y}')
    os.system(s)
    os.system(scan)
    print()
    read_scan = 'cat scans/' + y
    os.system(read_scan)

    input('\n[+] Scaning is done')
    main()

# _ __   ___     ___  __ ___   _____ 
#| '_ \ / _ \   / __|/ _` \ \ / / _ \
#| | | | (_) |  \__ \ (_| |\ V /  __/
#|_| |_|\___/___|___/\__,_| \_/ \___|
#          |_____|
#

def scan_no_save():
    print(
            '''
            [ 1 ] -sC: equivalent to --script=default
            [ 2 ] -sV: Probe open ports to determine service/version info
            [ 3 ] -p-: Scann all 65535 ports
            ''')
    flag = input(str('NmpLite >>> [+] Enter options: '))

    fl = ''
    if '1' in flag:
        fl = fl + '-sC'

    if '2' in flag:
        fl = fl + '-sV'

    if '3' in flag:
        fl = fl + '-p-'

    else:
        pass

    ip = input('NmpLite >>> [+] Enter ip addres: ')

    print()
    scan = (f'nmap {fl} {ip}')
    print(f'[===== {scan} =====]')
    print()
    os.system(scan)

    print()
    input('[+] Scann is done')
    main()

def help():
    pass

def error():
    print('''
    =================================
    || You entered invalid command ||
    || program will restart now!!! ||
    =================================
    ''')
    time.sleep(1)
    main()

def main():
    print(banner)
    print('Welcome to NmpLite')
    print(' [- 1 -] start scan')
    print(' [- h -] help')
    print(' [- 0 -]')

    global menu
    menu = input(str('NmpLite >>> '))
    chose()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n[!] Interupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
