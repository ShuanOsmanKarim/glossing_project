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

def gloss_clean(text):
    clean = re.sub("\\\glt ", "", text.strip())
    clean = re.sub("\\\gll ", "", clean)
    clean = re.sub("\\\\\\\\", "", clean)
    clean = re.sub(", ", ",", clean)
    clean = re.sub(" ", ",", clean)
    clean = re.sub("=", ",", clean)
    return clean

def ipa_con(text):
    res = re.sub("=", ",", text)
    res = re.sub("=", ",", res)
    return res



# # Set boolean variable that controlls  morpheme spacing
spacebool = False


sc_list = ["3pl", "3sg", "2sg", "2pl", "1sg", "1pl", #
"gen", "ez", "attr", "dir", "obl", #
# "f", "pl", "m", "dim", #
"\.m",  "\.f", "\.pl", "\.pl", #
"def", "indf", "cmpd", "sbjv", "ind", "pstc", "imp", "neg", #
"prs", "pst", "ptcp", "pvb", "povb", "compl", "adv", "add", "prox", #
# "add", "dem", "post", "cop", "nmlz", "clf", #
# "prox", "dist", "pn", "reflx", "intj", "ptcl", "hort", "fill", "voc", "exist" #
]


dicText = {"word": "glo"}
defList = []
dicRefin = {}

# Select file name
file = "Text_text"

# # Initialize line variables
# opening = ""
label = ""
sentence = ""
words = []
glosses = []
trans = ""
# parsing = ""
# gloss = ""
# translation = ""
# close = ""

# Open file
txtfile = open(file + '_test_dic.txt', 'w', encoding="utf-8")

# Process all dictionary entries
readfile = open(file + '.txt', encoding='utf-8')
for line in readfile:
    if "label" in line:
        label = gloss_strip("label{", "}", line)
    elif "textit" in line:
        sentence = line.strip()
    elif "gll" in line:
        words = gloss_clean(line).split(",")
        # words = remove_items(words, '')
        spacebool = True
    elif spacebool:
        glosses = gloss_clean(line).split(",")
        for i in range(len(glosses)):
            if glosses[i-1].endswith("\\textsc{"):
                glosses[i-1] = glosses[i-1][:-8]
            if glosses[i-1].endswith("\\textsc{"):
                glosses[i-1] = glosses[i-1][:-8]

        spacebool = False
    elif "glt" in line:
        trans = re.sub("\\\glt ", "", line)
        for i in range(len(words)):
            try:
                if glosses[i-1] not in dicText:
                    dicText[glosses[i-1]] = {words[i-1]: ["(" + label[:2] + "." + "\\ref{" + label + "})"]}
                elif words[i-1] not in dicText[glosses[i-1]]:
                    dicText[glosses[i-1]] = {words[i-1]: ["(" + label[:2] + "." + "\\ref{" + label + "})"]}
                else:
                    dicText[glosses[i-1]][words[i-1]].append("(" + label[:2] + "." + "\\ref{" + label + "})")
            except:
                pass
            # print(dicText[glosses[i-1]][words[i-1]])
# print(dicText)
# Create def list
readfile = open(file + '.txt', encoding='utf-8')

for line in readfile:
    if "textsc" in line:
        text = re.sub("\\\\textsc{", "", line)
        for w in sc_list:
            text = re.sub(w, "", text)
        text = re.sub("{|}|,|-|}.", "", text)
        text = re.sub("=", " ", text)
        # text = re.sub(",", "", text)
        # text = re.sub("=", "", text)
        textList = text.strip().split()
        for i in textList:
            if i not in defList:
                defList.append(i)
defList.remove(".")
defList.remove("\\\\")
for i in range(len(defList)):
    # if defList[i-1].endswith("f"):
    #     defList[i-1] = defList[i-1][:-1]
    # if defList[i-1].endswith("m"):
    #     defList[i-1] = defList[i-1][:-1]
    if defList[i-1].startswith("."):
        defList[i-1] = defList[i-1][1:]
    if defList[i-1].endswith("."):
        defList[i-1] = defList[i-1][:-1]
        if defList[i-1].endswith("."):
            defList[i-1] = defList[i-1][:-1]


# print(dicText)
for l in defList:
    ent = ""
    for key1, items1 in dicText.items():
        if l in key1:
            try:
                for key2, items2 in items1.items():
                    # keyClean = re.sub("}.", ".", key1)
                    test = [*key1]
                    if test.count("}") > test.count("{"):
                        key1 = key1[:-1]
                    key2 = re.sub("ā-ā", "ā-(ā)", key2)
                    key2 = re.sub("ā-ē", "(ā)-ē", key2)
                    key2 = re.sub("e-ā", "(e)-ā", key2)
                    key2 = re.sub("ā-e", "ā-(e)", key2)
                    key2 = re.sub("ē-e", "ē-(e)", key2)
                    ent += "\\textit{" + key2 + "} [" + key1 + "] "
                    ent += items2[0] +"; "
                    # print(ent)
                    dicRefin[l] = ent
            except:
                pass
            # print(ent)
# print(dicRefin)

for key, items in dicRefin.items():
    entry = "\entry{}{[\\textipa{}]: " + key +"}{PoS}{" + items[:-2] + "}\n\n"
    # for key2, items2 in items.items():
    #     entry += key2 + " "
    #     for i in items2:
    #         entry += "\\r" + i.strip() + ", "
    #     entry = entry[:-2] 
    # print(entry)
    txtfile.write(entry)

txtfile.close()