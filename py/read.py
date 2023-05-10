
import mne

import pandas as pd

from datetime import datetime

from constants import RAW_NEDF_FILENAME, RAW_FILENAME, RAW_FOLDER, SCRATCH_FOLDER, CSV_FILENAME
from configs import configs

def make_raw(sid):
    csv_file = RAW_FOLDER / CSV_FILENAME

    session_raw = []
    for session in ['1','2']:
        session_replace = "" if session == '1' else session
        raw_filename = RAW_NEDF_FILENAME.replace('ID', sid)
        raw_filename = raw_filename.replace('session', session_replace)

        infile = list(RAW_FOLDER.glob(raw_filename))[0]
        outfile = SCRATCH_FOLDER / RAW_FILENAME.replace('ID', sid)
       
        if outfile.exists() and not configs['overwrite']:
            print(f'raw.fif already exists for {sid}. Skipping.')
            return None

        raw = mne.io.read_raw_edf(infile).copy()
        raw.set_channel_types({'X': 'misc', 'Y': 'misc', 'Z': 'misc'})

        # Set montage
        montage = mne.channels.make_standard_montage('standard_1020')
        raw.set_montage(montage)
        
        raw.info['subject_info'] = {'his_id':sid}

        df = pd.read_csv(csv_file)
        df = df[df['Player'] == sid]
        df = df[df['Session'] == int(session)]

        raw = annotate_outofexperiment(raw, df, session)
        session_raw.append(raw)

    raw = mne.concatenate_raws(session_raw)
    raw.save(outfile, overwrite=True)


def annotate_outofexperiment(raw, df, session):
    def to_timedelta(timestamp):
        return (datetime.fromtimestamp(timestamp/1000)-begintime).total_seconds()
    
    begintime = raw.info['meas_date'].replace(tzinfo=None)

    # get timestamps from csv, convert to seconds
    timestamps = getTimestamps(df)
    datetime_list = [(to_timedelta(t1), to_timedelta(t2)) for t1,t2 in timestamps.values()]

    # Annotate bad out of experiment
    annotations = []
    for i in range(len(datetime_list)-1):
        start = datetime_list[i][1]
        dur = datetime_list[i+1][0] - start
        annotations.append((start, dur, 'BAD_QUESTIONNAIRE'))

    ## Anotate conditions in experiment
    for cond, times in timestamps.items():
        diff = cond[-1]
        game = cond[:-1]
        start = to_timedelta(times[0])
        dur = to_timedelta(times[1]) - start
        annotations.append((start, dur, f'{game}/{diff}/{session}'))
    
    # Make it into separate lists and make annotations
    starts, durs, labels = zip(*annotations)

    experiment_start = datetime_list[0][0]
    
    # if session == '1':
    #     # Mark testing time
    #     testing_duration = configs['testing_duration']
    #     experiment_start = experiment_start - testing_duration
    #     experiment_start = max(60, experiment_start)

    #     starts = list(starts)
    #     durs = list(durs)
    #     labels = list(labels)
    #     starts.append(experiment_start)
    #     durs.append(testing_duration)
    #     labels.append('TESTING')

    annotations = mne.Annotations(onset=starts, duration=durs, description=labels)
    raw.set_annotations(annotations)

    # Crop raw to before and after experiment and testing
    raw = raw.crop(tmin=experiment_start-1, tmax=datetime_list[-1][1])
    return raw

def getTimestamps(df):
    timestamps = {}
    for _, row in df.iterrows():
        cond = row['MiniGame'] + str(row['Version'])
        timestamps[cond] = (row['First_TimeStamp'],row['Last_Timestamp'])
    return timestamps


def test():
    make_raw(configs['test_id'])

if __name__ == '__main__':
    test()