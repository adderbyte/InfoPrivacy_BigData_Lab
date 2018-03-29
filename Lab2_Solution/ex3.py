from flask import Flask, request, jsonify,make_response,url_for,redirect
import base64
from random import randint
import hmac
import re
import hashlib




#"IhAdCBNOXQoCBUcOSw01CBEITFoMSA=="

app = Flask(__name__)


@app.route('/') # root or home route
def home():
		return 'Hello, World!'

@app.route('/ex3/login',methods=['POST','GET'])  # listen for  post request 
def login():
		n = 10 # lenght of the randome numner
		data = request.get_json()
		user = data['user']
		password = data['pass']

		##############  if else block below for capture administrator and others ################################

		if user == "administrator" and   password == "42":
			resp = make_response(jsonify({"status":"received","status_code":"ok"}),200)


			########### print and get user name ########################\
			print(user)
			type_= user ;
			#############################################################

			############ set cookie parameteres here ####################
			random_ = ''.join(["%s" % randint(0, 9) for num in range(0, n)])
			site_ = "com402"
			reason= "hw2"
			work = "ex3"
			HMAC = "IhAdCBNOXQoCBUcOSw01CBEITFoMSA=="
			HMACS = HMAC.encode('utf8')
			############################################################


			################ configure/specify cookies  ###########################
			cookie_spec = [user ,random_ ,site_ ,reason , work  ,  user]
			cookies = ','.join(cookie_spec);
			print (cookies)
			########################################################################

			########### sign the cookie  and append to cookie configuration above #################################
			sign = hmac.new(HMACS, cookies.encode('utf8') , hashlib.sha512).hexdigest()
			cookie_spec.append(sign)
			cookies_with_hmac = ','.join(cookie_spec);
			print (cookies_with_hmac)
			######################################################################################################


			################## Encode signed cookie ##############################
			cookies_ = base64.b64encode(cookies_with_hmac.encode())
			#######################################################################



			################## return response#####################################
			resp.set_cookie('LoginCookie', cookies_)
			return resp
			#######################administrator handling code ends here ##############################
		else:
			resp = make_response(jsonify({"status":"received","status_code":"ok"}),200) # configure response
			#redirect_to_index = redirect('/ex3/list')
			#resp = app.make_response(redirect_to_index )
			########### print and get user name ########################
			print(user)
			type_= user;
			#############################################################

			############ set cookie parameteres here ####################
			random_ = ''.join(["%s" % randint(0, 9) for num in range(0, n)])
			site_ = "com402"
			reason= "hw2"
			work = "ex3"
			comma = ","
			HMAC = "IhAdCBNOXQoCBUcOSw01CBEITFoMSA=="
			user_ ="user"
			HMACS = HMAC.encode('utf8')
			############################################################

			################ configure/specify cookies  ###########################
			cookie_spec = [user ,random_ ,site_ ,reason , work  ,  user_] # put cookie elements in a list
			cookies =  ','.join(map(str, cookie_spec)) # make coookie specification into string
			print(cookies)
			########################################################################

			########### sign the cookie  and append to cookie configuration above #################################
			sign = hmac.new(HMACS, cookies.encode('utf8') , hashlib.sha512).hexdigest()  # sign the cookie specification
			cookie_spec.append(sign) # append the signature to cookie spec
			cookies_with_hmac = ','.join(cookie_spec);# make the list comma separated
			print (cookies_with_hmac)
			######################################################################################################


			################## Encode signed cookie ##############################
			cookies_ = base64.b64encode(cookies_with_hmac.encode()) # encode the cookie
			#######################################################################


			################## return response#####################################
			resp.set_cookie('LoginCookie', cookies_)
			return resp


@app.route('/ex3/list',methods=['GET','POST'])
def getcookie():
	cookie = request.cookies.get('LoginCookie')
	#print(name)

	decoded_cookie = base64.b64decode(cookie)
	decoded_cookie = decoded_cookie.decode("utf-8")

	print (decoded_cookie)
	check_phrase = decoded_cookie.partition(',')[0] # user name administrator or otherwise
	print(check_phrase)
	############# administraator test ##################
	if check_phrase == "administrator":
		##############get admin details ############################################
		assert check_phrase == "administrator"
		admin=decoded_cookie.partition(',')[0] # check the administrator if , i.e administrator
		#print(admin)
		##############################################################################

		############### extract payload = cookie - hmac ############################
		cookie_payload = decoded_cookie.split(admin,2)[1]; # extract string between "administrator" keyword
		cookie_payload_full = admin + cookie_payload +  admin  # add admin to the start and end   given to make full payload
		############################################################################

		##############  GEt  HMAC from payload #################################
		cookie_mac = decoded_cookie.split(admin,2)[2].strip(',')
		cookie_mac = re.sub(',','',cookie_mac)  # remove , in the  cookie mac 
		print("------")
		print(cookie_mac)
		print ()
		######################################################################


		########### Compute HMAC from payload using secret######################
		HMAC = "IhAdCBNOXQoCBUcOSw01CBEITFoMSA==" # secret for HMAC
		HMACS = HMAC.encode('utf8') # encode as utf-8
		sign_test = hmac.new(HMACS, cookie_payload_full.encode('utf8') , hashlib.sha512).hexdigest()
		#######################################################################

		############### Check computed MAC with  MAC from payload################
		if sign_test == cookie_mac:
			return jsonify({"status":"received","status_code":"ok"}),200
		else:
			return  jsonify({"status":"received","status_code":"tampered cookie"}),403
	    ##################### Check for admin ends here ############################
	else:
		assert check_phrase != "administrator" # assert this is not admin
		user=check_phrase # mstore user name 

		############### extract payload = cookie - hmac ############################
		cookie_payload = decoded_cookie.split('user',1)[0]; # extract string between payload
		print("******** cookie payload  ")
		print (cookie_payload)
		cookie_payload_full = cookie_payload+"user"
		print ("***********full payload")
		print (cookie_payload_full)
		#############################################################################

		################ get MAC in payload ############################################
		cookie_mac = decoded_cookie.split("user",1)[1].strip(',')
		cookie_mac = re.sub(',','',cookie_mac)  # remove , 
		print("------")
		print(cookie_mac)
		print ("--------")
		##################################################################################

		############### Compute MAC from payload  using secret key#########################
		HMAC = "IhAdCBNOXQoCBUcOSw01CBEITFoMSA==" # secret key
		HMACS = HMAC.encode('utf8') # encode in utf-8
		sign_test = hmac.new(HMACS, cookie_payload_full.encode('utf8') , hashlib.sha512).hexdigest() # make the digest
		print (sign_test)
		#################################################################################

		#############   tverify cookie ################################################
		if sign_test == cookie_mac:
			return jsonify({"status":"user","status_code":"user_confirmed"}),201
		else:
			return   jsonify({"status":"user","status_code":"tampered"}),403



# start the server with the 'run()' method
if __name__ == '__main__':
		app.run(host='127.0.0.1',debug=True, port= 5000)








