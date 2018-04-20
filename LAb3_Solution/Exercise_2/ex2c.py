import string
import itertools
import hashlib




############################ Hash input ###################################################33
hash_ex2c = []
counter = 0
with open('hw3_ex2.txt') as inputfile:
    for line in inputfile:
        if "Exercise" in line :
            continue
        elif counter<20: #### ignore hashes from 1 to 20
            counter= counter +1
            #print(counter)
        elif counter <30: #### get hashes  between 20 and 30
            hash_ex2c.append(line.strip()) # append the hashes
            #print(counter, line)
            counter = counter + 1





###########################  Function to process Salt on input #####################
def salting_function(dictionary_element):
    '''
    input:  each line of dictionary text file
    output : append all salt component element to the word in each line

    '''
    output = [] # store output here
    for element in salts:
        output.append(''.join([dictionary_element,element]))
    return output

##############################################################################################333



############################ seperate hash from the salt ###################################################33


hash3_component = [] # store hash component here
salts = [] # store salt here 
for hash_salt in hash_ex2c:
    split_hash = hash_salt.split(", ") # split the hash from the salt
    hash3_component.append(split_hash[1]) # append hash the hash component 
    salts.append(split_hash[0])
############################ ###################################################33



##################### Loop to test dictionary ################333

output_file = open("ex2ca.txt", "w")
with open("datarock.txt") as inputfile:
    for line in inputfile:
        for salted_word in salting_function(line.strip()):
            computed_hash = hashlib.sha256(str.encode(salted_word)).hexdigest()
            if computed_hash in hash3_component:
                output_file.write("{0},\n".format(salted_word[:-2]))
                print(salted_word[:-2])
output_file.close()