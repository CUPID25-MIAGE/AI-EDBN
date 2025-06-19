from Utils.LogFile import LogFile
from Data.data import Data


def get_data(data_name, sep=",", time="completeTime", case="case", activity="event"):
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    log_files = [os.path.splitext(f)[0] for f in os.listdir(logs_dir) if f.endswith(".py")]
    if data_name in log_files:
        d = Data(data_name, LogFile(all_data[data_name], sep, 0, None, time, case, activity_attr=activity, convert=False))
        d.logfile.keep_attributes([activity, time])
        return d
    print("ERROR: Datafile not found")
    print("ERROR: Possibilities:", ",".join(all_data.keys()))
    raise NotImplementedError



def get_all_data():
    datasets = []
    for d in all_data:
        if d != "BPIC18":
            datasets.append(get_data(d))
    return datasets
