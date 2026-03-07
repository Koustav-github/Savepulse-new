import numpy as np


def compute_weights(feature_matrix):
    """
    feature_matrix shape: (num_hospitals, num_features)

    columns correspond to:
    [distance_score, availability_score, rating_score, facility_score]
    """

    variances = np.var(feature_matrix, axis=0)

    total_variance = np.sum(variances)

    if total_variance == 0:
        # fallback if dataset is degenerate
        return np.ones(len(variances)) / len(variances)

    weights = variances / total_variance

    return weights


if __name__ == "__main__":

    sample_features = np.array([
    [0.5, 0.2, 0.8],
    [0.3, 0.1, 0.7],
    [0.1, 0.5, 0.9]
])

    weights = compute_weights(sample_features)

    print("Weights:", weights)
    print("Sum:", np.sum(weights))