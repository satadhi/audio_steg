import getopt, math, os, struct, sys, wave

m = int(input("enter the value of m "))
c = int(input("enter the value of c "))
x=0
y=0
new_text=[]

with open('encoded.txt') as f:

    while True:
        old_letter = f.read(1)
        if not old_letter:
            pass
            break
        y = m * (x%255) + c
        new_letter = chr(ord(old_letter) - y)
        x=x+1
        new_text.append(new_letter)

#this is the file after we decode the data.
output=''.join(new_text)

# with open("encoded.txt", "w") as text_file:
#     text_file.write(output)
# print(''.join(new_text))
for i in new_text:
    print(i,end='')
