"""EDA 03 — Pulse of Prevention: Analyzing Heart Health for Better Outcomes."""
from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from .config import project_output, savefig
from .download import load_heart

CP_MAP = {0: "typical angina", 1: "atypical angina", 2: "non-anginal pain", 3: "asymptomatic"}
SEX_MAP = {0: "female", 1: "male"}


def clean_heart(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    if "target" not in df.columns:
        for alt in ("output", "condition", "num", "heart_disease"):
            if alt in df.columns:
                df = df.rename(columns={alt: "target"})
                break
    numeric_cols = [c for c in df.columns if c != "target"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["target"] = pd.to_numeric(df["target"], errors="coerce")
    df = df.dropna(subset=["target"])
    df["target"] = (df["target"] > 0).astype(int)
    df = df.drop_duplicates()
    # IQR winsorize clinical measures, keep a flag
    for col in ["trestbps", "chol", "thalach", "oldpeak"]:
        if col not in df.columns:
            continue
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        df[f"{col}_outlier"] = ~df[col].between(low, high)
        df[col] = df[col].clip(lower=low, upper=high)
    return df.reset_index(drop=True)


def run() -> dict:
    out = project_output("heart_health")
    raw = load_heart()
    df = clean_heart(raw)
    fig_dir = out / "figures"
    disease = df[df["target"] == 1]
    healthy = df[df["target"] == 0]

    plt.figure()
    sns.histplot(data=df, x="age", hue="target", bins=20, kde=True, palette=["#16a34a", "#dc2626"])
    plt.title("Age Distribution by Heart Disease Status")
    savefig(fig_dir / "01_age_by_target.png")

    plt.figure()
    tmp = df.copy()
    tmp["sex_label"] = tmp["sex"].map(SEX_MAP)
    sns.countplot(data=tmp, x="sex_label", hue="target", palette=["#16a34a", "#dc2626"])
    plt.title("Sex vs Heart Disease")
    savefig(fig_dir / "02_sex_target.png")

    plt.figure()
    sns.heatmap(df[["age", "trestbps", "chol", "thalach", "oldpeak", "ca", "target"]].corr(), annot=True, fmt=".2f", cmap="RdBu_r", center=0)
    plt.title("Correlation of Clinical Measures and Target")
    savefig(fig_dir / "03_correlation.png")

    plt.figure()
    tmp["cp_label"] = tmp["cp"].map(lambda x: CP_MAP.get(int(x), str(x)) if pd.notna(x) else "NA")
    sns.countplot(data=tmp, y="cp_label", hue="target", palette=["#16a34a", "#dc2626"])
    plt.title("Chest Pain Type vs Disease")
    savefig(fig_dir / "04_chest_pain.png")

    plt.figure()
    sns.boxplot(data=df, x="target", y="thalach", hue="target", palette=["#16a34a", "#dc2626"], legend=False)
    plt.title("Max Heart Rate by Disease Status")
    savefig(fig_dir / "05_thalach.png")

    pair_cols = ["age", "chol", "trestbps", "target"]
    g = sns.pairplot(df[pair_cols], hue="target", corner=True, palette=["#16a34a", "#dc2626"])
    g.fig.suptitle("Combined Risk Factors vs Heart Disease", y=1.02)
    g.savefig(fig_dir / "06_pairplot_risk.png", dpi=140, bbox_inches="tight")
    plt.close("all")

    avg_age = float(df["age"].mean())
    sex_counts = df["sex"].map(SEX_MAP).value_counts().to_dict()
    avg_bp = float(df["trestbps"].mean())
    high_fbs = int(df["fbs"].sum())
    cp_types = sorted(int(x) for x in df["cp"].dropna().unique())
    max_hr = float(df["thalach"].max())
    exang_pct = float(df["exang"].mean() * 100)
    avg_chol = float(df["chol"].mean())
    restecg2 = int((df["restecg"] == 2).sum())
    ca_dist = df["ca"].value_counts().sort_index().to_dict()

    age_chol = float(df[["age", "chol"]].corr().iloc[0, 1])
    hr_exang = df.groupby("exang")["thalach"].mean().round(2).to_dict()
    bp_sex = df.groupby("sex")["trestbps"].mean()
    tstat, pval = stats.ttest_ind(df.loc[df["sex"] == 1, "trestbps"].dropna(), df.loc[df["sex"] == 0, "trestbps"].dropna(), equal_var=False)
    fbs_xtab = pd.crosstab(df["fbs"], df["target"], normalize="index").round(3).to_dict()
    ca_xtab = pd.crosstab(df["ca"], df["target"], normalize="index").round(3).to_dict()
    oldpeak_cp = df.groupby("cp")["oldpeak"].mean().round(3).to_dict()
    thal_xtab = pd.crosstab(df["thal"], df["target"], normalize="index").round(3).to_dict()
    combos = (
        disease.groupby(["cp", "fbs", "exang", "thal"]).size().reset_index(name="counts").sort_values("counts", ascending=False).head(8)
    )

    corr_target = df.corr(numeric_only=True)["target"].drop("target").sort_values(key=np.abs, ascending=False)
    feature_cols = [c for c in ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"] if c in df.columns]
    X = df[feature_cols].fillna(df[feature_cols].median())
    y = df["target"]
    scaler = StandardScaler()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    clf = LogisticRegression(max_iter=500)
    clf.fit(scaler.fit_transform(X_train), y_train)
    proba = clf.predict_proba(scaler.transform(X_test))[:, 1]
    auc = float(roc_auc_score(y_test, proba))
    report = classification_report(y_test, clf.predict(scaler.transform(X_test)), output_dict=True)
    coefs = pd.Series(clf.coef_[0], index=feature_cols).sort_values(key=np.abs, ascending=False).round(3).to_dict()
    slope_cp = df.groupby("cp")["slope"].mean().round(3).to_dict()

    qa = {
        "basic": [
            {"q": "Average age", "a": round(avg_age, 2)},
            {"q": "Gender distribution", "a": {k: int(v) for k, v in sex_counts.items()}},
            {"q": "Average resting blood pressure", "a": round(avg_bp, 2)},
            {"q": "Patients with fasting blood sugar >120", "a": high_fbs},
            {"q": "Chest pain type codes present", "a": cp_types},
            {"q": "Maximum heart rate recorded", "a": round(max_hr, 1)},
            {"q": "Exercise-induced angina %", "a": round(exang_pct, 2)},
            {"q": "Average cholesterol", "a": round(avg_chol, 2)},
            {"q": "Patients with restecg = 2", "a": restecg2},
            {"q": "ca distribution", "a": {str(k): int(v) for k, v in ca_dist.items()}},
        ],
        "medium": [
            {"q": "Correlation age vs cholesterol", "a": round(age_chol, 4)},
            {"q": "Mean max HR by exercise angina", "a": hr_exang},
            {
                "q": "Resting BP male vs female (Welch t-test)",
                "a": {"male_mean": round(float(bp_sex.get(1, np.nan)), 2), "female_mean": round(float(bp_sex.get(0, np.nan)), 2), "p_value": round(float(pval), 4)},
            },
            {"q": "Heart-disease rate by fasting blood sugar", "a": fbs_xtab},
            {"q": "Heart-disease rate by vessel count (ca)", "a": ca_xtab},
            {"q": "Average oldpeak by chest pain type", "a": oldpeak_cp},
            {"q": "Thalassemia vs target", "a": thal_xtab},
            {"q": "Common risk combinations among disease=1", "a": combos.to_dict("records")},
            {
                "q": "Clinical means disease vs no disease",
                "a": {
                    "disease": disease[["age", "chol", "trestbps", "thalach", "oldpeak"]].mean().round(2).to_dict(),
                    "no_disease": healthy[["age", "chol", "trestbps", "thalach", "oldpeak"]].mean().round(2).to_dict(),
                },
            },
        ],
        "advanced": [
            {"q": "Strongest correlations with target", "a": corr_target.head(8).round(3).to_dict()},
            {"q": "Logistic regression hold-out AUC", "a": round(auc, 4)},
            {"q": "Logistic coefficients (standardized)", "a": coefs},
            {"q": "Classification report (weighted avg f1)", "a": round(report["weighted avg"]["f1-score"], 3)},
            {"q": "Mean ST slope by chest pain type", "a": slope_cp},
            {
                "q": "Thalassemia note on survival",
                "a": "Dataset is cross-sectional (no follow-up time); survival curves are not identifiable. Age vs thal by target is reported as a proxy only.",
            },
        ],
    }

    top_corr_name = corr_target.index[0]
    findings = {
        "slug": "heart_health",
        "code": "EDA 03",
        "title": "Pulse of Prevention: Analyzing Heart Health for Better Outcomes",
        "dataset": "Heart disease clinical records (Kaggle johnsmith88/heart-disease-dataset / UCI Cleveland family)",
        "overview": (
            "HealthPulse Analytics profiles cardiology patients to find demographic and clinical factors "
            "linked to heart-disease diagnosis and to support earlier prevention."
        ),
        "problem_statement": (
            "The institute needs a high-risk patient profile from age, sex, chest pain, blood pressure, "
            "cholesterol, ECG, exercise tests, fluoroscopy vessel counts, and thalassemia — then clear "
            "prevention actions for clinicians and patients."
        ),
        "methodology": [
            "Validate types, map target to binary disease, drop duplicates, and winsorize extreme labs.",
            "Describe demographics and clinical distributions.",
            "Correlate features with diagnosis; compare groups with t-tests and crosstabs.",
            "Fit a standardized logistic regression with a stratified hold-out set (AUC, F1).",
            "State ethical limits: this is decision support, not an autonomous diagnosis.",
        ],
        "data_overview": {
            "rows_raw": int(len(raw)),
            "rows_clean": int(len(df)),
            "disease_prevalence": round(float(df["target"].mean()), 3),
            "mean_age": round(avg_age, 2),
            "features": feature_cols,
        },
        "key_findings": [
            f"After cleaning, disease prevalence is {df['target'].mean():.1%} of unique patient rows.",
            f"Mean age is {avg_age:.1f} years; the cohort is mixed but typically middle-to-older adult.",
            f"The strongest numeric association with diagnosis in this extract is {top_corr_name} (r={corr_target.iloc[0]:.2f}).",
            f"Exercise angina share is {exang_pct:.1f}%; max heart rate averages differ by angina status.",
            f"A simple logistic model reaches AUC {auc:.2f} on unseen rows — useful for ranking risk, not replacing ECG/clinical judgment.",
        ],
        "limitations": [
            "UCI Cleveland-style data is small, referred, and historically male-skewed.",
            "No follow-up time, so survival analysis is not supported despite the prompt's wording.",
            "Coding of cp/thal/ca can differ across mirrors of the dataset.",
            "Outlier clipping and duplicate removal change counts versus the raw Kaggle file (often duplicated).",
            "Models can encode historical care bias; they must stay under clinician review and privacy controls.",
        ],
        "conclusion": (
            "Heart-disease labels in this table cluster with chest-pain type, ST depression, exercise angina, "
            "vessel counts, and max heart rate. Prevention should target those markers plus blood pressure "
            "and cholesterol, with sex-aware screening rather than a single threshold."
        ),
        "recommendations": [
            "Flag patients with typical high-risk combinations (chest pain + exang + elevated oldpeak/ca) for faster cardiology review.",
            "Pair lipid and blood-pressure programs with the age groups that dominate the cohort.",
            "Do not treat fasting blood sugar alone as a sufficient screen; combine it with exercise ECG markers.",
            "Keep any predictive score as a triage aid; document consent, purpose limitation, and audit of errors.",
            "Collaborate with clinicians to recode features and refresh the model as new labeled visits arrive.",
        ],
        "qa": qa,
        "figures": [str(p.relative_to(out.parent.parent)) for p in sorted(fig_dir.glob("*.png"))],
        "stakeholders": {
            "internal": ["Management", "Healthcare providers", "Data analysts"],
            "external": ["Patients", "Cardiology research institute", "Policymakers"],
        },
    }
    (out / "findings.json").write_text(json.dumps(findings, indent=2, default=str), encoding="utf-8")
    df.to_csv(out / "cleaned_sample.csv", index=False)
    return findings
