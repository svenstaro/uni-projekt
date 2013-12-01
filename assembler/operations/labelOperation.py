from operation import Operation


class LabelOperation(Operation):
    labels = None

    @staticmethod
    def create(typeLabelOperation, labels):
        newDict = dict(typeLabelOperation.__dict__)
        newDict["labels"] = labels
        newType = type(typeLabelOperation.__name__, typeLabelOperation.__bases__, newDict)
        return newType