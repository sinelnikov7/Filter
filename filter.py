#!/usr/bin/env python3

import argparse
import logging

from opusfilter.opusfilter import OpusFilter
from opusfilter.util import yaml

logging.basicConfig(level=logging.INFO)
logging.getLogger('mosestokenizer.tokenizer.MosesTokenizer').setLevel(logging.WARNING)

parser = argparse.ArgumentParser(prog='opusfilter',
    description='Filter OPUS bitexts')

parser.add_argument('config', metavar='CONFIG', help='YAML configuration file')
parser.add_argument('--overwrite', '-o', help='overwrite existing output files', action='store_true')
parser.add_argument('--last', type=int, default=None, help='Last step to run')
parser.add_argument('--single', type=int, default=None, help='Run only the nth step')
parser.add_argument('--n-jobs', type=int, default=None,
    help='Number of parallel jobs when running score, filter and preprocess.')

args = parser.parse_args()

configuration = yaml.load(open(args.config))

if args.n_jobs is not None:
    configuration['common']['default_n_jobs'] = args.n_jobs

of = OpusFilter(configuration)
if args.single is None:
    of.execute_steps(overwrite=args.overwrite, last=args.last)
else:
    of.execute_step(args.single, overwrite=args.overwrite)
