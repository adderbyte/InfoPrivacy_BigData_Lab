
from itertools import product
import string
import itertools
import hashlib

hash_ex2a = []
counter = 0
with open('hw3_ex2.txt') as inputfile:
    for line in inputfile:
        if "Exercise" in line :
            continue
        elif counter==10:
            break
        else:
            hash_ex2a.append(line.strip())
            counter = counter+1



chars = list(string.ascii_lowercase) + list(map(str,range(0,10))) # character set
password_length_list = [4,5,6]
count = 0 ; # counter to stop when 10 passwirds have been decrypted


def cracker(chars,password_length_list,hash_ex2a,count=0):
    assert count == 0;
    passwords = []
    for length in password_length_list: # only do lengths of 4,5,6
    #print(length)
        to_attempt = product(chars, repeat=length)
        for attempt in to_attempt:
            plain_text = ''.join(attempt)
            #print(plain_text)
            computed_hash = hashlib.sha256(str.encode(plain_text)).hexdigest()
            if computed_hash in hash_ex2a:
                assert computed_hash in hash_ex2a
                print(plain_text)
                passwords.append(plain_text)
                count = count +1
                #print(count)
            if count == 10:
                break
    return passwords


password = cracker(chars,password_length_list,hash_ex2a,count=0)


import csv
with open('ex2a_password_test.txt', "w") as output:
    writer = csv.writer(output, lineterminator=',')
    for val in passwords:
        writer.writerow([val]) 