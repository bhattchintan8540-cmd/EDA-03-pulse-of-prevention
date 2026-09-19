from __future__ import annotations

import pandas as pd

from src.heart_health import clean_heart


def test_heart_target_binarized_and_duplicates_removed():
    raw = pd.DataFrame(
        {
            "age": [63, 63, 41],
            "sex": [1, 1, 0],
            "cp": [3, 3, 1],
            "trestbps": [145, 145, 130],
            "chol": [233, 233, 250],
            "fbs": [1, 1, 0],
            "restecg": [0, 0, 1],
            "thalach": [150, 150, 168],
            "exang": [0, 0, 0],
            "oldpeak": [2.3, 2.3, 0.0],
            "slope": [0, 0, 2],
            "ca": [0, 0, 0],
            "thal": [1, 1, 2],
            "target": [1, 1, 0],
        }
    )
    clean = clean_heart(raw)
    assert len(clean) == 2
    assert set(clean["target"].unique()) <= {0, 1}
