#!/usr/bin/python3
#!/usr/bin/env python3

import re
import csv
import xlsxwriter
import pandas as pd

SR= open("shortreadExactMatchTranscripts.txt")
file1=SR.readlines()

# TO Count number of lines in the file
countFile1=0
for i in file1:
    if i.strip():
        countFile1 +=1
print("Number of lines in file1: ")
print(countFile1)

LR= open("directExactMatchTranscripts.txt")
file2=LR.readlines()

# TO Count number of lines in the file
countFile2=0
for i in file2:
    if i.strip():
        countFile2 +=1
print("Number of lines in file2: ")
print(countFile2)

M=open("mergedDirectExactMatchTranscripts.txt")
file3= M.readlines()

# TO Count number of lines in the file
countFile3=0
for i in file3:
    if i.strip():
        countFile3 +=1
print("Number of lines in file3: ")
print(countFile3)

# Matches column 2 
regexString='\t[A-Za-z,0-9,\\.\\-]{1,100}[|]rna[0-9]{1,100}'
#matches 1st and 2nd column
# regexString= 'TCONS_[0-9]{1,9}\tXLOC_[0-9]{1,9}\t[A-Z,0-9,\\.\\-]{3,100}[|]rna[0-9]{1,6}'
# regexString= "TCONS_[0-9]*\tXLOC_[0-9]{1,9}\t\'?\w+([-']\w+)*[|]rna[0-9]{1,6}"

# Counting matching Regex. Should be same as number of lines in file 1.
shortReadCount=0
for i in file1:
    temp=re.findall(regexString,i)
    if(temp):
        # print(temp)
        shortReadCount +=1
print("Shortread Count")
print(shortReadCount)

# Counting matching Regex. Should be same as number of lines in file 2. 
longReadCount=0
for i in file2:
    temp=re.findall(regexString,i)
    #print(temp)
    if(temp):
        longReadCount +=1
print("Longread count")
print(longReadCount)

# Counting matching Regex. Should be same as number of lines in file 3.
mergedCount=0
for i in file3:
    temp=re.findall(regexString,i)
    if(temp):
    #print(temp)
        mergedCount +=1
print("Merged count")
print(mergedCount)

shortReadCount=0
# Creating a list to store the matched Regex
finalTranscriptId = []

# If regex is matched, it is added in the list
for i in file1:
    temp=re.findall(regexString,i)
    if(temp):
        # print(temp[0])
        finalTranscriptId.append(temp[0])

print("Length of final after Shortreads :")
print(len(finalTranscriptId))

for i in file2:
    temp=re.findall(regexString,i)
    if(temp):
        # print(temp[0])
        finalTranscriptId.append(temp[0])

print("Length of final after longreads :")
print(len(finalTranscriptId))


for i in file3:
    temp=re.findall(regexString,i)
    if(temp):
        # print(temp[0])
        finalTranscriptId.append(temp[0])

print("Length of final after Merged reads :")
print(len(finalTranscriptId))

#Another method to remove duplicates
# res=[]
# for i in finalTranscriptId: 
#     if i not in res: 
#         res.append(i) 
  
# # printing list after removal  
# print ("The list after removing duplicates : ")
# print(len(res))

# Removing Duplicates from final Transcript ID Column list
finalTranscriptId = list(dict.fromkeys(finalTranscriptId))

print("After removing duplicates:")
print(len(finalTranscriptId))
#print(finalTranscriptId)

finalDictionary = []

# Iterating through dictionary
for indexFinal in finalTranscriptId:
    tempDictionary = {}
    tempDictionary['Transcript'] = indexFinal
    # print(indexFinal)
    for indexFile1 in file1:
        if indexFinal in indexFile1:
            tempDictionary['File 1'] = 'Yes'
            # print("Found in File 1")

    for indexFile2 in file2:
        if indexFinal in indexFile2:
            tempDictionary['File 2'] = 'Yes'
            # print("Found in File 2")


    for indexFile3 in file3:
        if indexFinal in indexFile3:
            tempDictionary['File 3'] = 'Yes'
            # print("Found in File 3")

    #print(tempDictionary)
    finalDictionary.append(tempDictionary)
#print(finalDictionary)
#print(len(finalDictionary))


    # for j in range(len(file2)):
    #     if temp[0] in file2[j]:
    #         shortReadCount +=1
        
#print("Shortread Count")
#print(shortReadCount)
print("Writing to File")

finalDictionary= pd.DataFrame(finalDictionary)


writer = pd.ExcelWriter('TranscriptPresence2.xlsx', engine='xlsxwriter')
finalDictionary.to_excel(writer, sheet_name='Sheet1')
writer.save()