# -*- coding: utf-8 -*-

import os # package for accesing file structures
import string # package for manipulating strings
import re # package for regular expressions

# Define function that strips 
def gloss_strip(sub1, sub2, text):
    # initializing substrings
    s=str(re.escape(sub1))
    e=str(re.escape(sub2))
    try:
        res=re.findall(s+"(.*)"+e,text)[0]
    except:
        res="?"
    return res

# Set boolean variable that controlls  morpheme spacing
spacebool = False

# Create glossary of grammatical forms
gram_gloss = {"3pl": [], "3sg": [], "2sg": [], "2pl": [], "1sg": [], "1pl": [], #
"gen": [], "ez": [], "attr": [], "dir": [], "obl": [], #
"f": [], "pl": [], "m": [], "dim": [], #
"def": [], "indf": [], "cmpd": [], "sbjv": [], "ind": [], "pstc": [], "imp": [], "neg": [], #
"prs": [], "pst": [], "ptcp": [], "pvb": [], "povb": [], "compl": [], "adv": [], #
"add": [], "dem": [], "post": [], "cop": [], "nmlz": [], "clf": [], #
"prox": [], "dist": [], "pn": [], "reflx": [], "intj": [], "ptcl": [], "hort": [], "fill": [], "voc": [], "exist": []}

# Create list of examples
ex_list = {"exLabel": ["lab", "sent", "par", "glo", "tra", "clo"]}

sc_list = ["3pl", "3sg", "2sg", "2pl", "1sg", "1pl", #
"gen", "ez", "attr", "dir", "obl", #
"f", "pl", "m", "dim", #
"def", "indf", "cmpd", "sbjv", "ind", "pstc", "imp", "neg", #
"prs", "pst", "ptcp", "pvb", "povb", "compl", "adv", #
"add", "dem", "post", "cop", "nmlz", "clf", #
"prox", "dist", "pn", "reflx", "intj", "ptcl", "hort", "fill", "voc", "exist" #
]

# Select file name
file = "Text_text"

# Open file
readfile = open(file + '.txt', encoding='utf-8')

# Pull glosses
for line in readfile:
    if "label" in line:
        label = gloss_strip("label{", "}", line) # "\ref" + gloss_strip("\label{", "}", line) + "}"
    elif "textsc{" in line:
        for g in sc_list:
            if g in line:
                gram_gloss[g].append(label)

# Open file
readfile = open(file + '.txt', encoding='utf-8')

# Build example entries
for line in readfile:
    if "label" in line:
        label = gloss_strip("label{", "}", line)
        ex_list[label] = [line]
    else:
        try:
            ex_list[label].append(line)
        except:
            pass

# Write examples
for key, item in gram_gloss.items():
    txtfile = open(key + '__examples.tex', 'w', encoding="utf-8")
    txtfile.write("\\chapter{All " + str(len(item)) + " examples of " + key + " in these texts are found in the following sentences:}\n\n")

    if item != []:
        for i in item:
            for line in ex_list[i]:
                txtfile.write(line)
    txtfile.close()