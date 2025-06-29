global_variable_sun = 1
global_variable_music = 1
global_variable_shutter_position = 0  # 0 -> closed, 1 -> open

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
    filter_event_to_block = ["doorOpened","doorClosed", "sunUp", "sunDown", "nicolasDetected", "nicolasNotDetected", "presenceOn", "presenceOff", "0"] #0 -> no prediction
    return not (data_to_filter in filter_event_to_block)


def get_time_stamp_case_id():
    import datetime
    now = datetime.datetime.now()
    now_minus_3h = now - datetime.timedelta(hours=4) #reset du case id at 3 pm to next day
    return now_minus_3h.strftime("%Y_%m_%d")

def get_time_stamp_month():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y_%m")

def add_and_create_log(row_data,date, case_id):
    import csv
    import os
    log_name = 'log_' + date + '.csv'
    filepath = 'Data/logs/' + log_name
    row_data.insert(0, case_id)
    if not os.path.exists(filepath):
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['case','completeTime', 'event'])
            writer.writerow(row_data)
    else :
        with open(filepath, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row_data)

def add_new_row_csv(row_data):
    global global_variable_sun
    log_date = get_time_stamp_case_id()
    log_month = get_time_stamp_month()
    add_and_create_log(row_data, log_date,log_date)
    add_and_create_log(row_data, log_month,log_date)

def do_action(action):
    return