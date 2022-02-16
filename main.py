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

# rounding function F will be :
# F(ki, m) = (ki xor m) there will be no initial or final permutation
# your system will use 4 rounds

# example input: 0123 fe23 a0f3d2219c
# output should be something like : ffaed0113b
# from STANDARD INPUT

import sys  # standard input
import binascii

Letters = ['S', 'A', 'M', 'A']
Primes = [71, 3, 43, 3]
primeIndexList = []
LettersInBin = []


# convert bin to hex:
def BinaryToHex(binary):
    dec = int(binary, 2)
    hex = hex(dec)
    return hex


# xor function in range of N
def exor(bit1, bit2, n):
    temp = ""
    for i in range(n):
        if bit1[i] == bit2[i]:
            temp += "0"
        else:
            temp += "1"
    # return resulting bit":
    return temp


def padBinary(binary, paddingLen):  # makes sure binary strings have exactly 8 bits
    padding = ""
    for a in range(paddingLen - len(binary)):  # repeat for the difference between 8 and the current length
        padding += "0"
    return padding + binary


def feistalCipher():
    # collect the ascii value from the letters:
    greatestBit = 0
    asciiValues = get_ascii_value(Letters)
    for ascii in asciiValues:
        # collect the index to the primes
        primeIndexList.append(calculate_index(ascii))
    for letter in Letters:
        byte_array = letter.encode()
        binary = int.from_bytes(byte_array, "big")
        binstr = bin(binary)
        conver_ascii()
    print(asciiValues)
    print(LettersInBin)

def conver_ascii():
    for value in asciiValues:
        LettersInBin.append(getBinary(value, 8))


def getBinary(decimal, padding):  # convert to binary
    decimal = int(decimal)
    binary = ''
    if decimal == 0: decimal = 0
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal = decimal >> 1
    binary = padBinary(binary, padding)
    return binary


def parse_primes_txt():
    with open('primes.txt') as f:
        lines = f.readlines()
        for line in lines:
            for c in line:
                if not c.isdigit():
                    continue
                primeIndexList.append(c)


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


def calculate_index(asciiValue):
    return asciiValue - 64


def get_input():
    for lineRead in sys.stdin:
        # print(f'Input : {line}')
        return lineRead


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asciiValues = get_ascii_value(Letters)
    print("ascii values:")
    print(asciiValues)
    feistalCipher()

    # line = get_input()
