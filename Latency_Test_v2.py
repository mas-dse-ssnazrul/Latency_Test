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

def BatchScript(Rack, Node_List):
    '''
    Generates and submits a batch script for running OMB Latency testing
    :param Node_Pair (int list): The pair of nodes. (int list)
    :return: None
    '''
    #Generate a batch script
    f=open("batch_script", "w")
    f.write("#!/bin/bash")
    description='''
#SBATCH --job-name=comet-%02d-[%02d-%02d]
#SBATCH -o comet-%02d-[%02d-%02d].out
#SBATCH -e comet-%02d-[%02d-%02d].err
#SBATCH --nodes %d
#SBATCH -w comet-%02d-[%02d-%02d]
#SBATCH --ntasks-per-node 1
#SBATCH -t 01:00:00
#SBATCH --mail-type END, FAIL
#SBATCH --mail-user sadatnazrul@gmail.com
#SBATCH -A use300
export BINARY=/home/ssnazrul/mpi_test/osu-micro-benchmarks-4.4.1/mpi/pt2pt/osu_latency
        '''%(
            Rack, Node_List[0], Node_List[-1],     #Job Name
            Rack, Node_List[0], Node_List[-1],     #Output File
            Rack, Node_List[0], Node_List[-1],     #Error File
            len(Node_List),                        #Number of Nodes
            Rack, Node_List[0], Node_List[-1]      #Node list
    )
    f.write(description)
    Node_Combinations=combinations(Node_List)
    for Node_Pair in Node_Combinations:
        [node1,node2]=Node_Pair
        node1=int(node1)
        node2=int(node2)
        f.write("\n")
        f.write("echo comet-%02d-%02d,comet-%02d-%02d\n"%(Rack,node1,Rack,node2))
        f.write("srun -w comet-%02d-%02d,comet-%02d-%02d -N 2 -n 2  --mpi=pmi2 $BINARY\n"%(Rack,node1,Rack,node2))
    f.write("python analyze.py *out")
    f.close()
    subprocess.call(["sbatch","batch_script"])     #Submit Batch Script
    subprocess.call(["rm","batch_script"])         #Delete Batch Script after submission

#Running latency test
racks=[int(i) for i in np.linspace(1,29,29)]
racks.remove(9)
racks.remove(24)
for rack in racks:
    BatchScript(10,np.linspace(1,18,18))
    BatchScript(10,np.linspace(19,36,18))
    BatchScript(10,np.linspace(37,54,18))
    BatchScript(10,np.linspace(55,72,18))
