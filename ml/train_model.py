"""
ML Return Prediction Model
==========================
Trains Logistic Regression and Decision Tree classifiers to predict
whether an e-commerce order will be returned.

Features used:
  - category, sub_category, payment_method, shipping_type,
    customer_segment, region
  - discount_percent, unit_price, quantity, delivery_days, customer_age

Target: is_returned (binary: True/False)

Saves trained model pipeline to ml/model.pkl and metrics to ml/metrics.json.
"""

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from analysis import clean_and_load_data

try:
    import joblib
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (
        classification_report,
        confusion_matrix,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
    from sklearn.tree import DecisionTreeClassifier

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


CATEGORICAL_FEATURES = [
    "category",
    "sub_category",
    "payment_method",
    "shipping_type",
    "customer_segment",
    "region",
]

NUMERICAL_FEATURES = [
    "discount_percent",
    "unit_price",
    "quantity",
    "delivery_days",
    "customer_age",
]

ALL_FEATURES = CATEGORICAL_FEATURES + NUMERICAL_FEATURES
TARGET = "is_returned"


def prepare_features(df: pd.DataFrame):
    """Prepare feature matrix X and target vector y from cleaned dataframe."""
    df_ml = df.copy()

    # Ensure all features exist, fill missing
    for col in CATEGORICAL_FEATURES:
        if col not in df_ml.columns:
            df_ml[col] = "Unknown"
        df_ml[col] = df_ml[col].fillna("Unknown").astype(str)

    for col in NUMERICAL_FEATURES:
        if col not in df_ml.columns:
            df_ml[col] = 0.0
        df_ml[col] = pd.to_numeric(df_ml[col], errors="coerce").fillna(0.0)

    if TARGET not in df_ml.columns:
        raise ValueError(f"Target column '{TARGET}' not found in dataset.")

    df_ml = df_ml.dropna(subset=[TARGET])
    df_ml[TARGET] = df_ml[TARGET].astype(int)

    X = df_ml[ALL_FEATURES]
    y = df_ml[TARGET]

    return X, y


def build_pipeline(model_type: str = "logistic"):
    """Build a sklearn Pipeline with preprocessing + classifier."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
            ("num", StandardScaler(), NUMERICAL_FEATURES),
        ]
    )

    if model_type == "logistic":
        clf = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    elif model_type == "decision_tree":
        clf = DecisionTreeClassifier(max_depth=8, min_samples_leaf=20, random_state=42, class_weight="balanced")
    elif model_type == "random_forest":
        clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight="balanced", n_jobs=-1)
    else:
        raise ValueError(f"Unknown model_type: {model_type}")

    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", clf)])
    return pipeline


def compute_metrics(y_true, y_pred, y_prob=None, model_name: str = "Model"):
    """Compute and return classification metrics as a dict."""
    cm = confusion_matrix(y_true, y_pred).tolist()
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)

    auc = None
    if y_prob is not None:
        try:
            auc = float(roc_auc_score(y_true, y_prob))
        except Exception:
            auc = None

    return {
        "model": model_name,
        "confusion_matrix": cm,
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1_score": round(float(f1), 4),
        "roc_auc": round(auc, 4) if auc else None,
        "classification_report": report,
    }


def get_feature_importances(pipeline, model_type: str):
    """Extract feature names and importances from a fitted pipeline."""
    try:
        preprocessor = pipeline.named_steps["preprocessor"]
        clf = pipeline.named_steps["classifier"]

        # Get feature names after one-hot encoding
        cat_feature_names = preprocessor.named_transformers_["cat"].get_feature_names_out(CATEGORICAL_FEATURES).tolist()
        num_feature_names = NUMERICAL_FEATURES
        all_feature_names = cat_feature_names + num_feature_names

        if hasattr(clf, "feature_importances_"):
            importances = clf.feature_importances_
        elif hasattr(clf, "coef_"):
            importances = np.abs(clf.coef_[0])
        else:
            return []

        feat_imp = sorted(
            zip(all_feature_names, importances.tolist()),
            key=lambda x: x[1],
            reverse=True,
        )
        return [{"feature": f, "importance": round(v, 6)} for f, v in feat_imp[:20]]
    except Exception:
        return []


def train_and_save(model_type: str = "random_forest"):
    """
    Full training pipeline:
    1. Load & clean data
    2. Prepare features
    3. Train/test split
    4. Fit pipeline
    5. Evaluate & save metrics
    6. Save model.pkl
    """
    if not SKLEARN_AVAILABLE:
        print("scikit-learn not installed. Cannot train model.")
        return None, None

    print("Loading and cleaning dataset...")
    df, _ = clean_and_load_data()
    X, y = prepare_features(df)

    print(f"Dataset size: {len(X)} rows | Return rate: {y.mean() * 100:.1f}%")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training {model_type} model on {len(X_train)} samples...")
    pipeline = build_pipeline(model_type)
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = None
    try:
        y_prob = pipeline.predict_proba(X_test)[:, 1]
    except Exception:
        pass

    model_display_name = {
        "logistic": "Logistic Regression",
        "decision_tree": "Decision Tree (depth=8)",
        "random_forest": "Random Forest (100 trees)",
    }.get(model_type, model_type)

    metrics = compute_metrics(y_train, pipeline.predict(X_train), model_name=f"{model_display_name} [Train]")
    test_metrics = compute_metrics(y_test, y_pred, y_prob, model_name=f"{model_display_name} [Test]")
    feature_importances = get_feature_importances(pipeline, model_type)

    output = {
        "model_type": model_type,
        "model_display_name": model_display_name,
        "train_size": len(X_train),
        "test_size": len(X_test),
        "return_rate_pct": round(float(y.mean() * 100), 2),
        "features": ALL_FEATURES,
        "target": TARGET,
        "train_metrics": metrics,
        "test_metrics": test_metrics,
        "feature_importances": feature_importances,
    }

    # Save metrics
    metrics_path = ML_DIR / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Metrics saved to {metrics_path}")

    # Save pipeline
    model_path = ML_DIR / "model.pkl"
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")

    print(f"\n=== {model_display_name} Test Results ===")
    print(f"  Precision: {test_metrics['precision']:.4f}")
    print(f"  Recall:    {test_metrics['recall']:.4f}")
    print(f"  F1-Score:  {test_metrics['f1_score']:.4f}")
    if test_metrics["roc_auc"]:
        print(f"  ROC AUC:   {test_metrics['roc_auc']:.4f}")

    return pipeline, output


def predict_single_order(
    category: str = "Electronics",
    sub_category: str = "Mobiles",
    payment_method: str = "Cash on Delivery",
    shipping_type: str = "Standard",
    customer_segment: str = "Consumer",
    region: str = "North",
    discount_percent: float = 10.0,
    unit_price: float = 5000.0,
    quantity: int = 1,
    delivery_days: float = 5.0,
    customer_age: float = 30.0,
    model_path: str = None,
):
    """
    Load saved model and predict return probability for a single order.
    Returns dict with probability and risk label.
    """
    if not SKLEARN_AVAILABLE:
        return {"error": "scikit-learn not available"}

    import joblib as jl

    path = Path(model_path) if model_path else ML_DIR / "model.pkl"
    if not path.exists():
        return {"error": f"Model not found at {path}. Run train_and_save() first."}

    pipeline = jl.load(path)

    input_data = pd.DataFrame(
        [
            {
                "category": category,
                "sub_category": sub_category,
                "payment_method": payment_method,
                "shipping_type": shipping_type,
                "customer_segment": customer_segment,
                "region": region,
                "discount_percent": float(discount_percent),
                "unit_price": float(unit_price),
                "quantity": int(quantity),
                "delivery_days": float(delivery_days),
                "customer_age": float(customer_age),
            }
        ]
    )

    prediction = int(pipeline.predict(input_data)[0])
    try:
        prob = float(pipeline.predict_proba(input_data)[0][1])
    except Exception:
        prob = float(prediction)

    risk_label = "High Risk" if prob >= 0.45 else "Medium Risk" if prob >= 0.25 else "Low Risk"
    risk_color = "#ef4444" if risk_label == "High Risk" else "#f59e0b" if risk_label == "Medium Risk" else "#10b981"

    return {
        "predicted_return": bool(prediction),
        "return_probability": round(prob * 100, 1),
        "risk_label": risk_label,
        "risk_color": risk_color,
        "input_features": {
            "category": category,
            "sub_category": sub_category,
            "payment_method": payment_method,
            "shipping_type": shipping_type,
            "customer_segment": customer_segment,
            "region": region,
            "discount_percent": discount_percent,
            "unit_price": unit_price,
            "quantity": quantity,
            "delivery_days": delivery_days,
            "customer_age": customer_age,
        },
    }


if __name__ == "__main__":
    pipeline, metrics = train_and_save(model_type="random_forest")
