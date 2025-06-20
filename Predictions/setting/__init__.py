from Predictions.setting.setting import Setting

STANDARD = Setting(10, "train-test", True, False, 70, 1)

DBN = Setting(5, "test-train", False, True, 70, filter_cases=1)

ALL = [DBN]