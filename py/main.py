from constants import SUBJECTS, SCRATCH_FOLDER, BANDPOWER_FILENAME, RESULTS_FOLDER

from read import make_raw
from preprocess import preprocess
from extract import extract_features

import pandas as pd

def process_all():
    for id in SUBJECTS:
        print('')
        print(f'Processing {id}')
        print('')

        # make_raw(id)
        
        # preprocess(id)
        
        extract_features(id)

def collect_features():
    dfs = []
    for id in SUBJECTS:
        print(f'Collecting features for {id}')
        dfs.append(pd.read_csv(SCRATCH_FOLDER / BANDPOWER_FILENAME.replace('ID', id)))

    df = pd.concat(dfs)
    print(df.head())
    df.to_csv(RESULTS_FOLDER / 'features.csv', index=False)
    
    
def main():
    process_all()
    collect_features()

if __name__ == '__main__':
    main()