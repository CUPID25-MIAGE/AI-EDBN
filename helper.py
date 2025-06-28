global_variable_sun = 1

def sun_up():
    global global_variable_sun
    global_variable_sun = 1
    print("Sun is up")
    return global_variable_sun
def sun_down():
    global global_variable_sun
    global_variable_sun = 0
    print("Sun is down")
    return global_variable_sun

def filter_check(data_to_filter): #return false if the result should be filtered out
    filter_event_to_block = ["doorOpened","doorClosed", "sunUp", "sunDown", "nicolasDetected", "nicolasNotDected", "0"] #0 -> no prediction
    return data_to_filter not in filter_event_to_block


def get_time_stamp_case_id():
    import datetime
    now = datetime.datetime.now()
    now_minus_3h = now - datetime.timedelta(hours=4) #reset du case id at 3 pm to next day
    return now_minus_3h.strftime("%Y%m%d")

def add_new_row_csv(row_data):
    global global_variable_sun
    import csv
    import os
    log_date = get_time_stamp_case_id()
    log_name = 'log_' + log_date + '.csv'
    filepath = 'Data/logs/' + log_name
    row_data.insert(0, log_date)
    row_data.insert(3, global_variable_sun)
    if not os.path.exists(filepath):
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['case_id','completeTime', 'event','sunUp'])
            writer.writerow(row_data)
    else :
        with open(filepath, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row_data)

def do_action(action):
    return