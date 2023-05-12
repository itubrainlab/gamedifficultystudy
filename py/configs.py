
configs = {

    ## General
    'overwrite' : 0,
    'run_ICA' : 1,

    ## Reading
    'testing_duration' : 60*10, # seconds
    'buffer_time' : 1, # seconds

    ## Preprocessing
    'l_freq' : 1,
    'h_freq' : 100, 

    ## ICA
    'ica_variances_explained' : 0.99,
    'ica_method' : 'infomax',
    'random_state' : 42,
    'segmentation_tstep': 4,
    'reject_blink': {'eeg': 1000e-6}, # microvolts

    ## Epoching
    'epo_length': 1,
    'epo_overlap' : 0.1,
    'epo_thresh_mult' : 10,

    ## Bandpower
    'bands' : ['alpha', 'beta', 'gamma'],
    'alpha_min' : 7, 
    'alpha_max' : 13,
    'beta_min' : 12,
    'beta_max' : 30,
    'gamma_min' : 30,
    'gamma_max' : 60,

    'test_id' : 'GD5JC6',
}
