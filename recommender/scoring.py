import numpy as np


def compute_scores(feature_matrix, weights):
    """
    feature_matrix shape: (num_hospitals, num_features)
    weights shape: (num_features,)
    """

    scores = np.dot(feature_matrix, weights)
    
    return scores


if __name__ == "__main__":

    # simple test

    feature_matrix = np.array([
        [0.4, 0.2, 0.8],
        [0.3, 0.5, 0.7],
        [0.2, 0.1, 0.9]
    ])

    weights = np.array([0.43, 0.46, 0.11])

    scores = compute_scores(feature_matrix, weights)

    print(scores)