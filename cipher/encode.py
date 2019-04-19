import getopt, math, os, struct, sys, wave

#
# This is the inverse of chr() for 8-bit strings and of unichr() for unicode
# objects. If a unicode argument is given and Python was built with UCS2 Unicode,
# then the character’s code point must be in the range [0..65535] inclusive.



text = open('hide.txt','r') # reading hide.txt that is to be hidden
m = int(input("enter the value of m "))
c = int(input("enter the value of c "))
x=0
new_text=[]

with open('hide.txt') as f:
  while True:
    old_letter = f.read(1)
    if not old_letter:
      pass
      break
    y =( m * (x) + c)%65534
    new_letter = chr(ord(old_letter) + y)
    x=x+1
    new_text.append(new_letter)

#the keys are included alone with the encoded.txt
# new_text.append(chr(m))
# new_text.append(chr(c))
#this is the list after we encode the data.
output=''.join(new_text)

with open("encoded.txt", "w") as text_file:
    text_file.write(output)
# print(''.join(new_text))
# for i in new_text:
#     print(i,end='')
