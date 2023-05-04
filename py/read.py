
import mne

from datetime import datetime

from constants import RAW_EDF_FILENAME, RAW_FILENAME, RAW_FOLDER, SCRATCH_FOLDER, CSV_FILENAME
from configs import configs

def make_raw(id):
    infile = list(RAW_FOLDER.glob(RAW_EDF_FILENAME.replace('ID', id)))[0]
    outfile = SCRATCH_FOLDER / RAW_FILENAME.replace('ID', id)
    csv_file = RAW_FOLDER / CSV_FILENAME.replace('ID',id)

    if outfile.exists() and not configs['overwrite']:
        print(f'raw.fif already exists for {id}. Skipping.')
        return None

    raw = mne.io.read_raw_edf(infile)
    raw.set_channel_types({'X': 'misc', 'Y': 'misc', 'Z': 'misc'})

    # Set montage
    montage = mne.channels.make_standard_montage('standard_1020')
    raw.set_montage(montage)
    
    raw.info['subject_info'] = {'his_id':id}

    raw = annotate_outofexperiment(raw, csv_file)
    
    raw.save(outfile, overwrite=True)


def annotate_outofexperiment(raw, csv_file):
    def to_timedelta(timestamp):
        return (datetime.fromtimestamp(timestamp/1000)-begintime).total_seconds()
    
    begintime = raw.info['meas_date'].replace(tzinfo=None)
    timestamps = getTimestamps(csv_file)
    datetime_list = [(to_timedelta(t1), to_timedelta(t2)) for t1,t2 in timestamps.values()]

    annotations = []
    for i in range(len(datetime_list)-1):
        start = datetime_list[i][1]
        dur = datetime_list[i+1][0] - start
        annotations.append((start, dur, 'BAD_OUT'))

    ## Anotate conditions in experiment
    for cond, times in timestamps.items():
        diff = cond[-1]
        game = cond[:-1]
        start = to_timedelta(times[0])
        dur = to_timedelta(times[1]) - start
        annotations.append((start, dur, f'{game}/{diff}'))
    
    # Make it into separate lists and make annotations
    starts, durs, labels = zip(*annotations)
    annotations = mne.Annotations(onset=starts, duration=durs, description=labels)
    raw.set_annotations(annotations)

    # Crop raw to before and after experiment
    raw = raw.crop(tmin=datetime_list[0][0]-1, tmax=datetime_list[-1][1]+1)
    return raw


def getTimestamps(filePathcsv: str, hasHeader = False) -> dict[str ,(int, int)]:
    file = open(filePathcsv)
    dic_timestamp = {}

    if (hasHeader):
        lines = file.readlines()[1:]
    else:
        lines = file.readlines()   
  
    for line in lines:
        if (not line.strip() and line):
            continue # skip empty lines
        parts = line.split(",")

        game_version = parts[0] + parts[1]
        startTime = parts[3]
        endTime = parts[4]
        dic_timestamp[game_version] = (int(startTime), int(endTime))
    return dic_timestamp


def test():
    make_raw('bdaFDd')

if __name__ == '__main__':
    test()