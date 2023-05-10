from constants import SUBJECTS, SCRATCH_FOLDER, BANDPOWER_FILENAME, RESULTS_FOLDER

from read import make_raw
from preprocess import preprocess
from extract import extract_features

import pandas as pd

def process_all():
    for sid in SUBJECTS:
        print('')
        print(f'Processing {sid}')
        print('')

        # make_raw(sid)
        
        # preprocess(sid)

        extract_features(sid)

def collect_features():
    dfs = []
    for sid in SUBJECTS:
        print(f'Collecting features for {sid}')
        dfs.append(pd.read_csv(SCRATCH_FOLDER / BANDPOWER_FILENAME.replace('ID', sid)))

    df = pd.concat(dfs)
    print(df.head())
    df.to_csv(RESULTS_FOLDER / 'features.csv', index=False)
    
    
def main():
    # Individual functions
    process_all()
    
    # Collective functions
    collect_features()

if __name__ == '__main__':
    main()