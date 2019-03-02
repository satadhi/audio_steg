import getopt, math, os, struct, sys, wave
import Lexical
import pickle
import Convertor
# reading the wav file
sound= wave.open('../audio1.wav','r')
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


# obtaining raw lexonacci bit representation of the given wav file data
lex_raw_data =[]
for i in raw_data:
    lex_raw_data.append(Lexical.printLexRepresentation(i))

# embedding the message bit by bit
key = [] # frams that are effected, that is stored in hidden audio files
j=0 # this is used to iterate over the input data values
i=0 # this is iterating over the audio frames.
while (j < len(input_data_bits) and (i < len(lex_raw_data))):
    temp = lex_raw_data[i][:]
    temp[-1] = input_data_bits[j]
    sum = Lexical.back_to_decimal(temp)
    temp2 = Lexical.printLexRepresentation(sum)
    temp2.reverse()
    if temp == temp2:
        lex_raw_data[i][-1] = input_data_bits[j]
        j+=1
        key.append(i)
        print(i)
    i+=1
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

# this create the new stego wav file !
wav_file=wave.open('lemonjuice.wav',"wb")
values = []
wav_file.setparams((num_channels, sample_width, framerates, num_frames, "NONE", "not compressed"))
for s in decimal_list:
    values.append(struct.pack(fmt[-1], s)) # when packing we need B or h not whole of num_samples
wav_file.writeframes(b"".join(values))
wav_file.close()
print("successful")
