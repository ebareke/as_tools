import argparse
import os

def parse_args():
    # parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_folder', required=True)
    parser.add_argument('--output_folder', required=True)
    parser.add_argument('--coverage_cutoff', type=int, required=True)
    parser.add_argument('--ild_cutoff', type=float, required=True)
    parser.add_argument('--fdr_cutoff', type=float, required=True)
    return parser.parse_args()

def check_files(input_folder):
    # check if all 5 required files are present in the input folder
    required_files = ['SE.MATS.JC.txt', 'RI.MATS.JC.txt', 'A3SS.MATS.JC.txt', 
                      'A5SS.MATS.JC.txt', 'MXE.MATS.JC.txt']
    for f in required_files:
        if not os.path.exists(os.path.join(input_folder, f)):
            raise ValueError(f'{f} not found in input folder')

def compute_event_length(event_type, event_coords):
    # compute length of event based on event type and coordinates
    if event_type == 'SE':
        return event_coords['exonEnd'] - event_coords['exonStart_0base']
    elif event_type == 'RI':
        return event_coords['riExonEnd'] - event_coords['riExonStart_0base']
    elif event_type == 'A3SS':
        return event_coords['longExonEnd'] - event_coords['longExonStart_0base']
    elif event_type == 'A5SS':
        return event_coords['longExonEnd'] - event_coords['longExonStart_0base']
    elif event_type == 'MXE':
        return event_coords['2ndExonEnd'] - event_coords['1stExonStart_0base']
    else:
        raise ValueError(f'Unrecognized event type: {event_type}')

def compute_coverage(inc_counts, skip_counts):
    # compute coverage as sum of inclusion and skipping counts
    return sum(inc_counts) + sum(skip_counts)

def determine_significance(pvalue, fdr):
    # determine if event is significant based on pvalue and fdr cutoffs
    if pvalue < args.fdr_cutoff and fdr < args.fdr_cutoff:
        return 'significant'
    else:
        return 'not significant'

def process_input_file(input_file, event_type, output_folder, coverage_cutoff, ild_cutoff, fdr_cutoff):
    # open input file and output file for writing
    with open(input_file, 'r') as f_in, open(os.path.join(output_folder, f'{event_type}.ALL.JC.txt'), 'w') as f
