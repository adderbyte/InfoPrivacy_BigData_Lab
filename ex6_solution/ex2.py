from cothority import Cothority
from hashlib import sha256


#################################### Url and cothority block###########################################3
url_site = 'ws://com402.epfl.ch:7003'
blocks_new = Cothority.getBlocks(url_site, bytes.fromhex('e0e932a37e113432fcbd24de7945477c96a576b32ac69091c55360e087a59e38'))

################## last block#######################################################
end_block = blocks_new[len(blocks_new)-1]

################ hash of the laqst block #########################################
hash_of_last_block = end_block.Hash
my_mail = b'lukman.olagoke@epfl.ch'
###############################################################################33

################# parameter to be used ################################################
counter = 0 # counter to increment to check max
range_loop = 800000000 # loop range
store = []
max_received =3 # max to end computation
###########################################################################33

def validation_test(hash_val,url_site,test_data,end_block):
    '''
    
    This function computes new block and 
    returns last block and hash of the last block for the new computed block
    '''
    try:
        fresh_block = Cothority.createNextBlock(end_block, test_data)
        msg = Cothority.storeBlock(url_site, fresh_block)

        blocks_new = Cothority.getBlocks(url_site, bytes.fromhex('e0e932a37e113432fcbd24de7945477c96a576b32ac69091c55360e087a59e38'))
        end_block = blocks_new[len(blocks_new)-1]
        #data_block = end_block.Data
        hash_of_last_block = end_block.Hash
        return hash_of_last_block,end_block
    except:
        print('error')

for l in range(0,range_loop):
    one_time_use = l.to_bytes(32,'big')
    test_data = one_time_use + hash_of_last_block + my_mail
    hash_val = sha256(test_data)
    if counter != max_received and  hash_val.hexdigest().startswith("000000"):
         hash_of_last_block, end_block = validation_test(hash_val,url_site,test_data,end_block) # call the validation function
         store.append(hash_val.hexdigest()) # store the nex values
         counter = counter + 1
    elif  counter == max_received:
         break
    else:
        continue
print(store)