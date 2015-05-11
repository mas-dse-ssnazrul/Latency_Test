    Generates every combination of an array

    Args:
        array (list): List of nodes
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

    Args:
        filename (string): name of output file
    '''

    file=open(filename)
    str2search=''
    for message in file:
            str2search += message
    word_search=re.search(pattern,str2search)
    result=(word_search.group()).split()
    result.remove('1')
    return result

def BatchScript(Rack, Node_List):
    '''
    Generates and submits a batch script for running OMB Latency testing

    Args:
        Node_Pair (int list): The pair of nodes. (int list)
    '''
    #Generate a batch script
    f=open("batch_script", "w")
    f.write("#!/bin/bash")
    description='''
#SBATCH -o results.out
#SBATCH -e results.err
#SBATCH --nodes %d
#SBATCH -w comet-%02d-[%02d-%02d]
#SBATCH --ntasks-per-node 1
#SBATCH -t 01:00:00
#SBATCH --mail-type ALL
#SBATCH --mail-user sadatnazrul@gmail.com
#SBATCH -A use300
export BINARY=/home/ssnazrul/mpi_test/osu-micro-benchmarks-4.4.1/mpi/pt2pt/osu_latency
        '''%(len(Node_List),Rack,Node_List[0],Node_List[-1])
    f.write(description)
    Node_Combinations=combinations(Node_List)
    for Node_Pair in Node_Combinations:
        [node1,node2]=Node_Pair
        node1=int(node1)
        node2=int(node2)
        f.write("\n")
        f.write("echo comet-%02d-%02d,comet-%02d-%02d\n"%(Rack,node1,Rack,node2))
        f.write("srun -w comet-%02d-%02d,comet-%02d-%02d -n 2 $BINARY\n"%(Rack,node1,Rack,node2))
    f.close()
    subprocess.call(["sbatch","batch_script"])
#    subprocess.call(["rm","batch_script"])

for i in 3*range(20):
    BatchScript(10,np.linspace(i+1,i+3,3))

