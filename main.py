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
#   1. parition m and calculate subkeys
#   2. R0 is encoded using F(K, m) = (ki xor m) and store that in variable E
#   3. new L1 = R0
#   4. new R1 = L0 xor E, where E is our function(ki,m), ki from our subkeys from nonce and primes.
#   5. concatenate L1 and R1 to obtain complete result.


import sys  # standard input
import numpy  # converting and rotating bits in a array list.

NameLetters = ['S', 'A', 'M', 'A']
NamePrimes = [71, 3, 43, 3]
NameLettersInBin = []
# 0xFF:
BinFFByte16 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]


# convert bin to hex:
def convertBinaryToHex(binary):
    dec = int(binary, 2)
    hex = hex(dec)
    return hex


# convert to binary, pad an amount
def convertDecToBinaryAndPad(decimal, padding):
    decimal = int(decimal)
    binary = ''
    if decimal == 0: decimal = 0
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal = decimal >> 1
    binary = padBinary(binary, padding)
    return binary


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


def convertNameAsciiToBin(asciiValues):
    for value in asciiValues:
        NameLettersInBin.append(convertDecToBinaryAndPad(value, 8))


# calculate the index for each letter in name for prime list:
# adding this in case I have time to automate looking up primes:
def calculate_index(asciiValue):
    return asciiValue - 64


# read in input from stdin:
def getInput():
    for lineRead in sys.stdin:
        return lineRead


# may use with numpy:
def rotateBitsLeft(binary, numOfBitsToRotate):
    return (binary << numOfBitsToRotate) | (binary >> (16 - numOfBitsToRotate))


# converts to list first:
def stripOff0xOfHexValueReturnsStr(fullHexValue):
    cList = list(fullHexValue)
    cList = cList[2:]
    cList = ''.join(cList)
    return cList


# returns the lower 8 bits of 16, 32, etc:
def getLowerByte(twoBytesList):
    return twoBytesList[8:]


# xor wrapper, must be same type or hex ^ int
# cannot be 'str' and 'int'.
def exor(byteA, byteB):
    return byteA ^ byteB


def convertBinStringToDec(binStr):
    decInt = int(binStr, 2)
    return decInt


def convertBinListToStr(binList):
    binStr = [str(binList) for binList in binList]
    binStr = ''.join(binStr)
    return binStr


def getStartingFromNonce(nonceStr):
    return int(nonceStr[0])


# encryption function, where most are pieced together:
def feistelEncrypt():
    # input name letters to retrieve ascii:
    print("please type nonce: 0123, a key and a message to encrypt separated by spaces. ex: 0123 fe23 a0f3d2219c")
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
    print("----------[Input]---------------")
    print("nonce: " + nonce)
    print("key: " + key)
    print("message: " + message)
    print("--------------------------------")
    subKeys = calcSubKeys(key)
    addCounterToNonce(nonce, message, subKeys)


def addCounterToNonce(nonce, message, subKeys):
    if (len(message) % 2) > 0:
        print("error, must be an even number of character in message")
        print("message length:")
        print(len(message))
        exit(0)

    # counters for the number of rounds - may make dynamic later:
    counters = [0, 0, 0, 0]
    # converts message into an array of chars to use append method:
    # the message must be an even number of bytes to partition later:
    arrayChar = [char for char in message]
    for char in arrayChar:
        if len(arrayChar) < 4:
            arrayChar.append("0")  # if its not, pad with 0's
    for char in arrayChar:
        if (len(arrayChar) % 4) > 0:
            arrayChar.append("0")  # if its not, pad with 0's
            counters[0] = counters[0] + 1

    # partition the message into sets of 4 characters:
    arrayMsgPartitioned = [arrayChar[i:i + 4] for i in range(0, len(arrayChar), 4)]
    print("arrayMsgPartitioned:", arrayMsgPartitioned, type(arrayMsgPartitioned))

    concatenatedMsgFromPartition = []
    i = 0
    while i < len(arrayMsgPartitioned):
        if len(arrayMsgPartitioned) > counters[1]:
            hexMsg = "".join(arrayMsgPartitioned[counters[1]])
            counters[1] = counters[1] + 1
            concatenatedMsgFromPartition.append(hexMsg)
        i = i + 1
    # print("concatenated Values:", concatenatedMsgFromPartition, type(concatenatedMsgFromPartition))

    msgBinary = []
    i = 0
    while i < len(concatenatedMsgFromPartition):
        if len(concatenatedMsgFromPartition) > counters[2]:
            paddedBinMsg = "{0:8b}".format(int(concatenatedMsgFromPartition[counters[2]], 16))
            counters[2] = counters[2] + 1
            msgBin = [int(msg) for msg in str(paddedBinMsg)]
            msgBinary.append(msgBin)
        i = i + 1

    # print("concatenated Msg From Partition",concatenatedMsgFromPartition, type(concatenatedMsgFromPartition))

    i = 0
    while i < len(msgBinary):
        while len(msgBinary[i]) < 16:
            msgBinary[i].insert(0, 0)
        i = i + 1
    #print("msg binary:", msgBinary, type(msgBinary))

    completeEncryptedMessage = []
    while counters[3] < len(msgBinary):
        nonce = int(nonce)
        newNonce = nonce + counters[3]
        print("nonce : ", newNonce, type(newNonce))
        nStr = str(newNonce)
        while len(nStr) < 4:
            nStr = '0' + str(nStr)  # adding leading zero to the nonce string
        print("nonce str :", nStr, type(nStr))
        currentRoundResult = fiestelStructure(nStr, subKeys)
        currentRoundResult = ''.join(currentRoundResult)
        currentRoundResult = str(currentRoundResult).replace(' ', '').replace('[', '').replace(']', '')
        # F(subkey) xor message byte:
        encryptedMessage = hex(int(currentRoundResult, 16) ^ int(concatenatedMsgFromPartition[counters[3]], 16))
        # append to the series of bytes to complete the output, without the 0x:
        completeEncryptedMessage.append(encryptedMessage[2:])
        counters[3] = counters[3] + 1
    # the final result of encryption:
    completeEncryptedMessage = ''.join(completeEncryptedMessage)
    print("completeEncryptedMessage", completeEncryptedMessage)


def fiestelStructure(nStr, subKeys):
    counterN = 0
    numberOfRounds = 4
    # convert nonce for encryption:
    nonceList = [int(char) for char in str(nStr)]
    nonceArray = numpy.roll(nonceList, 0, axis=None)
    # split nonce in half:
    nLeft = nonceArray[0:2]
    nRight = nonceArray[2:]

    nRight = str(nRight).replace(' ', '').replace('[', '').replace(']', '')
    nLeft = str(nLeft).replace(' ', '').replace('[', '').replace(']', '')

    print("nleft:", nLeft, "nright:", nRight)
    print("subkeys", subKeys)
    # the Rounding function F(ki, m) = (ki xor m):
    # where ki = subkey[i]
    # nleft is left half of nonce, nright is right of nonce (constants)
    # here is where the key and the nonce are xor'ed together to later be used with m:
    while counterN < numberOfRounds:
        rightNxorKey = hex(int(nRight, 16) ^ int(subKeys[counterN], 16))
        newValue = hex(int(rightNxorKey, 16) ^ int(nLeft, 16))
        # switch left to be last origin right:
        nLeft = nRight
        # change original right to be our new encrypted value:
        nRight = newValue  # new right.
        counterN = counterN + 1
    # the result of ki xord with nonce:
    result = numpy.concatenate((nRight[2:], nLeft[2:]), axis=None)
    return result


# takes a list of ascii values and returns a list of hex
def convertAsciiDecToHex(asciiDec):
    hexList = []
    for dec in asciiDec:
        hexnum = hex(dec)
        hexList.append(hexnum)
    return hexList


# calculate the subkeys needed from the set of primes to xor with Keyi:
def calcSubKeys(key):
    print("--[ Calculating Subkeys ] --")
    subKeys = []
    print("Name Primes:")
    print(NamePrimes)
    # the number of rounds N = 0, 1, 2, 3:
    numOfCycles = [0, 1, 2, 3]

    for cycle in numOfCycles:
        counterN = numOfCycles[cycle]
        # padding:
        keyBin = "{0:08b}".format(int(key, 16))
        binNamePrimes = "{0:b}".format(NamePrimes[counterN])

        keyStr = []
        for bit in keyBin:
            keyStr.append(int(bit))

        binNamePrimesList = []
        # convert from string to list of bits:
        for binary in binNamePrimes:
            binNamePrimesList.append(int(binary))
        while len(binNamePrimesList) < 16:
            binNamePrimesList.insert(0, 0)
        print("binNamePrimes:", binNamePrimes, type(binNamePrimes))
        print("binNamePrimesStr: ", binNamePrimesList, type(binNamePrimesList))
        # rotating the key left N * 4 :
        rotateLeftKeyList = numpy.roll(keyStr, -abs(counterN * 4), axis=None)
        # here for the sake of conversion to nda array:
        binNamePrimesList = numpy.roll(binNamePrimesList, 0, axis=None)

        keyAndFFList = rotateLeftKeyList & BinFFByte16

        primesAndFFList = binNamePrimesList & BinFFByte16

        print("rolled key:", rotateLeftKeyList, type(rotateLeftKeyList))
        print("key and 0xFF:", keyAndFFList, type(keyAndFFList))
        print("primes and 0xFF", primesAndFFList, type(primesAndFFList))

        lowerByteKeyAndFFList = getLowerByte(keyAndFFList)
        lowerBytePrimesAnd1FFList = getLowerByte(primesAndFFList)

        print("lowerByteKeyAndFFList:", lowerByteKeyAndFFList, type(lowerByteKeyAndFFList))
        print("lowerBytePrimesAndFFList", lowerBytePrimesAnd1FFList, type(lowerBytePrimesAnd1FFList))

        # xor to get the subkey based on primes and key/counter:
        subkeyN = exor(lowerBytePrimesAnd1FFList, lowerByteKeyAndFFList)

        print("subkeyN", subkeyN, type(subkeyN))
        subkeyNStr = convertBinListToStr(subkeyN)

        subkeyNDec = convertBinStringToDec(subkeyNStr)
        print("subkeyNDec", subkeyNDec, type(subkeyNDec))
        subkeyNHex = hex(subkeyNDec)
        print("subkeyNHex", subkeyNHex)
        subKeysNHexStr = stripOff0xOfHexValueReturnsStr(subkeyNHex)
        print("sub keys in hex stripped: ", subKeysNHexStr)
        subKeys.append(subKeysNHexStr)
    return subKeys


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    feistelEncrypt()
