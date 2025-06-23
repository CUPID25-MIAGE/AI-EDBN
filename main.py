from Methods.EDBN import Predictions as edbn_predict
from Methods.EDBN.Train import train
from Methods.EDBN.Predictions import (
    learn_duplicated_events,
    predict_next_event_row,
    predict_case_suffix_loop_threshold,
    get_prediction_attributes,
    predict_event,
    coach_event
)
import Predictions.setting
import Data
from Utils.LogFile import LogFile
from helper import *


#CONFIGURATION
DATASET_NAME = "train"
SETTINGS = Predictions.setting.DBN


def prepare_data(filename=DATASET_NAME):
    print("PREPARE DATA")
    data_object = Data.get_data(filename)
    data_object.prepare(SETTINGS)
    return data_object.logfile


def train_model(log):
    print("TRAINING MODEL")
    return train(log)



def get_current_row(log, model, activity_attr):
    latest_case_id = log.contextdata.iloc[-1:]["case"].iloc[0]
    trace = log.get_cases().get_group(latest_case_id)
    all_parents, attributes = get_prediction_attributes(model, activity_attr)
    current_row = {
        i: [getattr(trace.iloc[-(i + 1)], attr) if len(trace) > i else 0 for attr in attributes]
        for i in range(log.k + 1)
    }
    return current_row, attributes, all_parents, trace


def predict_suffix(log, model): # ------> function to use for prediction
    model.duplicate_events = {}
    current_row, attributes, all_parents, trace = get_current_row(log, model, log.activity)
    predicted_event_int, predicted_event_str, prob_event, explanation = predict_event(
        log,
        all_parents=all_parents,
        attributes=attributes,
        current_row=current_row,
        model=model
    )

    if filter_check(predicted_event_str):
        from datetime import datetime
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        add_new_row_csv([formatted_datetime,predicted_event_str, 0])
        print("Predicted next event (code):", predicted_event_int)
        print("Predicted next event:", predicted_event_str)
        print("Probability of next event:", prob_event)
        print("Explanation: ",explanation)
    else:
        print("No action to be done.")

    return all_parents, attributes, current_row
    

coach = True #TO DO: for testing : should be set dynamically (reconnaissance vocale)

def main():
    print("===== START PROCESS =====")
    #executed once
    log = prepare_data()
    model = train_model(log)

    #TO DO: while true:
    #TO DO: if event received:
    all_parents, attributes, current_row = predict_suffix(log, model)
    if coach:
        coach_event(
            model=model,
            all_parents=all_parents,
            attributes=attributes,
            current_row=current_row,
            outcome=log.convert_string2int(log.activity, "lampOn") #TO DO: example, on recupere ca de la reconnaissance vocale
        )

def mainV2():
    print("===== START PROCESS =====")
    #executed once
    log = prepare_data()
    model = train_model(log)

    #TO DO: while true:
    #TO DO: if event received:
    while(True):
        csvName = input("enter csv name to predict (or 'exit' to quit): ")
        csvLog = prepare_data(csvName)
        all_parents, attributes, current_row = predict_suffix(csvLog, model)
        if coach:
            coach_event(
                model=model,
                all_parents=all_parents,
                attributes=attributes,
                current_row=current_row,
                outcome=log.convert_string2int(log.activity, "lampOn") #TO DO: example, on recupere ca de la reconnaissance vocale
            )


if __name__ == '__main__':
    main()
