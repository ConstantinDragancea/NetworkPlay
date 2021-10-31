import sys

BUFFER_SIZE = 1400

def main(file1 : str, file2 : str):
    fd1 = open(file1, 'rb')
    fd2 = open(file2, 'rb')

    msg1 = fd1.read(BUFFER_SIZE)
    msg2 = fd2.read(BUFFER_SIZE)

    while (len(msg1) != 0 or len(msg2) != 0):
        if (msg1 != msg2):
            print("Fisierele nu coincid!")
            exit(-1)
        msg1 = fd1.read(BUFFER_SIZE)
        msg2 = fd2.read(BUFFER_SIZE)
    
    print("Fisierele sunt egale!")

if __name__ == "__main__":
    file1, file2 = sys.argv[1], sys.argv[2]
    main(file1, file2)