# Category: Forensics

## Weird File
Points: 20

If we want for a document to run arbitary code, we can do so through macros. Opening the file normally with macros enabled (generally a bad idea, but I trust PicoCTF here) gives us a table and an image, but nothing interesting.

Opening the macro editor in LibreOffice showed us the following code:

````
Rem Attribute VBA_ModuleType=VBADocumentModule
Option VBASupport 1
Sub AutoOpen()
    MsgBox "Macros can run any program", 0, "Title"
    Signature

End Sub
 
 Sub Signature()
    Selection.TypeText Text:="some text"
    Selection.TypeParagraph
    
 End Sub
 
 Sub runpython()

Dim Ret_Val
Args = """" '"""
Ret_Val = Shell("python -c 'print(\"cGljb0NURnttNGNyMHNfcl9kNG5nM3IwdXN9\")'" & " " & Args, vbNormalFocus)
If Ret_Val = 0 Then
   MsgBox "Couldn't run python script!", vbOKOnly
End If
End Sub
````

In particular, the Python print line is worth investigating into. If you de-escape the quotes and convert from Base64 to ASCII, you get the flag.

Flag: picoCTF{m4cr0s_r_d4ng3r0us}

##Information
Points: 10

Initial inspection of the file with `file`, `strings` and `xxd` commands did not seem to yield anything new. Since the hint suggested the flag is hidden in the metadata, I ran the `exiftool` commmand on it.

Unbeknownst to me until after the competition, the flag was base64 encoded in the "License" tag.
It was in plain sight all along.


```
grayhimakar@grayhimakar-VirtualBox:~/Downloads$ exiftool cat.jpeg 
ExifTool Version Number         : 11.88
File Name                       : cat.jpeg
Directory                       : .
File Size                       : 858 kB
File Modification Date/Time     : 2021:05:25 22:36:33-04:00
File Access Date/Time           : 2021:05:25 22:37:06-04:00
File Inode Change Date/Time     : 2021:05:25 22:37:05-04:00
File Permissions                : rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.02
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Current IPTC Digest             : 7a78f3d9cfb1ce42ab5a3aa30573d617
Copyright Notice                : PicoCTF
Application Record Version      : 4
XMP Toolkit                     : Image::ExifTool 10.80
License                         : cGljb0NURnt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9
Rights                          : PicoCTF
Image Width                     : 2560
Image Height                    : 1598
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 2560x1598

grayhimakar@grayhimakar-VirtualBox:~/Downloads$ echo "cGljb0NURnt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9" | base64 -d
picoCTF{the_m3tadata_1s_modified}
```

Flag: picoCTF{the_m3tadata_1s_modified}

## Matryoshka doll
Points: 30

We are given a file `dolls.jpg`. However, when we try to open this with Image Viewer, we get the error of "Error interpreting JPEG image file (Not a JPEG file: starts with 0x89 0x50)". This indicates to us that this file is being obfuscated as an image.

We can use the tool binwalk, which according to the Kali Linux website, is used for "searching a given binary image for embedded files and executable code."

~~~~~
grayhimakar@grayhimakar-VirtualBox:~/Downloads$ binwalk dolls.jpg 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 594 x 1104, 8-bit/color RGBA, non-interlaced
3226          0xC9A           TIFF image data, big-endian, offset of first image directory: 8
272492        0x4286C         Zip archive data, at least v2.0 to extract, compressed size: 378950, uncompressed size: 383938, name: base_images/2_c.jpg
651608        0x9F158         End of Zip archive, footer length: 22
~~~~~
From binwalk we can see that the file is actually a zip archive. If we change the file's extension to .zip and extract it, it produces a folder with another image inside. From the hint, we also know this new .jpg file is also a zip archive.

I ended up creating a bash script that repeatedly unzips the nested image until we arrived at the flag file. This is the main while loop:
~~~~~~sh
while [ -d $FOLDER ]
do
    echo "$FOLDER exists on your filesystem."
    cd ./base_images
    unzip -o *
done
echo "Flag found!"
cat flag.txt 
~~~~~~
Turns out the nesting only goes four directories deep, but it was good practice for learning how to write a simple Bash script that repeatedly unzips files.

Flag: picoCTF{4f11048e83ffc7d342a15bd2309b47de}


##tunn3l v1s10n
#Points: 40

We are given a file named "tunn3l_v1s10n" without a file extension. If we try to open it directly, we get the error "BMP image has unsupported header size". If we run `exiftool` on this file, we do indeed see that it detected it as a bitmap (.bmp) image.

From the error that we received, we can try to analyze the image header and see if anything is out of the ordinary. A useful reference guide to have is the Bitmap File Format: https://en.wikipedia.org/wiki/BMP_file_format#DIBs_in_memory 

One of the things that point out right away is the "BAD00000" (x2) entry in the header. The people who created this image likely had messed with the values here. If we take a look at the reference article, we can see that the first entry refers to the the offset of the byte where the bitmap image data can be found, where the second entry is the size of the DIB header (which, accordingly to the article, is usually 40 bytes nowadays).

The bitmap image data comes after the Bitmap File Header and DIB header, which are 14 bytes and 40 bytes, respectively (`0d14 + 0d40 = 0d54 = 0x36`)

Similarly, for the DIB header size: `0d40 = 0x28`. 
Altogether, we can replace the "BAD00000" with the right values
~~~~~
BA D0 00 00 => 36 00 00 00
BA D0 00 00 => 28 00 00 00
~~~~~
If we try to open the file with these changes, we get a partial image with the text "notaflag{sorry}". If we go back to exiftool, we can see that the "Image Length" seems to be much greater than the given dimensions of the file. Since the width of the image seems fine, we can assume that it's the image height metadata that is incorrect.

We can calculate the length of a single pixel row for this image to be:
```(1134*3)+(1134 mod 4) = 3404```. 

The reason why we multipled by 3 is because of the rgb representation. The mod tackled at the end accounts for the byte padding that BMP images tacks on.
If we divide the Image Length by this pixel row length, we see that our image should be ```2893400 / 3404 = 850``` pixels tall. The location of this metadata, according to the ref, is at offset 0x16 for 4 bytes. 850 is 0x325 in hexadecimal, and when accounted for little endianess, we know to write "25 03 00 00" at that location.

With this last change, the full image is now revealed to us.

Flag: picoCTF{qu1t3_a_v13w_2020}

# Glory of the Garden
Points: 70

Based on the hint we know we have to use a hex editor on the image. The flag was included at the end of the hexdump output. We could have also use "strings garden.jpg" to solve the problem.

Flag: picoCTF{more_than_m33ts_the_3y33dd2eEF5}

# Wireshark doo dooo do doo...
Points: 50

We were given a pcap file to analyze with Wireshark. If we follow the TCP streams, in stream #4 we see the following packet:

~~~~~~~
HTTP/1.1 200 OK
Date: Mon, 10 Aug 2020 01:51:45 GMT
Server: Apache/2.4.29 (Ubuntu)
Last-Modified: Fri, 07 Aug 2020 00:45:02 GMT
ETag: "2f-5ac3eea4fcf01"
Accept-Ranges: bytes
Content-Length: 47
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html

Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}
~~~~~~~

If we apply ROT-13 decoding to the last line, we get the following bacl `The flag is picoCTF{p33kab00_1_s33_u_deadbeef}`.
Another way we could have solved this problem is by exporting the HTTP packets (File -> Export Objects -> HTTP), cd into that folder, and run "file *". From the output we can see that a few special files marked as ASCII text. If we cat a file named "instance-action" we will get the the same packet that we saw before.

Flag: picoCTF{p33kab00_1_s33_u_deadbeef}

# MacroHard WeakEdge
Points: 60

In this problem we are given a .pptm file. At first glance we would think that the problem involves macros, but when we inspect the macro code in LibreOffice we find the following:

~~~~~~~
Rem Attribute VBA_ModuleType=VBAModule
Sub Module1
Rem Sub not_flag()
Rem     Dim not_flag As String
Rem     not_flag = "sorry_but_this_isn't_it"
Rem End Sub
Rem 
End Sub
~~~~~~~~

Interestingly, one thing we should note about Powerpoint files is that they can be extracted like Zip files. This behavior can be confirmed by running `binwalk` on the file. Note: This is only a portion of the complete output.
~~~~~~~~
sed size: 387, uncompressed size: 811, name: ppt/viewProps.xml
86808         0x15318         Zip archive data, at least v2.0 to extract, compressed size: 172, uncompressed size: 182, name: ppt/tableStyles.xml
87029         0x153F5         Zip archive data, at least v2.0 to extract, compressed size: 342, uncompressed size: 666, name: docProps/core.xml
87682         0x15682         Zip archive data, at least v2.0 to extract, compressed size: 556, uncompressed size: 3784, name: docProps/app.xml
88548         0x159E4         Zip archive data, at least v2.0 to extract, compressed size: 81, uncompressed size: 99, name: ppt/slideMasters/hidden
100071        0x186E7         End of Zip archive, footer length: 22
~~~~~~~~

If we `unzip` the file and take a look through the different directories, we would find a cryptic message in ppt/slideMasters/hidden:

`Z m x h Z z o g c G l j b 0 N U R n t E M W R f d V 9 r b j B 3 X 3 B w d H N f c l 9 6 M X A 1 f Q`

This appears to be base64 encoding. We can remove all the spacing with Python .replace(" ","") and then use a base64 to ascii decoder.

Editor's Note: I still don't understand what the 'WeakEdge' part of the problem title is referring to.

Flag: picoCTF{D1d_u_kn0w_ppts_r_z1p5}