# Solution guide
Answers for **Pulse of Prevention: Analyzing Heart Health for Better Outcomes**.

## Basic-level questions
### 1. Average age
54.42
### 2. Gender distribution
```json
{
  "male": 206,
  "female": 96
}
```
### 3. Average resting blood pressure
131.26
### 4. Patients with fasting blood sugar >120
45
### 5. Chest pain type codes present
```json
[
  0,
  1,
  2,
  3
]
```
### 6. Maximum heart rate recorded
202.0
### 7. Exercise-induced angina %
32.78
### 8. Average cholesterol
245.38
### 9. Patients with restecg = 2
4
### 10. ca distribution
```json
{
  "0": 175,
  "1": 65,
  "2": 38,
  "3": 20,
  "4": 4
}
```

## Medium-level questions
### 1. Correlation age vs cholesterol
0.1989
### 2. Chest pain type mix by age group
```json
{
  "0": {
    "21-40": 0.333,
    "41-50": 0.382,
    "51-60": 0.504,
    "61-80": 0.544
  },
  "1": {
    "21-40": 0.167,
    "41-50": 0.263,
    "51-60": 0.155,
    "61-80": 0.089
  },
  "2": {
    "21-40": 0.333,
    "41-50": 0.329,
    "51-60": 0.264,
    "61-80": 0.266
  },
  "3": {
    "21-40": 0.167,
    "41-50": 0.026,
    "51-60": 0.078,
    "61-80": 0.101
  }
}
```
### 3. Mean max HR by exercise angina
```json
{
  "0": 155.66,
  "1": 137.21
}
```
### 4. Resting BP male vs female (Welch t-test)
```json
{
  "male_mean": 130.71,
  "female_mean": 132.44,
  "p_value": 0.4166
}
```
### 5. Heart-disease rate by fasting blood sugar
```json
{
  "0": {
    "0": 0.451,
    "1": 0.489
  },
  "1": {
    "0": 0.549,
    "1": 0.511
  }
}
```
### 6. Heart-disease rate by vessel count (ca)
```json
{
  "0": {
    "0": 0.257,
    "1": 0.677,
    "2": 0.816,
    "3": 0.85,
    "4": 0.25
  },
  "1": {
    "0": 0.743,
    "1": 0.323,
    "2": 0.184,
    "3": 0.15,
    "4": 0.75
  }
}
```
### 7. Average oldpeak by chest pain type
```json
{
  "0": 1.352,
  "1": 0.316,
  "2": 0.807,
  "3": 1.383
}
```
### 8. Thalassemia vs target
```json
{
  "0": {
    "0": 0.5,
    "1": 0.667,
    "2": 0.218,
    "3": 0.761
  },
  "1": {
    "0": 0.5,
    "1": 0.333,
    "2": 0.782,
    "3": 0.239
  }
}
```
### 9. Common risk combinations among disease=1
```json
[
  {
    "cp": 2,
    "fbs": 0,
    "exang": 0,
    "thal": 2,
    "counts": 41
  },
  {
    "cp": 1,
    "fbs": 0,
    "exang": 0,
    "thal": 2,
    "counts": 30
  },
  {
    "cp": 0,
    "fbs": 0,
    "exang": 0,
    "thal": 2,
    "counts": 23
  },
  {
    "cp": 2,
    "fbs": 1,
    "exang": 0,
    "thal": 2,
    "counts": 10
  },
  {
    "cp": 0,
    "fbs": 0,
    "exang": 1,
    "thal": 2,
    "counts": 6
  },
  {
    "cp": 2,
    "fbs": 0,
    "exang": 0,
    "thal": 3,
    "counts": 6
  },
  {
    "cp": 3,
    "fbs": 0,
    "exang": 0,
    "thal": 2,
    "counts": 5
  },
  {
    "cp": 1,
    "fbs": 0,
    "exang": 0,
    "thal": 3,
    "counts": 4
  }
]
```
### 10. Clinical means disease vs no disease
```json
{
  "disease": {
    "age": 52.59,
    "chol": 241.03,
    "trestbps": 129.13,
    "thalach": 158.38,
    "oldpeak": 0.59
  },
  "no_disease": {
    "age": 56.6,
    "chol": 250.54,
    "trestbps": 133.79,
    "thalach": 139.2,
    "oldpeak": 1.55
  }
}
```

## Advanced-level questions
### 1. Strongest correlations with target
```json
{
  "exang": -0.436,
  "oldpeak": -0.435,
  "cp": 0.432,
  "thalach": 0.42,
  "ca": -0.409,
  "slope": 0.344,
  "thal": -0.343,
  "sex": -0.284
}
```
### 2. Logistic regression hold-out AUC
0.8648
### 3. Logistic coefficients (standardized)
```json
{
  "cp": 0.993,
  "sex": -0.738,
  "ca": -0.661,
  "thal": -0.635,
  "thalach": 0.616,
  "oldpeak": -0.595,
  "exang": -0.504,
  "chol": -0.446,
  "slope": 0.291,
  "restecg": 0.212,
  "trestbps": -0.184,
  "age": 0.025,
  "fbs": 0.008
}
```
### 4. Classification report (weighted avg f1)
0.773
### 5. Mean ST slope by chest pain type
```json
{
  "0": 1.259,
  "1": 1.68,
  "2": 1.5,
  "3": 1.261
}
```
### 6. Thalassemia note on survival
Dataset is cross-sectional (no follow-up time); survival curves are not identifiable. Age vs thal by target is reported as a proxy only.
