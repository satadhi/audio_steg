# Python program for Zeckendorf's theorem. It finds
# representation of n as sum of non-neighbouring
# Fibonacci Numbers.

# Returns the greatest Fibonacci Numberr smaller than
# or equal to n.
def construct_fib_series(p):
    arr=[1]
    i=1
    while(arr[-1] <= 255):

        if(i <= p):
            arr.append(1)
        else:
            arr.append(arr[i-1]+arr[i-1-p])
        i+=1
    #removing the extra number from the back
    if ( arr[-1] > 255):
        arr.pop()
    #removing extra ones from the list
    l_set = set(arr)
    arr = list(l_set)
    arr.sort()
    print(arr)
    return arr
def nearestSmallerEqFib(n,p):

    fib_series = construct_fib_series(p)
    # Finds the greatest Fibonacci Number smaller
    # than n.
    if(n <= 0):
        return 0
    for i in range(len(fib_series)-1,-1,-1):
        if ( fib_series[i] <=n ):
            return fib_series[i]


# Prints Fibonacci Representation of n using
# greedy algorithm
def printFibRepresentation(n,p):
    fib_series = construct_fib_series(p)
    Fib_base_binary = [0]*len(fib_series)
    while (n>0):

        # Find the greates Fibonacci Number smaller
        # than or equal to n
        f = nearestSmallerEqFib(n,p);

        # Print the found fibonacci number
        x=fib_series.index(f)
        Fib_base_binary[x] = 1


        # Reduce n
        n = n-f
    Fib_base_binary.reverse()
    # print(Fib_base_binary)
    Fib_base_binary = [str(i) for i in Fib_base_binary]
    #Fib_base_binary.insert(0,'0b')
    return Fib_base_binary

def back_to_decimal(n,p):
    fib_series = construct_fib_series(p)
    sum = 0
    n.reverse()
    for i in range(len(fib_series)):
        if n[i] == '1':
            sum += fib_series[i]
    return sum


# Driver code test above functions
if __name__== "__main__":
    # n = int(input("enter the number "))
    # print(printFibRepresntation(n)
    #print(construct_fib_series(2))
    # for i in range(100)
    #     # print(i)
        # print(printFibRepresentation(i,2))
        #print(back_to_decimal(printFibRepresentation(i,2)))
    construct_fib_series(2)
