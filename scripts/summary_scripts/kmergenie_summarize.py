import pandas as pd
import numpy as np
import sys


def main():
    quast_report = sys.argv[1]
    assembly_data = pd.read_csv(quast_report, sep='\t')
    reads = assembly_data['Assembly'].apply(lambda x: x.strip('-contigs'))
    kg_kmers = [] 
    root = '/projects/btl/eerhan/simulated_data/ecoli'
    for read in reads:
        read_dir = read[4:]
        # k = read[:3]
        kmergenie_path = "{}/{}/kmergenie/kg_kmer.txt".format(root, read_dir)
        print(kmergenie_path)
        with open(kmergenie_path) as kgenie_file:
            optimal_k = kgenie_file.readline().rstrip().split(': ')[1]
            kg_kmers.append(int(optimal_k))
            kgenie_file.close()
    kmergenie_data = pd.DataFrame({"kmergenie": pd.Series(kg_kmers, index=reads)}, index=reads)
    kmergenie_data.to_csv('kmergenie_summary.tsv', sep='\t')


if __name__ == "__main__":
    main()
