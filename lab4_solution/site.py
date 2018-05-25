#!/usr/bin/env python3                                                                                                                              
import os
import sys
import populate
from flask import g
from flask import Flask, current_app
from flask import render_template, request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw4_ex3"

## This method returns a list of messages in a json format such as                                                                                  
## [                                                                                                                                                
##  { "name": <name>, "message": <message> },                                                                                                       
##  { "name": <name>, "message": <message> },                                                                                                       
##  ...                                                                                                                                             
## ]                                                                                                                                                
## If this is a POST request and there is a parameter "name" given, then only                                                                       
## messages of the given name should be returned.                                                                                                   
## If the POST parameter is invalid, then the response code must be 500.                                                                            
@app.route("/messages",methods=["GET","POST"])
def messages():
                                                                              
    users=[]                                                                                                         
    with db.cursor() as cursor:
        ## your code here  
        name =request.form.get("name") # get username 
       
        if request.method == "POST": # check if post request
            if  name != None: # check if name is not none
                if type(name) is str :   # check if name is string                                                                                                                     
                    sql= "SELECT *  from messages  WHERE  name = %s"; # prepare query
                    cursor.execute(sql, (name)) # execute query
                    row_data = cursor.fetchall() # fetch all data
                    #fun = lambda x,y:({"name": x , "message": y})
                    #response = [ fun for (name, message) in row_data] 
                    response=[{"name": name, "message": message} for (name, message) in row_data]  # format message resposne   
                       
                    return jsonify(response),200 # json response
                else:
                    return jsonify({ "status_code":500 }),500 # return this if name is not string
            else :
                return jsonify({ "status_code":500 }),500 # return this if name is none
        else:
             sql_2 = "SELECT *  from messages" ; # if not request post :: use this query
             cursor.execute(sql_2); # execute this query
             row2_data = cursor.fetchall() # fetch all returned messages
             response_2 = [{"name": name, "message": message} for (name, message) in row2_data] # prepare json respose
             return jsonify(response_2),200 # jsonify and return resposne

                
## This method returns the list of users in a json format such as                                                                                   
## { "users": [ <user1>, <user2>, ... ] }                                                                                                           
## This methods should limit the number of users if a GET URL parameter is given                                                                    
## named limit. For example, /users?limit=4 should only return the first four                                                                       
## users.                                                                                                                                           
## If the paramer given is invalid, then the response code must be 500.                                                                             
@app.route("/users",methods=["GET"])
def contact():
    with db.cursor() as cursor:
        ## your code here   
        Limit = request.args.get('limit',"") # get input parameter

        if Limit != '' : # check if parameter 'LImit' is empty
            if ( str(Limit).isnumeric() and int(Limit) >= 0): # checlk if it is of instance digit or int greater that zero
                 											 # check if a valid input basically	
                users_select_with_limit = "SELECT * from users"; # make a query with valid input
            
                cursor.execute(users_select_with_limit + " LIMIT %s", int(Limit)) # execute query using cursor handle
            

                users = cursor.fetchall() # get all users returned 
                json =  ({"users":users}) # prepare the json content

                return jsonify(json),200 # return response as json
            else:

                return jsonify({ "status_code":500 }),500 # rreturn this if resposne is not instance digit or invalid
        else:
             users_select = "SELECT * from users"; # if no paramets detected return users using this sql
             cursor.execute(users_select) # execute this select query
             users = cursor.fetchall() # fetch all users
             json =  ({"users":users}) # prepare json content

             return jsonify(json),200 
                



if __name__ == "__main__":                                                                                                                          
    seed = "randomseed"                                                                                                                             
    if len(sys.argv) == 2:                                                                                                                          
        seed = sys.argv[1]                                                                                                                          
                                                                                                                                                    
    db = pymysql.connect("localhost",                                                                                                               
                username,                                                                                                                           
                password,                                                                                                                           
                database)                                                                                                                           
    with db.cursor() as cursor:                                                                                                                     
        populate.populate_db(seed,cursor)                                                                                                           
        db.commit()                                                                                                                                 
    print("[+] database populated")                                                                                                                 
                                                                                                                                                    
    app.run(host='0.0.0.0',port=80)                                                                                                                 


