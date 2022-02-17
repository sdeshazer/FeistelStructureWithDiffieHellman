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
import array as arr
import numpy

NameLetters = ['S', 'A', 'M', 'A']
NameAsciiValues = []
NamePrimes = [71, 3, 43, 3]
primeIndexList = []
NameLettersInBin = []
MessageInAsciiValue = []
MessageInBin = []

subKeys = []


def convertMessageLetterToBin(message):
    for letter in message:
        ascii = ord(letter)
        messageInBin = convertDecToBinaryAndPad(ascii, 8)
        MessageInBin.append(messageInBin)


def convertLettersToBin(str):
    lettersInBin = []
    for letter in str:
        ascii = ord(letter)
        letterBin = bin(ascii)
        lettersInBin.append(letterBin)
    return lettersInBin


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


def convertBinStrToBinary(binstr):
    num = int(binstr, 2)
    binary = bin(num)
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
def getInput():
    for lineRead in sys.stdin:
        return lineRead


def rotateBitsLeft(binary, numOfBitsToRotate):
    return (binary << numOfBitsToRotate) | (binary >> (16 - numOfBitsToRotate))


def getStartingFromNonce(nonceStr):
    return int(nonceStr[0])


# encryption function, where most are pieced together:
def feistelEncrypt():
    # input name letters to retrieve ascii:
    asciiNameValues = get_ascii_value(NameLetters)
    print("please type nonce: 0123, a key and a message to encrypt. ex: 0123 fe23 a0f3d2219c")
    line = getInput()
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
    print("----------[Input Check]---------------")
    print("nonce: " + nonce)
    print("key: " + key)
    print("message: " + message)
    addCounterToNonce(nonce, message)
    # split the message in half:
    left = message[:len(message) // 2]
    right = message[len(message) // 2:]
    print("left: " + left)
    print("right: " + right)
    leftascii = convertLetterToAscii(left)
    rightascii = convertLetterToAscii(right)
    print("left message in Ascii:")
    print(leftascii)
    leftBin = []
    rightBin = []
    for dec in leftascii:
        byteInBin = convertDecToBinaryAndPad(dec, 8)
        leftBin.append(byteInBin)
    for dec in rightascii:
        byteInBin = convertDecToBinaryAndPad(dec, 8)
        rightBin.append(byteInBin)

    # print("message in Bin:")
    # print("left: ")
    # print(leftBin)
    # print("right: ")
    # print(rightBin)
    # print("----------------------------------")
    # print("----------[key Check]-------------")
    # print("key:" + key)
    keyascii = convertLetterToAscii(key)
    keyBin = []
    for dec in keyascii:
        byteInBin = convertDecToBinaryAndPad(dec, 8)
        keyBin.append(byteInBin)

    calcSubKeys(key)


# takes a list of ascii values and returns a list of hex
def convertAsciiDecToHex(asciiDec):
    hexList = []
    for dec in asciiDec:
        hexnum = hex(dec)
        hexList.append(hexnum)
    return hexList


def addCounterToNonce(nonce, message):
    if (len(message) % 2) > 0:
        print("error, must be an even number of character in message")
        print("message length:")
        print(len(message))
        exit(0)

    counter0 = 0
    counter1 = 0
    counter2 = 0
    counter3 = 0
    # converts message into an array of chars to use append method:
    arrayChar = [char for char in message]
    print("message in array:")
    for char in arrayChar:  # check that the message is of greater length than 4 bytes.
        if len(arrayChar) < 4:
            arrayChar.append("0")  # else we add a 0 byte
    for char in arrayChar:
        if (len(arrayChar) % 4) > 0:  # check that it can be evenly split
            arrayChar.append("0")  # if It's not even, append to make it even.
            counter0 = counter0 + 1  # increment the first counter

    # partition the message into sets of 4 characters:
    arrayMsgParitioned = [arrayChar[i:i + 4] for i in range(0, len(arrayChar), 4)]
    print("arrayMsgParitioned:")
    print(arrayMsgParitioned)

    concatinatedValues = []
    for msg in arrayMsgParitioned:
        if len(arrayMsgParitioned) > counter1:
            hexMsg = "".join(arrayMsgParitioned[counter1])
            counter1 = counter1 + 1
            concatinatedValues.append(hexMsg)
    print("concatinated Values:")
    print(concatinatedValues)

    msgBinary = []
    for msg in concatinatedValues:
        if len(concatinatedValues) > counter2:
            paddedBinMsg = "{0:8b}".format(int(concatinatedValues[counter2], 16))
            counter2 = counter2 + 1
            msgBin = [int(msg) for msg in str(paddedBinMsg)]
            msgBinary.append(msgBin)

    print("msg binary:")
    print(msgBinary)
    i = 0
    while i < len(msgBinary):
        while len(msgBinary[i]) < 16:
            msgBinary[i].insert(0, 0)
        i = i + 1

    combinedMsg = []

    while counter3 < len(msgBinary):
        nonce = int(nonce)
        newNonce = nonce + counter3
        print("new nonce")
        print(newNonce)
        nStr = str(newNonce)
        while len(nStr) < 4:
            nStr = '0' + str(nStr)  # adding leading zero to the nonce string
        print(nStr)
        counter3 = counter3 + 1


def calcSubKeys(key):
    print("Name Primes:")
    print(NamePrimes)
    # the number of rounds:
    numOfCycles = [0, 1, 2, 3]

    for cycle in numOfCycles:
        counter = numOfCycles[cycle]
        rollValue = counter * 4
        rollValue = -abs(rollValue)
        keyBin = "{0:08b}".format(int(key, 16))
        # print("binaryKey:")
        # print(keyBin)
        binNamePrimesStr = "{0:b}".format(NamePrimes[counter])
        # print("binary name:")
        # print(type(binName))

        namePrimesInBin = []
        # convert from string to list of bits:
        for binary in binNamePrimesStr:
            namePrimesInBin.append(int(binary))
            if len(namePrimesInBin) < 16:
                namePrimesInBin.insert(0,0)
        print("name prime bin sting:")
        print(binNamePrimesStr)
        print("namePrimesInBin")
        print(namePrimesInBin)



# the function to which we xor the key :
def functionXor(keyInBin, rightMessageBin):
    print("keyInBin:")
    print(keyInBin)
    print("right half of message bin:")
    print(rightMessageBin)
    print(type(keyInBin[0]))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    feistelEncrypt()
