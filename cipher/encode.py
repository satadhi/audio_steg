import getopt, math, os, struct, sys, wave


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
    y = m * (x%255) + c
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
