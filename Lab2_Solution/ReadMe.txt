I##############################################################
#			READ ME				     #
##############################################################



##############  Exercise 1 ########################################################

For exercise one the file ex1.py provides the solution. For the	  
encryption, it should be noted that the encryption algorithm      
named “superencryption”  used in the first homework was		  
rewritten in python to be integrated in the solution to this
exercise.

1) The username and password are retrieved from the “POST”
request in json format

2) The username is parsed into the “superencryption” function 
together with the mysecureOneTimePad string variable. 

3) The returned variable is stored in variable password.

4) Then the final step involves comparing the password with the 
stored “password” stored in the system. It returns 200 if okay and
400 otherwise

5) Occasionally, the post request are tested using curl as below:
curl  http://127.0.0.1:5000/hw2/ex1 -H  "Content-Type:application/json" -X POST -d '{"user":"lukman@epfl.ch", "pass": "password"}'

##################  Exercise  4 #####################################################

############# For exercise 4a: 

1) The nginx server is started. Running :
		$ curl http://localhost
we can test the local host and return index.html.

2) The task is to configure the local host for https. Thus there is need for key
and certificate

3) The keys and certificate were generated using the openssl  with the correct
arguments as below:

$ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout 
/etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt


4) Thereafter the content of the default.conf file is being corrected to reflect the path
or location of the certificate and key for https. Then listen 443 (ssl port) is added, 
to listen for https.
Details of the  content of default.conf for ex4a is in the file ex4a.conf.

5) Effecting the changes above , and  running:

		$ curl —insecure https:localhost

will return the index.html file. The insecure argument is needed since the certificate is
self-assigned. And it is not verified by certified authority.

6) This is verified using “./verify.sh a “ and the token is returned


#############  For Exercise 4b: 

1) The keys and .csr file (certificate signing request file) will be generated as below:

$ openssl req -new -newkey rsa:2048 -nodes -keyout /etc/ssl/private/signed_by_dedis.key  
 -out  /etc/ssl/certs/signed_by_dedis.csr

2) The .csr file (certificate signing request file) will be uploaded to the
 http://com402.epfl.ch/hw2/ . The certicicate, .crt file is downloaded, and saved 
as signed_by_dedis.crt

3) Finally the signed_by_dedis.key and signed_by_dedis.crt path/location are 
copied to the default.conf file and  verified “./verify.sh b”



############### For Exercise 3 ################

1) Check if the user is "administrator"  and password = "42"

2) If the above is true create  the cookie payload as indicated in the instruction. Compute hash using payload and salt(password). Then append the result of hash  to the cookie payload - This is the full cookie.
   Thus Cookie now contains the  "payload + hash". Send this as Cookie response.

3) If an ordinary user,  construct the cookie payload as indicated in instruction. Compute Hash. Append hash to cookie. Send cookie response.

4) If user logs in again: check if the user is adiniatrator or not:
	A) For administrator

	i) if administrator, extract the payload minus the hash. Then extract hash separately.
	ii) Recompute the hash on payload
	iii) return 200 if the computed hash is equal to extrated hash. Else return 403.
	
	B) Normal Use --Normal Cookie

	i) Repeat process in A and check if cookie is not tampered . Here username will be username -- not admin.
	ii) if the computed cookie matches with extracted cookie , retrun 200
	iii) Else return 403


#### Exercise 2###############

Exercise 2 can be solved by making the computation follow the diagram illustrated in the instruction for Homework 2 ex 2.
The websockets library was used. The only tricky thing is using pow(a,b,c) to do modular exponentiation in order to save time.
In addition to leverage in the modular property when computing  S that is, S = (B-g^x)^(a+u*x) % N = pow((B%N-pow(g,x,N)) ,(a+u*x),N).
	

 