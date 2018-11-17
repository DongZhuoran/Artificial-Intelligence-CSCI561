# -*- coding: utf-8 -*-
try:
    fp = open("input.txt", "r")
    output = open("output.txt", "w")
    for line in fp:
        temp = line.rstrip("\n").split(",")
        if len(temp) == 2:
            if temp[1] == "Dirty":
                output.write("Suck\n")
            elif temp[0] == "A":
                output.write("Right\n")
            elif temp[0] == "B":
                output.write("Left\n")
    # Delete '\n' at the end of the output file.
    output.seek(-1, 1)
    output.truncate()
except IOError:
    pass
else:
    fp.close()
    output.close()