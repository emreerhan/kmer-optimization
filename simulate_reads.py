import argparse, os, glob
import pandas as pd


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true')
    # arts_illumina params
    parser.add_argument("name", type=str, help="Name of simulation runs")
    parser.add_argument("reference", type=str, help="The path to the reference to make reads from")
    parser.add_argument("num_simulations", type=int, help="The number of total simulations to run")
    parser.add_argument("-l", "--length", type=int, default=150, help="Length of reads (Default: 150)")
    parser.add_argument("-m", "--frag-length", type=int, default=600, help="Fragment length (Default: 600)")
    parser.add_argument("-f", "--coverage", type=int, default=20, help="Coverage (Default: 20")
    parser.add_argument("-s", "--std-dev", type=int, default=10,
                        help="The standard deviation of DNA/RNA fragment size for paired-end simulations (Default: 10)")
    # ntcard params
    parser.add_argument("-k", "--kmer-range", type=str, default="32,64,96,128",
                        help="Comma delimited, kmer-range (Default: 32,64,96,128)")
    parser.add_argument("-c", "--max-coverage", type=int, default="300",
                        help="the maximum coverage of kmer in output (Default: 300)")
    args = parser.parse_args()
    return args


def main():
    # For internal use:
    genomescope = '/home/eerhan/Software/genomescope/genomescope.R'

    args = parse_args()
    debug = args.debug
    # Simulate reads
    for sim_num in range(1, args.num_simulations+1):
        sim_name = "{}_{}".format(args.name, sim_num)
        # -------------------------------------
        command = 'mkdir {}'.format(sim_name)
        print(command)
        if not debug:
            os.system(command)
        # -------------------------------------
        command = 'cd {}'.format(sim_name)
        print(command)
        if not debug:
            os.chdir(sim_name)
        # -------------------------------------
        command = 'art_illumina -ss HSXt -sam -i {} -p -l {} -f {} -m {} -s {} -o paired_dat > simulation.info'.format(
            args.reference, args.length, args.coverage, args.frag_length, args.std_dev)
        print(command)
        if not debug:
            #print('skipping')
            os.system(command)
        # -------------------------------------
        command = 'mkdir ntcard'
        print(command)
        if not debug:
            os.system(command)
        # -------------------------------------
        command = 'mkdir genomescope'
        print(command)
        if not debug:
            os.system(command)
        # -------------------------------------
        command = 'cd ntcard'
        print(command)
        if not debug:
            os.chdir('ntcard')
        # ntcard ------------------------------
        ntcard_call = 'ntcard -c {} -k {} -t 2 ../paired_dat1.fq ../paired_dat2.fq'.format(
            args.max_coverage, args.kmer_range)
        print(ntcard_call)
        if not debug:
            #print('skipping')
            os.system(ntcard_call)
        # GenomeScope
        for k in args.kmer_range.split(','):
            path = '../genomescope/k{}'.format(k)
            command = 'mkdir {}'.format(path)
            print(command)
            if not debug:
                os.system(command)
            # ----------------------------------
            command = 'cat freq_k{}.hist | sed \'s/\\t/ /g; s/f//g; /F/d\' > formatted_freq_k{}.hist'.format(k, k)
            print(command)
            if not debug:
                os.system(command)
            # ----------------------------------
            command = 'Rscript {} formatted_freq_k{}.hist {} {} ../genomescope/k{} {}'.format(
                genomescope, k, k, args.length, k, args.max_coverage)
            print(command)
            if not debug:
                os.system(command)
        command = 'cd ../..'
        print(command)
        if not debug:
            os.chdir('../..')


if __name__ == '__main__':
    main()
