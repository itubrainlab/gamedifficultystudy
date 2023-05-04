from datetime import datetime
from constants import RESULTS_FOLDER

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

configs = {

    'exp_name' : 'test',
    'timestamp' : timestamp,
    'overwrite' : 0,

    'run_ICA' : 1,

    ## Preprocessing
    'l_freq' : 1,
    'h_freq' : 70, 

    ## ICA
    'ica_variances_explained' : 0.99,
    'ica_method' : 'infomax',
    'random_state' : 42,
    'segmentation_tstep': 4,
    'reject_blink': {'eeg': 1000e-6}, # microvolts

    ## Epoching
    'epo_length': 1,
    'epo_overlap' : 0.2,
    'epo_thresh_mult' : 3,

    ## Bandpower
    'bands' : ['alpha', 'beta', 'gamma'],
    'alpha_min' : 8, 
    'alpha_max' : 12,
    'beta_min' : 12,
    'beta_max' : 30,
    'gamma_min' : 30,
    'gamma_max' : 60,

    'test_id' : 'GD5JC6',
}

# def make_config_file(exp_folder):
#     config_file = exp_folder / 'config.txt'
#     with open(config_file, 'w') as f:
#         for key, value in configs.items():
#             f.write(f'{key}: {value}\n\n')
# 
# exp_folder = RESULTS_FOLDER / f'{configs["exp_name"]}_{timestamp}'