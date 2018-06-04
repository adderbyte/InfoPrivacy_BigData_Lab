########################## import important files ######################################33
import wave
import bitarray
import random
import binascii

my_file = "lukman.olagoke@epfl.ch.wav"

####read the audio file #################################################################3
audio_provided   = wave.open(my_file, "r")


############## Get audio_channels in audio file ############################################3   
audio_channels = audio_provided.getnchannels()

############## Get audio_channels in audio file ############################################33

frames = audio_provided.getnframes() # get  frames
samples = frames * audio_channels  # get the samples

######################################################################################### 
def frames_(frames):
    '''
    input: frame 
    output : string search

    '''
    value = ""
    collector = ""
    for i in range(frames) :
        data = audio_provided.readframes(1)
        
        collector += str(data[0] % 2) + str(data[2] % 2)

        if (len(collector) == 8) :
            n = chr(int(collector, 2))    
            value += n    

            collector = ""
    return value 
########################################################################################


value = frames_(frames)
print("----Congratulations----")
print(value)

