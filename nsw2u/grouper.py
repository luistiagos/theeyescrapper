import pandas as pd
import csv
import ast

def read_switchroms():
    # read the csv file into a pandas dataframe
    df = pd.read_csv('switchroms2.csv', sep=';', error_bad_lines=False, encoding='utf-8')
    # group the data by name and aggregate the links as a list
    grouped = df.groupby('title')['links'].agg(list)
    # convert the series back to a dataframe
    df_new = grouped.to_frame().reset_index()
    df = df.sort_values(by='title')
    # write the new dataframe to a csv file
    df_new.to_csv('output_file.csv', index=False)
    
def group():
    with open('output_file.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        with open('jogos_switch.csv', 'w+', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            for row in csv_reader:
                arr = [row[0]]
                for r in ast.literal_eval(row[1]):
                    arr.append(r)
                writer.writerow(arr)
                
def divide_base_update():
    df = pd.read_csv('jogos_switch.csv', sep=';', error_bad_lines=False, encoding='utf-8')
    df_update = df[df.iloc[:,0].str.contains("Update")]
    df_update.to_csv('jogos_switch_atualizacoes.csv', index=False)
    df_dlc = df[~df.iloc[:,0].str.contains("Update") & df.iloc[:,0].str.contains("DLC")]
    df_dlc.to_csv('jogos_switch_dlc.csv', index=False)
    df_base = df[~df.iloc[:,0].str.contains("Update|DLC")]
    df_base.to_csv('jogos_switch_base.csv', index=False)

divide_base_update()
#read_switchroms()
#group()
    
    
    