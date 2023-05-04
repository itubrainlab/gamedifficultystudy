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
RAW_EDF_FILENAME = '*_ID.edf'

RAW_FILENAME = 'ID_raw.fif'
RAW_PREP_FILENAME = 'ID_eeg.fif'
CSV_FILENAME = 'ID_Data.csv'
ICA_FILENAME = 'ID_ica.fif'
BANDPOWER_FILENAME = 'ID_bandpower.csv'

## SUBJECTS
SUBJECTS = []