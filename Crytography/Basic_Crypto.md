#Category: Cryptography

##Mod 26
Points: 10

The hint asked us about ROT-13, which is a letter subsitution cipher. We can decipher by performing ROT-13 again on the ciphertext.

```
huydai@huydai-Ubuntu:~$ echo "cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_hyLicInt}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
picoCTF{next_time_I'll_try_2_rounds_of_rot13_ulYvpVag}
```
