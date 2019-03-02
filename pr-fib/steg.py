import getopt, math, os, struct, sys, wave
import Zeckendorf
import pickle
import Convertor

#taking p-value
p_value = int(input("enter p value of p-series : "))
r_value = int(input("enter r value of r-series : "))
# reading the wav file
sound= wave.open('../audio2.wav','r')
#spf2 = wave.open('opera_new.wav','r')
params = sound.getparams()
num_channels = sound.getnchannels()
sample_width = sound.getsampwidth()
num_frames = sound.getnframes()
num_samples = num_frames * num_channels

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
    fib_raw_data.append(Zeckendorf.printFibRepresentation(i,p_value,r_value))

key = 0 # total no of bits that is stored which is equal to input_data_bits

# embedding the message bit by bit
# embedding the message bit by bit
key = [] # frams that are effected, that is stored in hidden audio files
j=0 # this is used to iterate over the input data values
i=0 # this is iterating over the audio frames.
while (j < len(input_data_bits)) and (i < len(fib_raw_data)):
    temp = fib_raw_data[i][:]
    temp[-1] = input_data_bits[j]
    sum = Zeckendorf.back_to_decimal(temp,p_value,r_value)
    temp2 = Zeckendorf.printFibRepresentation(sum,p_value,r_value)
    temp2.reverse()
    if temp == temp2:
        fib_raw_data[i][-1] = input_data_bits[j]
        j+=1
        key.append(i)
    i+=1
#saving the p_value at the end of the key files
key.append(p_value)
key.append(r_value)
#saving the key file as a binay file
with open('keyfile', 'wb') as fp:
    pickle.dump(key, fp)

# converting the fib_raw_data back to back_to_decimal
decimal_list =[]
for i in range(len(fib_raw_data)):
    decimal_list.append(Zeckendorf.back_to_decimal(fib_raw_data[i],p_value,r_value))
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
# adding value of p at the end of the key
print('success')
print(j)
