import random
import time

#A typical size for n is 1024 bits, or 309 decimal digits
# Bits represents the highest bit
bits = 8

def bitNumberGenerator(bits):
    # Bits > 2
    return random.randrange(2**(bits - 1) + 1, 2**bits - 1)

def dprime(num):
    if num > 1:
        for i in range (2, int(num/2)+1):
            if (num % i) == 0:
                return 0
            else:
                return 1

def gcd(x, y):
# Create the gcd of two positive integers.
    if(y == 0):
        return x
    return gcd(y, x%y)

def is_coprime(x, y):
    return gcd(x,y) == 1

# Need to check that p and q are prime
def prime_check(a):
    if(a==2):
        return True
    elif((a<2) or ((a%2)==0)):
        return False
    elif(a>2):
        for i in range(2,a):
            if not(a%i):
                return False
    return True

#Used to find the value of d
def modInverse(a, b):
	
	for i in range(1, b):
		if (((a%b) * (i%b)) % b == 1):
			return i
	return -1


def RSA(p, q):
    n = p*q
    phi = (p - 1)*(q - 1)
    e = 0

    #Printing the values of variables
    print("*****************************************************")
    print("N value: ", n ,"\nPHI value: ",phi)
    print("*****************************************************")

    # Choose an int e such 1 < e < phi, simple terms gcd(e, phi) = 1
    for i in range(1,10000):

        if(gcd(i,phi) == 1):
            e=i
    
    print("e value: ", e)

    # e^-1 (mod phi )
    d = modInverse(e, phi)
    print("*****************************************************")

    print("d value: ", d)

    public = (e, n)
    private = (d, n)
    return public, private

def encrypt(publickey, message):

    e, n = publickey
    # M^e( mod n)
    Cipher = []
    m = 0
    # Itterating through messagge
    for i in message:
        #Upper Case Letters
        if(i.isupper()):
            #Unicode Number Conversion
            m = ord(i) 
            # charactor cipher
            c = (m**e) % n
            Cipher.append(c)
            print("Message char:", i, "Cipher #: ",c)
        #Lower Case letters 
        elif(i.islower()):
            #Unicode Numver Conversion
            m = ord(i) 
            # charactor cipher
            c = (m**e) % n
            Cipher.append(c)
            print("Message char:", i, "Cipher #: ",c)
        elif(i.isspace()):
            #Coded the value fo space due to problems with consistant unicode conversion
            #Space is sean as null or empty space thus unable to give it a value
            spc = 400
            c = (spc**e) % n
            Cipher.append(c)
            print("Message char:", "space", "Cipher #: ", c) 
    return Cipher

def decrypt(privateKey, cipher):
    
    d, n = privateKey
    txt = cipher.split(",")
    message = ''
    m = 0
    for i in txt:
        m = (int(i)**d) % n
        if( m == 400):
            message += ' '
            print("Cipher Value:", i, "Message char: ","space") 
        else:
            m = (int(i)**d) % n
            c = chr(m)
            message +=c
            print("Cipher Value:", i, "Message char: ", c) 
    return message


print("RSA ENCRYPTION/DECRYPTION")
print("*****************************************************")

#Not Part part of RSA Algorithm ---> Need to quickly use cipher and turn it into a message
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    length = len(s)
    position = 0
    # traverse in the string  
    for ele in s:
        if(position != length):
            str1 += str(ele)
            if(position != length-1):
                str1 += ","
        position += 1
    
    # return string  
    print(str1)
    return str1 

# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67, 
                     71, 73, 79, 83, 89, 97, 101, 103, 
                     107, 109, 113, 127, 131, 137, 139, 
                     149, 151, 157, 163, 167, 173, 179, 
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]
  
  
def getLowLevelPrime(n):
    #Generate a prime candidate divisible 
    while True:
        # Obtain a random number
        pc = bitNumberGenerator(n)
         # Test divisibility by pre-generated 
         # primes
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else: return pc
  
def isMillerRabin(mrc):
    DivisionByTwo = 0
    ec = mrc-1
    while ec % 2 == 0:
        ec >>= 1
        DivisionByTwo += 1
    assert(2**DivisionByTwo * ec == mrc-1)
    #If this test false than the number is not prime
    #If a number is a composite we know its not prime
    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(DivisionByTwo):
            if pow(round_tester, 2**i * ec, mrc) == mrc-1:
                return False
        return True
  
    # Set number of trials here
    numberOfRabinTrials = 20 
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True

def probPrime():
    while True:
        toc = time.perf_counter()
        prime_candidate = getLowLevelPrime(bits)
        if not isMillerRabin(prime_candidate):
            continue
        else:
            tic = time.perf_counter()
            print("Execution Time For Finding Prime: ", tic - toc, " sec")
            return prime_candidate

def main():
    ftoc = time.perf_counter()
    ktoc = time.perf_counter()
    #Searching for prime by probability
    p = probPrime()
    q = probPrime()

    print("P value: ",p,"  Q value: ",q)
    public, private = RSA(p, q)
    ktic = time.perf_counter()
    print("\n Time to generate key: ", ktic-ktoc, "\n")
    print("*****************************************************")
    print("Public key: ",public)
    print("Private key: ",private)
    print("*****************************************************")
    print("Message to be encrypted: ")
    message = "Growing up we had the best dog ever. He was half English Bulldog and just the funniest guy with amazing comedic timing. He didn't look like an English bully at all though. He looked like a pitbull, at the height of pitbull fear in the 90's. Like many Bulldogs, he was fascinated by wheels. He loved to attack skateboard wheels, big wheels, etc. One of his favorite things was when the UPS truck would stop on our street. It got to the point that he would hear it coming and wait at the window. He got out once and chased one, but we caught him before he caught the truck. For 10 years, the UPS truck was his love and his nemesis. Anyway... We were on a family vacation and had to cut it short because he got very sick while at the kennel. We took him to his vet and learned that he had a very aggressive form of lung cancer (he had no symptoms until he was at the kennel. Had just been to the vet a few months prior). We had to euthanize him that day. He was that bad off. It was truly one of the most unexpected depressing events of my life. I took him outside for his final walk. Right across from the vet's office was a Wendy's (fast food restaurant). As I was walking him, and crying over how frail and sick he seemed, a UPS truck pulled right up to us. The driver jumped out to grab his lunch. Well...you know how they leave the doors open on those trucks? He perked up. He looked at the truck. He looked at me. I said 'Ok, go for it' and as weak as he was, he pulled me over to the truck. Hopped up into the passenger side and checked the whole thing out, tail wagging. Got out and got inspect all 4 tires. For his last hurrah, my sweet, goofy boy finally caught his UPS truck."
    print(message)
    print("*****************************************************")
    print("Cipher: ")
    etoc = time.perf_counter()
    cipher = encrypt(public, message)
    etic = time.perf_counter()
    print(cipher)
    print("*****************************************************")
    print("Message: ")
    cipher_T = listToString(cipher)
    ctoc = time.perf_counter()
    message = decrypt(private, cipher_T)
    ctic = time.perf_counter()
    print(message)
    print("*****************************************************")
    ftic = time.perf_counter()
    print("Total Time to Execute Program: ", ftic-ftoc, "\n Time to Encrypt: ", etic-etoc,
    "\n Time to Decrypt: ", ctic-ctoc, "\n Time to generate key: ", ktic-ktoc, "\n")
    print("*****************************************************")

if __name__ == "__main__":
    main()
