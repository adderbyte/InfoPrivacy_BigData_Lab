import string
import itertools
import hashlib


################################################ Get the hashes for ex2b ######################
hashes_for_ex2b = [] # store the hashes
counter = 0 # count the number of lines and exit when we havwe 10 words
with open('hw3_ex2.txt') as inputfile: # input file is hw2_ex2.txt
	for line in inputfile:
		if "Exercise" in line : # exclude line with the word exercise
			continue
		elif counter<10: # if iline less then 10 increment count
			counter= counter +1
			#print(counter)
		elif counter <20: ## line from 11 should be added to the list
			hashes_for_ex2b.append(line.strip()) # append hash to the list
			#print(counter, line)
			counter = counter + 1 # increment counter here to increase  till value 20 is achieved
		   
###########################################################################################################		 


###################### Preparation : the modification list ################################################################

possible_transformation = [('e', '3'), ('o', '0'), ('i', '1'), ('e', '3'), ('o', '0'), ('i', '1')] # possible variation or modification
#################  preparation ######################################################################

################### Define function to apply required modification ########################################################333
def modification(word):
	'''
	input: copy of candidate password
	output: augmented copy . Modified by simple transformations

	returns a modification of input base in the possible transfirmations 
	'''
	augmented_list_store = [word, word.title()] # add capital letter modification
	for transform in possible_transformation: # iterate through the poddible traansformation 
		for string_ in augmented_list_store: 
			if transform[0] in string_: # if a possible_transformable letter is in string
				new_string = string_.replace(transform[0], transform[1]) # make a new string replacin new letter with transform
				if new_string not in augmented_list_store: # check if new string is in the store
					augmented_list_store.append(new_string) # if not in store already add it
				if new_string.title() not in augmented_list_store:# apply capital modification and chek is we have this in the lsit too
					augmented_list_store.append(new_string.title()) # if true augment the list with this
	return augmented_list_store
######################################################################################################################################

#################  Conduct search for the password applying modification using the modification function ####################ä
# #### data rock data set was used 
# it was transformed using the command : iconv -f ISO-8859-1 -t UTF-8 rockyou.txt > datarock.txt ###################	
#### rockyou.txt is the file downloaded from provided link in the homeaork 

output_file = open("ex2ba.txt", "w") # store output list here

with open("datarock.txt") as inputfile:
	for line in inputfile: # input line
		change_words = modification(line.strip()) # apply modifiĉation function
		
		for word in change_words:
			
			computed_hash = hashlib.sha256(str.encode(word)).hexdigest() # compute hash
			
			if computed_hash in hashes_for_ex2b: # check if hash in list
				output_file.write("{0},\n".format(word))
				print(word)

output_file.close()
