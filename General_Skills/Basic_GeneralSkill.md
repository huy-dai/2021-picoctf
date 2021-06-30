#Category: General Skills

##Wave a flag
Points: 10

The problem wanted for us to interact with an .sh file they gave us by passing the -h or --help flag.

````
huydai@huydai-Ubuntu:~/Downloads$ ./warm -h
Oh, help? I actually don't do much, but I do have this flag here: picoCTF{b1scu1ts_4nd_gr4vy_f0668f62}
````

flag: picoCTF{b1scu1ts_4nd_gr4vy_f0668f62}

##Nice Netcat
Points: 15

After running the netcat command, I saw that it gave me about 30-40 lines of numbers, ranging from 10 to 125. Given the hint about the program not speaking English, I thought it was in decimal ASCII encoding. Trying that got some of the letters translated, but not all, so I switched to decimal to UTF-8 encoding instead.

Flag: picoCTF{g00d_k1tty!_n1c3_k1tty!_afd5fda4}

##Magickarp Ground Mission
#Points: 30

This problem wants us to ssh to a specific VM instance and navigate to different directories (~, /, etc.)

Flag: picoCTF{xxsh_0ut_0f_\/\/4t3r_71be5264}