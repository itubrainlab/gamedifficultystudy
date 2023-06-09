from pathlib import Path
# Recording Constants
SFREQ = 500

# Paths
BASE_PATH = Path(__file__).parent.parent
RAW_FOLDER = BASE_PATH / 'Raw' 
SCRATCH_FOLDER = BASE_PATH / 'Scratch'
RESULTS_FOLDER = BASE_PATH / 'Results'

# Filenames
## RAW
RAW_NEDF_FILENAME = '*_IDsession.edf'
RAW_FILENAME = 'ID_raw.fif'

## PREPROCESSING
RAW_PREP_FILENAME = 'ID_prep_eeg.fif'
CSV_FILENAME = 'subject_data.csv'
ICA_FILENAME = 'ID_ica.fif'

## RESULTS
BANDPOWER_FILENAME = 'ID_bandpower.csv'
FEATURE_FILENAME = 'features.csv'

## SUBJECTS
SUBJECTS = ['GD5JC6', 'MNZ37D', 'D43TCP', 'MKB21T', 'D72PSN',
            'PTS92Q', 'WMS12P', 'QAC39D', 'bluefox45', 'lionheart123',
            'PizzaSlice', 'PSF63U']

ELECTRODES = ['T7', 'O1', 'C1', 'Fp1', 'O2', 'C2', 'Fp2', 'T8']