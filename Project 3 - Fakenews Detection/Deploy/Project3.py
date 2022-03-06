import pandas as pd
import re
import numpy as np
import nltk
import csv

df = pd.DataFrame()

def count_para(text):
    num_paragraph = text.replace("\n\n", "\n").rstrip().split("\n")
    return len(num_paragraph)


def num_of_letter_in_paragraph(text):
    num_letter = 0
    num_letter += len(text.split(" "))
    return num_letter/count_para(text)


VnEmoLex = pd.read_excel("./data/VnEmoLex.xlsx")
list_positive = VnEmoLex[VnEmoLex["Positive"] == 1]["Vietnamese"]
list_negative = VnEmoLex[VnEmoLex["Negative"] == 1]["Vietnamese"]




def dem_positive(text):
    counter = 0
    for item in list_positive:
        if re.search(item, text) != None:
            counter+=1
    return counter



def dem_negative(text):
    counter = 0
    for item in list_negative:
        if re.search(item, text) != None:
            counter+=1
    return counter




def count_image(text):
    patterns = [r' Hình:',
                r'- Ảnh',
                r' Hinh Anh:',
                r' Anh:', 
           ]

    counter = 0
    for pat in patterns:
        counter += len(re.findall(pat, text))
    return counter

def count_date(text):
    num_date=0
    a=re.findall(r'\b([1-9]|1[0-9]|2[0-9]|3[0-1])\b([\/\-])\b([1-9]|1[0-2])\b',text)
    num_date=num_date+len(a)
    return num_date

#Đếm số lượng số dương trong câu, tỉ lệ số bắt đầu bằng chữ số 1
def count_pos_num(text):
    arrTemp=text.split(' ')
    count=0
    for k in range(0,len(arrTemp)):
        arrTemp[k] =  arrTemp[k].replace(".", "")
        arrTemp[k] =  arrTemp[k].replace(",", "")
        if arrTemp[k].isdigit():
            count=count+1
    return count
def average_count_num_begin_1(text):
    arrTemp=text.split(' ')
    count=0
    for k in range(0,len(arrTemp)):
        arrTemp[k] =  arrTemp[k].replace(".", "")
        arrTemp[k] =  arrTemp[k].replace(",", "")
        if arrTemp[k][0]=='1':
            count=count+1
    return count/count_pos_num(text)

vnese_alphabet = ['a', 'á', 'à', 'ạ', 'ã', 'ả', 'ă', 'ắ', 'ằ', 'ặ', 'ẵ', 'ẳ', 'â', 'ấ', 'ầ', 'ậ', 'ẫ', 'ẩ', 'b', 'c', 'd', 'đ', 'e', 'é', 'è', 'ẹ', 'ẽ', 'ẻ', 'ê', 'ế', 'ề', 'ệ', 'ễ', 'ể', 'g', 'h', 'i', 'í', 'ì', 'ị', 'ĩ', 'ỉ', 'k', 'l', 'm', 'n', 'o', 'ó', 'ò', 'ọ', 'õ', 'ỏ', 'ô', 'ố', 'ồ', 'ộ', 'ỗ', 'ổ', 'ơ', 'ớ', 'ờ', 'ợ', 'ỡ', 'ở', 'p', 'q', 'r', 's', 't', 'u', 'ú', 'ù', 'ụ', 'ũ', 'ủ', 'ư', 'ứ', 'ừ', 'ự', 'ữ', 'ử', 'v', 'x', 'y', 'ý', 'ỳ', 'ỵ', 'ỹ', 'ỷ', 
                  'A', 'Á', 'À', 'Ạ', 'Ã', 'Ả', 'Ă', 'Ắ', 'Ằ', 'Ặ', 'Ẵ', 'Ẳ', 'Â', 'Ấ', 'Ầ', 'Ậ', 'Ẫ', 'Ẩ', 'B', 'C', 'D', 'Đ', 'E', 'É', 'È', 'Ẹ', 'Ẽ', 'Ẻ', 'Ê', 'Ế', 'Ề', 'Ệ', 'Ễ', 'Ể', 'G', 'H', 'I', 'Í', 'Ì', 'Ị', 'Ĩ', 'Ỉ', 'K', 'L', 'M', 'N', 'O', 'Ó', 'Ò', 'Ọ', 'Õ', 'Ỏ', 'Ô', 'Ố', 'Ồ', 'Ộ', 'Ỗ', 'Ổ', 'Ơ', 'Ớ', 'Ờ', 'Ợ', 'Ỡ', 'Ở', 'P', 'Q', 'R', 'S', 'T', 'U', 'Ú', 'Ù', 'Ụ', 'Ũ', 'Ủ', 'Ư', 'Ứ', 'Ừ', 'Ự', 'Ữ', 'Ử', 'V', 'X', 'Y', 'Ý', 'Ỳ', 'Ỵ', 'Ỹ', 'Ỷ']
eng_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def count_char_not_num(text):
    num_char=0
    for c in text:
        if (c in vnese_alphabet or c in eng_alphabet):
            num_char += 1
    return num_char

f_dic=open("./data/VDic_uni.txt","r",encoding="utf8").readlines()
for i in range(len(f_dic)):
    f_dic[i]=f_dic[i].replace("\n","")
    f_dic[i] = f_dic[i].split('\t', 1)[0]

def word_separate(sen):
    wlist = []
    char = ''
    char1 =''
    for word in sen.split(' '):
        char += word
        if char not in f_dic: 
            wlist.append(char1)
            char = word
        char1 = char
        char += ' '
    wlist.append(char1)
    if ',' in wlist:
        wlist.remove(',')
    if '' in wlist:
        wlist.remove('')
    if '.' in wlist:
        wlist.remove('.')
    return wlist

def word_in_paragraph(text):
    num_word = 0
    num_paragraph = text.replace("\n\n", "\n").rstrip().split("\n")
    for i in num_paragraph:
        num_word += len(word_separate(i))
    return num_word/len(num_paragraph)

def countwordtype(tags):
    countNN=0
    for tag in tags:
        if tag[1]=="NN":
            countNN=countNN+1
        elif tag[1]=="NNP":
            countNN=countNN+1
    return countNN

def countnoun(text):
    count=0
    num_paragraph = text.replace("\n\n", "\n").rstrip().split("\n")
    for i in num_paragraph:
        tokens = nltk.word_tokenize(i)
        text1= nltk.Text(tokens)
        tags= nltk.pos_tag(text1)
        count=count+countwordtype(tags)
    return count

num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def averge_num_char(text):
    count_num=0
    for cha in text:
        if cha in num:
            count_num += 1
    return (count_num/len(text))*100




text=open("./data/text.txt","r",encoding="utf8").read()
df["count_paragraph"]=[count_para(text)]
df["average_words_in_paragraph"]=[num_of_letter_in_paragraph(text)]
df["count_positive"]=[dem_positive(text)]
df["count_negative"]=[dem_negative(text)]
df["count_image"]=[count_image(text)]
df["count_date"]=[count_date(text)]
df["num_num_in_df"]=[count_pos_num(text)]
df["percent_num_start_1"]=[average_count_num_begin_1(text)]
df["average_words"]=[word_in_paragraph(text)]
df["noun"]=[countnoun(text)]
df["num_per_cha(%)"]=[averge_num_char(text)]
print(df)
df.to_csv('./data/input.csv',index=False)