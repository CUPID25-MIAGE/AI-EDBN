from Utils.LogFile import LogFile
from Data.data import Data
import os

logs_dir = os.path.join(os.path.dirname(__file__), "logs")
log_files = [os.path.splitext(f)[0] for f in os.listdir(logs_dir) if f.endswith(".csv")]

def get_data(data_name, sep=",", time="completeTime", case="case", activity="event"):   
    if data_name in log_files:
        file_path = file_path = os.path.join(logs_dir, data_name + ".csv")
        d = Data(data_name, LogFile(file_path, sep, 0, None, time, case, activity_attr=activity, convert=False))
        d.logfile.keep_attributes([activity, time])
        return d
    print("ERROR: Datafile not found")
    print("ERROR: Possibilities:", ",".join(log_files))
    raise NotImplementedError



def get_all_data():
    datasets = []
    for d in log_files:
        datasets.append(get_data(d))
    return datasets
