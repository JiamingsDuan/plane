w = [5, 40, 40, 5, 5, 40, 5, 40, 15, 40, 15, 15, 15, 40, 40, 40, 15, 40, 5]


def normalized_weights(weights):
    return [round(w / sum(weights) * 100, 0) for w in weights]

