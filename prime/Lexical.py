# greedy algorithm
# this is for 8 bit audio file only
def nearestSmallerEqLex(n,limit):

    lex_series = [1,2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]

    if(n <= 0):
        return 0
    for i in range(len(lex_series)-1-limit,-1,-1):
        if ( lex_series[i] <=n ):
            return lex_series[i]

def printLexRepresentation(n):
    lex_series = [1,2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]

    lex_base_binary = [0]*len(lex_series)
    limit=0
    while (n>0):

        # Find the greates Fibonacci Number smaller
        # than or equal to n
        f = nearestSmallerEqLex(n,limit);
        #print(f)
        # Print the found fibonacci number
        x=lex_series.index(f)
        if(lex_base_binary[x] != 1):
            lex_base_binary[x] = 1
            n = n-f
        else:
            limit +=1

        # Reduce n

    lex_base_binary.reverse()
    # print(Fib_base_binary)
    lex_base_binary = [str(i) for i in lex_base_binary]
    #Fib_base_binary.insert(0,'0b')
    return lex_base_binary

def back_to_decimal(n):
    lex_series = [1,2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,]
    sum = 0
    n.reverse()
    for i in range(len(lex_series)):
        if n[i] == '1':
            sum += lex_series[i]
    return sum


# Driver code test above functions
if __name__== "__main__":

    # n = int(input("enter the number "))
    print(printLexRepresentation(255))
    #print(nearestSmallerEqLex(20))
