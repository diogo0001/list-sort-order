#   Autor: Diogo Tavares
#   Projeto: Sistema de ordenação de livros 

import csv
import sys
import json


# Leitura de config.json -------------------------------------------
try:
    config_f = open('config.json')
except:
    print("Não foi possível abrir o arquivo: ",config_f)
    sys.exit(1)

config = json.load(config_f)
config_f.close()

try:
    path = config['path_file']
except:
    print("Não foi possível encontrar 'path_file'")
    sys.exit(1)

try:
    livros_f = open(path)
except:
    print("Não foi possível abrir o arquivo: ",path)
    sys.exit(1)

try:
    dic = config['sort_mode']    
except:
    print("Exceção: Não foi possível encontrar 'sort_mode'")
    sys.exit(1)

# Dados do arquivo para ordenação ------------------------------------
reader = csv.reader(livros_f, delimiter=';')
header = next(reader)                       

index_i = header.index('#')
title_i = header.index('Title')
author_i = header.index('Author')
ed_i = header.index('Edition Year')
data = []

for row in reader:
    index = int(row[index_i])
    title = row[title_i]
    author = row[author_i]
    ed = int(row[ed_i])
    data.append([index,title,author,ed])
        
# print(data)

# Ordenação ----------------------------------------------------------
def output(data):
    for i in range(len(data)):
        print(data[i][0])

if bool(dic)==False:
    print("Nenhum modo de ordenação (vazio)") 

else:
    j = 0
    for key in dic:                                  # Apenas uma das opções deve estar como true em config.json 
        if dic[key]:                                 # será atendida a primeira ocorrência de valor true                      
            if key =='default':                   
                print(key)
                arg = lambda k: k[title_i]           # arg recebe o índice da coluna pela qual será feita a ordenação   
                data.sort(key=arg)
                arg = lambda k: k[author_i]         
                data.sort(key=arg)
                output(data)    
                break 

            if key == 'title_up':
                print(key)
                arg = lambda k: k[title_i]         
                data.sort(key=arg)
                output(data)  
                break

            if key == 'author_up_title_down':
                print(key)
                arg = lambda k: k[title_i]         
                data.sort(key=arg, reverse=True) 
                arg = lambda k: k[author_i]         
                data.sort(key=arg)
                output(data)  
                break

            if key == 'edition_down_author_down_title_up':
                print(key)
                arg = lambda k: k[title_i]         
                data.sort(key=arg)
                arg = lambda k: k[author_i]         
                data.sort(key=arg,reverse=True) 
                arg = lambda k: k[ed_i]         
                data.sort(key=arg,reverse=True)
                output(data)  
                break
                
        else:                                           
            j = j + 1
            if j == len(data):
                print("Nenhum modo de ordenação (vazio)") 
                        
if j != len(data):                          # Caso houve a ordenação
    data.insert(0,header)
    print(data)
    
    with open('lista_ord.csv', mode='w',newline='') as list_ord:
        write_f = csv.writer(list_ord, delimiter=';')
        for row in data:
            write_f.writerow(row)
    