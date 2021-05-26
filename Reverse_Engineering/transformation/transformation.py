def testing_encoding():
    flag = "picoCT"
    for i in range(0, len(flag), 2):
        print(ord(flag[i])<<8)
    out = ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
    print(out)


testing_encoding()
with open('./transformation/enc.txt') as f:
    flag = f.readlines()[0]
    print("Original flag",flag)
    out = ''
    for i in range(0, len(flag)):
        out += chr(ord(flag[i])>>8)
        out += chr(ord(flag[i]) & 0xff)
    print(out)