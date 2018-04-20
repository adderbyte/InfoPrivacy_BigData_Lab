# hello 
from netfilterqueue import NetfilterQueue
from scapy.all import *
from scapy.all import IP
import sys


'''
################################################################################
For this session:
I read the analysis of TLS packet from the link below:

http://blog.fourthbit.com/2014/12/23/traffic-analysis-of-an-ssl-slash-tls-session

This gives me a lot of information I needed to know. In particular I have referenced 
to recognise the work of the blog author Alvaro CAstro-Castilla. And Also this will 
serve as future reference for me ar anyone.

To detect the version of the TLS session the following blog was useful:

https://security.stackexchange.com/questions/100029/how-do-we-determine-the-ssl-tls-version-of-an-http-request

The following stack overflow page was also useful esüecially for the FIN packet generation:

https://stackoverflow.com/questions/42422457/how-can-i-close-a-connection-via-scapy-sending-a-fin-packet
######################################################################################
'''

conf.L3socket=L3RawSocket

def print_and_accept(pkt):
    
    payload = pkt.get_payload() # get the payload and store in variable payload
    ip = IP(payload) # create an IP packet from payload
    ###################### Get packer identities, to be used later ##########################################
    ip_src=ip.src # Src ip address
    ip_dst= ip.dst # destination ip address
    ip_dport = ip[TCP].dport # destination port
    ip_sport = ip[TCP].sport # src port
    ##########################################################################################################

    ################################# TLS packet identifiers##################################################
    TLSv1_2 = b'\x16\x03\x03' # identfier for TLS 1.2 handshake packet 
    TLSv1_1 = b'\x16\x03\x02' # identifier for TLS 1.2 handshake packet 
    ##########################################################################################################

    ################ Main Program LOgic for packet detection ################################################

    ########### ******************Main IF LOCK ****************************************#######################################3
    # checks if packet has raw and TCP poacket (2 conditions)
    if ip.haslayer(Raw) and  ip.haslayer(TCP):
            tls_load = ip[Raw].load # get raw packet
            
            if TLSv1_2 in tls_load or TLSv1_1 in tls_load:
                    pkt.drop() # drop packet of TLS v1.2 or 1.1
                    pkt_=IP(src=ip_dst , dst=ip_src) # Construct a new packet to send

                    #####################FIN PACKET generation ###################################
                    FIN=pkt_/TCP(sport=ip_dport, dport=ip_sport, flags="FA",seq= ip[TCP].ack,ack= ip[TCP].seq+1) # FIN packet with required port
                    # In the implementation the src and dest address have been reversed.
                    # This turns out to work especially in this solution.
                    # A solution is also possible without it being reversed.

                    ################# Send FIN packet #########################################33
                    sr1(FIN) # using sr1 instead of send ensures that the one waits for  acknowledgement should be received

                    ##################### And receipt of answer ##################################
                    LASTACK = pkt_/TCP(sport=ip_dport, dport=ip_sport, flags="A",seq= ip[TCP].ack,ack= ip[TCP].seq+1) # ack packet
                    send(LASTACK) # send ack packet
            ############################# else statementg to accêpt all other packets with RAW including TLSv1.0 #############################
            else:
                pkt.accept()# äccept all other poacket
    ######## else for the main IF block ###############################
    ########********This accept TCP packet (packet without raw) *************###########
    else:
        pkt.accept()


################# NFQUEUE BLOCK ###############################################################
nfqueue = NetfilterQueue() # generate queue
nfqueue.bind(0, print_and_accept) # bind queue to queue number and call back function

############################### Try Catch Loop for the main function ############################
try:
    nfqueue.run() # Run nfqueue
except KeyboardInterrupt:
    sys.exit(0) # exit on keyboard interrupt

###########################################################################################33

################# End pragram ##############################################################333
nfqueue.unbind()
sys.exit(0)
#####################################################################################################


