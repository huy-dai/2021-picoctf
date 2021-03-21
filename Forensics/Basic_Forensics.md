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