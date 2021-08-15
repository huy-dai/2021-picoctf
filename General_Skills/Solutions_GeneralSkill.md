# Category: General Skills

## Wave a flag
Points: 10

The problem wanted for us to interact with an .sh file they gave us by passing the -h or --help flag.

````
huydai@huydai-Ubuntu:~/Downloads$ ./warm -h
Oh, help? I actually don't do much, but I do have this flag here: picoCTF{b1scu1ts_4nd_gr4vy_f0668f62}
````

flag: picoCTF{b1scu1ts_4nd_gr4vy_f0668f62}

## Nice Netcat
Points: 15

After running the netcat command, I saw that it gave me about 30-40 lines of numbers, ranging from 10 to 125. Given the hint about the program not speaking English, I thought it was in decimal ASCII encoding. 

Flag: picoCTF{g00d_k1tty!_n1c3_k1tty!_afd5fda4}

## Magickarp Ground Mission
Points: 30

This problem wants us to ssh to a specific VM instance and navigate to different directories (~, /, etc.)

Flag: picoCTF{xxsh_0ut_0f_\/\/4t3r_71be5264}

## Lets Warm Up
Points: 50

The problem ask us to convert hexadecimal 0x70 to ASCII and wrap the answer with 'picoCTF{}'.

Flag: picoCTF{p}

## Warmed Up
Points: 50

The problem ask is to convert 0x3D to decimal and wrap the answer like in previous challenges.

Flag: picoCTF{61}

## The Numbers
Points: 50

We are given an image with a string of numbers and two "{" and "}" symbols in between. Using process of elimination we can infer these numbers represent the location of letters within the alphabet. Thus, we can solve this problem by writing a simple Python script, accounting for them counting 'a' as `1`.

Flag: PICOCTF{THENUMBERSMASON}

## 2 Warm
Points: 50

Need to convert 0d42 to binary.

Flag: picoCTF{101010}

## what's a net cat?

Points: 100

We can connect to a text-based web service using the command:

`nc [address] [port]`

Flag: picoCTF{nEtCat_Mast3ry_3214be47}

## strings it

Points: 100

We can search for ASCII strings in the hex of the file by doing:

~~~console
$ strings strings | grep "pico"
picoCTF{5tRIng5_1T_7f766a23}
~~~

Flag: picoCTF{5tRIng5_1T_7f766a23}