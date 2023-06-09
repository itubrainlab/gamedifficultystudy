import mne
from matplotlib import pyplot as plt

import numpy as np

from constants import SCRATCH_FOLDER, RAW_FILENAME, RAW_PREP_FILENAME, ICA_FILENAME, RESULTS_FOLDER
from configs import configs

id = configs['test_id']
prepfile = SCRATCH_FOLDER / RAW_PREP_FILENAME.replace('ID', id)
rawfile = SCRATCH_FOLDER / RAW_FILENAME.replace('ID', id)

# raw = mne.io.read_raw_fif(rawfile, preload=True).copy()
raw = mne.io.read_raw_fif(prepfile, preload=True).copy()

picks = mne.pick_types(raw.info, eeg=True, eog=False, stim=False, misc=False)


epos = mne.make_fixed_length_epochs(raw, duration=1, reject_by_annotation=True,overlap=0.2)
tester = epos.compute_psd(fmin=8,fmax=12).get_data().mean(axis=2)
print(epos.ch_names[:8])
print(tester.shape)
print(len(epos))

# thresh = 3
# sum(tester>np.mean(tester)*thresh)
# bads = np.where(tester>np.mean(tester)*thresh)[0]
# print(bads,len(bads))

# epos[bads].plot()