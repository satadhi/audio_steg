import getopt, math, os, struct, sys, wave
import Zeckendorf
import pickle
import Convertor

#reading the key file
with open ('keyfile', 'rb') as fp:
    key = pickle.load(fp)
r_value = key.pop()
p_value = key.pop()
# file_name = input("enter the wav file name ")
#reading the audio with hidden data
sound= wave.open('lemonjuice.wav','r')
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


# raw data to fib representation of the decimanl number
fib_raw_data =[]
for i in raw_data:
    fib_raw_data.append(Zeckendorf.printFibRepresentation(i,p_value,r_value))

actual_text_bits = []

# for i in range(100):
#     print(fib_raw_data[i])

for i in key:
    actual_text_bits.append(fib_raw_data[i][-1])



actual_text_bits = ''.join(actual_text_bits)


text = Convertor.text_from_bits(actual_text_bits)

print(text)
