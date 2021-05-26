#Category: Forensics

##Weird File
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
