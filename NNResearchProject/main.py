import functions
import numpy as np
from config import max_letters, language_tags
import pandas as pd

word_data = []
language_data = []
master_dic = []


def doAll():
    count = 0
    for tag in language_tags.keys():
        print('generating dictionary for ' + tag)
        dic = functions.generate_dictionary(tag, max_letters)
        for word in dic:
            master_dic.append(word)
            #print(word)
            #print(len(master_dic))
        vct = functions.convert_dic_to_vector(dic, max_letters)
        for vector in vct:
            word_data.append(vector)
        output_vct = functions.create_output_vector(count, len(language_tags))
        for i in range(len(vct)):
            language_data.append(output_vct)
        count += 1


    arr = []
    for i in range(len(word_data)):
        entry = []
        entry.append(master_dic[i])
        for digit in language_data[i]:
            entry.append(float(digit))
        for digit in word_data[i]:
            entry.append(float(digit))
        arr.append(entry)
    return arr

#print(len(master_dic))
arra = doAll()
print("Saving to arr.npy")
arr = np.array(arra)
np.save('arr.npy', arr)
df=pd.DataFrame(arr)
df.to_csv('data.csv')
