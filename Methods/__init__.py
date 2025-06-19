from Methods.method import Method


def get_prediction_method(method_name):
    if method_name == "DBN":
        from Methods.EDBN.Train import train, update
        from Methods.EDBN.Predictions import test
        return Method("DBN", train, test, update)
    else:
        print("ERROR: method name not found!")
        print("ERROR: Possible methods are:" + ",".join(ALL))
        raise NotImplementedError()


ALL = ["DBN"]
