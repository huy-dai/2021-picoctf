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

