_author_='Syed Sadat Nazrul'

import subprocess
import numpy as np
import re

def combinations(array):
    '''
    Generates every combination of an array
    :param array (list): List of nodes
    :return: combinations (list)
    '''
    combo=[]
    for i in array:
        for j in array:
            if i != j and set([i,j]) not in combo:
                combo.append([i,j])
    return combo

def latency_time(filename):
    '''
    Collects latency value from output file
    :param filename (string): name of output file
    :return: latency times for 1 Mb (CSV file)
    '''

    file=open(filename)
    str2search=''
    for message in file:
	    str2search += message
    word_search=re.search('(?!1\s+)([\d\.]+)',str2search)
    result=(word_search.group()).split()
    return result

def BatchScript(Rack, node1,node2):
    '''
    Generates and submits a batch script for running OMB Latency testing
    :param Node_Pair (int list): The pair of nodes. (int list)
    :return: None
    '''
    #Generate a batch script
    f=open("batch_"+str(node1)+"_"+str(node2), "w")
    description='''
#!/bin/bash
#SBATCH -o %02d-%02d.out
#SBATCH -e %02d-%02d.err
#SBATCH --nodes %d
#SBATCH -w comet-%02d-%02d,comet-%02d-%02d
#SBATCH --ntasks-per-node 1
#SBATCH -t 01:00:00
#SBATCH --mail-type ALL
#SBATCH --mail-user sadatnazrul@gmail.com
#SBATCH -A use300
export BINARY=/home/ssnazrul/mpi_test/osu-micro-benchmarks-4.4.1/mpi/pt2pt/osu_latency
ibrun -v $BINARY
        '''%(node1,node2,node1,node2,2,Rack,node1,Rack,node2)
    f.write(description)
    f.close()
    subprocess.call(["sbatch","batch_script"])
    subprocess.call(["rm","batch_script"])

for i in 3*range(20):
    BatchScript(10,np.linspace(i+1,i+2,3))