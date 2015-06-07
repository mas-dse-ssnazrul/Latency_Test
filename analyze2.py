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

def read_nodes(filename):
    '''
    Parse node cluster infromation from file name
    :param filename (string):name of the output file
    :return: [rack, initial node, final node]
    '''
    rack=int(filename[6:8])
    initial_node=int(filename[10:12])
    final_node=int(filename[13:15])
    return [rack, initial_node, final_node]

def parse_latency(filename):
    '''
    :param filename:
    :return:
    '''
    latency_time=[]
    file=open(filename)
    lines=file.readlines()
    for line in range(len(lines)):
        if lines[line][0]=='c':
            if lines[line+4][0]=='1':
                interest_line=lines[line+4].split()
                latency_time.append(interest_line[1])
            else:
                latency_time.append('X')
    file.close()
    return latency_time

def get_results(filename):
    '''
    Generates a CSV file of latency times
    :param filename (string): Name of latency test output file
    :return: CSV file with latency times
    '''
    #Extract Latency from Matrix
    latency_times=parse_latency(filename)
    #Extract info from filename to crate fieldnames
    [rack, node1, node2] = read_nodes(filename)
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
        node_dict['#']='comet-'+str(rack)+'-'+str(matrix_row+node1)
        for matrix_col in range(node2-node1+1):
            node_dict['comet-'+str(rack)+'-'+str(matrix_col+node1)]=matrix[matrix_row][matrix_col]
        writer.writerow(node_dict)
    print '%s created!'%(filename.replace('.out','.csv'))


get_results('comet-19-[55-72].out')