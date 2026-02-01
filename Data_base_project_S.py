import socket,time,mysql.connector,os,bcrypt
from cryptography.fernet import Fernet
def give_ip():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.bind(('', 5001))
    msg = b'HELLO_CLIENT'
    while True:
        server.sendto(msg, ('<broadcast>', 5000))
        print("Broadcast sent")
        time.sleep(0.5)
        server.settimeout(0.01)
        try:
            data, addr = server.recvfrom(1024)
            if data.decode().lower() == 'x':
                print(f"Stopping server, client {addr[0]} got IP")
                break
        except socket.timeout:
            pass
def connect(data_base_name,password1):
    connection=mysql.connector.connect(
        host='localhost',
        user='root',
        #enter your database name and password here
        password=
        database=
    )
    print("Connected to Database:")
    return connection
def Gmail_checker(gmail):
    if '@gmail.com' in gmail:
        return gmail
    else:
        return 0
def get_user_id(gmail):
    connction=connect('security','10by10is1')
    cursor=connction.cursor()
    cursor.execute('select email,id from user_data')
    result=cursor.fetchall()
    for i in range(len(result)):
        if gmail == result[i][0]:
            return result[i][1]
give_ip()
tries=0
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('0.0.0.0',1000))
server.listen(1)
conn,add=server.accept()
connction=connect('security','10by10is1')
cursor=connction.cursor()
print("Client Connected:",add[0])
print("Data Base server Started:")
Logged_IN_STATUS=False
Gmail_good=''
locked_accounts=[]
while True:
    time.sleep(1.2)
    conn.sendall('Welcome to our  cloud Site please choose the options according to your needs\n1:Register user\n2:Login\n3:Access your Cloud'.encode())
    choice=conn.recv(1024).decode()
    print(f"User Choosed {choice}")
    if choice=='1':
        conn.sendall('Enter your Gmail'.encode())
        Gmail=conn.recv(1024).decode()
        if Gmail_checker(Gmail)==0:
            conn.sendall('0'.encode())
            continue
        print(f"User Gmail is {Gmail}")
        conn.sendall('Enter Your password:'.encode())
        password=conn.recv(1024).decode()
        if len(password)<8:
            conn.sendall('0'.encode())
            continue
        password_0=conn.recv(1024).decode()
        if password!=password_0:
            print("Password Do not Match Previous Password try again:")
            continue
        conn.sendall('Enter Phone number'.encode())
        phone_no=conn.recv(1024).decode()
        print(f'User Phone no is {phone_no}')
        conn.sendall('Enter your Name:'.encode())
        name=conn.recv(1024).decode()
        print(f"User Name is {name}")
        try:
            password = password.encode()
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            cursor.execute(
    "INSERT INTO user_data (name,email,phone_number,password) VALUES (%s,%s,%s,%s)",
    (name, Gmail, phone_no, hashed)
)
            connction.commit()
            print("Succesfull Registration")
            conn.sendall('1'.encode())
            cursor.execute('select email from user_data')
            result=cursor.fetchall()
            for i in range(len(result)):
                if Gmail in result[i][0]:
                    id=i+1
            os.system(f'mkdir {id}')
        except mysql.connector.Error as er:
            print('Something went Wrong Error code',er)
            conn.sendall('0'.encode())
    elif choice=='2':
        gmail=conn.recv(1024).decode()
        if gmail in locked_accounts:
            conn.sendall('s'.encode())
            continue
        else:
            conn.sendall('o'.encode())
        cursor.execute('select email from user_data')
        result=cursor.fetchall()
        found=False
        for i in range(len(result)):
            if gmail == result[i][0]:
                conn.sendall("Gmail Found:\nEnter Your Password to login:".encode())
                id=i
                found=True
        if not(found):
            conn.sendall('0'.encode())
            continue
        user_password=conn.recv(1024).decode()
        cursor.execute("SELECT id, password FROM user_data WHERE email=%s", (gmail,))
        row = cursor.fetchone()
        user_id, db_hash = row
        if tries<3:
            if bcrypt.checkpw(user_password.encode(), db_hash.encode()):
                print("Login success")
                Logged_IN_STATUS=True
                Gmail_good=gmail
                conn.sendall('1'.encode())
            else:
                print("Invalid password")
                conn.sendall('0'.encode())
            tries+=1
        elif tries>=3:
            prompt='Account Locked'
            print(prompt)
            locked_accounts.append(gmail)
            conn.sendall(prompt.encode())
            tries=0
            continue
    elif choice=='3':
        conn.sendall(('1'if Logged_IN_STATUS==True else '0').encode())
        if Logged_IN_STATUS:
            while True:
                conn.sendall('Make your Choice:\n1:Upload File\n2:Download file from your Cloud\n3:Quit/Back'.encode())
                user_id=get_user_id(Gmail_good)
                choice_n=conn.recv(1024).decode()
                if choice_n=='1':
                    while True:
                        file_name=conn.recv(1024).decode()
                        if file_name=='q':
                            break
                        conn.sendall('Ready for Transfer:'.encode())
                        file_size_str=conn.recv(1024).decode()
                        if file_size_str=='0':
                            print("Client could not find the file retrying:")
                            continue
                        file_size=int(file_size_str)
                        path=f'D:/University/Programming/Data_base_work/{id}/{file_name}'
                        recevied=0
                        with open(path,'wb') as f:
                            while recevied<file_size:
                                data=conn.recv(1024)
                                if not data:
                                    break
                                f.write(data)
                                recevied+=len(data)
                        print('DONE:')
                        conn.sendall('1'.encode())
                elif choice_n=='2':
                    while True:
                        result=''
                        id=get_user_id(Gmail_good)
                        for i in os.listdir(str(id)):
                            result+=i+'\n'
                        conn.sendall(result.encode())
                        data=conn.recv(1024).decode()
                        if data=='q':
                            print("Going Back:")
                            break
                        file_name=conn.recv(1024).decode()
                        dir_list=os.listdir(str(user_id))
                        print(file_name)
                        path=f'D:/University/Programming/Data_base_work/{user_id}/{file_name}'
                        size = os.path.getsize(path)
                        print(size)
                        conn.sendall(str(size).encode())
                        with open(path, "rb") as f:
                            conn.sendfile(f)
                        ack = conn.recv(1024).decode()
                        print("ACK:", ack)
                        if ack=='1':
                            print("Client Got the file Successfully")
                elif choice_n=='3':
                    print("Going Back:")
                    break
        else:
            conn.sendall('0'.encode())
    else:
        conn.sendall('Invalid Choice:'.encode())
        continue