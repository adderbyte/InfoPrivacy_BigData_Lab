#!/usr/bin/env python3
import random, datetime, sys, csv
from random import randrange, randint
import hashlib,binascii

#from datetime import datetime


date_start = datetime.date(2000, 1, 1)
date_period = 365 * 17

# Reads in emails.txt and movies.txt and creates 'nbr_movies' entries for each
# email.
# Returns the database, the emails and the movies in the following format:
# [ [ user, movie, date, grade ], ... ]
def create_db(nbr_movies):
	with open("emails.txt") as f:
		emails = f.read().split("\n");
	while "" in emails:
		emails.remove("")

	with open("movies.txt") as f:
		movies = f.read().split("\n");
	while "" in movies:
		movies.remove("")

	db = []

	for email in emails:
		movies_index = list(range(0, len(movies)))
		random.shuffle(movies_index)
		for i, f in enumerate(movies_index[0:nbr_movies]):
			dat = date_start + datetime.timedelta(randint(1, date_period))
			db.append(
				[email, movies[f], dat.strftime("%Y/%m/%d"), randint(1, 5)])
	
	return db, emails, movies


# Anonymize the given database, but still let the get_movies_with_rating
# function give the right answers.
mappings  = {}; 
mappings_date = {};
mappings_movies = {};
seen_movie_user_pair = set([])
seen_movie_user_pair_update= seen_movie_user_pair.update


def randN(n):
	'''
	input: integer
	output : generate pseudorandom numbers

	'''
	depth = int(10e300)
	c = list(range(0, n))
	l = random.sample(c, n)
	return int(''.join(str(d) for d in l[:n]))

def hash(string,salt):
	'''
	input : word to be hashed, salt
	output: hased string using salt
	'''
	hashed = hashlib.pbkdf2_hmac('sha512', bytes(string.encode('utf8')), bytes(salt.encode('utf8')), 100000)#.decode("utf-8")
	return hashed


def anonymize_1(db):
	'''
	input : list of list containing user mail, movies, date and ratings
	output : anonymized version of înput. ûser mail and date is anonymized
	'''
	for i in db:
		temp = i[0] # email
		temp_ = i[1] # movie
   
   
		if (temp, temp_) not in seen_movie_user_pair: 
			seen_movie_user_pair_update([(temp,temp_)]) # store user , movie pair in set
	   
			i[0] = '*' # anonymize user email
		
			if i[1] in mappings_movies.keys(): # check if movie was stored earlier
				i[1] = mappings_movies[i[1]] # get the stored value for the movie
			else:
				i[1] = randN( len(i[1])) # assign number to the movie if movie does not exiat
				mappings_movies[temp_] = i[1] # store the number in dictioanry

		#i[1] = randN(len(i[1]))
			i[2] = '*' # anonymize the date


		else:
			pass
	
	

	return db


# For a given anonymized-database and a rating, this function should return
# the films with the given rating.
def get_movies_with_rating(anon, rating):
	'''
	input : anon, raitng 
	output : films with given rating , no duplicate allowed

	'''

	movie_selct =[i for i in anon if i[3] == rating] # get movies with rating
	
	movies_ = [item[1] for item in movie_selct] # retirn only the movies from selection in movie_select
	
	m =  list(set(movies_)) # get unique movie list

	return m


# A bit lesser anonymization than anonymize_1, but still no date. The returned
# database should have enough information to be used by get_top_rated. If you
# use a too simple hashing-function like sha-256, the result will be rejected.

mappings_2  = {}; # dictionary to store user mail and his encryption (hmac)


seen_movie_user_pair_2 = set([]) # for to store user 
seen_movie_user_pair_update_2= seen_movie_user_pair_2.add # add user to set if not exist


################## Anonymize 2 Starts Here #############################################################################


def anonymize_2(db):

	'''
	input :  list of list containing user mail, movies, date and ratings
	output :  anonymized version of înput. date is anonymized


	'''
	for i in db:
		temp = i[0] # user mail
		temp_ = i[1] # movie
		temp_date = i[2] # date 
		#full_temp = i.copy()
		if temp not in seen_movie_user_pair_2: 
			seen_movie_user_pair_update_2(temp) # update user set if not seen before
			i[0] = hash(temp,temp_) # hash the user  using hmac
			#mappings_2[i[0]]  = full_temp
			mappings_2[temp]  = i[0] # store in dictionary
		
			i[2] = '*' # anonymize date
		
		elif temp  in seen_movie_user_pair_2: # if user exist in the set seen_movie_user_pair_2
		
			i[0]= [mappings_2[i] for i in mappings_2.keys() if i == temp][0] # Get the user email encryption 
			# dictionary
			i[2] = '*' # anonymize date
	return db
	
	


# get_top_rated searches for all users having rated a movie and searches their
# top-rated movie(s). It returns a list of all found movies, also doubles!

def get_top_rated(anon, movie):
	'''
	input : anon , movie
	output: top rated movie for user

	'''
	user_list = [i[0] for i in anon if i[1] == movie ] # get users that rate the movie
	#print(user_list)
	top_rated= [i for i in anon if i[0] in  user_list ] # extract the movies of users that rated movie
	
	collect = [] # collect results here 
	
	user_list = [item[0] for item in top_rated] # get user mail here with duplicates
	unique_list = list(set(user_list)) # get unique mail encryption here: remove duplicate


	for i in unique_list: # iterate through each unique user in unique list
		movie_u = [item for item in top_rated if item[0] == i   ] # get the movie for one user 
		max_ = max([item[3] for item in top_rated if item[0] == i   ]) # get the highes rating value
		q =  [item[1] for item in movie_u if item[3] == max_ ] # retrieve movies that have rating value = max rating
		collect.append(q) # collect moview here

	collector = [item for sublist in collect for item in sublist ]# convert list to flat list. Make sublist
	# disappear and have a flat lisz
	return collector
	


# This is called when you start the script on localhost, and when the
# checker wants to run your functions.
if __name__ == "__main__":
	# This part can be modified at your convenience.
	if len(sys.argv) == 1:
		print("Testing mode")
		db, emails, movies = create_db(1)
		


		anon_db1 = anonymize_1(db)
		#print(get_movies_with_rating(anon_db1, 1))

		anon_db2 = anonymize_2(db)
		#print(get_top_rated(anon_db2, movies[0]))

	# If you modify this part, don't complain if it doesn't work anymore!
	# This part is used to communicate with the verification-script. So you
	# should not touch it (unless you're looking for a bug to exploit the
	# verification script - but we didn't plan to put one in there).
	if len(sys.argv) >= 3:
		db_file, ex = sys.argv[1:3]
		with open(db_file) as f:
			db = list(csv.reader(f, skipinitialspace=True))
		# Get nice ints for comparisons
		for i, line in enumerate(db):
			db[i][3] = int(line[3])

		result = []
		if ex == "ex1aa":
			result = anonymize_1(db)
		elif ex == "ex1ag":
			rating = int(sys.argv[3])
			result = [get_movies_with_rating(db, rating)]
		elif ex == "ex1ba":
			result = anonymize_2(db)
		elif ex == "ex1bg":
			movie = sys.argv[3]
			result = [get_top_rated(db, movie)]

		with open("/tmp/student.csv", "w") as f:
			writer = csv.writer(f)
			writer.writerows(iter(result))
