import mne
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from constants import SCRATCH_FOLDER, RAW_PREP_FILENAME, BANDPOWER_FILENAME
from configs import configs

def extract_features(sid):
    infile = SCRATCH_FOLDER / RAW_PREP_FILENAME.replace('ID', sid)
    outfile = SCRATCH_FOLDER / BANDPOWER_FILENAME.replace('ID', sid)

    if outfile.exists() and not configs['overwrite']:
        print(f'{outfile.name} already exists for {sid}. Skipping.')
        return None
    
    raw = mne.io.read_raw_fif(infile, preload=True).copy()
    picks = mne.pick_types(raw.info, eeg=True, eog=False, stim=False, misc=False)
    
    epos = mne.make_fixed_length_epochs(raw, duration=configs['epo_length'], reject_by_annotation=True, overlap=configs['epo_overlap'])

    # testing_epos = epos[np.array(conds) == 'TESTING']
    # exp_epos = epos[np.array(conds) != 'TESTING']

    thresh_power = epos.compute_psd(fmin=8,fmax=12, picks=picks).get_data().mean(axis=(1,2))
    good_is = np.where(thresh_power<np.mean(thresh_power)*configs['epo_thresh_mult'])[0]
    epos = epos[good_is]

    # test_power = testing_epos.compute_psd(fmin=8,fmax=12, picks=picks).get_data().mean(axis=(1,2))
    # good_is = np.where(test_power<np.mean(thresh_power)*configs['epo_thresh_mult'])[0]
    # testing_epos = testing_epos[good_is]
    # quarter = int(len(testing_epos)/4)
    # testing_epos = testing_epos[quarter:-quarter]

    scores = {}
    # Handle labels from annotations
    def get_cond(x):
        if len(x) == 0:
            return '-/-/-'
        else:
            return x[0][2]
    exp_conds = [get_cond(x) for x in epos.get_annotations_per_epoch()]
    uniqs = np.unique(exp_conds)
    if len(uniqs) < 25:
        print('BAD number')
        quit()

    game, diff, session = zip(*[c.split('/') for c in exp_conds if (c != 'TESTING' and c!= 'BAD_QUESTIONNAIRE')])
    scores['game'] = game
    scores['difficulty'] = diff
    scores['session'] = session
    scores['id'] = [sid] * len(epos)
    scores['timestep'] = np.arange(len(epos))

    # Make a df with bandpower for each epoch
    bp_dfs = []
    for band in configs['bands']:
        power = epos.compute_psd(fmin=configs[f'{band}_min'], fmax=configs[f'{band}_max'], picks=picks)
        data = power.get_data().mean(axis=2) # average over frequencies - shape: (n_epochs,channels,frequencies)

        # Calc baseline for testing_epos
        baseline_power = epos.compute_psd(fmin=configs[f'{band}_min'], fmax=configs[f'{band}_max'], picks=picks).get_data().mean(axis=2)
        baseline_mean = baseline_power.mean(axis=0)
        baseline_std = baseline_power.std(axis=0)

        data_normed = (data - baseline_mean) / baseline_std # normalize
        scores['band'] = band
        for i, ch in enumerate(epos.ch_names[:8]):
            scores[ch] = data_normed[:,i]

        bp_df = pd.DataFrame(scores)
        bp_dfs.append(bp_df)
    
    df = pd.concat(bp_dfs)
    df.to_csv(outfile, index=False)


if __name__ == '__main__':
    extract_features(configs['test_id'])
    print('Done!')