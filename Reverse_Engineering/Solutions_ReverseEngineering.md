# Category: Reverse Engineering

## Transformation

Points: 20

The code snippet that they provided us in the problem:
~~~~~py
''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
~~~~~

provides insight into how the flag string was encoded. In this case it was essentially converting from UTF-8 to UTF-16 encoding, where we took the integer value of every pair of characters (assumed to be less than one byte each) and concatenate them together to form a new value.

To reverse the process, we just have to read the 2 bytes value from each character in the flag string.

~~~~~py
with open('./transformation/enc.txt') as f:
    flag = f.readlines()[0]
    print("Original flag",flag)
    out = ''
    for i in range(0, len(flag)):
        out += chr(ord(flag[i])>>8)
        out += chr(ord(flag[i]) & 0xff)
    print(out)
~~~~~

The alternative method is to throw this string into `cyberchef` with the "magic" recipe setting. [Link](https://gchq.github.io/CyberChef#recipe=Magic(5,true,true,''&input=54Gp5o2v5I2U5Jm744S25b2i5qW0542f5qWu542044y05pGf5r2m5by45b2k45Sy5oy25oi54429))

Flag: picoCTF{16_bits_inst34d_of_8_d52c6b93}

## keygenme-py

Points: 30

Upon inspection of the code, it appears that the full key is built from three parts:

~~~~~py
username_trial = "FRASER"
bUsername_trial = b"FRASER"

key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial
~~~~~

Later in the code we see the dynamic part is generated from performing a sha256 hash on the username and then pulling specific indices from that hash to generate the 8-length string. Since we have full access to the code and we know the username is "FRASER", we simply perform and print out the encrypted dynamic part ourselves.

~~~~~py
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
~~~~~

## vault-door-training

Points: 50

We were given a Java file. The password was in cleartext.

Flag: picoCTF{w4rm1ng_Up_w1tH_jAv4_3808d338b46}

## speeds and feeds

Points: 50

When we netcat into the network application, we get back a large number of lines of unfamilar code. From the problem's hint about CNC machine, we can infer that this output is G-code. Each line of G-code represents an action for the machine to perform. For example `G0 X7 Y18` tells to rapidly move the mahine to that coordinate point. Other commands provides instructions to carve at speific points.

Using a g-code simulator (link: https://nraynaud.github.io/webgcode/) and xclip to copy the `nc` output to our clipboard, we were able to get a representation for what the code is trying to carve.

Flag: picoCTF{num3r1cal_c0ntr0l_775375c7}

## Shop

Points: 50

The hint in the problem tells us to check for edge cases. If we start up the program and try to buy an item with negative quantity, then we'll gain coins instead of losing coins. Once we've gotten over 100 coins, we can then purchase the "fruitful flag" item.

`Flag is:  [112 105 99 111 67 84 70 123 98 52 100 95 98 114 111 103 114 97 109 109 101 114 95 51 100 97 51 52 97 56 102 125]`

Using a decimal to ASCII decoder, we get the challenge's flag.

Flag: picoCTF{b4d_brogrammer_3da34a8f}


## ARMssembly 1

Points: 70

**Prompt:** For what argument does this program print `win` with variables 87, 3 and 3? File: chall_1.S Flag format: picoCTF{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be picoCTF{0055aabb})

This is my first time going through ARM Assembly code, and I found it to be quite an interesting exercise. We first start at the .global `func` function, which would be called as part of main:

~~~~~arm
func:
    sub	sp, sp, #32
    str	w0, [sp, 12] 
    mov	w0, 87
    str	w0, [sp, 16] 
    mov	w0, 3
    str	w0, [sp, 20] 
    mov	w0, 3
    str	w0, [sp, 24]
~~~~~

The instructions allocate 4 words on the stack. First it stores our user input at [sp, 12], and then stores the value 87, 3, and 3 following it (at sp+16, sp+20, and sp+24 respectively).

~~~~~arm
	ldr	w0, [sp, 20]
	ldr	w1, [sp, 16]
	lsl	w0, w1, w0
	str	w0, [sp, 28]
~~~~~

LDR stands for Load Immediate Offset. It loads 3 into register w0, and 87 into w1. Then the LSL instruction is called, which performs a Logical Shift Left. The syntax of the instruction is:

lsl x,y,z

which shifts the value in y by z and stores the result in x. In our case it stores 87 << 3 = 0d696 back into w0 and then put it on the stack at sp+28

~~~~~arm
	ldr	w1, [sp, 28]
	ldr	w0, [sp, 24]
	sdiv w0, w1, w0
	str	w0, [sp, 28]
~~~~~

It then loads 696 back into w1 and 3 into w0. The sdiv instruction is Signed Integer Division, and here it's performing w0 <- 696 / 3 = 232 and then storing it back at sp+28.

~~~~~arm
	ldr	w1, [sp, 28]
	ldr	w0, [sp, 12]
	sub	w0, w1, w0
	str	w0, [sp, 28]
	ldr	w0, [sp, 28]
	add	sp, sp, 32
	ret
~~~~~

The program then loads 232 into w1, our user input to w1, perform w0 <- 232 - user_input, and then stores the result at sp+28, and then loads it back into w0 and return. Thus, 232 - user_input will be the return value of this function.

Below `func` we also see two string objects which are defined for the program:

```arm
.LC0:
	.string	"You win!"
	.align	3
.LC1:
	.string	"You Lose :("
	.text
	.align	2
	.global	main
	.type	main, %function
```
In particular we want to trigger LC0 because that is our win message. We see in the later parts that .LC1 is printed within .L4 using the puts function.

~~~arm
.L4:
	adrp	x0, .LC1
	add	x0, x0, :lo12:.LC1
	bl	puts
~~~

Now we turn our attention to the `main` function:

~~~arm
main:
	stp	x29, x30, [sp, -48]!
	add	x29, sp, 0
	str	w0, [x29, 28]
	str	x1, [x29, 16]
	ldr	x0, [x29, 16]
	add	x0, x0, 8
	ldr	x0, [x0]
	bl	atoi
	str	w0, [x29, 44]
	ldr	w0, [x29, 44]
	bl	func
	cmp	w0, 0
	bne	.L4
	adrp	x0, .LC0
	add	x0, x0, :lo12:.LC0
	bl	puts
	b	.L6
~~~

We can ignore most of the beginning logic. The bl instruction in `bl func` stands for Branch and Link, and is equivalent to the `call` instruction in RISC-V. 

After calling func, the program then checks whether w0 is 0. From what we know earlier about func, we know that our user input needs to be 232 for this to happen. If w0 is not zero, the program then proceeds to branch into .L4, which will print out our losing message. Otherwise, .LC0 is printed using puts.

From the problem's prompt, we also know that we need to provide the input in terms of hex 32-bit without 0x.

Thus, the solution is:

Flag: picoCTF{000000e8}