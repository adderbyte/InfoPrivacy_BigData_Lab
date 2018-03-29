#!/usr/bin/env python

import random
import asyncio
import websockets
import hashlib
import hmac
import binascii


from random import randint

def random_with_N_digits(n):
	'''
	Function to generate random numbers
	'''
	range_start = 10**(n-1)
	range_end = (10**n)-1
	return randint(range_start, range_end)

async def hello():
	async with websockets.connect('ws://com402.epfl.ch/hw2/ws') as websocket:
		#name = input("What's your email? ")
		name = "lukman.olagoke@epfl.ch"
		name = name.encode('utf-8')
		#name = binascii.hexlify(name).decode()# binascii.hexlify(A_bytes).decode()
		print ("Client Sending:")
		await websocket.send(name)
		print(" > {}".format(name))


		salt = await websocket.recv()


		#print("< {}".format(greeting))
		#feedback_ = ("< {}".format(greeting))
		print ("Server response: <<<  " + salt )

		#a = 123;
		a =  random.getrandbits(129)

		g = 2;
		N = "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3"
		'''
		##### convert a to hex ###############
		a = a_temp.to_bytes((a_temp.bit_length()+ 7)//8,'big')
		a = binascii.hexlify(a).decode()

		g = g_temp.to_bytes((g_temp.bit_length()+ 7)//8,'big')
		g = binascii.hexlify(g).decode(g)
		'''

		####### Conver N to number ############
		N_ =  binascii.unhexlify(N)
		N_ =  int.from_bytes(N_,'big')
		######################################

		A = pow(g,a,N_)#(g**a)%N_

		####### convert A to hex #################

		A_bytes = A.to_bytes((A.bit_length()+ 7)//8,'big')
		A_ =binascii.hexlify(A_bytes).decode()

		print ("Client Sending...:")
		print(" > {}".format(A_))
		###########################################

		########### send A #######################
		await websocket.send(A_)

		B = await websocket.recv()

		print ("Server response <<< : "+ B)
		############################################

		password = "IhAdCBNOXQoCBUcOSw01CBEITFoMSA=="

		B_bytes = binascii.unhexlify(B)
		#B = binascii.hexlify(B).decode()
		A_B = A_bytes + B_bytes;

		H_A_B = hashlib.sha256(A_B).hexdigest()

		U  = binascii.unhexlify(H_A_B);




		######################################
		salt_ = binascii.unhexlify(salt)
		H_P_U = hashlib.sha256(name+":".encode('utf-8')+password.encode('utf-8')).hexdigest()

		salt_ = binascii.unhexlify(salt)

		x = hashlib.sha256(salt_+binascii.unhexlify(H_P_U)).hexdigest()
		#x = hashlib.sha256(binascii.unhexlify(salt+H_P_U)).hexdigest()




		####################################

		B_number = int.from_bytes(B_bytes, 'big')


		#  x
		x_=binascii.unhexlify(x)
		x_number =  int.from_bytes(x_,'big')

		# u

		#u_ = binascii.unhexlify(U)
		u_number =int.from_bytes(U,'big')

		##################

		#g_power = 
		B_comp = (B_number%N_ -pow(g,x_number,N_))
		a_comp =  (a + (u_number * x_number));

		s_number = pow (B_comp ,a_comp ,N_)

		s_bytes  =s_number.to_bytes((s_number.bit_length()+ 7)//8,'big')
		s  = binascii.hexlify(s_bytes).decode()


		A_B_S = hashlib.sha256(A_bytes+B_bytes +s_bytes).hexdigest()

		print ("Client Sending...:")
		print(" > {}".format(A_B_S))
		await websocket.send(A_B_S)

		answer = await websocket.recv()

		print ("Server response: <<< ")
		print(answer)

asyncio.get_event_loop().run_until_complete(hello())

'''
import asyncio
import websockets

async def hello(uri):
	async with websockets.connect('ws://com402.epfl.ch/hw2/ws') as websocket:
		await websocket.send("Hello world!")

asyncio.get_event_loop().run_until_complete(
	hello('ws://localhost:8765'))
'''