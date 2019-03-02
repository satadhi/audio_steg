import getopt, math, os, struct, sys, wave
import Zeckendorf

import Convertor
# reading the wav file
sound= wave.open('../audio4.wav','r')
#spf2 = wave.open('opera_new.wav','r')
params = sound.getparams()
num_channels = sound.getnchannels()
sample_width = sound.getsampwidth()
num_frames = sound.getnframes()
num_samples = num_frames * num_channels
# print(num_samples)
framerates = params[2]
if (sample_width == 1):  # samples are unsigned 8-bit integers
    fmt = "{}B".format(num_samples)
    #min_sample = -(1 << 8)
elif (sample_width == 2):  # samples are signed 16-bit integers
    fmt = "{}h".format(num_samples)
else:
    # Python's wave module doesn't support higher sample widths
    raise ValueError("File has an unsupported bit-depth")

raw_data = list(struct.unpack(fmt, sound.readframes(num_frames)))

text = open('hide.txt','r') # reading hide.txt that is to be hidden

input_data_bits = Convertor.text_to_bits(text.read()) #the bits are in str format


# obtaining raw fibonacci bit representation of the given wav file data
fib_raw_data =[]
for i in raw_data:
    fib_raw_data.append(Zeckendorf.printFibRepresntation(i,sample_width))

key = 0 # total no of bits that is stored which is equal to input_data_bits
#the greater of 2 number and using it to run the loop for saving the hidddentext

# embedding the message bit by bit
for i in range(min(len(input_data_bits) ,len(fib_raw_data))):
    fib_raw_data[i][-1] = 0
    fib_raw_data[i][-2] = 0
    fib_raw_data[i][-1] = input_data_bits[i]
    key += 1

# we cannot have have lsb as 1 if 2nd lsb is also 1 according the Zeckendorf
#theorem. so we make all the fib_raw_data[10] = 0 in that way we avoid contradicting
# Zeckendorf constraints


# converting the fib_raw_data back to back_to_decimal
decimal_list =[]
for i in range(len(fib_raw_data)):
    decimal_list.append(Zeckendorf.back_to_decimal(fib_raw_data[i],sample_width))
# # this is for check the difference between the first 15 number of decimal
# for i in range(len(decimal_list)):
#     print('{} -- {}'.format(raw_data[i], decimal_list[i]))

# this create the new stego wav file !
wav_file=wave.open('lemonjuice.wav',"wb")
values = []
wav_file.setparams((num_channels, sample_width, framerates, num_frames, "NONE", "not compressed"))
for s in decimal_list:
    values.append(struct.pack(fmt[-1], s)) # when packing we need B or h not whole of num_samples
wav_file.writeframes(b"".join(values))
wav_file.close()
print('{} is the key for your file '.format(key))
