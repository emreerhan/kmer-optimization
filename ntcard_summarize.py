import pandas as pd
import numpy as np
import sys

def main():
    quast_report = sys.argv[1]
    assembly_data = pd.read_csv(quast_report, sep='\t')
    reads = assembly_data['Assembly'].apply(lambda x: x.strip('-contigs'))
    
    root = '/projects/btl/eerhan/simulated_data/ecoli'
    ntcard_data = pd.DataFrame(dtype=np.float64)
    for read in reads:
        read_dir = read[4:]
        k = read[:3]
        ntcard_path = "{}/{}/ntcard/freq_{}.hist".format(root, read_dir, k)
        temp = pd.read_csv(ntcard_path, sep='\t', index_col=0, header=None, names=["{}_{}".format(k, read_dir)])
        ntcard_data["{}_{}".format(k, read_dir)] = temp["{}_{}".format(k, read_dir)]
    
    ntcard_data = ntcard_data.T
    ntcard_data.to_csv('ntcard_summary.tsv', sep='\t')

if __name__ == "__main__":
    main()
