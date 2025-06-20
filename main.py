from explanation import explain_last_prediction
from Methods.EDBN import Predictions as edbn_predict
import Predictions.setting
import Methods
from Utils.LogFile import LogFile
import Data
import Predictions.metric
from Methods.EDBN.Train import train, update
from Methods.EDBN.Predictions import test, predict_next_event


if __name__ == '__main__':
    print("PREPARE")
    data_object = Data.get_data("events")
    #print(dir(data_object.logfile))

    print("SELECT SETTINGS")
    settings = Predictions.setting.STANDARD

    print("PREPARE DATA")
    data_object.prepare(settings)
    log= data_object.logfile

    #print("GET PREDICTION METHOD")  
    #m = Methods.get_prediction_method("DBN")

    print("TRAIN MODEL")
    model = train(log)
    
    #print("\n_____*********************************************\npriniting model")
    #print(dir(model.iterate_variables()))
    #model.print_parents()
    #print("TEST MODEL")
    #predictions = predict_next_event(model, log)
    # Step 4: Display predictions
    #for actual, predicted, p_predicted, p_actual in predictions:
    #    print(f"Actual: {actual}, Predicted: {predicted}, P(Predicted): {p_predicted:.4f}, P(Actual): {p_actual:.4f}")
        
    results = test(model, log)
    predicted_event = log.convert_int2string(log.activity, results[-1][1])
    
    print("predicted event is: ")
    print(predicted_event)

    print("GET ACCURACY")
    accuracy = Predictions.metric.ACCURACY.calculate(results)
    print("Accuracy:", accuracy)

    #%%
    #Prepare context
    log.create_k_context()
    # Grab the last k-context row
    context_row = log.contextdata.iloc[-1:]
    print("context row is: ")
    print(context_row)
    row_tuple = list(context_row.iterrows())[0]
    print("row_tuple is: ")
    print(row_tuple)
    # Run the prediction
    true_val, predicted_val, confidence, true_prob = edbn_predict.predict_next_event_row(
        row_tuple,
        model=model,
        activity=log.activity
    )
    # Convert int values to strings for readability
    true_event = log.convert_int2string(log.activity, true_val)
    predicted_event = log.convert_int2string(log.activity, predicted_val)
    # Display result
    print("True next event (if known):", true_event)
    print("Predicted next event:", predicted_event)
    print("Confidence:", confidence)
    print("Probability assigned to actual:", true_prob)

    # Show the explanation
    predicted_label, explanation = explain_last_prediction(log, model, activity_attr=log.activity)
    print("Explication :", explanation)
    #%%



#UPDATE
"""     #Update the model
    print("PREPARE THE UPDATED LOG")
    data_object = Data.get_data("BPIC112")
    print(dir(data_object.logfile))

    print("PREPARE UPDATED DATA")
    data_object.prepare(settings)
    log= data_object.logfile

    print("updating the model")
    update(model, log)

    #%%
    # Make sure context is prepared
    print("\n\n***********************************************\n")
    print("\n\n\nPrediction after update:\n")
    log.create_k_context()

    # Grab the last k-context row
    context_row = log.contextdata.iloc[-1:]
    print("context row is: ")
    print(context_row)
    row_tuple = list(context_row.iterrows())[0]
    print("row_tuple is: ")
    print(row_tuple)

    # Run the prediction
    true_val, predicted_val, confidence, true_prob = edbn_predict.predict_next_event_row(
        row_tuple,
        model=model,
        activity=log.activity
    )

    # Convert int values to strings for readability
    true_event = log.convert_int2string(log.activity, true_val)
    predicted_event = log.convert_int2string(log.activity, predicted_val)

    # Display result
    print("True next event (if known):", true_event)
    print("Predicted next event:", predicted_event)
    print("Confidence:", confidence)
    print("Probability assigned to actual:", true_prob) """
