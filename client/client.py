from _thread import *
from helper import *
import socket
import os
import random
import platform
import time
import pickle
import random

global local_rfcs, added_rfcs
local_rfcs = []
added_rfcs = []

def check_if_file_exists(rfc_num):
    if str(rfc_num) in local_rfcs:
        return True
    else:
        return False

def serve_peers():
    peer_response_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_response_host = socket.gethostname()
    peer_response_socket.bind((peer_response_host, upload_port))
    peer_response_socket.listen()
    while True:
        p_connection, p_ip = peer_response_socket.accept()
        file_data = p_connection.recv(4096).decode('utf-8')
        flag = verify_peer_request(file_data)
        if(flag):
        # print(file_data)
            flg = verify_p2p_version(file_data)
            if(flg):
                items = file_data.split()
                rfc_number = items[2]
                response = read_file(rfc_number)
                p_connection.send(pickle.dumps(response))
            else:
                response_data = ""
                version_not_supported_msg = send_version_not_supported_msg()
                p_connection.send(pickle.dumps([version_not_supported_msg, response_data]))
        else:
            response_data = ""
            bad_request_msg = send_bad_request_msg()
            p_connection.send(pickle.dumps([bad_request_msg, response_data]))
        p_connection.close()
    peer_response_socket.close()

def create_file(filename, content):

    rcf_dir_path = "\\RFC_Store\\" + filename if platform.system == "Windows" else "/RFC_Store/" + filename
    file_location = os.getcwd() + rcf_dir_path
    with open(file_location, 'w') as handler:
        handler.write(content)

def read_file(rfc_num):
    file_name = "RFC" + str(rfc_num) + ".txt"
    rcf_dir_path = "\\RFC_Store\\" + file_name if platform.system == "Windows" else "/RFC_Store/" + file_name
    file_location = os.getcwd() + rcf_dir_path
    try:
        data = open(file_location)
        message = send_msg(file_location)
        return [message, str(data.read())]
    except Exception as e:
        file_data = ""
        file_not_found_msg = send_file_not_found_msg()
        return [file_not_found_msg, file_data]
    

def list_all():
    connection_msg = list_msg(socket, upload_port)
    clientSocket.send(pickle.dumps([connection_msg, "LIST"]))
    server_data = pickle.loads(clientSocket.recv(4096))
    print(server_data[0])
    for rfc_data in server_data[1]:
        print(rfc_data)

def lookup():
    rfc_num = input("RFC Number? \n")
    rfc_ttl = "RFC" + str(rfc_num)

    connection_msg = lookup_msg(rfc_num, socket, upload_port, rfc_ttl)
    clientSocket.send(pickle.dumps([connection_msg, "LOOKUP", rfc_num]))
    server_data = pickle.loads(clientSocket.recv(4096))
    
    print(server_data[0])
    for rfc_data in server_data[1]:
        print(rfc_data)

def add_rfc(rfc_number):
    if str(rfc_number) in added_rfcs:
        print("This RFC is already added. Try again with a different RFC")
    else:
        rfc_title = "RFC" + str(rfc_number)
        connection_msg = add_msg(rfc_number, rfc_title, socket, upload_port)
        clientSocket.send(pickle.dumps([connection_msg, "ADD", rfc_number, rfc_title]))
        added_rfcs.append(rfc_number)
        print(clientSocket.recv(4096).decode('utf-8'))
        print("RFC : {0} was successfully added".format(str(rfc_number)))

def get_rfc():

    rfc_num = input("RFC Number? \n")
    if str(rfc_num) in local_rfcs:
        print("The requested RFC is already present in your local RFC Store\n")
        return
    version = input("P2P-CI version? \n")
    host = input("Host? \n")
    port = input("Host's client serving port? \n")

    try:
        peer_connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_connection_socket.connect((str(host), int(port)))
        os_type_version = platform.platform()
        msg = get_rfc_msg(int(rfc_num), socket, os_type_version, version)
        peer_connection_socket.send(bytes(msg, 'utf-8'))
        rfc_data = peer_connection_socket.recv(4096)
        time.sleep(1)
        response = pickle.loads(rfc_data)
        print(response[0])
        if len(response[1]) > 0:
            filename = "RFC" + str(rfc_num) + ".txt"
            create_file(filename, response[1])
            local_rfcs.append(str(rfc_num))
            peer_connection_socket.close()
            print("RFC file was successfully added to the local RFCs store\n")

    except Exception as e:
        print("Failed to connect to the peer. Try again with proper host and port values \n")

def inputs_listener():
    while True:
        method = input("\n\nSelect the operation number you wanna perform:\n1. GET\n2. ADD\n3. LOOKUP\n4. LIST\n5. EXIT\n")
        
        if method == '5':
            clientSocket.send(pickle.dumps(["", "EXIT"]))
            break
        elif method == '1':
            get_rfc()
        elif method == '3':
            lookup()
        elif method == '4':
            list_all()
        elif method == '2':
            rfc_number = input("RFC Number? \n")
            if check_if_file_exists(rfc_number):
                add_rfc(rfc_number)
            else:
                print(" The entered RFC file does not exist in your local RFC store. Try again with different RFC!\n")
        else:
            print("Invalid Input, Try Again!.\n")
    print("Exiting")
    clientSocket.close()


if __name__ == "__main__":

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverHost = '192.168.33.1'  
    serverPort = 7734
    clientSocket.connect((serverHost, serverPort))
    upload_port = 5555
    rfc_list = []

    folder_location = "\\RFC_Store" if platform.system == "Windows" else "/RFC_Store"
    rfc_storage_path = os.getcwd() + folder_location

    connection_message = establish_connection_msg(socket, upload_port)

    for file_name in os.listdir(rfc_storage_path):
        rfc_number = file_name[file_name.find("C")+1:file_name.find(".")]
        rfc_title = file_name[file_name.find("R"):file_name.find(".")]
        item = {}
        item['RFCNumber'] = rfc_number
        item['RFCTitle'] = rfc_title
        local_rfcs.append(str(rfc_number))
        added_rfcs.append(str(rfc_number))
        rfc_list.insert(0, item)

    clientSocket.send(pickle.dumps([connection_message, rfc_list, upload_port]))
    print(clientSocket.recv(4096).decode('utf-8'))

    start_new_thread(serve_peers, ())
    inputs_listener()





