import string


input = [16,9,3,15,3,20,6,20,8,5,14,21,13,2,5,18,19,13,1,19,15,14]
lib  = string.ascii_lowercase
print(lib)
print(lib[16])

out = ""
for val in input:
    out += lib[val-1]

print(out.upper())
