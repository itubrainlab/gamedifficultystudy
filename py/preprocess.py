import mne

import numpy as np

from constants import SCRATCH_FOLDER, RAW_FILENAME, RAW_PREP_FILENAME, ICA_FILENAME, RESULTS_FOLDER
from configs import configs


def preprocess(id):
    infile = SCRATCH_FOLDER / RAW_FILENAME.replace('ID', id)
    outfile = SCRATCH_FOLDER / RAW_PREP_FILENAME.replace('ID', id)
    ica_file = SCRATCH_FOLDER / ICA_FILENAME.replace('ID', id)

    if outfile.exists() and not configs['overwrite']:
        print(f'{outfile.name} already exists for {id}. Skipping.')
        return None
    
    raw = mne.io.read_raw_fif(infile, preload=True).copy()

    picks = mne.pick_types(raw.info, eeg=True, eog=False, stim=False, misc=False)
    raw.notch_filter(np.arange(50, 250, 50), picks=picks, filter_length='auto',phase='zero')
    raw.filter(configs['l_freq'], configs['h_freq'], fir_design='firwin', phase='zero', picks=picks)

    if configs['run_ICA']:
        ica = run_ICA(raw)
        ica.save(ica_file, overwrite=True)
    else:
        ica = mne.preprocessing.read_ica(ica_file)
    raw = ica.apply(raw)
    
    
    raw.save(outfile, overwrite=True)

def run_ICA(raw):
    
    # Set parameters from configs
    ica_variances_explained = configs['ica_variances_explained']
    random_state = configs['random_state']
    t_step = configs['segmentation_tstep']
    
    # Get subject info
    s_info = raw.info['subject_info']['his_id']

    # Get rejection threshold
    events = mne.make_fixed_length_events(raw, duration=t_step)
    epochs = mne.Epochs(raw, events, tmin=0, tmax=t_step, baseline=None, preload=True, reject=None, reject_by_annotation=False)
    # threshold = get_rejection_threshold(epochs)
    threshold = configs['reject_blink']
    print(f'Rejection threshold: {threshold}')

    # Drop bad epochs based on threshold
    epochs.drop_bad(reject=threshold)

    # Run ICA
    ica = mne.preprocessing.ICA(n_components=ica_variances_explained,
                                method=configs['ica_method'],
                                random_state=random_state) 
    ica.fit(epochs, tstep=t_step)

    # Plot components and sources
    # Set title for plots
    title = f'ICA - {s_info}'
    components_fig = ica.plot_components(show=True, title=f'{title} - components')[0]
    components_fig.savefig(RESULTS_FOLDER / 'ica' / f'{title} - components.png')

    sources_fig = ica.plot_sources(raw, show=False, title=f'{title} - sources', show_scrollbars=True, start=10, stop=50)
    sources_fig.savefig(RESULTS_FOLDER / 'ica' / f'{title} - sources.png')

    # Manually select components to exclude
    blink_component = input()
    ica.exclude = [int(x) for x in blink_component.split(',')]

    return ica


def test():
    preprocess('bdaFDd')

if __name__ == '__main__':
    test()

