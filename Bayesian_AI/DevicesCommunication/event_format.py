from event import Event

FORMAT_DICTIONARY = {
    "lighton" : "lampOn",
    "lightoff" : "lampOff",
    "dooron" : "doorOpened",
    "dooroff" : "doorClosed",
    "sunbelow_horizon" : "sunDown",
    "sunabove_horizon" : "sunUp",
    "presenceon" : "presenceOn",
    "presenceoff" : "presenceOff",
}

def event_format(data):
    entity = data.get('entity')
    new_state = data.get('new_state')
    timestamp = data.get('time')

    event_name = FORMAT_DICTIONARY.get(entity + new_state)
    return Event(event_name, timestamp)