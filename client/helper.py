from _thread import *
from datetime import date
import os
import random
import platform
import time
import pickle
import random

def add_msg(rfc_num, rfc_title, socket, upload_client_port):
    msg = "ADD RFC " + str(rfc_num) + " P2P-CI/1.0 \n" \
        "Host: " + socket.gethostbyname(socket.gethostname()) + "\n" \
        "Port: " + str(upload_client_port) + "\n" \
        "Title: " + rfc_title + "\n"
    return msg

def get_rfc_msg(rfc_num, socket, os_type_version, version):
    msg = "GET RFC " + str(rfc_num) + " P2P-CI/" + str(version) + "\n" \
        "Host: " + socket.gethostbyname(socket.gethostname()) + "\n" \
        "OS: " + str(os_type_version) + "\n"
    return msg

def establish_connection_msg(socket, upload_client_port):
    msg = "ESTABLISH CONNECTION P2P-CI/1.0 \n" \
        "Host: " + socket.gethostbyname(socket.gethostname()) + "\n" \
        "Port: " + str(upload_client_port) + "\n"
    return msg

def lookup_msg(rfc_num, socket, upload_client_port, rfc_ttl):
    msg = "LOOKUP" + " RFC " + str(rfc_num) + " P2P-CI/1.0 \n" \
        "Host: " + socket.gethostbyname(socket.gethostname()) + "\n" \
        "Port: " + str(upload_client_port) + "\n" \
        "Title: " + rfc_ttl + "\n"
    return msg

def list_msg(socket, upload_client_port):
    msg = "LIST ALL P2P-CI/1.0 \n" \
        "Host: " + socket.gethostbyname(socket.gethostname()) + "\n" \
        "Port: " + str(upload_client_port) + "\n" 
    return msg

def send_msg(file_location):
    msg = "P2P-CI/1.0 200 OK \n" \
            "Date: " + str(date.today()) + "\n" \
            "OS: " + str(platform.system()) + "\n" \
            "Last-Modified: " + str(time.ctime(os.path.getmtime(file_location))) + "\n" \
            "Content-Length: " + str(os.path.getsize(file_location)) + "\n" \
            "Content-Type: text/plain \n"
    return msg

    
def send_file_not_found_msg():
    msg = "P2P-CI/1.0 404 Not Found \n"
    return msg

def send_bad_request_msg():
    msg = "P2P-CI/1.0 400 Bad Request \n"
    return msg

def send_version_not_supported_msg():
    msg = "P2P-CI/1.0 505 P2P-CI Version Not Supported \n"
    return msg

def verify_peer_request(data):
    if "P2P-CI" in data and "GET RFC" in data and "Host" in data and "OS" in data:
        return True
    else:
        return False

def verify_p2p_version(data):
    items = data.split()
    version_info = items[3]
    if(str(version_info[7:10]) == "1.0"):
        return True
    else:
        return False



