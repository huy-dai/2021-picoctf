# Category: Cryptography

## Mod 26

Points: 10

The hint asked us about ROT-13, which is a letter subsitution cipher. We can decipher by performing ROT-13 again on the ciphertext.

```console
huydai@huydai-Ubuntu:~$ echo "cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_hyLicInt}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
picoCTF{next_time_I'll_try_2_rounds_of_rot13_ulYvpVag}
```

## Mind your Ps and Qs

Points: 20

In RSA, if the value of N is small, it becomes easier to find the prime factors p and q of N. Using factordb.com, I was able to find that the p and q values are 1955175890537890492055221842734816092141 and 670577792467509699665091201633524389157003. Using a nifty tool call RsaCtfTool (link: https://github.com/Ganapati/RsaCtfTool), I was able to provide it the parameters and get it to decrypt the message.

```console
huydai@huydai-Ubuntu:~/Tools/RsaCtfTool$ python3 RsaCtfTool.py -n 1311097532562595991877980619849724606784164430105441327897358800116889057763413423 -e 65537 -p 1955175890537890492055221842734816092141 -q 670577792467509699665091201633524389157003 --uncipher 861270243527190895777142537838333832920579264010533029282104230006461420086153423
private argument is not set, the private key will not be displayed, even if recovered.

Results for /tmp/tmpu8c6u9o1:

Unciphered data :
HEX : 0x007069636f4354467b736d6131315f4e5f6e305f67306f645f31333638363637397d
INT (big endian) : 13016382529449106065927291425342535437996222135352905256639573959002849415739773
INT (little endian) : 3711971977671268622040852236510036125495501942684770673221105381148513202625671168
STR : b'\x: 00picoCTF{sma11_N_n0_g0od_13686679}'
```

flag: picoCTF{sma11_N_n0_g0od_13686679}

## Easy Peasy

Points: 40

When we first access the Python server, it prints out the encrypted flag, which was encrypted using integer values read from a file used as a one-time pad. For each plaintext character they performed `chr(val) ^ key_int` and then formatted the output as 02x (two digits hex). Due to the way that system implements the one-time pad, once it uses up all of its 50,000 pre-generated integers, it would wrap around and reuse the starting numbers.

Thus, using pwntools, we can send `50,000-32` padding characters (we need to account for the 32 characters used to encrypt the flag) and then send the encrypted flag in ASCII form so that the XOR operation will cause the original flag to be returned to us. After that, we just need to wrap the flag with "picoCTF{}" as the directions instructed.

Flag: picoCTF{7f9da29f40499a98db220380a57746a4}

## New Caesar

Points: 60

In the provided new_caesar.py file, we can see that the challenge is implementing its own version of the Caesar cipher. Specifically, it is working with its own alphabet set, which is the letters a-p. First, it takes each character of the flag, converts it to binary, and interpret each nibble as an index into the custom alphabet array. For each character in the new string, it then Caesar shifts it by some constant from 0-16 (we know this from the assertions that the key is a one-character string that has to be within the custom alphabet).

To reverse, we can simply iterate through all the possible inverse key values (e.g. `16-i for i in range(len(ALPHABET))`) and use it to de-Caesar shift the ciphertext, and then perform some binary splicing to get the original keywords.

Once we've printed out all possible 16 outputs, we can pick the one that seem to make the most sense.

Flag: picoCTF{et_tu?_07d5c0892c1438d2b32600e83dc2b0e5}

Editor's Note: Get it? New Caesar? Etu Brute?

## Mini RSA

Points: 70

In RSA, to encrypt a message we do:

`ciphertext = msg^e (mod n)`

And to decrypt we perform:

`msg = ciphertext^d (mod n)`

In this problem, since e is small, we can focus on brute-forcing the encryption step. We can rewrite the equation as:
$$c \mod n = m^e$$
$$tn + c = m^e \; \; \text{for some t}$$ 
$$\sqrt[e]{tn + c} = m$$

Thus we can iterate through values for t and find the ones which gives us an exact value for m after the cube root (since `e=3`). Since the values we are dealing with are going to be rather large, we need a library which can support arbitary integer precision when performing root calculation. We can use the function `iroot` from gmpy2 library for this purpose. It's particularly useful because `iroot(x,n)` returns a 2-element tuple *(y,b)* where y is the integer n-th root of x and b is True if the root is exact.

Install the library with:

`sudo apt-get install -y python3-gmpy2`

Our decryption script becomes: 

~~~py
from gmpy2 import iroot

cipher = 1220012318588871886132524757898884422174534558055593713309088304910273991073554732659977133980685370899257850121970812405700793710546674062154237544840177616746805668666317481140872605653768484867292138139949076102907399831998827567645230986345455915692863094364797526497302082734955903755050638155202890599808145893251774383242888588567652079502880522005531571120463301333725071534050137246298274874319432561063978068140428652193294702808687000503934999928337234367205234422580586283326017530708854836817980318398277272759022724136418545105867685463283579824831916699431331460258806680372323026200534791012439563034432826050072742892112790177234284090476467119938191076883854821999876464545771711445501514467804193760659882386680300508589975451301720477703627085437101600726487172968870448635983769708507451946168500510817590720157574816563284526466526806699820426206566718022595284382939272542309819250701217431454132436646725890151031992160610219312035760562959174778547776304922277751548955049884940378

n = 1615765684321463054078226051959887884233678317734892901740763321135213636796075462401950274602405095138589898087428337758445013281488966866073355710771864671726991918706558071231266976427184673800225254531695928541272546385146495736420261815693810544589811104967829354461491178200126099661909654163542661541699404839644035177445092988952614918424317082380174383819025585076206641993479326576180793544321194357018916215113009742654408597083724508169216182008449693917227497813165444372201517541788989925461711067825681947947471001390843774746442699739386923285801022685451221261010798837646928092277556198145662924691803032880040492762442561497760689933601781401617086600593482127465655390841361154025890679757514060456103104199255917164678161972735858939464790960448345988941481499050248673128656508055285037090026439683847266536283160142071643015434813473463469733112182328678706702116054036618277506997666534567846763938692335069955755244438415377933440029498378955355877502743215305768814857864433151287
e = 3


for t in range(1,10000):
    result, is_exact = iroot(t*n+cipher,e)
    if is_exact:
        print(f"Possible i value: {result}")
        msg = format(result,'x') #convert to hex
        msg = bytearray.fromhex(msg).decode() #convert to ASCII
        print(msg)
~~~

We noted that even though the value of e is small, t is not necessarily small. Additionally, the `result` variable produced from iroot is not an integer, but rather of the mpz type. To convert from RSA numeric form to text we needed to turn it into a hex byte array before decoding to ASCII.

Flag: picoCTF{e_sh0u1d_b3_lArg3r_0b39bbb1}

## Daschund Attacks

Points: 80

Based on the hint of a pet daschund, we can gather that the problem wants for us to implement the Wiener's Attack to crack the ciphertext. The attack uses the "continued fraction" method to expose the private key `d` when d is small. The math behind it doesn't seem too bad ([Link](https://en.wikipedia.org/wiki/Wiener%27s_attack)), though for us, we already have a tool called [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool) which can perform the attack for us:

After connecting to the server through netcat, we can pull the given parameters and give it to the tool to decrypt. Notice that we tell the tool to use the Wiener attack.

```console
python3 RsaCtfTool.py -e 103693892268063230048369424983769629886362685474670660150707446916496765414920829965363345382878152444191174869027555313065927128622608684691894888299953907579052220275009173768344687807111635950738741372838998885723231931196980871843184102477718222994868871146227723626647922780799537342078278152911914798311 -n 108668334545990970479830295006896189713130895925967616640748329077597367331270081898331902817500875281132044013730978288439662911897275216086061584436294208377005308418511625459641888663535104170301283050164743723169147663825831384213576460268440694211655367192030370799124100994133166946904298566591366829861 --uncipher 26364050768592812267329831409243364374342722934165870014676531400760681813269825349251180430919116864415362398006010117449366543184708373776063540113053603923850148956970405237754630335480513975433483619805767151493363918157022854384842894816591898323309879814189154140909885894080375404704094310124574785369 --attack wiener

[...]

Unciphered data :
HEX : 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007069636f4354467b70726f76696e675f7769656e65725f383635323833387d
INT (big endian) : 198614235373674103788888306985643587194108045477674049828799144970222254205
INT (little endian) : 87932145396148932059615429966149114713997789808065925487271287281462886815524865448021899539131447567413047404880918510626590155170188374485852436456370234251315515770139196911933573438126652677031217132404307795452669075732689656801634329803604086091428855864513651629865994518352500181847559225305454346240
utf-8 : picoCTF{proving_wiener_8652838}
```

Flag: picoCTF{proving_wiener_8652838}