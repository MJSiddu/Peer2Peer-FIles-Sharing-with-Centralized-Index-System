from _thread import *
from datetime import date
import pickle
import socket
import platform
import time

global active_clients, client_rfcs

active_clients = []
client_rfcs = []

def update_server_registry(client_info, data, connectionSocket):

    msg = "P2P-CI/1.0 200 OK \n"
    rfc_list = []
    for rfc in data[1]:
        rfc_num = rfc['RFCNumber']
        rfc_ttl = rfc['RFCTitle']
        clt_rfc = {}
        clt_rfc['RFCNumber'] = str(rfc_num)
        clt_rfc['RFCTitle'] = rfc_ttl
        clt_rfc['HostName'] = client_info['HostName']
        clt_rfc['PortNumber'] = str(client_info['PortNumber'])
        client_rfcs.insert(0, clt_rfc)
        rfc_list.append(rfc_num)

    # print("Connection with client: {0} established successfully. It's port number is: {1}".format(client_info['HostName'], client_info['PortNumber']))
    connectionSocket.send(bytes("Connection to server: {0} established successfully, and RFCs {1} were noted.".format(socket.gethostbyname(serverHost), rfc_list) + "\n" + msg, 'utf-8'))

def lookup_notfound_message():
    msg = "P2P-CI/1.0 404 Not Found " + "\n" \
        "Date: " + str(date.today()) + "\n" \
        "OS: " + str(platform.platform()) + "\n"
    return msg

def drop_client(hName, peerPort):
    print("Client: {0} with port: {1} exited".format(hName, str(peerPort)))
    remove_list = []
    for client in active_clients:
        if client.get('HostName') == hName and client.get('PortNumber') == str(peerPort):
            remove_list.append(client)
    for clnt in remove_list:
        active_clients.remove(clnt)

def remove_client_rfcs(hName, peerPort):
    remove_list = []
    for rfc in client_rfcs:
        if rfc.get('HostName') == hName and rfc.get('PortNumber') == str(peerPort):
            remove_list.append(rfc)
    for rfc_item in remove_list:
        client_rfcs.remove(rfc_item)

def add_rfc(connection_socket, address, client_data, peer_port):
    rfc_number = client_data[2]
    rfc_title = client_data[3]
    connection_socket.send(bytes("P2P-CI/1.0 200 OK \nRFC " + rfc_number + " " + rfc_title + " " + str(address[0]) + " " + str(peer_port), 'utf-8'))
    client_rfc = {}
    client_rfc['RFCNumber'] = str(rfc_number)
    client_rfc['RFCTitle'] = rfc_title
    client_rfc['HostName'] = address[0]
    client_rfc['PortNumber'] = str(peer_port)
    client_rfcs.insert(0, client_rfc)

def lookup_rfcs(number):
    flag = True
    response = []
    for rfc_dic in client_rfcs:
        if rfc_dic['RFCNumber'] == number:
            flag = False
            str_var = 'RFC ' + rfc_dic['RFCNumber'] + ' ' + rfc_dic['RFCTitle'] + ' ' + rfc_dic['HostName'] + ' ' + rfc_dic['PortNumber'] + '\n'
            response.append(str_var)
    if flag:
        message = lookup_notfound_message()
        return pickle.dumps((message, response))
 
    message = "P2P-CI/1.0 200 OK " + "\n"
    return pickle.dumps((message, response))

def list_rfcs():
    rfc_items = []
    for rfc_dic in client_rfcs:
        str_var = 'RFC ' + rfc_dic['RFCNumber'] + ' ' + rfc_dic['RFCTitle'] + ' ' + rfc_dic['HostName'] + ' ' + rfc_dic['PortNumber'] + '\n'
        rfc_items.append(str_var)
    return rfc_items

def request_handler_thread(connectionSocket, address):
    data = pickle.loads(connectionSocket.recv(1024))
    peer_port = data[2]
    client_info = {}
    client_info['HostName'] = address[0]
    client_info['PortNumber'] = str(peer_port)
    active_clients.insert(0, client_info)
    print("Server is currently serving the following clients:\n ", active_clients)
    update_server_registry(client_info, data, connectionSocket)

    while True:
        client_data = pickle.loads(connectionSocket.recv(1024))
    
        if client_data[1] == 'EXIT':
            drop_client(address[0], peer_port)
            remove_client_rfcs(address[0], peer_port)
            break
        else:
            print(client_data[0])
            if client_data[1] == 'LIST':
                connection_msg = "P2P-CI/1.0 200 OK" + "\n"
                rfc_items = list_rfcs()
                connectionSocket.send(pickle.dumps([connection_msg, rfc_items]))
            elif client_data[1] == "ADD":
                add_rfc(connectionSocket, address, client_data, peer_port)
            elif client_data[1] == "LOOKUP":
                new_data = lookup_rfcs(client_data[2])
                connectionSocket.send(new_data)
    
    if len(active_clients) == 0:
        print("Server is currently not serving any clients")
    else:
        print("Server is currently serving the following clients:\n ", active_clients)
    connectionSocket.close()


def req_handler():

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((serverHost,serverPort))

    # listen for client requests
    serverSocket.listen()

    while True:
        try:
            connectionSocket, address = serverSocket.accept()
            start_new_thread(request_handler_thread, (connectionSocket, address))
        except Exception as e:
            print("exited due to some exception - " + e)
            break
    serverSocket.close()
    

if __name__ == "__main__":
    serverPort = 7734
    
    serverHost = socket.gethostname()    
    ipAddress = socket.gethostbyname(serverHost)

    print(serverHost)
    print(ipAddress)

    # handle client requests
    req_handler()
    




