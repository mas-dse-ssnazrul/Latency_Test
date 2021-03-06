__author__='Syed Sadat Nazrul'

import re
import numpy as np
import csv
import argparse

def combinations(array):
    '''
    Generates every combination of an array
    :param array (list): List of nodes
    :return: combinations ([[list]])
    '''
    combo=[]
    for i in array:
        for j in array:
            if i != j and set([i,j]) not in combo:
                combo.append([i,j])
    combo1=[]
    [combo1.append(x) for x in combo if set(x) not in combo]
    return combo1

def get_results(filename):
    '''
    Generates a CSV file of latency times
    :param filename (string): Name of latency test output file
    :return: CSV file with latency times
    '''
    #Extract Latency from Matrix
    file=open(filename)
    str2search=''
    latency_times=[]
    for message in file:
        str2search += message
    file.close()
    pattern=re.compile('^1\s+([\d.]+)$',re.M)
    word_search=re.findall(pattern,str2search)
    latency_times=[float(i) for i in word_search]
    #Extract info from filename to crate fieldnames
    rack=int(filename[6:8])
    node1=int(filename[10:12])
    node2=int(filename[13:15])
    array=combinations(np.linspace(node1,node2, node2-node1+1))
    fieldnames=['#']
    fieldnames+=['comet-'+str(rack)+'-'+str(int(i)) for i in np.linspace(node1,node2, node2-node1+1)]
    #Matrix of latency times
    matrix=np.zeros((node2-node1+1,node2-node1+1))
 
    print node1
    print node2
    print len(latency_times)
    print latency_times
    print len(array)
    print array


    for first_node in np.linspace(node1,node2, node2-node1+1):
        for combo in array:
            if combo[0]==first_node:
                node_pair_index=array.index(combo)
                matrix[combo[0]-node1][combo[1]-node1]=latency_times[node_pair_index]
                matrix[combo[1]-node1][combo[0]-node1]=latency_times[node_pair_index]
    #Creation of CSV file
    csvfile = open(filename.replace('.out','.csv'), 'w')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow(dict((fn,fn) for fn in fieldnames))
    for matrix_row in range(node2-node1+1):
        node_dict={}
        node_dict['#']='comet-'+str(rack)+'-'+str(matrix_row+node1)
        for matrix_col in range(node2-node1+1):
            node_dict['comet-'+str(rack)+'-'+str(matrix_col+node1)]=matrix[matrix_row][matrix_col]
        writer.writerow(node_dict)
    print '%s created!'%(filename.replace('.out','.csv'))

def analyze(filenames):
   '''
   Takes in filenames from arg parser and runs them through get_results()
   :param: filenames of latency output files
   :return: CSV file with latency times
   '''
   for f in filenames:
	get_results(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''Tool for analysis of Latency Tests''')
    parser.add_argument(
        'filenames', metavar='filenames', type=str, nargs="+",
        help='Files to process. You may use wildcards, e.g., "python analyze.py *.out".')
    args = parser.parse_args()
    analyze(args.filenames)
