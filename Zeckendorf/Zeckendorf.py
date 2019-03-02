# Python program for Zeckendorf's theorem. It finds
# representation of n as sum of non-neighbouring
# Fibonacci Numbers.
# 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368
# Returns the greatest Fibonacci Numberr smaller than
# or equal to n.
def nearestSmallerEqFib(n):

    # Corner cases
    if (n == 0 or n == 1):
        return n

    # Finds the greatest Fibonacci Number smaller
    # than n.
    f1,f2,f3 = 0,1,1
    while (f3 <= n):
        f1 = f2;
        f2 = f3;
        f3 = f1+f2;
    return f2;


# Prints Fibonacci Representation of n using
# greedy algorithm
def printFibRepresntation(n,sample_width):
    if sample_width == 1:
        fib_series = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
        Fib_base_binary = [0]*12
    if sample_width == 2:
        fib_series = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368]
        Fib_base_binary = [0]*23

    while (n>0):

        # Find the greates Fibonacci Number smaller
        # than or equal to n
        f = nearestSmallerEqFib(n);

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

def back_to_decimal(n,sample_width):
    if sample_width == 1:
        fib_series = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
        Fib_base_binary = [0]*12
    if sample_width == 2:
        fib_series = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368]
        Fib_base_binary = [0]*23
    sum = 0
    n.reverse()
    for i in range(12):
        if n[i] == '1':
            sum += fib_series[i]
    return sum


# Driver code test above functions
if __name__== "__main__":
     n = int(input("enter the number "))

    # temp =   ['0', '1', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0']
    # temp1 =  ['0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '1', '1']
    # x = back_to_decimal(temp1)
    # x1 = back_to_decimal(temp)
    # print(x)
    # print(x1)
