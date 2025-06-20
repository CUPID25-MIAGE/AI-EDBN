from Methods.EDBN import Predictions as edbn_predict

def explain_last_prediction(log, model, activity_attr="activity"):
    row_index, row_data = list(log.contextdata.iterrows())[-1]

    activity_var = model.variables[activity_attr]
    parents = activity_var.conditional_table.parents

    val_tuple = tuple(getattr(row_data, parent.attr_name) for parent in parents)
    probs, _ = edbn_predict.get_probabilities(activity_var, val_tuple, parents)

    predicted_val = max(probs, key=probs.get)
    predicted_label = log.convert_int2string(activity_attr, predicted_val)

    explanation = f"J’ai prédit que la prochaine activité sera **« {predicted_label} »** car "
    elements = []

    for parent in parents:
        if not parent.attr_name.startswith(activity_attr + "_Prev"):
            continue

        raw_val = getattr(row_data, parent.attr_name)
        step = parent.attr_name.split("_Prev")[-1]
        base_attr = parent.attr_name.split("_")[0]

        try:
            str_val = log.convert_int2string(base_attr, raw_val)
        except:
            str_val = str(raw_val)

        step_txt = "la dernière activité" if step == "0" else f"l’activité {int(step)+1}ᵉ avant"
        elements.append(f"{step_txt} était « {str_val} »")

    explanation += ", ".join(elements)
    explanation += f". Cette prédiction a une probabilité de {probs[predicted_val]*100:.1f}%."

    top_others = sorted(probs.items(), key=lambda x: x[1], reverse=True)[1:3]
    if top_others:
        other_options = ", ".join(
            f"« {log.convert_int2string(activity_attr, act)} » ({prob*100:.1f}%)"
            for act, prob in top_others
        )
        explanation += f" Autres possibilités : {other_options}."

    return predicted_label, explanation
