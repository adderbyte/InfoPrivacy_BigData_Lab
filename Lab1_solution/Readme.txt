
###############################################################
#                 READ ME 				      #
###############################################################

1) This file documents how to run the interceptor.py file which has the 
solution to the homework 1. And a brief explanation on how the exercises were
solved

2) Each exercise  has its own function in the interceptor.py file. 
The function name reflects the exercise it solves.

3) There is also a question in exercise 3 which is answered here


################################################################################
RUNNING THE SOURCE CODE FILE
#######################################################################

This  interceptor.py file  contains solutions to the
Homework 1 which has 4 exercises.

The names of each function has corresponds to 
the exercise number. E .g

def ex3:
	"This defines function to solve exercise3"


To see the solution to each exercise , from the command
line type:

						
		python3 -c 'from  interceptor import * ;  exercise3()'


where interceptor is the name of the file (ie this file) and exercise3 is the 
function that solves the corresponsing exercise of interest- in this case exercise 3.

Use CTRL-C to terminate exercution
######################################################################################


        


########################## Exercise  1   ###################################


For exercise one: The java script code for the site was inspected. It is observed that the 
encryption was done on the client side. The solution consist in taking the encryption function and using the right username (my email) and secureOneTimePad (“Never send a human to do a machine's job"). The function is run on the browser javascript console. It returns the right password on using the right username and msg. The source code also explains this. 
The function for exercise one will not run as python code because it is a javascript. Run it on console instead with right parameters.

Typring :
		python3 -c 'from  interceptor import * ;  exercise1 ’


as explained on how to run the code will not work for exercise 1. Since there is no python
function for exercise one its just a javascript code



########################## Exercise 2###################################

The solution involves decoding the cookie. Then change the “user” term in the cookie to “administrator”. One should be mindful of comma here.
Then decode the new cookie with “administrator” term then reuse the cookie in the browser.

The problem is that the website tracks users but the cookie is that securely encrypted. Which makes it vulnerable to bypass admin.

To run function for exercise 2 , do :

	python3 -c 'from  interceptor import * ;  ex2_cookies()’

This function returns the new cookie which should be used to replace the cookie in the 
browser in order to be granted access.


########################## Exercise 3   ##########################################

The solution to exercise 2 requires following the instructions properly. Intercepting and 
decoding the application layer payload. Then changing the shipping address to my email .

After this one uses the requests library to send a new packet with the address changed:

To run function for exercise 3:
 
		python3 -c 'from  interceptor import * ;  exercise3’



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
EXERCISE 3: 

QUESTION: Why would there not be an application layer in a tcp packet?


ANSWER The TCP packet is at the ip layer and does not concern itself with applicator layer.

It is an abstraction that has been built into the OSI model the same way “hub” will not have an “ip packet” because it is at lower layer. But the IP packer will have information from the ip layer down to the physical or data layer.

Same way , the application layer can have ip packer information since its at the higher layer.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



########################## Exercise 4###################################

Exercise 4 follows same pattern as exercise 3.

The solve this. The decoded application layer is piped to a text file. Then one can gently
search for those words or letters that matches the sensitive data.

On getting those sensitive data, a new packet is sent with sensitive data to retrieve token.

To run function for exercise 3:
 cd 
		python3 -c 'from  interceptor import * ;  exercise4()’









