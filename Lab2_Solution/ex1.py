from flask import Flask, request, jsonify
import base64

app = Flask(__name__)


@app.route('/') # root or home route
def home():
		return 'Hello, World!'

@app.route('/hw2/ex1', methods=['POST'])  # listen for  post request 
def login():
		#if request.method == 'POST':
		data = request.get_json()  # get the json data payload from content
		#print(data)
		## Input data
		user = data['user']  # get username
		password =data['pass']  #get password
		#print (type(data['user']))
		def superencryption(msg,key):
			'''
			The encryption function
			Input : Messgae and encryption
			Output :  password 
			The password is to be verified against 
			the user "input Password" called here
			password_internal_verification.
			'''
			if len(key) < len(msg):
				diff = len(msg) - len(key);
				key += key[0:diff]
					#print (key)
			amsg = [ord(x) for x in msg]
			akey = [ord(x) for x in key[0:len(msg)] ]
			collector = [];
			for index,message in enumerate( amsg ):
				temp = message ^ akey[index]
				collector.append(temp);
			NewValue = ''.join(map(chr, collector))
			enc = base64.b64encode(NewValue.encode())
			enc = enc.decode("utf-8")  # make string
			return enc

		mySecureOneTimePad = "Never send a human to do a machine's job";
		password_internal_verification = superencryption(user, mySecureOneTimePad);
		#profile = 'lukman.olagoke@epfl.ch'
		if password== password_internal_verification:
			# If verification is okay return this
						return jsonify ({"status":"ok", "status_code":"200" }),200
		else :
			# return this if there is an error
			return  jsonify({"status":"error", "status_code":"400" }),400

# start the server with the 'run()' method
if __name__ == '__main__':
		app.run(host='127.0.0.1',debug=True, port= 5000)

