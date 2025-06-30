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
#from Bayesian_AI.DevicesCommunication.requests import *


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
        """         if predicted_event_str == "lampOn":
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
            request_music_off() """
    else:
        print(f"Predicted {predicted_event_str}, no action to be done.")

    return all_parents, attributes, current_row, explanation, parent_tuple
    

coach = True #TO DO: for testing : should be set dynamically (reconnaissance vocale)
explain = True
logsList = ["realtime_day_of_week", "realtime_weekend"]

def main():
    print("===== START PROCESS =====")
    log = prepare_data()
    model = train_model(log)

    for realtime in logsList:
        #print(f"* Log {realtime} content : ")
        #print_csv_content(realtime)
        #print("\n\n")
        print("\n--------------------------------------------------------------------------\nCURRENT LOG: ",realtime)
        print("--------------------------------------------------------------------------")
        csvLog = prepare_data(realtime, log.values)
        current_row, attributes, all_parents, _ = get_current_row(csvLog, model)
        #predict
        all_parents, attributes, current_row, explanation, parent_tuple = predict_suffix(
            csvLog,
            model,
            all_parents=all_parents,
            attributes=attributes,
            current_row=current_row
        )
        if explain:
            print("Explanation: ",explanation)
            #request_speak(explanation)
        #example of coaching in weekend
        if coach and realtime == "realtime_weekend":
            coached_int=log.convert_string2int(log.activity, "musicOn") 
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
                csvLog,
                model,
                all_parents=all_parents,
                attributes=attributes,
                current_row=current_row
            )


if __name__ == '__main__':
    main()