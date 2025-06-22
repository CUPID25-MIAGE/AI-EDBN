from explanation import explain_last_prediction
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
from explanation import *
import pandas as pd


#CONFIGURATION
DATASET_NAME = "events_with_context"
SETTINGS = Predictions.setting.DBN


def prepare_data():
    print("PREPARE DATA")
    data_object = Data.get_data(DATASET_NAME)
    data_object.prepare(SETTINGS)
    return data_object.logfile


def train_model(log):
    print("TRAINING MODEL")
    return train(log)


def predict_next_event_row(log, model): #used for testing the model
    print("=== TEST: Predict next event for a single row ===")
    context_row = log.contextdata.iloc[-1:]
    row_tuple = list(context_row.iterrows())[0]

    true_val, predicted_val, confidence, true_prob = predict_next_event_row(
        row_tuple, log, model=model, activity=log.activity
    )

    print("True next event:", log.convert_int2string(log.activity, true_val))
    print("Predicted event:", log.convert_int2string(log.activity, predicted_val))
    print("Confidence:", confidence)
    print("Probability assigned to true label:", true_prob)


def get_current_row(log, model, activity_attr):
    latest_case_id = log.contextdata.iloc[-1:]["case"].iloc[0]
    trace = log.get_cases().get_group(latest_case_id)
    all_parents, attributes = get_prediction_attributes(model, activity_attr)
    current_row = {
        i: [getattr(trace.iloc[-(i + 1)], attr) if len(trace) > i else 0 for attr in attributes]
        for i in range(log.k + 1)
    }
    return current_row, attributes, all_parents, trace


def predict_suffix_threshold(log, model): # ------> function to use for prediction
    #print("=== TEST: Predict case suffix with loop threshold ===")
    #print("event mapping:", log.values["event"])
    #learn duplicate events threshold
    model.duplicate_events = {}
    current_row, attributes, all_parents, trace = get_current_row(log, model, log.activity)
    predicted_event_int, predicted_event_str, prob_event = predict_event(
        log,
        all_parents=all_parents,
        attributes=attributes,
        current_row=current_row,
        model=model,
        activity_attr=log.activity,
        end_event=log.convert_string2int(log.activity, "END")
    )
    #print("model.variables = ",model.variables)
    #print("attributes: ",attributes)

    if predicted_event_int:
        print("Predicted next event (code):", predicted_event_int)
        print("Predicted next event:", predicted_event_str)
        print("Probability of next event:", prob_event)
    else:
        print("No prediction made for suffix.")

    #---------------coach
    coach_event(
        model=model,
        all_parents=all_parents,
        attributes=attributes,
        current_row=current_row
    )

    #---------------predict again
    current_row, attributes, all_parents, trace = get_current_row(log, model, log.activity)
    predicted_event_int, predicted_event_str, prob_event = predict_event(
        log,
        all_parents=all_parents,
        attributes=attributes,
        current_row=current_row,
        model=model,
        activity_attr=log.activity,
        end_event=log.convert_string2int(log.activity, "END")
    )

    if predicted_event_int:
        print("Predicted next event (code):", predicted_event_int)
        print("Predicted next event:", predicted_event_str)
        print("Probability of next event:", prob_event)
    else:
        print("No prediction made for suffix.")


def main():
    print("===== START PROCESS =====")
    log = prepare_data()
    model = train_model(log)

    #predict_next_event_row(log, model)
    predict_suffix_threshold(log, model)


if __name__ == '__main__':
    main()
