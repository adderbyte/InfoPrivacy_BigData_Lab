from flask import Flask, request, jsonify , make_response
import base64
import bcrypt


app = Flask(__name__)


@app.route('/') # root or home route
def home():
		return 'Hello, World!'

@app.route('/hw4/ex2', methods=['POST'])  # listen for  post request 
def login():
		#if request.method == 'POST':

		###########^Get password and username of post content ######################
		data = request.get_json()  # get the json data payload from content
		#print(data)
		## Input data
		user = data['user']  # get username
		password =data['pass']  #get password
		#print (type(data['user']))
		############################################################################

		############ Encode password as utf 8  ######################################3
		password_utf8 = password.encode('utf8'); # this convert to byte and ensure we can compute hash
		#################################################################333

		################### Use bcrypt function for hash ##########################
		hashed_password = bcrypt.hashpw(password_utf8, bcrypt.gensalt(14))	
		#############################################################################3


		##################### Make response #############################################
		resp = make_response( hashed_password) # the hash of passwors in the response
		resp.status_code = 200 # the status code of repsose 
		###########################################################################3

		return resp 
	

# start the server with the 'run()' method
if __name__ == '__main__':
		app.run(host='127.0.0.1',debug=True, port= 5000)

 