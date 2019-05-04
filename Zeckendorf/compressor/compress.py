import getopt, math, os, struct, sys, wave
import pickle
import array as arr

with open ('../keyfile', 'rb') as fp:
    key = pickle.load(fp)

new_key = []
for i  in key:
    print(i)

for i in range(1,len(key)):
    new_key.append(key[i]-key[i-1])

 # for i  in new_key:
 #     print(i)
a = arr.array('i', new_key)

with open('../compressed_keyfile', 'wb') as fp:
    pickle.dump(new_key, fp)
