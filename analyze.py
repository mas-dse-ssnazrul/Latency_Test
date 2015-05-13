import re

filename = 'cat.out'
file=open('cat.out')
str2search=''
for message in file:
	str2search += message
word_search=re.search('1\s+([\d\.]+)',str2search)
result=(word_search.group()).split()
result.remove('1')
print result


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


#if __name__ == "__main__":
#    parser = argparse.ArgumentParser(
#        description='''Tool for analysis of Latency Tests''')
#    parser.add_argument(
#        'filenames', metavar='filenames', type=str, nargs="+",
#        help='Files to process. You may use wildcards, e.g., "python analyze.py *.out".')
#    args = parser.parse_args()
#    analyze(args.filenames)
