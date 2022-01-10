"""
Names / IDs:

Abdallah Adham      20180161
Hashem Khaled       20180326
Ahmed Emad          20180017

"""

import random

# Fermat Test for Prime Numbers
def Fermat(n):

    if n == 2:
        return True
    if not n & 1:
        return False

    return SquareAndMultiply(2, n-1, n) == 1

# Square and Multiply
def SquareAndMultiply(b, p, mod):
    exp = bin(p)

    print(exp)

    value = b #base

    for t in range(3, len(exp)):

        value = (value * value) % mod

        if(exp[t]=='1'):

            value = value*b % mod

    return value


# Defining if n is a Prime number or not
def isPrime(n):

    if not Fermat(n):

        return False

    else:

        return True


# Return random large prime number of keysize bits in size
def generateLargePrime(keysize):

    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isPrime(num)):
            return num


def generateKeys(p, q, keysize=1024):
    e = d = n = 0

    n = p * q   # RSA Modulus

    Phi = (p - 1) * (q - 1)    # Totient

    print("--------------------------------------------")
    print("p = ", p)
    print("q = ", q)
    print("n = ", n)
    print("Phi = ", Phi)
    print("--------------------------------------------")

    # choose e
    # e is coprime with phiN & 1 < e <= phiN
    while True:
        e = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isCoPrime(e, Phi)):
            break

    # choose d
    # d is mod inv of e with respect to phiN, e * d (mod phiN) = 1
    d = ModInv(e, Phi)

    return e, d, n


# Euclidean Algorithm ti find gcd between p and q
def gcd(p, q):

    while q:
        p, q = q, p % q
    return p


# return True if gcd(p, q) is 1
def isCoPrime(p, q):
    return gcd(p, q) == 1


# Extended Greatest Common Dominator
def egcd(a, b):
    s = 0; priv_s = 1
    t = 1; priv_t = 0
    r = b; priv_r = a

    while r != 0:
        quotient = priv_r // r
        priv_r, r = r, priv_r - quotient * r
        priv_s, s = s, priv_s - quotient * s
        priv_t, t = t, priv_t - quotient * t

    return priv_r, priv_s, priv_t


# Modular Inverse
def ModInv(a, b):
    gcd, x, y = egcd(a, b)

    if x < 0:
        x += b
    return x


# RSA Encryption
def Encryption(e, n, Msg):
    Cipher = ""

    for m in Msg:
        ascii = ord(m)      # return the Ascii of each char in Msg
        Cipher += str(SquareAndMultiply(ascii, e, n)) + " "     # Cipher = Msg ^ e mod N

    return Cipher

# RSA Normal Decryption
def Decryption(d, n, Cipher):
    Msg = ""

    parts = Cipher.split()      # Split CipherText into parts

    for part in parts:
        if part:       # if exist anything not null
            c = int(part)
            Msg += chr(SquareAndMultiply(c, d, n))        # Msg = Cipher ^ d mod N

    return Msg

# Chinese Remainder Theorem
def CRT(dq, dp, p, q, ciphertext):

    Decrypted_Cipher = []

    parts = ciphertext.split ( )

    for part in parts:

        if part:
            c = int(part)

            # Message part 1
            m1 = SquareAndMultiply(c,dp,p)

            # Message part 2
            m2 = SquareAndMultiply(c,dq,q)

            qinv = ModInv(q, p)

            h = (qinv * (m1 - m2)) % p

            m = m2 + h * q

            m = chr(m)

            Decrypted_Cipher.append(m)

    plaintext = "".join(Decrypted_Cipher)

    return plaintext

# Main Function
if __name__ == "__main__":

    print("--------------------------------------------")
    print("Welcome to RSA Encrypt / Decrypt Program!")
    print("--------------------------------------------")

    Msg = input("Enter the Message : ")

    keySize = 32

    # Get prime nums, p & q
    # p = generateLargePrime(1024)
    # q = generateLargePrime(1024)

    # e, d, n = generateKeys(p, q, keySize)

    p = int(input("Enter p (1st prime number) : "))
    q = int(input("Enter q (2nd prime number) : "))

    n = p * q

    Phi = (p - 1) * (q - 1)  # Totient

    e = int(input("Enter Euler Exponent e : "))

    d = ModInv (e, Phi)     # d = e ^ -1 mod Phi

    ciphertext = Encryption(e, n, Msg)

    plaintext = Decryption(d, n, ciphertext)

    dp = d % (p - 1)
    dq = d % (q - 1)

    plaintext2 = CRT (dq, dp, p, q, ciphertext)

    print("--------------------------------------------")
    print("p = ", p, ", q = ", q, ", n = ", n, ", Phi = ", Phi)

    print("e = ", e, ", d = ", d)
    print("--------------------------------------------")
    print("Message = ", Msg)
    print ("--------------------------------------------")
    print("CipherText (Encryption) = ", ciphertext)
    print("--------------------------------------------")
    print("PlainText (Normal Decryption) = ", plaintext)
    print ("--------------------------------------------")
    print ("PlainText (CRT Decryption) = ", plaintext2)

