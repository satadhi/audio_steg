import getopt, math, os, struct, sys, wave
import Zeckendorf
import pickle
import Convertor

#taking p-value
p_value = int(input("enter p value of p-series : "))
r_value = int(input("enter r value of r-series : "))

multi_bit = int(input("Enter the no of bits: "))

# reading the wav file
sound= wave.open('../audio4.wav','r')
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
last_loop= len(input_data_bits)%multi_bit #number of bits to be used in last sample
#for _ in range(no_of_loops):


while (j < (len(input_data_bits)-last_loop) and i < len(fib_raw_data)):
    temp = fib_raw_data[i][:]
    #check_bit_for_3_bit = 0
    for x in range(multi_bit):
        if x==2:
            temp[-(6)] = input_data_bits[j+x]
        else:
            temp[-(1+x*3)] = input_data_bits[j+x]

    sum = Zeckendorf.back_to_decimal(temp,p_value,r_value)
    temp2 = Zeckendorf.printFibRepresentation(sum,p_value,r_value)
    temp2.reverse()
    # print(temp)
    # print(temp2)
    if temp == temp2:
        for x in range(multi_bit):
            if x==2:
                temp[-(6)] = input_data_bits[j+x]
            else:
                fib_raw_data[i][-(1+x*3)] = input_data_bits[j+x]
                #print(input_data_bits[j+x],end='')
        j+=multi_bit
        key.append(i)


    i+=1

#same thing for the last loop of the hiding porcess
while i < len(fib_raw_data) and j < len(input_data_bits):
    temp = fib_raw_data[i][:]
    for x in range(last_loop):
        temp[-(1+x*3)] = input_data_bits[j+x]
    sum = Zeckendorf.back_to_decimal(temp,p_value,r_value)
    temp2 = Zeckendorf.printFibRepresentation(sum,p_value,r_value)
    temp2.reverse()
    if temp == temp2:
        for x in range(last_loop):
            fib_raw_data[i][-(1+x*3)] = input_data_bits[j+x]
        j+=multi_bit
        key.append(i)
        break
    i+=1

#the last two bits are extra infromation
key.append(multi_bit)#second last
key.append(last_loop)#number of bits to be used in last sample
key.append(r_value)
key.append(p_value)
#saving the key file as a binay file
with open('keyfile', 'wb') as fp:
    pickle.dump(key, fp)
    # for i in range(50):
    #     print(fib_raw_data[i])
# converting the fib_raw_data back to back_to_decimal
decimal_list =[]
for i in range(len(fib_raw_data)):
    decimal_list.append(Zeckendorf.back_to_decimal(fib_raw_data[i],p_value,r_value))
# # this is for check the difference between the first 15 number of decimal
# for i in range(len(decimal_list)):
#     print('{} -- {}'.format(raw_data[i], decimal_list[i]))

#----------> In this section we are calculation snr
sigma_x = 0
sigma_y = 0

for i in range(key[-5]):
     sigma_x = sigma_x + raw_data[i]


for i in range(key[-5]):
     sigma_y +=decimal_list[i]

print("sigma_x {}  sigma_y {}".format(sigma_x,sigma_y))
snr = 10*math.log10(abs(sigma_x**2/(sigma_x**2 - sigma_y**2)))
print("the snr value is {}".format(snr))

#--------------> End of the section for calculating snr

# this create the new stego wav file !
wav_file=wave.open('lemonjuice.wav',"wb")
values = []
wav_file.setparams((num_channels, sample_width, framerates, num_frames, "NONE", "not compressed"))
for s in decimal_list:
    values.append(struct.pack(fmt[-1], s)) # when packing we need B or h not whole of num_samples
wav_file.writeframes(b"".join(values))
wav_file.close()
print("total sample-> {} and total sample used -> {}".format(key[-5]+3,len(key)-2))

#print("successful")
