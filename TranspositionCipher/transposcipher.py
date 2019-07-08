"""
Algorithm for Columnar Transposition Cipher found at:
http://www.crypto-it.net/eng/simple/columnar-transposition.html?tab=2

"""
#Function written to test the code for the columnar transposition cipher algorithm
def main():
   print("\nColumnar Transposition Cipher Algorithm\n")
   while True:
       userMessage = input("Please write the message you wish to encrypt: ")
       userKey = input("Please write the key you would like to use: ")

       ciphertext = encrypt(userMessage, userKey)

       print("\n")
       print("Encryption using key " + "\"" + userKey + "\" returns ciphertext:")
       print("\"" + ciphertext + "\"\n")

       plaintext = decrypt(ciphertext, userKey)

       print("Decryption using key " + "\"" + userKey + "\" returns plaintext:")
       print("\"" + plaintext + "\"\n")
       quit = input("Enter 1 to quit, or 0 to try another message and key: ")
       print("")
       if (int(quit) == 1):
           break

def encrypt(message, keyword):
  #Fills a matrix of len() width of the keyword sequence with the user's message
  matrix = createEncMatrix(len(keyword), message)
  #Converts the keyword into a number sequence and returns
  #a list with each seperate number in the sequence having it's
  #own index.
  keywordSequence = getKeywordSequence(keyword)
  ciphertext = "";
  #Iterates through the matrix and appends the letters with the smallest
  #sequence number first to create the cipher text.
  for num in range(len(keywordSequence)):
    pos = keywordSequence.index(num+1)
    for row in range(len(matrix)):
      if len(matrix[row]) > pos:
        ciphertext += matrix[row][pos]
  return ciphertext

def createEncMatrix(width, message):
  r = 0
  c = 0
  matrix = [[]]
  #Appends the information from message to a matrix the width of the
  #sequence key.
  for pos, ch in enumerate(message):
    matrix[r].append(ch)
    c += 1
    if c >= width:
      c = 0
      r += 1
      matrix.append([])
  return matrix

#Converts a user created key to a sequence list that
#determines the width of the matrix to be built later.
def getKeywordSequence(keyword):
  sequence = []
  for pos, ch in enumerate(keyword):
    previousLetters = keyword[:pos]
    newNumber = 1
    for previousPos, previousCh in enumerate(previousLetters):
      if previousCh > ch:
        sequence[previousPos] += 1
      else:
        newNumber += 1
    sequence.append(newNumber)
  return sequence


def decrypt(message, keyword):
  #Uses the sequence number and the cipher text to create a matrix similar to
  #the encrption matrix.
  matrix = createDecrMatrix(getKeywordSequence(keyword), message)
  plaintext = "";
  #Iterates the decryption matrix and appends the letters in the matrix from
  #top to bottom, and left to right, creating the original plaintext message.
  for r in range(len(matrix)):
    for c in range (len(matrix[r])):
      plaintext += matrix[r][c]
  return plaintext


def createDecrMatrix(keywordSequence, message):
  width = len(keywordSequence)
  #FIXED: "/" to integer division "//"
  #to fix type error from using range(height) in createEmptyMatrix()
  height = len(message) // width
  if height * width < len(message):
    height += 1
  #An empty matrix is created using the original dimensions of the Encryption
  #matrix.
  matrix = createEmptyMatrix(width, height, len(message))
  pos = 0
  #Fills the matrix with letters under the same
  #sequence numbers as before.
  for num in range(len(keywordSequence)):
    column = keywordSequence.index(num+1)
    r = 0
    while (r < len(matrix)) and (len(matrix[r]) > column):
      matrix[r][column] = message[pos]
      r += 1
      pos += 1
  return matrix

#Helper function that creates an empty matrix matching the
#size of the original encryption matrix.
def createEmptyMatrix(width, height, length):
  matrix = []
  totalAdded = 0
  for r in range(height):
    matrix.append([])
    for c in range(width):
      if totalAdded >= length:
        return matrix
      matrix[r].append('')
      totalAdded += 1
  return matrix

main()
