from Methods.EDBN import Predictions as edbn_predict
from Methods.EDBN.Train import train, update
from Methods.EDBN.Predictions import (
    get_prediction_attributes,
    predict_event,
    coach_event
)
import Predictions.setting
import Data
from Utils.LogFile import LogFile
from helper import *
from datetime import datetime
from Bayesian_AI.DevicesCommunication.requests import *


#CONFIGURATION
DATASET_NAME = "train_v5"
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
    predicted_event_int, predicted_event_str, prob_event, explanation, parent_tuple = predict_event(
        log,
        all_parents=all_parents,
        attributes=attributes,
        current_row=current_row,
        model=model
    )

    if filter_check(predicted_event_str):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        add_new_row_csv([formatted_datetime,predicted_event_str, 0])
        
        print("Predicted next event (code):", predicted_event_int)
        print("Predicted next event:", predicted_event_str)
        print("Probability of next event:", prob_event)
        if predicted_event_str == "lampOn":
            request_lamp_on()
        elif predicted_event_str == "lampOff":
            request_lamp_off()
        elif predicted_event_str == "blindsOpen":
            request_shutter_open()
        elif predicted_event_str == "blindsClosed":
            request_shutter_close()
        elif predicted_event_str == "musicOn":
            request_music_on()
        elif predicted_event_str == "musicOff":
            request_music_off()
    else:
        print(f"Predicted {predicted_event_str}, no action to be done.")

    return all_parents, attributes, current_row, explanation, parent_tuple
    

coach = True #TO DO: for testing : should be set dynamically (reconnaissance vocale)
explain = True
logsList = ["realtime_day_of_week", "realtime_weekend"]

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
    sauvegard = ""
    while(True):
        csvName = input("enter csv name to predict (or 'exit' to quit): ")
        csvLog = prepare_data(csvName, log.values)

        """         #to be deleted
        print("----------------------mapping realtime: ")
        if "event" in log.values:
            for i, val in enumerate(csvLog.values["event"], 1): 
                print(f"{val} -> {i}")
        else:
            print("No mapping found for 'event'")
         """
        
        current_row, attributes, all_parents, _ = get_current_row(csvLog, model)
        all_parents, attributes, current_row, explanation, parent_tuple = predict_suffix(
            log,
            model,
            all_parents=all_parents,
            attributes=attributes,
            current_row=current_row
        )
        # 
        if explain:
            print("Explanation: ",explanation)
            request_speak(explanation)
        if coach:
            coached_int = log.convert_string2int(log.activity, "lampOn")
            coach_event(
                model=model,
                all_parents=all_parents,
                attributes=attributes,
                current_row=current_row,
                outcome=coached_int #TO DO: example, on recupere ca de la reconnaissance vocale
            )
            #save_coach_model(parent_tuple, coached_int)
            
            #model=update(model, csvLog)
            """ print("\n--------------------PREDICTION AFTER UPDATING: ")
            current_row, attributes, all_parents, _ = get_current_row(csvLog, model)
            all_parents, attributes, current_row, explanation, parent_tuple = predict_suffix(
                log,
                model,
                all_parents=all_parents,
                attributes=attributes,
                current_row=current_row
            )


            model=update_coach_model(model)
            current_row, attributes, all_parents, _ = get_current_row(csvLog, model)
            print("\n--------------------PREDICTION AFTER UPDATE+COACH: ")
            all_parents, attributes, current_row, explanation, parent_tuple = predict_suffix(
                log,
                model,
                all_parents=all_parents,
                attributes=attributes,
                current_row=current_row
            )
 """

            #to do: add car j'etais coaché à faire ça.. dasn explanation


def mainV3():
    log = prepare_data()
    model = train_model(log)
    lastLine = ""

    while True:
        line, log_name = get_last_line_csv()
        if (lastLine == "") or line!=lastLine:
            csvLog = prepare_data(log_name, log.values)
            current_row, attributes, all_parents, _ = get_current_row(csvLog, model)

            all_parents, attributes, current_row, explanation, parent_tuple = predict_suffix(
                log,
                model,
                all_parents=all_parents,
                attributes=attributes,
                current_row=current_row
            )
            if explain:
                print("Explanation: ",explanation)
                request_speak(explanation)
            if coach:
                coached_int = log.convert_string2int(log.activity, "lampOn")
                coach_event(
                    model=model,
                    all_parents=all_parents,
                    attributes=attributes,
                    current_row=current_row,
                    outcome=coached_int #TO DO: example, on recupere ca de la reconnaissance vocale
                )
        lastLine = line

def mainV4():
    print("===== START PROCESS =====")
    log = prepare_data()
    model = train_model(log)

    for realtime in logsList:
        csvLog = prepare_data(realtime, log.values)
        #TO DO: print content of the csv
        current_row, attributes, all_parents, _ = get_current_row(csvLog, model)
        #predict
        all_parents, attributes, current_row, explanation, parent_tuple = predict_suffix(
            log,
            model,
            all_parents=all_parents,
            attributes=attributes,
            current_row=current_row
        )
        if explain:
            print("Explanation: ",explanation)
            request_speak(explanation)
        #example of coaching in weekend
        if coach and realtime == "realtime_weekend":
            coached_int = log.convert_string2int(log.activity, "musicOn")
            coach_event(
                model=model,
                all_parents=all_parents,
                attributes=attributes,
                current_row=current_row,
                outcome=coached_int 
            )
            #predict
            current_row, attributes, all_parents, _ = get_current_row(csvLog, model)
            all_parents, attributes, current_row, explanation, parent_tuple = predict_suffix(
                log,
                model,
                all_parents=all_parents,
                attributes=attributes,
                current_row=current_row
            )


if __name__ == '__main__':
    mainV2()