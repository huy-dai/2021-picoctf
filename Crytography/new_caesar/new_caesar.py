import string

LOWERCASE_OFFSET = ord("a")
print(LOWERCASE_OFFSET)
ALPHABET = string.ascii_lowercase[:16]
print("Alphabet",ALPHABET)

def b16_encode(plain):
	enc = ""
	for c in plain:
		binary = "{0:08b}".format(ord(c))
		enc += ALPHABET[int(binary[:4], 2)]
		enc += ALPHABET[int(binary[4:], 2)]
	return enc

def shift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET # - 97
	t2 = ord(k) - LOWERCASE_OFFSET # - 97
	return ALPHABET[(t1 + t2) % len(ALPHABET)]

flag = "picoCTFlmaonevermindeveryone"
key = "d"
#assert all([k in ALPHABET for k in key])
#assert len(key) == 1

b16 = b16_encode(flag)
enc = ""
for i, c in enumerate(b16):
	enc += shift(c, key[i % len(key)])
print("Encrypted test flag",enc)

#Debugging Test Cases (for myself)
#str = "picoCTF{123}"
#print(b16_encode(str))

#Decode by enumerating all keys

def b16_decode(in_str):
	out = ""
	for i in range(0,len(in_str),2):
		first_val = ALPHABET.index(in_str[i])
		sec_val = ALPHABET.index(in_str[i+1])
		#print(first_val,sec_val)
		binary = "{0:04b}{1:04b}".format(first_val,sec_val)
		out += chr(int(binary,2))
		#print(binary)
	return out

enc = "dcebcmebecamcmanaedbacdaanafagapdaaoabaaafdbapdpaaapadanandcafaadbdaapdpandcac"
#enc = "kdjmjgjchgihhjjpjajejcjbjikjjikfjajmjbjhjikjjikfkmjcjbji"

for k_inv in range(len(ALPHABET)):
	dec = ""
	for c in enc:
		dec += shift(c, ALPHABET[k_inv])
	#print(dec)
	print(b16_decode(dec)+'\n')







