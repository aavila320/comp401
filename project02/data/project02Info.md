#RSA Encryption Algorithm

The RSA Encryption Algorithm was created by Rivest, Shamir and Adleman and is a crypto system used for public-key encryption. This idea was originally considered in 1977 by Ron Rivest, Adi Shamir and Leonard Adleman of MIT. The RSA is known as asymmetric and public-key cryptography where there is one public and one private key are linked together mathematically. Anyone can share the public key but the private key must remain unknown and secret. With the public and private keys, a message can be encrypted. The key not used to encrypt can then be used to decrypt the message. The RSA uses a "Miller-Rabin" test to determine if the numbers used in our RSA are prime or composite.
	The RSA has become one of the most widely used algorithms because of its difficulty in cracking. The RSA uses the factoring of two large integers of which are the product of two large prime numbers. These numbers are then multiplied together but the process of determining the original prime numbers is very time consuming and could take today's super computers an infeasible amount of time. Because the RSA relies on computational difficulty, it is pretty secure however all encryption algorithms are vulnerable to attacks.
	
#Functions
Euclidean - This function will return the GCD of a and b
compositePrime - returns True if the values in our list are composite primes.
extendedEuclidean - returns a tuple of x,y and z values
modInverse - returns multiplicative inverse  
extractTwos - returns integer tuple which is represented as m = (2 ** n) - 1
convertTwo - convert positive integer to a base two list in reverse order
modExponent - returns a**d (mod n) -> modding exponent
MillerRabinTest - testing if our number is prime or not
tryComposite - determines what n is
primeTime - returns list k+1
 isPrime - returns True if n is absolutely prime
findPrime - returns a number that has common properties with our prime number
generateKey - creates public and private keys
stringInt - converts string to list of integers
intString - converts integers to a string
numBlock - combine our list to our block size (n)
blockNum - changes block size n to a list
encrypt - encrypts message
decrypt - decrypts message
main - driver of program