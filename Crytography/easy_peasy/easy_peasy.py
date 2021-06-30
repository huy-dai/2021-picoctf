from pwn import *

def decode_hex(data):
    '''
    Given a hex string formatted as 02x, return
    an array representing the int values.
    '''
    split_arr = [data[i:i+2] for i in range(0,len(data)-1,2)]
    hex_arr = [int(val,16) for val in split_arr]
    print("Data:",data)
    print(split_arr)
    print(hex_arr)
    return hex_arr

enc_flag = "5541103a246e415e036c4c5f0e3d415a513e4a560050644859536b4f57003d4c"
print("Length of flag",len(enc_flag))
flag_arr = decode_hex(enc_flag)

r = remote('mercury.picoctf.net',36981)
r.recvuntil("What data would you like to encrypt?")
log.info("Sending data...")
#Send a total of 50,000-32 characters in multiple queries
exp = "A"*(5000)
for i in range(9):
    r.sendline(exp)
    r.recvuntil("What data would you like to encrypt?")
r.sendline("A"*(5000-32))
r.recvuntil("What data would you like to encrypt?")

recoded_flag = "".join([chr(val) for val in flag_arr])
r.sendline(unhex(enc_flag)) #Interesting to note that this performs the same operation as the function I wrote above
r.recvline() #Dumps "Here ya go!" line

res = r.recvline().decode('utf-8')
res_arr = decode_hex(res)

out = "".join([chr(val) for val in res_arr])
print("The flag is",out)
print("Make sure to wrap it with picocTF{}!")
