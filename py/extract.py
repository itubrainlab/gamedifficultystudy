import mne
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from constants import SCRATCH_FOLDER, RAW_PREP_FILENAME, BANDPOWER_FILENAME
from configs import configs

def extract_features(id):
    infile = SCRATCH_FOLDER / RAW_PREP_FILENAME.replace('ID', id)
    outfile = SCRATCH_FOLDER / BANDPOWER_FILENAME.replace('ID', id)

    if outfile.exists() and not configs['overwrite']:
        print(f'{outfile.name} already exists for {id}. Skipping.')
        return None
    
    raw = mne.io.read_raw_fif(infile, preload=True).copy()
    picks = mne.pick_types(raw.info, eeg=True, eog=False, stim=False, misc=False)
    
    epos = mne.make_fixed_length_epochs(raw, duration=configs['epo_length'], reject_by_annotation=True, overlap=configs['epo_overlap'])

    test_power = epos.compute_psd(fmin=8,fmax=12, picks=picks).get_data().mean(axis=(1,2))
    good_is = np.where(test_power<np.mean(test_power)*configs['epo_thresh_mult'])[0]
    num_before = len(epos)
    epos = epos[good_is]
    print("\nNumber of epochs after thresholding: ", len(epos), "of", num_before,"\n")

    del test_power

    scores = {}
    for band in configs['bands']:
        power = epos.compute_psd(fmin=configs[f'{band}_min'], fmax=configs[f'{band}_max'], picks=picks)
        data = power.get_data().mean(axis=(1,2)) # average over channels and frequencies
        data_normed = (data - data.mean()) / data.std() # normalize
        scores[band] = data_normed

    # Handle labels from annotations
    def get_conds(x):
        if len(x) == 0:
            return "-/-/-"
        else:
            return x[0][2]
    conds = [get_conds(x) for x in epos.get_annotations_per_epoch()]
    game, diff, session = zip(*[c.split('/') for c in conds])
    scores['game'] = game
    scores['difficulty'] = diff
    scores['session'] = session
    scores['id'] = id
    scores['timestep'] = np.arange(len(epos))
    
    # make dataframe and save
    df = pd.DataFrame(scores)
    print(df.head())
    print(df.shape)
    df.to_csv(outfile, index=False)

def BP_plot(id):
    infile = SCRATCH_FOLDER / BANDPOWER_FILENAME.replace('ID', id)
    df = pd.read_csv(infile)
    # drop rows with "-" in game column
    df = df[df['game'] != '-']
    df = df.groupby(['game', 'difficulty']).mean().reset_index()
    
    games = df['game'].unique()

    # Make a grouped bar chart for each band
    for band in configs['bands']:
        gmeas = {}
        for diff in range(1,4):
            power = df.loc[df["difficulty"] == str(diff), band]
            gmeas[diff] = power.values

        x = np.arange(len(games))  # the label locations
        width = 0.2  # the width of the bars
        multiplier = 0

        fig, ax = plt.subplots(layout='constrained')

        for attribute, measurement in gmeas.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, measurement, width, label=attribute)
            #ax.bar_label(rects, padding=4)
            multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('power')
        ax.set_title(band)
        ax.set_xticks(x + width, games)
        ax.legend(loc='upper left', ncols=3)

    plt.show()

# def BP_plot(id):
#     infile = SCRATCH_FOLDER / BANDPOWER_FILENAME.replace('ID', id)
#     df = pd.read_csv(infile)
#     df = df.groupby(['game', 'difficulty']).mean().reset_index()
#     df = df.melt(id_vars=['game', 'difficulty'], var_name='band', value_name='power')
#     print(df)


if __name__ == '__main__':
    # extract_features(configs['test_id'])
    BP_plot(configs['test_id'])
    print('Done!')