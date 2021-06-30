#Category: Reverse Engineering

##Transformation
Points: 20

The code snippet that they provided us in the problem: 
````py
''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
````
provides insight into how the flag string was encoded. In this case it was essentially converting from UTF-8 to UTF-16 encoding, where we took the integer value of every pair of characters (assumed to be less than one byte each) and concatenate them together to form a new value.

To reverse the process, we just have to read the 2 bytes value from each character in the flag string.

```py
with open('./transformation/enc.txt') as f:
    flag = f.readlines()[0]
    print("Original flag",flag)
    out = ''
    for i in range(0, len(flag)):
        out += chr(ord(flag[i])>>8)
        out += chr(ord(flag[i]) & 0xff)
    print(out)
```
The alternative method is to throw this string into `cyberchef` with the "magic" recipe setting. [Link](https://gchq.github.io/CyberChef#recipe=Magic(5,true,true,''&input=54Gp5o2v5I2U5Jm744S25b2i5qW0542f5qWu542044y05pGf5r2m5by45b2k45Sy5oy25oi54429))

Flag: picoCTF{16_bits_inst34d_of_8_d52c6b93}


##keygenme-py
Points: 30

Upon inspection of the code, it appears that the full key is built from three parts:

```py
username_trial = "FRASER"
bUsername_trial = b"FRASER"

key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial
```

Later in the code we see the dynamic part is generated from performing a sha256 hash on the username and then pulling specific indices from that hash to generate the 8-length string. Since we have full access to the code and we know the username is "FRASER", we simply perform and print out the encrypted dynamic part ourselves.

```py
def check_key(key, username_trial):

    global key_full_template_trial

    print(key)
    print(username_trial)

    user = "FRASER"
    user = user.encode('utf-8')
    
    hash = hashlib.sha256(user).hexdigest()
    order = [4,5,3,6,2,7,1,8]

    decrypt_key = ''
    for num in order:
        decrypt_key += hash[num]
    print(decrypt_key)

```