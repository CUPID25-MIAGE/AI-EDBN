def filter_check(data_to_filter): #return false if the result should be filtered out
    filter_event_to_block = ["doorOpened","doorClosed", "sunUp", "sunDown", "nicolasDetected", "nicolasNotDected", "0"] #0 -> no prediction
    return not (data_to_filter in filter_event_to_block)


def get_time_stamp_case_id():
    import datetime
    now = datetime.datetime.now()
    now_minus_3h = now - datetime.timedelta(hours=4) #reset du case id at 3 pm to next day
    return now_minus_3h.strftime("%Y%m%d")