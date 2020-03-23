import pickle
import numpy as np
import nudat_scrape as nscrape

data = nscrape.nuclear_quantity("2", "+", [80, 80], [50, 62], parameter="Energy", number=1)

#write the data as txt file, Neutrons Protons energy deltaenergy
with open("file.txt", "w") as f:
    for s in data:
        f.write(str(s[1]) +" "+ str(s[2]) +" "+ str(s[3][0]) +" "+ str(s[3][1]) +"\n")