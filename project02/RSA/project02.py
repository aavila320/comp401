# Imports
# Note: itertools -> combinations will help produce
# l-length tuples in sorted order with no repeated elements
# Copy will be used to create "shallow" copies of elements which
# uses the contents of the origional object but creates a reference to
# create a new one.
# Time is used as an import to create a short pause, as if the computer is 
# "slowly" encrypting and decrypting 
import random
from itertools import combinations
import math
import copy
import time
outputFileName = "driver.py"
outputFile = open( outputFileName, 'w' )

# This function will return the GCD of a and b
def Euclidean(a, b):
    a = abs(a)
    b = abs(b)
    if a < b:
        a, b = b, a
    while b != 0:
        a, b = b, a % b
    return a

# This function will return True if all of the values in our list (L)
# are composite primes. If they are not, false is returned.
def compositePrime(l):
    for i, j in combinations(l, 2):
        if Euclidean(i, j) != 1:
            return False
    return True

# This function will return a tuple of x, y and z values.
# x is the GCD of a and b, and x = y * a + z * b
def extendedEuclidean(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extendedEuclidean(b % a, a)
        return g, x - (b // a) * y, y

# Returns the multiplicative inverse of a mod m
# This number will be a positive value between 0 and m-1
# a and m will be composite primes to one another
def modInverse(a, m):
    # notice that a and m need to co-prime to each other.
    if compositePrime([a, m]):
        linearCombination = extendedEuclidean(a, m)
        return linearCombination[1] % m
    else:
        return 0

# This function will return the integer tuple (s, d)
# such that m (a positive integer) is represented as m = (2 ** n) - 1.
def extractTwos(m):
    assert m >= 0   # assert is used to test the condition
    i = 0
    while m & (2 ** i) == 0:
        i += 1
    return i, m >> i

# This function will convert the positive integer x into a 
# list of in reverse order as base two.
def convertTwo(x):
    assert x >= 0
    bitInverse = []
    while x != 0:
        bitInverse.append(x & 1)
        x >>= 1
    return bitInverse

# This function will return a ** d (mod n)
# which will mod our exponent
def modExponent(a, d, n):
    assert d >= 0
    assert n >= 0
    base2D = convertTwo(d)
    base2DLength = len(base2D)
    modArray = []
    result = 1
    for i in range(1, base2DLength + 1):
        if i == 1:
            modArray.append(a % n)
        else:
            modArray.append((modArray[i - 2] ** 2) % n)
    for i in range(0, base2DLength):
        if base2D[i] == 1:
            result *= base2D[i] * modArray[i]
    return result % n

# This is a test function - if True is returned, our number is prime
# if False is returned, we know the number is composite.
# An error will be raised if (n,k) are not positive integers as well 
# as if n is not 1.
def MillerRabinTest(n, k):
    assert n >= 1     # verify n is bigger than 1
    assert k > 0      # veify k is a positive integer
   
    if n == 2:
        return True 

    if n % 2 == 0:
        return False  # must return False for all numbers greater than 2
   
    extract2 = extractTwos(n - 1)
    s = extract2[0]
    d = extract2[1]
    assert 2 ** s * d == n - 1

    # This function will determine whether the "identity" of n will be uncovered
    def tryComposite(a):
        x = modExponent(a, d, n)
        if x == 1 or x == n - 1:
            return None
        else:
            for j in range(1, s):
                x = modExponent(x, 2, n)
                if x == 1:
                    return False
                elif x == n - 1:
                    return None
            return False

    for i in range(0, k):
        a = random.randint(2, n - 2)
        if tryComposite(a) == False:
            return False
    return True


# This function will return a list (k + 1)
# The list is prime if list[i] == 1
# The list is a composite if list[i] == 0
# The list is not defined if list[i] == -1
def primeTime(k):

    # This function will return True is n is absolutely prime
    # False will be returned otherwise
    def isPrime(n):
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    result = [-1] * (k + 1)
    for i in range(2, int(k + 1)):
        if isPrime(i):
            result[i] = 1
        else:
            result[i] = 0
    return result

# This function will return a pseudo-prime number or a number that shares
# common properties with a prime number. This pseudo-prime number will be
# between a and b and can even be possibly larger than b.
# A ValueError will be raised if a pseudo-prime number cannot be found 
# after 10 * ln(x) + 3 tries
def findPrime(a, b, k):
    x = random.randint(a, b)
    for i in range(0, int(10 * math.log(x) + 3)):
        if MillerRabinTest(x, k):
            return x
        else:
            x += 1
    raise ValueError

# This function will try and find two pseudo-prime numbers roughly
# between a and b. The public and private keys for the RSA Encryption
# are also created. Similarly to the last function, a ValueError will
# be raised if a pseudo-prime is not found.
def generateKey(a, b, k):
    try:
        p = findPrime(a, b, k)
        while True:
            q = findPrime(a, b, k)
            if q != p:
                break
    except:
        raise ValueError
    n = p * q
    m = (p - 1) * (q - 1)
    while True:
        e = random.randint(1, m)
        if compositePrime([e, m]):
            break
    d = modInverse(e, m)
    return (n, e, d)

# This function will convert our string to a list of integers.
# Please note these integers are based on ASCII values.
def stringInt(strn):
    return [ord(chars) for chars in strn]

# This function will convert our integers to a string
def intString(l):
    return ''.join(map(chr, l))

# This function will combine our list of integers to a block size (n)
# using the base of 256. If len(L) mod n != 0, random junk will be used
# to fill L.
def numBlock(l, n):
    returnList = []
    toProcess = copy.copy(l)
    if len(toProcess) % n != 0:
        for i in range(0, n - len(toProcess) % n):
            toProcess.append(random.randint(32, 126))
    for i in range(0, len(toProcess), n):
        block = 0
        for j in range(0, n):
            block += toProcess[i + j] << (8 * (n - j - 1))
        returnList.append(block)
    return returnList


# This function is the opposite of our numBlock and will change
# our block size n to a list
def blockNum(blocks, n):
    toProcess = copy.copy(blocks)
    returnList = []
    for numBlock in toProcess:
        inner = []
        for i in range(0, n):
            inner.append(numBlock % 256)
            numBlock >>= 8
        inner.reverse()
        returnList.extend(inner)
    return returnList

# This function will encrypt our message
def encrypt(message, modN, e, blockSize):
    numList = stringInt(message)
    numBlocks = numBlock(numList, blockSize)
    return [modExponent(blocks, e, modN) for blocks in numBlocks]


# This function will decrypt our message
def decrypt(secret, modN, d, blockSize):
    numBlocks = [modExponent(blocks, d, modN) for blocks in secret]
    numList = blockNum(numBlocks, blockSize)
    return intString(numList)


if __name__ == '__main__':
    (n, e, d) = generateKey(10 ** 100, 10 ** 101, 50)
    print ('n = {0}'.format(n)) # n is what we use to mod
    print ('e = {0}'.format(e)) # (n,e) is the public key
    print ('d = {0}'.format(d)) # (n,d) is the private key
    outputFile.write('n = {0}'.format(n))
    outputFile.write('e = {0}'.format(e))
    outputFile.write('d = {0}'.format(d))    
    
    # secretMessage = raw_input("Please enter a message to encrytpt: ")
    # These can be uncommented if user input is wanted    
    # Please note, because of the block size, some input will result in extra
    # characters after our deciphered text is output.
    secretMessage = """
    The quick brown fox jumped over the lazy dog in an attempt to catch a
    squirrel.  He was too slow, so the squirrel was safe and very happy!!!
"""
    cipherText = encrypt(secretMessage, n, e, 15)
    print ("\nPrinting cipher text..... \n")
    outputFile.write("\nPrinting cipher text..... \n")
    time.sleep(2) # added a pause to make it appear slower, like it was "thinking"
    
    print(cipherText)
    outputFile.write(str(cipherText))
    decipherText = decrypt(cipherText, n, d, 15)
    print ("\nPrinting deciphered text...\n")
    outputFile.write("\nPrinting deciphered text...\n")
    
    time.sleep(2) # added a pause ro make it appear slower, like it was "thinking"
    print(decipherText)
    outputFile.write(str(decipherText))