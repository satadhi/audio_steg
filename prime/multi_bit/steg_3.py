import getopt, math, os, struct, sys, wave
import Lexical
import pickle
import Convertor

# reading the wav file
sound= wave.open('../../audio4.wav','r')
#spf2 = wave.open('opera_new.wav','r')
params = sound.getparams()
num_channels = sound.getnchannels()
sample_width = sound.getsampwidth()
num_frames = sound.getnframes()
num_samples = num_frames * num_channels

multi_bit = int(input("Enter the no of bits: "))

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


# obtaining raw lexonacci bit representation of the given wav file data
lex_raw_data =[]
for i in raw_data:
    lex_raw_data.append(Lexical.printLexRepresentation(i))

# embedding the message bit by bit
key = [] # frams that are effected, that is stored in hidden audio files
j=0 # this is used to iterate over the input data values
i=0 # this is iterating over the audio frames.
last_loop= len(input_data_bits)%multi_bit #number of bits to be used in last sample
#for _ in range(no_of_loops):


while (j < (len(input_data_bits)-last_loop) and i < len(lex_raw_data)):
    temp = lex_raw_data[i][:]
    #check_bit_for_3_bit = 0
    for x in range(multi_bit):
        if x == 2 :
            # for r in range(6):
            #         check_bit_for_3_bit = temp[-(4+r)]
            # if check_bit_for_3_bit == 0:
            temp[-(10)] = input_data_bits[j+x]
            #print(x)
        else:
            temp[-(1+x*2)] = input_data_bits[j+x]
    sum = Lexical.back_to_decimal(temp)
    temp2 = Lexical.printLexRepresentation(sum)
    temp2.reverse()
    # print(temp)
    # print(temp2)
    if temp == temp2:
        for x in range(multi_bit):
            if x == 2 :
                lex_raw_data[i][-(10)] = input_data_bits[j+x]
                #print(input_data_bits[j+x],end='')
            else:
                lex_raw_data[i][-(1+x*2)] = input_data_bits[j+x]
                #print(input_data_bits[j+x],end='')
        j+=multi_bit
        key.append(i)


    i+=1

#same thing for the last loop of the hiding porcess
while i < len(lex_raw_data) and j < len(input_data_bits):
    temp = lex_raw_data[i][:]
    for x in range(last_loop):
        temp[-(1+x*2)] = input_data_bits[j+x]
    sum = Lexical.back_to_decimal(temp)
    temp2 = Lexical.printLexRepresentation(sum)
    temp2.reverse()
    if temp == temp2:
        for x in range(last_loop):
            lex_raw_data[i][-(1+x*2)] = input_data_bits[j+x]
        j+=multi_bit
        key.append(i)
        break
    i+=1

#the last two bits are extra infromation
key.append(multi_bit)#second last
key.append(last_loop)#number of bits to be used in last sample
#saving the key file as a binay file
with open('keyfile', 'wb') as fp:
    pickle.dump(key, fp)
    # for i in range(50):
    #     print(lex_raw_data[i])
# converting the lex_raw_data back to back_to_decimal
decimal_list =[]
for i in range(len(lex_raw_data)):
    decimal_list.append(Lexical.back_to_decimal(lex_raw_data[i]))
# # this is for check the difference between the first 15 number of decimal
# for i in range(len(decimal_list)):
#     print('{} -- {}'.format(raw_data[i], decimal_list[i]))

#----------> In this section we are calculation snr
sigma_x = 0
sigma_y = 0
for i in range(key[-3]):
     sigma_x = sigma_x + raw_data[i]


for i in range(key[-3]):
     sigma_y +=decimal_list[i]

print("sigma_x {}  sigma_y {}".format(sigma_x,sigma_y))
snr = 10*math.log10(abs(sigma_x**2/(sigma_x**2 - sigma_y**2)))
print("the snr value is {}".format(snr))

#--------------> End of the section for calculating snr


#----------> In this section we are calculation spcc

sigma_x = 0
sigma_y = 0
sigma_x_avg = 0
sigma_y_avg = 0


#this is calculating average of cover signal
for i in range(key[-3]):
     sigma_x_avg = sigma_x_avg + raw_data[i]

sigma_x_avg = sigma_x_avg/(len(key)-2)


#this is calculating average of stego signal
for i in range(key[-3]):
     sigma_y_avg = sigma_y_avg + decimal_list[i]

sigma_y_avg = sigma_y_avg/(len(key)-2)


#calculating sigma of x - x_avg
temp_x = 0
for i in range(key[-3]):
    temp_x += (raw_data[i]-sigma_x_avg)*(raw_data[i]-sigma_x_avg)
temp_x = math.sqrt(temp_x)


#calculating sigma of y - y_avg
temp_y = 0
for i in range(key[-3]):
    temp_y += (decimal_list[i]-sigma_y_avg)*(decimal_list[i]-sigma_y_avg)
temp_y = math.sqrt(temp_y)

#calculating the acutal spcc
spcc = 0

for i in range(key[-3]):
    spcc += ((raw_data[i]-sigma_x_avg) * (decimal_list[i]-sigma_y_avg))/(temp_x * temp_y)

spcc = spcc*spcc

print("the value of spcc is -> {}".format(spcc))

#--------------> End of the section for calculating spcc

# this create the new stego wav file !
wav_file=wave.open('lemonjuice.wav',"wb")
values = []
wav_file.setparams((num_channels, sample_width, framerates, num_frames, "NONE", "not compressed"))
for s in decimal_list:
    values.append(struct.pack(fmt[-1], s)) # when packing we need B or h not whole of num_samples
wav_file.writeframes(b"".join(values))
wav_file.close()
print("total sample-> {} and total sample used -> {}".format(key[-3],len(key)))

#print("successful")
