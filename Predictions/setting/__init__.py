from Predictions.setting.setting import Setting

STANDARD = Setting(10, "train-test", True, False, 70, 0)

DBN = Setting(3, "test-train", False, False, filter_cases=0)

ALL = [DBN]