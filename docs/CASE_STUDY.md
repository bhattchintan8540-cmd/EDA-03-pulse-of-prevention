# Case study — Pulse of Prevention: Analyzing Heart Health for Better Outcomes

## Problem statement
The institute needs a high-risk patient profile from age, sex, chest pain, blood pressure, cholesterol, ECG, exercise tests, fluoroscopy vessel counts, and thalassemia — then clear prevention actions for clinicians and patients.

## Overview
HealthPulse Analytics profiles cardiology patients to find demographic and clinical factors linked to heart-disease diagnosis and to support earlier prevention.

## Stakeholders
- Internal: Management, Healthcare providers, Data analysts
- External: Patients, Cardiology research institute, Policymakers

## Data dictionary
| Column | Description |
| --- | --- |
| `age` | Patient age |
| `sex` | 1 = male, 0 = female |
| `cp` | Chest pain type (0-3) |
| `trestbps` | Resting blood pressure (mm Hg) |
| `chol` | Serum cholesterol (mg/dl) |
| `fbs` | Fasting blood sugar > 120 mg/dl |
| `restecg` | Resting ECG result (0-2) |
| `thalach` | Maximum heart rate achieved |
| `exang` | Exercise-induced angina |
| `oldpeak` | ST depression vs rest |
| `slope` | Peak exercise ST slope |
| `ca` | Major vessels colored by fluoroscopy |
| `thal` | Thalassemia code |
| `target` | Heart-disease diagnosis (1 = yes) |

## Assignment questions
The brief's basic, medium, and advanced questions are answered in `docs/SOLUTION_GUIDE.md` and `outputs/heart_health/findings.json`.
