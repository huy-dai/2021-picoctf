# Category: Cryptography

## Mod 26
Points: 10

The hint asked us about ROT-13, which is a letter subsitution cipher. We can decipher by performing ROT-13 again on the ciphertext.

```
huydai@huydai-Ubuntu:~$ echo "cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_hyLicInt}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
picoCTF{next_time_I'll_try_2_rounds_of_rot13_ulYvpVag}
```

## Mind your Ps and Qs
Points: 20

In RSA, if the value of N is small, it becomes easier to find the prime factors p and q of N. Using factordb.com, I was able to find that the p and q values are 1955175890537890492055221842734816092141 and 670577792467509699665091201633524389157003. Using a nifty tool call RsaCtfTool (link: https://github.com/Ganapati/RsaCtfTool), I was able to provide it the parameters and get it to decrypt the message.

````
huydai@huydai-Ubuntu:~/Tools/RsaCtfTool$ python3 RsaCtfTool.py -n 1311097532562595991877980619849724606784164430105441327897358800116889057763413423 -e 65537 -p 1955175890537890492055221842734816092141 -q 670577792467509699665091201633524389157003 --uncipher 861270243527190895777142537838333832920579264010533029282104230006461420086153423
private argument is not set, the private key will not be displayed, even if recovered.

Results for /tmp/tmpu8c6u9o1:

Unciphered data :
HEX : 0x007069636f4354467b736d6131315f4e5f6e305f67306f645f31333638363637397d
INT (big endian) : 13016382529449106065927291425342535437996222135352905256639573959002849415739773
INT (little endian) : 3711971977671268622040852236510036125495501942684770673221105381148513202625671168
STR : b'\x: 00picoCTF{sma11_N_n0_g0od_13686679}'
````

flag: picoCTF{sma11_N_n0_g0od_13686679}

## Easy Peasy
Points: 40

When we first access the Python server, it prints out the encrypted flag, which was encrypted using integer values read from a file used as a one-time pad. For each plaintext character they performed `chr(val) ^ key_int` and then formatted the output as 02x (two digits hex). Due to the way that system implements the one-time pad, once it uses up all of its 50,000 pre-generated integers, it would wrap around and reuse the starting numbers.

Thus, using pwntools, we can send `50,000-32` padding characters (we need to account for the 32 characters used to encrypt the flag) and then send the encrypted flag in ASCII form so that the XOR operation will cause the original flag to be returned to us. After that, we just need to wrap the flag with "picoCTF{}" as the directions instructed.

Flag: picoCTF{7f9da29f40499a98db220380a57746a4}