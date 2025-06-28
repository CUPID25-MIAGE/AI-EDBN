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
from datetime import datetime

#CONFIGURATION
DATASET_NAME = "train"
SETTINGS = Predictions.setting.DBN


def prepare_data(log=DATASET_NAME, event_mapping=None):
    print("PREPARE DATA")
    data_object = Data.get_data(log)
    data_object.prepare(SETTINGS, event_mapping)
    return data_object.logfile


def train_model(log):
    print("TRAINING MODEL")
    return train(log)



def get_current_row(log, model):
    latest_case_id = log.contextdata.iloc[-1:]["case"].iloc[0]
    trace = log.get_cases().get_group(latest_case_id)
    all_parents, attributes = get_prediction_attributes(model, log.activity)
    current_row = {
        i: [getattr(trace.iloc[-(i + 1)], attr) if len(trace) > i else 0 for attr in attributes]
        for i in range(log.k + 1)
    }
    return current_row, attributes, all_parents, trace

def predict_suffix(log, model, all_parents, attributes, current_row): # ------> function to use for prediction
    predicted_event_int, predicted_event_str, prob_event, explanation = predict_event(
        log,
        all_parents=all_parents,
        attributes=attributes,
        current_row=current_row,
        model=model
    )

    if filter_check(predicted_event_str):
        #current_datetime = datetime.now()
        #formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        #add_new_row_csv([formatted_datetime,predicted_event_str, 0])
        print("Predicted next event (code):", predicted_event_int)
        print("Predicted next event:", predicted_event_str)
        print("Probability of next event:", prob_event)
    else:
        print(f"Predicted {predicted_event_str}, no action to be done.")

    return all_parents, attributes, current_row, explanation
    

coach = False #TO DO: for testing : should be set dynamically (reconnaissance vocale)
explain = True

def main():
    print("===== START PROCESS =====")
    #executed once
    log = prepare_data()
    model = train_model(log)
    model.duplicate_events = {}
    print(log.values)
    event_mapping = log.values[log.activity]
    #TO DO: while true:
    #TO DO: if event received:
    realtime= prepare_data("realtime", log.values)
    current_row, attributes, all_parents, trace = get_current_row(realtime, model)
    all_parents, attributes, current_row, explanation = predict_suffix(
        log,
        model,
        all_parents=all_parents,
        attributes=attributes,
        current_row=current_row
    )
    if explain:
        print("Explanation: ",explanation)
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
        csvLog = prepare_data(csvName, log.values)
        current_row, attributes, all_parents, _ = get_current_row(csvLog, model)
        all_parents, attributes, current_row, explanation = predict_suffix(
            log,
            model,
            all_parents=all_parents,
            attributes=attributes,
            current_row=current_row
        )
        if explain:
            print("Explanation: ",explanation)
            #speak(explanation)
        if coach:
            coach_event(
                model=model,
                all_parents=all_parents,
                attributes=attributes,
                current_row=current_row,
                outcome=log.convert_string2int(log.activity, "lampOn") #TO DO: example, on recupere ca de la reconnaissance vocale
            )


if __name__ == '__main__':
    mainV2()