__author__='Syed Sadat Nazrul'

import re
import numpy as np
import csv
import argparse
from itertools import combinations
import matplotlib.pyplot as plt

def get_results(output):
    '''
    :param output: Output file
    :return: Histogram with statistics and Latency data on text file
    '''
    #Parse data
    text_handle=open(output)
    lines=text_handle.readlines()
    text_handle.close()
    data=[]
    for i in range(len(lines)-4):
        if lines[i][0:5]=='comet':
            head=lines[i].split(',')
            info=lines[i+4]
            if info[0]=='1':
                info=float(info.split()[1])
            else:
                info=np.nan
            data.append([head[0],head[1][:-1],info])

    #Text file
    new_text=open(output[0:-4]+'.txt','a')
    for line in data:
        line=line[0]+'\t'+line[1]+'\t'+str(line[2])+'\n'
        new_text.write(line)
    new_text.close()

    #Statistics
    latency=[i[2] for i in data]
    avg=float('{0:0.3f}'.format(np.nanmean(latency)))
    stdev=float('{0:0.3f}'.format(np.nanstd(latency)))
    nancount=latency.count(np.nan)
    latency=[i for i in latency if np.isnan(i)==False]

    #Plot
    hist, bins = np.histogram(latency, bins=10)
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    f=plt.figure()
    ax=f.add_subplot(111)
    ax.bar(center, hist, align='center',width=width)
    ax.set_xlabel(r'Latency Times / (us)')
    ax.set_ylabel('Frequency')
    ax.set_title(output[0:-4])
    plot_text='mean: '+str(avg)+' us\nst. dev.: '+str(stdev)+' us\nNaN: '+str(nancount)
    plt.text(0.8,0.9,plot_text,ha='center',va='center',transform=ax.transAxes)
    plt.savefig(output[0:-4]+'.png',dpi=f.dpi)

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
