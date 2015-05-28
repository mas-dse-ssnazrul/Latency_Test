__author__='Syed Sadat Nazrul'

import re
import numpy as np
import csv

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
    return combo

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
    word_search=re.findall('(1\s+)([\d\.]+)',str2search)
    for sub_group in word_search:
        if '1\n' not in sub_group:
            latency_times.append(float(sub_group[1]))
    #Extract info from filename to crate fieldnames
    rack=int(filename[6:8])
    node1=int(filename[10:12])
    node2=int(filename[13:15])
    array=combinations(np.linspace(node1,node2, node2-node1+1))
    fieldnames=['#']
    fieldnames+=['comet-'+str(rack)+'-'+str(int(i)) for i in np.linspace(node1,node2, node2-node1+1)]
    #Matrix of latency times
    matrix=np.zeros((node2-node1+1,node2-node1+1))
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
        node_dict['#']='comet-'+str(rack)+'-'+str(int(first_node))
        for matrix_col in range(node2-node1+1):
            node_dict['comet-'+str(rack)+'-'+str(matrix_col+node1)]=matrix[matrix_col][matrix_row]
        writer.writerow(node_dict)
    print '%s created!'%(filename.replace('.out','.csv'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''Tool for analysis of Latency Tests''')
    parser.add_argument(
        'filenames', metavar='filenames', type=str, nargs="+",
        help='Files to process. You may use wildcards, e.g., "python analyze.py *.out".')
    args = parser.parse_args()
    analyze(args.filenames)
