# Samantha Deshazer
# python 3.9   w/ Pycharm
# CS 427 Spr 2022
# S A M A
# --------------------------------------
#  Prime Index: [83 - 64] = 19 : S Index
#  65 - 64 = 1 : A Index
#  77 - 64 = 13 : M Index
#  65 - 64 = 1 : A Index
# -----------------------
# Primes from index: https://primes.utm.edu/lists/small/1000.txt
# 19 : S: 71
# 1  : A: 3
# 13 : M: 43
# 1  : A: 3

# [x] Name Part:
# key schedule based on the bits of your name
# the cipher will be a 16-bit block cipher
# the 8 bit ascii letters from the first 4 BYTES of your full name in uppercase
#               S A M A
#          DEC: 83 | 65 | 77 | 65 | 78
#         BIN: 01010011  | 01000001 | 01001101 | 01000001 | 01001110
# For each BYTE of your first name calculate prime [BYTE - 64]
#         ex : B  is 66-64 = |2|, prime[2] = 5 in the list, 2 as the INDEX.
#
# The Cipher:
# The key must be 16 BITS, we will break the key into 4 subkeys:
# SubkeyN = lowerBYTE( ActualKey RotatedLeft (N * 4)) XOR lowerBYTE( NamePrimesN )
# the first round is 0, the last round 3. N = 0,1,2,3.
# use bitwise masks to compute the lowerBYTE(). we want the least significant 8 BITs from the 16 BIT key
# after rolling it.
# you can use the nonce as an initial value to the counter. Nonce is a constant.

# rounding function F will be :
# F(ki, m) = (ki xor m) there will be no initial or final permutation
# your system will use 4 rounds
#               nonce key message
# example input: 0123 fe23 a0f3d2219c
# output should be something like : ffaed0113b
# from STANDARD INPUT

# m = plain text
#   1. divide M into two parts L0 and R0
#   2. R0 is encoded using F(K, m) = (ki xor m) and store that in variable E
#   3. new L1 = R0
#   4. new R1 = L0 xor E
#   5. concatenate L1 and R1 to obtain result.


import sys  # standard input
import binascii

NameLetters = ['S', 'A', 'M', 'A']
NameAsciiValues = []
NamePrimes = [71, 3, 43, 3]
primeIndexList = []
NameLettersInBin = []
MessageInAsciiValue = []
MessageInBin = []

subKeys = []


def convertLetterToBin(message):
    for letter in message:
        ascii = ord(letter)
        messageInBin = convertDecToBinaryAndPad(ascii, 8)
        MessageInBin.append(messageInBin)


# convert bin to hex:
def convertBinaryToHex(binary):
    dec = int(binary, 2)
    hex = hex(dec)
    return hex


def convertDecToBinaryAndPad(decimal, padding):  # convert to binary
    decimal = int(decimal)
    binary = ''
    if decimal == 0: decimal = 0
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal = decimal >> 1
    binary = padBinary(binary, padding)
    return binary


def convertLetterToAscii(str):
    arrayOfAsciiValues = []
    for letter in str:
        arrayOfAsciiValues.append(ord(letter))
    return arrayOfAsciiValues


# xor function in range of Nonce
def xor(bit1, bit2, n):
    temp = ""
    for i in range(n):
        if bit1[i] == bit2[i]:
            temp += "0"
        else:
            temp += "1"
    # return resulting bit":
    return temp


# make sure binary is 8 bits, paddingLen = 8 for example :
def padBinary(binary, paddingLen):
    padding = ""
    for a in range(paddingLen - len(binary)):
        padding += "0"
    return padding + binary

# parse a text file for primes:
def parse_primes_txt():
    with open('primes.txt') as f:
        lines = f.readlines()
        for line in lines:
            for c in line:
                if not c.isdigit():
                    continue
                primeIndexList.append(c)


# hard coded ascii values for testing name:
def get_ascii_value(letterArray):
    asciiValues = []
    i = 0
    while i < len(letterArray):
        # print(i)
        if letterArray[i] == 'S':
            asciiValues.append(83)
        if letterArray[i] == 'A':
            asciiValues.append(65)
        if letterArray[i] == 'M':
            asciiValues.append(77)
        i = i + 1
    return asciiValues

def convertNameAsciiToBin(asciiValues):
    for value in asciiValues:
        NameLettersInBin.append(convertDecToBinaryAndPad(value, 8))

# calculate the index for each letter in name for prime list:
def calculate_index(asciiValue):
    return asciiValue - 64


# read in input from stdin:
def get_input():
    for lineRead in sys.stdin:
        return lineRead

def feistel():
    # input name letters to retrieve ascii:
    asciiNameValues = get_ascii_value(NameLetters)
    print("please type cycles: 0123, a key and a message to encrypt. ex: 0123 fe23 a0f3d2219c")
    line = get_input()
    i = 0
    input = line.split()
    for item in input:
        if i == 0:
            nonce = item
        if i == 1:
            key = item
        if i == 2:
            message = item
        i = i + 1
    print("nonce: " + nonce)
    print("key: " + key)
    print("message: " + message)
    print("---------------------------------")
    messageAscii = convertLetterToAscii(message)
    print("message in Ascii:")
    print(messageAscii)
    messageInBin = []
    for dec in messageAscii:
        byteInBin = convertDecToBinaryAndPad(dec, 8)
        messageInBin.append(byteInBin)
    print("message in Bin:")
    print(messageInBin)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   feistel()




