from explanation import explain_last_prediction
from Methods.EDBN import Predictions as edbn_predict
from Methods.EDBN.Train import train
from Methods.EDBN.Predictions import (
    predict_next_event_row,
    predict_case_suffix_loop_threshold,
    get_prediction_attributes,
    predict_event
)
import Predictions.setting
import Data
from Utils.LogFile import LogFile
from explanation import *


#CONFIGURATION
DATASET_NAME = "events_with_context"
SETTINGS = Predictions.setting.STANDARD


def prepare_data():
    print("PREPARE DATA")
    data_object = Data.get_data(DATASET_NAME)
    data_object.prepare(SETTINGS)
    return data_object.logfile


def train_model(log):
    print("TRAINING MODEL")
    return train(log)


def test_predict_next_event_row(log, model):
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


def test_predict_suffix_threshold(log, model):
    print("=== TEST: Predict case suffix with loop threshold ===")
    last_case = list(log.get_cases())[-1]
    trace = last_case[1]

    all_parents, attributes = get_prediction_attributes(model, log.activity)

    current_row = {
        i: [getattr(trace.iloc[-(i + 1)], attr) if len(trace) > i else 0 for attr in attributes]
        for i in range(log.k + 1)
    }

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
        print("Predicted next event:", predicted_event_str)
        print("Probability of next event:", prob_event)
    else:
        print("No prediction made for suffix.")


def main():
    print("===== START PROCESS =====")
    log = prepare_data()
    model = train_model(log)

    #test_predict_next_event_row(log, model)
    test_predict_suffix_threshold(log, model)


if __name__ == '__main__':
    main()
