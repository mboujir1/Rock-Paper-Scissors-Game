#!/usr/bin/python3

import socket
import sys, os

def get_winner(p1, p2):
    if p1 == p2:
        result = 'Draw'
    elif (p1 == 'paper' and p2 == 'rock') or (p1 == 'rock' and p2 == 'scissor') or \
    (p1 == 'scissor' and p2 == 'paper'):
        result = 'Player 1 Wins'
    else:
        result = 'Player 2 Wins'
    return result

if __name__ == '__main__':
    choices = ['rock', 'paper', 'scissor']
    prompt = ','.join(choices) + '? '
    if (len(sys.argv) == 1) or (len(sys.argv) > 3):
        fn = sys.argv[0].split('/')[-1]
        print('>> Usage: ./{} startnewgame'.format(fn))
        print('>> Play existing game: ./{} connect <HOST>'.format(fn))
        sys.exit(1)
    if (sys.argv[1] == 'startnewgame'):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', 6000))
            s.listen(1)
            print('[*] waiting Player 2...')
            try:
                c, addr = s.accept()
                if(c.recv(1024).decode('ASCII') == 'connected!'):
                    print('[*] Game initialized .. Start Playing...')
                while True:
                    os.system('clear')
                    print("\n~~~~~~~~~~> Rock Paper Scissors <~~~~~~~~~~\n")
                    p1 = input(prompt).lower()
                    if (not p1 in choices):
                        print("[!] please choose either: rock, paper or scissor [!]")
                        c.send('error'.encode('ASCII'))
                        break
                    c.send('choosed'.encode('ASCII'))
                    print('\nwaiting until Player2 Choose..')
                    p2 = c.recv(1024).decode('ASCII')
                    result = get_winner(p1, p2)
                    popup_r = '\n~~~~~~~~~~> ' + result + ' <~~~~~~~~~~'
                    print(popup_r)
                    if result == 'Player 2 Wins':
                        print('~~~~~~~~~~> YOU LOSE <~~~~~~~~~~\n')
                    elif result == 'Player 1 Wins':
                        print('~~~~~~~~~~> YOU WIN <~~~~~~~~~~\n')
                    c.send(popup_r.encode('ASCII'))
                    break
                sys.exit(0)
            except KeyboardInterrupt:
                print('\n\nYou Pressed <CTRL+C> .. Exiting...')
                sys.exit(1)
        except Exception as e:
            print(str(e))
    elif (sys.argv[1] == 'connect'):
        if (len(sys.argv) == 2):
            print('[!] Please specify host.')
            sys.exit(1)
        host = sys.argv[2]
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, 6000))
            s.send('connected!'.encode('ASCII'))
            while True:
                os.system('clear')
                print("\n~~~~~~~~~~> Rock Paper Scissors <~~~~~~~~~~\n")
                print('\nwaiting until Player1 Choose..')
                rcv = s.recv(1024).decode('ASCII')
                if (rcv == 'error'):
                    print('Error.. exiting...')
                    break
                elif 'choosed' in rcv:
                    print('Player1 choice has been chosen.. now your turn\n\n')
                    p2 = input(prompt).lower()
                    if (not p2 in choices):
                        print("[!] please choose either: rock, paper or scissor [!]")
                        s.send('error'.encode('ASCII'))
                        break
                    s.send(p2.encode('ASCII'))
                    r = s.recv(1024).decode('ASCII')
                    print(r)
                    if 'Player 2 Wins' in r:
                        print('~~~~~~~~~~> YOU WIN <~~~~~~~~~~\n')
                    elif 'Player 1 Wins' in r:
                        print('~~~~~~~~~~> YOU LOSE <~~~~~~~~~~\n')
                    break
        except Exception as e:
            print(str(e))
        sys.exit(0)
    else:
        print('[!] Invalid Option')
        sys.exit(1)