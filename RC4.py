
import time

mod = 256
ktoc = 0.0
ktic = 0.0
def KSA(key):
    #
    # Keylenght is 1 <= length <= 256 between 5 and 16 bytes or 40- 128 bits
    # first S is initially to the identity permutation
    # S is array and S_i belongs to the 256 iterations 
    # *#
    key_lenght = len(key)
    S = list(range(mod))
    j = 0
    for i in range(mod):
        if key_lenght > 0:
            j = (j + S[i] + key [i% key_lenght]) % mod
            S[i], S[j] = S[j], S[i]
        else:
            j = (j + S[i] + key [i% key_lenght]) % mod
            S[i], S[j] = S[j], S[i]
    return S

#Pseudo-random generation algorithm
def PRGA(S, n):
    # 
    # Incrementing by I
    # look up at the i element of S, S[i] and add to j
    # We have an exchange the value of S[i] S[j]
    # #
    i = 0
    j = 0
    key = []
    while n > 0:
        n = n -1
        i = (i + 1) % mod
        j = (j + S[i]) % mod
        S[i] , S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % mod]
        key.append(K)
    
    return key

def prepare(S):
    return [ord(a) for a in S]

def encrypt(key, pT):
    print("*****************************************************************\n")
    print("Input:\n")
    print("Key: \n", key)
    print("Plain Text: \n", pT)
    global ktoc, ktic
    ktoc = time.perf_counter()
    key = prepare(key)
    pT = prepare(pT)
    S = KSA(key)
    keyStream = PRGA(S, len(pT))
    ktic = time.perf_counter()
    
    print("*****************************************************************\n")
    print("Prepared Variables:\n")
    print("Key: \n", key)
    print("S: \n", S)
    print("Prepared KeyStream: \n", keyStream)
    print("Prepared Plain Text: \n", pT)
    print("*****************************************************************\n")
    print("Completed Cipher:\n")
    #This is a list of Integers
    cipherI = []
    #This is a list of Hex
    cipherH = []
    #For every element in list in keyStream and pT
    #XOR to create cipher
    for i in range(len(pT)):
        c = keyStream[i] ^ pT[i]
        #Append the newly created XOR digit to list
        cipherI.append(c)
        #Append the newly created XOR digit and convert to hex to list
        cipherH.append(hex(c))
    print("Cipher: \n", cipherH)
    # This print statement will print all the char UNI 8
    print("Char in Cipher\n", [chr(c) for c in cipherI])
    print("*****************************************************************\n")

    return cipherH

def decrypt(key, cipher):
    print("*****************************************************************\n")
    print("Prepared Variables:\n")
    cipherI = []
    key = prepare(key)

    # Converting list of hexs back to a list of integers
    for i in range(len(cipher)):
        cipherI.append(int(cipher[i],base=16))
    print("Hex to Decimal Conversion",cipherI)
    print("*****************************************************************\n")
    print("Decryption:\n")
    S = KSA(key)
    keyStream = PRGA(S, len(cipher))
    #List of int values for the plaintext
    plainTextDecimal = []
    #String that will hold the screat message
    plainText = ""
    for i in range(len(cipherI)):
        c = cipherI[i] ^ keyStream[i]
        plainTextDecimal.append(c)
        plainText += chr(c)
    print("Decimal in plaintex: ",plainTextDecimal)
    print("Plaintex: ",plainText)

    return plainText
    
def main():

    ftoc = time.perf_counter()
    key = 'Need more Keys'
    plaintext = "Growing up we had the best dog ever. He was half English Bulldog and just the funniest guy with amazing comedic timing. He didn't look like an English bully at all though. He looked like a pitbull, at the height of pitbull fear in the 90's. Like many Bulldogs, he was fascinated by wheels. He loved to attack skateboard wheels, big wheels, etc. One of his favorite things was when the UPS truck would stop on our street. It got to the point that he would hear it coming and wait at the window. He got out once and chased one, but we caught him before he caught the truck. For 10 years, the UPS truck was his love and his nemesis. Anyway... We were on a family vacation and had to cut it short because he got very sick while at the kennel. We took him to his vet and learned that he had a very aggressive form of lung cancer (he had no symptoms until he was at the kennel. Had just been to the vet a few months prior). We had to euthanize him that day. He was that bad off. It was truly one of the most unexpected depressing events of my life. I took him outside for his final walk. Right across from the vet's office was a Wendy's (fast food restaurant). As I was walking him, and crying over how frail and sick he seemed, a UPS truck pulled right up to us. The driver jumped out to grab his lunch. Well...you know how they leave the doors open on those trucks? He perked up. He looked at the truck. He looked at me. I said 'Ok, go for it' and as weak as he was, he pulled me over to the truck. Hopped up into the passenger side and checked the whole thing out, tail wagging. Got out and got inspect all 4 tires. For his last hurrah, my sweet, goofy boy finally caught his UPS truck."
    etoc = time.perf_counter()
    cipher = encrypt(key, plaintext)
    etic = time.perf_counter()
    print(cipher)
    ctoc = time.perf_counter()
    decrypt(key,cipher)
    ctic = time.perf_counter()
    ftic = time.perf_counter()

    print("*****************************************************")
    print("Total Time to Execute Program: ", ftic-ftoc, "\n Time to Encrypt: ", etic-etoc,
    "\n Time to Decrypt: ", ctic-ctoc, "\n Key set up time: ", ktic-ktoc, "\n")
    print("*****************************************************")




if __name__ == "__main__":
    main()