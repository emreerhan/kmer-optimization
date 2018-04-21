import pandas as pd
import numpy as np
import sys, os

def main():
    quast_report = sys.argv[1]
    assembly_data = pd.read_csv(quast_report, sep='\t')
    reads = assembly_data['Assembly'].apply(lambda x: x.strip('-contigs'))
    root = '/projects/btl/eerhan/simulated_data/ecoli'
    genomescope_data = pd.DataFrame()
    for read in reads:
        read_dir = read[4:]
        k = read[:3]
        genomescope_path = "{}/{}/genomescope/k{}/summary.tsv".format(root, read_dir, k)
        if os.stat('genomescope_path').st_size != 0:
            temp = pd.read_csv(genomescope_path, sep='\t', header=2, index_col=0, usecols=[0, 1, 2])
            temp = temp.T.loc[:, ['Genome Haploid Length', 'Genome Repeat Length', 'Genome Unique Length']]
            temp = temp.applymap(lambda x: x.replace(',',''))
            temp = temp.apply(pd.to_numeric)
            average = temp.apply(np.mean)
            average.name = '{}_{}'.format(k, read_dir)
            genomescope_data.append(average)
    genomescope_data.to_csv('genomescope_summary.tsv', sep='\t')


if __name__ == '__main__':
    main()
