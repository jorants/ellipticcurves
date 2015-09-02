
import sys
outname = ".".join(sys.argv[1].split(".")[:-1])
data = open(sys.argv[1]).read()

WS = [" ","\t"]
lines = data.split("\n")

blocks = []

block = [lines[0]]


for line in lines[1:]:
    if len(line.strip())<1:
        continue
    if line[0] in WS:
        block+= [line]
    elif len("\n".join(block).strip())>0:
        b = "\n".join(block).strip()
        if (b.startswith("def") or b.startswith("class")):
            blocks+= [b]
        block = [line]


if len("\n".join(block).strip())>0:
    blocks+= ["\n".join(block).strip()]


import os
if not os.path.exists(outname):
    os.mkdir(outname)

for i,b in enumerate(blocks):
    fp = open(os.path.join(outname,"%03i" % i),"w")
    fp.write(b)
    fp.close()

print len(blocks)
