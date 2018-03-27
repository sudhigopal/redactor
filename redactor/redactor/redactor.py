#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os.path
import sys
import argparse
import glob
import nltk
import datefinder
from nltk.tag import StanfordNERTagger
from itertools import chain
from nltk import pos_tag, ne_chunk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize
from pathlib import Path

def concept_redactor(file_input,concept):
    
    sent = nltk.sent_tokenize(file_input)
    synword = wn.synsets(concept) 
    sync = set(chain.from_iterable([word.lemma_names() for word in synword]))
    
    for sen in sent:
        if any(item in sen.lower() for item in sync):
            file_input = file_input.replace(sen,'█'*len(sen))
    
    return file_input

def date_redactor(file_input):
    
    dates_list = []
    matches = datefinder.find_dates(file_input, source = True)
    
    for match in matches:
        dates_list.append(match[1])
    for date in dates_list:
        file_input = file_input.replace(date,"█"*len(date))
    
    return file_input

def name_loc_redactor(file_input,tag):

#    st = StanfordNERTagger('/usr/share/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz',
#            '/usr/share/stanford-ner-2015-04-20/stanford-ner.jar',
#            encoding='utf-8')
    
    chunk = ne_chunk(pos_tag(word_tokenize(file_input)))
    name_list = []
    loc_list = []
    for i in chunk:
        if hasattr(i,'label') and i.label:
            if i.label()=='PERSON':
                name_list.append(' '.join([chunks[0] for chunks in i]))
            if (i.label()=='LOCATION' or i.label()=='GPE'):
                loc_list.append(' '.join([loc_chunk[0] for loc_chunk in i]))
    
    if(tag == '--name'):
        for n in name_list:
            file_input = file_input.replace(n,"█"*len(n))
    if(tag == '--places'):
        for l in loc_list:
            file_input = file_input.replace(l,'█'*len(l))
    
    return file_input

def phone_redactor(file_input):

    phone_re = re.compile('(\+\d{0,3}\s?\(?\d{3}\)?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{4})|(\(?\d{3}\)?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{4})')
    p_list = []
    phone_list = phone_re.findall(file_input)
    
    for i in phone_list:
        if i[0]=='':
            p_list.append(i[1])
        else:
            p_list.append(i[0])
    for n in p_list:
        file_input = (file_input.replace(n,"█"*len(n)))
    
    return file_input

def address_redactor(file_input):
    data = file_input
    address_re = re.compile('[A-Z\s]+?\d{1,6} [A-Z\s]+[\-\/\.]?[A-Z\d]+[A-Z\s]+\-?\d{5}[\-?]\d{4}?|\d{1,6} [A-Z\s]+[\-\/\.]?[A-Z\d]+[A-Z\s]+\-?\d{5}[\-?]\d{4}?|\d{1,6} [A-Z\s]+\-?\d+|\d{1,6} [A-Z\s]+\-?\d+[\-]\d{4}?|')
    
    find = address_re.findall(data)

    for i in find:
        data = data.replace(i,"█"*len(i))
    return data

def gender_redactor(file_input):
    
    gen_list = ['him','she','her','male','female','herself','man','men','women','woman','boy','girl','himself','his','hers','bachelor','bachelorette','actor','actress']
    words = word_tokenize(file_input)
    
    for word in words:
        for gen in gen_list:
            if word.lower()==gen and not None:
                file_input=file_input.replace(word,'█'*len(word))
    
    file_input=re.sub(r'\bhe\b','██',file_input)
    file_input=re.sub(r'\bHe\b','██',file_input)
    file_input=re.sub(r'\bHE\b','██',file_input)

    return file_input

if  __name__=='__main__':
    '''
    Extract all the file names from the path described from the command line argument, and store it in a list.
    '''
    text_file = glob.glob(sys.argv[2],recursive=True)
    other_file = glob.glob(sys.argv[4],recursive=True)
    
    '''
    The next part of the main function help us to give command line arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=str,action='append',required=True,help='Enter the path where files resides')
    parser.add_argument('--names',action='store_true',help='--name flag is required to redact names in the file')
    parser.add_argument('--places',action='store_true',help='--places flag is required to redact places in the file')
    parser.add_argument('--dates',action='store_true',help='--dates flag is required to redact dates in the file')
    parser.add_argument('--addresses',action='store_true',help='--addresses flag is required to redact address in the file')
    parser.add_argument('--phones',action='store_true',help='--phones flag is required to redact phone number in the file')
    parser.add_argument('--genders',action='store_true',help='--genders flag is required to redact gender references in the file')
    parser.add_argument('--concept',type=str,required=True,help='--name flag is required to redact concept in the file')
    parser.add_argument('--output',type=str,required=True,help='Enter the path where you want to write the output')
    args = parser.parse_args()
    
    all_files = text_file+other_file
    
    save_path="files/" #To store the result

    for files in all_files:
        txt_file = open(files,'r')
        file_data = txt_file.read()
        
        '''
        To process the data provided in the command line
        '''

        if(args.names==True):
            file_data = name_loc_redactor(file_data,'--name')
        if(args.places==True):
            file_data = name_loc_redactor(file_data,'--places')
        if(args.addresses==True):
            file_data = address_redactor(file_data)
        if(args.phones==True):
            file_data = phone_redactor(file_data)
        if(args.dates==True):
            file_data = date_redactor(file_data)
        if(args.genders==True):
            file_data = gender_redactor(file_data)
        file_data = concept_redactor(file_data,args.concept)
        
        path = Path(files)        
        #Write to output file and store it in the desired destination

        out_file = os.path.join(save_path,path.name)
        with open(out_file,'w') as tf:
            tf.write(file_data)
