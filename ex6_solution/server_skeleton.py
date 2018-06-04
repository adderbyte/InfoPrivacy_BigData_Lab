#!/usr/bin/env python3

import sys
import socket
import threading
import binascii

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

PRIMARY_SERVER_ID = 0

RSA_MODULUS_SIZE = 1024

AES_IV_SIZE = AES.block_size
AES_MODE    = AES.MODE_CBC

CHAT_MSG_INDEX_SIZE = 20
CHAT_MSG_BODY_SIZE  = 44
CHAT_MSG_NB = 10

UDP_RECV_TIMEOUT = 10

class RiffleServer:

    # Server id - determines the order of onion decryption
    server_id = None

    server_ip   = None
    udp_port    = None
    udp_socket  = None

    # Dictionary of all servers, key is server_id and value is (ip, port) pair
    all_servers = None

    # Public/Private RSA key pair
    rsa_key_pair = None

    # AES key shared with the client which will send all the chat messages
    client_shared_key = None

    # Dictionary of chat messages, key is message index and value is msg itself
    chat_messages = None

    def __init__(self, server_id, server_ip, udp_port, all_servers):

        self.server_id    = server_id
        self.server_ip    = server_ip
        self.udp_port     = udp_port
        self.all_servers  = all_servers
        self.rsa_key_pair = RSA.generate(RSA_MODULUS_SIZE)

        self.udp_socket   = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((server_ip, udp_port))
        self.udp_socket.settimeout(UDP_RECV_TIMEOUT)

        self.chat_messages = dict()

    # Method expects skey_encrypted as a hex-string, which unhexlified
    # respresents the rsa encryption(with our pub key) of the client shared key
    # Decrypt it and store as client_shared_key
    def recv_client_shared_key(self, skey_encrypted):
        self.client_shared_key = self.rsa_key_pair.decrypt(binascii.unhexlify(skey_encrypted))

    ################### Helper functions ###################################333
    # Helper function to remove one layer of encryption
    def encryption_layerOne_remover(self, msg_encrypted):
        '''
        input : encrypted message
        output: one layer decryption

        '''
        message = binascii.unhexlify(msg_encrypted)
        aes = AES.new(self.client_shared_key, AES_MODE, message[0:AES_IV_SIZE])
        decrypt_1 = aes.decrypt(message[AES_IV_SIZE:])
        return decrypt_1

    #compute xor
    def XOR_func(self, val1, val2):
        '''
        input : val1 and val2 
        performs xor of input values 
        änd returns results

        '''
        result = []
        if len(val1) != len(val2):
            return result

        
        result = [val1[i] ^ val2[i] for i in range(len(val1)) ]

        return bytes(result)
    #######################################################################################3
    # Receive a chat message from the client, only the primary server
    # should receive this message. The message is onion-encrypted,
    # primary server should start the onion-decryption process.
    # So, primary server should decrypt the message with the client_shared_key
    # and send result to the next server in chain.
    # Method expects msg_encrypted as a hex-string, which unhexlified
    # respresents the AES onion-encrypted chat message
    def recv_chat_msg_client(self, msg_encrypted):
        
         
        # Only primary server should receive/process
        # a chat message from a client
        ######################### check pry server #########################33333
        if self.server_id != PRIMARY_SERVER_ID:
            return
        ######################################################################333

        assert self.server_id == PRIMARY_SERVER_ID


        #########################3one layer 0f encryption remover function called here Remove a layer of encryption#########
        message =  self.encryption_layerOne_remover(msg_encrypted)
        ##################################################################################################


        ############## checking if there is next server ################################33
        # If there is next server send the decrypted message to it,
        id_for_next_server = self.server_id + 1
        #############################################################################3
        
        
        ########################### ###################################################3
        # check if there is next server in the chain
        # if no next server store mesage
        if id_for_next_server in self.all_servers.keys():
            hexlify_message = binascii.hexlify(message)
            receiver_id = self.all_servers[id_for_next_server];
            self.udp_socket.sendto(b'chat_msg_server ' + hexlify_message,receiver_id)
        else:
            self.chat_messages[int(message[:CHAT_MSG_INDEX_SIZE])] = message[CHAT_MSG_INDEX_SIZE:].decode()

    # Receive a chat message from another server (the previous server in the chain)
    def recv_chat_msg_server(self, msg_encrypted, sender):

         # Check if the message is sent by the previous server in the chain
        # If not, ignore the messsage
        ###################### check previous user is sender ###########################33
        previous_server = self.all_servers[self.server_id - 1]
        if previous_server != sender: 
            return
        ####################################################################


        ###############use assertion to enforce check #####################
        assert  previous_server == sender;
        ################################################################3


        ############ one layer 0f encryption remover function called here #######################
        message =  self.encryption_layerOne_remover(msg_encrypted)
        #######################################################################33


        ####################### decryotion one layer by laŷer###################################33333
        # If there is next server send the decrypted message to it,
        # else this is the last server, store the message and broadcast it
        id_for_next_server = self.server_id + 1

        
        if id_for_next_server in self.all_servers.keys():
            hexalify_message =  binascii.hexlify(message)
            receiver_id = self.all_servers[id_for_next_server]
            self.udp_socket.sendto(b'chat_msg_server ' + hexalify_message, receiver_id)
        else:
            self.chat_messages[int(message[:CHAT_MSG_INDEX_SIZE])] = message[CHAT_MSG_INDEX_SIZE:].decode()
            for server in self.all_servers.values():
                self.udp_socket.sendto(b'chat_msg_plain ' + message, server)



    # Receive the plain-text chat message. This happens when the last server
    # in the chain onion-decrypts a message from a client and thus obtains
    # the plain-text message which is then broadcasted to all servers.
    # So, this method should just store the message
    def recv_chat_msg_plain(self, msg):
        self.chat_messages[int(msg[:CHAT_MSG_INDEX_SIZE])] = msg[CHAT_MSG_INDEX_SIZE:]


    # Process the PIR request from a client. Bitmask has _n_ bits,
    # where _n_ is the number of chat messages. Each bit _j_ in the bitmask
    # corresponds to the chat message with index _j_. If _j_ is set to 1,
    # the message with this index is 'selected'.
    # Xor all messages selected by the bitmask and send the result back
    def process_pir_request(self, bitmask, sender):
        result = b''
        temp = bytes([0 for i in range(CHAT_MSG_BODY_SIZE)])
        
        for i in range(CHAT_MSG_NB):
            if 1 << i & bitmask != 0:
                temp = self.XOR_func(temp, self.chat_messages[i].encode())
        
        result = temp
        # Please be careful here, our client expects the result as bytes
        # type(result) = <class 'bytes'> in Python3 
        self.udp_socket.sendto(result, sender)
    


    # Method which runs in a thread
    def run(self):

        print('Server', self.server_id, 'starting...')

        while(True):

            # Server will listen on the assigned port and wait for a message
            # If no message is received for more than the timeout time,
            # which is set in the init method, exception will be raised,
            # and thread will stop.
            try:
                message, sender = self.udp_socket.recvfrom(4096)
            except socket.timeout:
                print('Server %d udp-receive timedout' % self.server_id)
                break

            # Received message is of type bytes, so we decode it to get string
            message = message.decode()

            # Message format: op_code body
            op_code = message.split()[0]
            print('Server', self.server_id, 'received op_code:', op_code)

            if op_code == 'pubkey_req':
                # Request for server's RSA public key
                # Just export pubkey and send it back to the sender
                pub_key = self.rsa_key_pair.publickey().exportKey()
                self.udp_socket.sendto(pub_key, sender)

            elif op_code == 'shared_key':
                # Client sends an encrypted shared key
                shared_key = message.split(' ', 1)[1]
                self.recv_client_shared_key(shared_key)

            elif op_code == 'chat_msg_client':
                # Client sends an onion-encrypted chat message
                chat_msg = message.split(' ', 1)[1]
                self.recv_chat_msg_client(chat_msg)

            elif op_code == 'chat_msg_server':
                # Previous server sends an onion-encrypted chat message
                chat_msg = message.split(' ', 1)[1]
                self.recv_chat_msg_server(chat_msg, sender)

            elif op_code == 'chat_msg_plain':
                # Last servers server sends a plain-text chat message
                chat_msg = message.split(' ', 1)[1]
                self.recv_chat_msg_plain(chat_msg)

            elif op_code == 'pir_req':
                # Client sends PIR request
                bitmask = int(message.split(' ', 1)[1])
                self.process_pir_request(bitmask, sender)

            elif op_code == 'quit':
                print('Server', self.server_id, 'quiting...')
                break

            else:
                err_msg = 'Op_code %s not supported' % op_code
                self.udp_socket.sendto(err_msg.encode(), sender)

def read_server_data():

    # Read data about the servers from a file
    servers_filename = 'all_servers.txt'

    all_servers = dict()
    with open(servers_filename, 'r') as fp:

        for line in fp.readlines():
            server_id = int(line.split()[0])
            server_ip = line.split()[1]
            udp_port  = int(line.split()[2])

            all_servers[server_id] = (server_ip, udp_port)

    return all_servers


def main():

    all_servers = read_server_data()

    # Create RiffleServers and run each one in a separate thread
    server_threads = []
    for server_id, (server_ip, udp_port) in all_servers.items():

        ser = RiffleServer(server_id, server_ip, udp_port, all_servers)
        server_threads.append(threading.Thread(target=ser.run))
        server_threads[-1].start()

    for thr in server_threads:
        thr.join()


if __name__ == '__main__':
    main()
