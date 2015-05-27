import re
import numpy as np
import csv

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

def analyze(filenames):
    fieldnames=['#']
    fieldnames+=[str(i) for i in np.linspace(1,18,18)]
    csvfile = open('results.csv', 'w')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for f in filenames:
        r = get_results(f)
        r["#"] = f
        writer.writerow(r)
    print("Results written to results.csv!")



filename='comet-17-[12-14].out'
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

rack=int(filename[6:8])
node1=int(filename[10:12])
node2=int(filename[13:15])
array=combinations(np.linspace(node1,node2, node2-node1+1))
fieldnames=['#']
fieldnames+=['comet-'+str(rack)+'-'+str(i) for i in np.linspace(node1,node2, node2-node1+1)]
csvfile = open('results.csv', 'w')
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writerow(dict((fn,fn) for fn in fieldnames))

for first_node in np.linspace(node1,node2, node2-node1+1):
    writer.writerow({'#':'comet-'+str(rack)+'-'+str(first_node)})
    for combo in array:
        if combo[0]==first_node:
            node_pair_index=array.index(combo)
#            writer.writerow({'#':first_node,str(array[node_pair_index][1]):latency_times[node_pair_index]})


print rack

#if __name__ == "__main__":
#    parser = argparse.ArgumentParser(
#        description='''Tool for analysis of Latency Tests''')
#    parser.add_argument(
#        'filenames', metavar='filenames', type=str, nargs="+",
#        help='Files to process. You may use wildcards, e.g., "python analyze.py *.out".')
#    args = parser.parse_args()
#    analyze(args.filenames)
