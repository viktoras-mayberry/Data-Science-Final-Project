"""
Evaluation Utilities
====================
Reusable functions for model evaluation, comparison, and visualization.

Usage:
    from src.evaluation import (plot_confusion_matrix, plot_roc_curves,
                                 print_classification_report, compare_models)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    classification_report,
)


def plot_confusion_matrix(y_true, y_pred, model_name="Model", figsize=(6, 5)):
    """
    Plot a styled confusion matrix heatmap.

    Args:
        y_true: True labels.
        y_pred: Predicted labels.
        model_name (str): Name of the model (used in the title).
        figsize (tuple): Figure size.

    Example:
        plot_confusion_matrix(y_test, y_pred, model_name="Random Forest")
    """
    cm = confusion_matrix(y_true, y_pred)
    labels = ["No Churn", "Churn"]

    plt.figure(figsize=figsize)
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels,
        cbar_kws={"label": "Count"},
    )
    plt.title(f"Confusion Matrix — {model_name}", fontsize=14, fontweight="bold")
    plt.xlabel("Predicted", fontsize=12)
    plt.ylabel("Actual", fontsize=12)
    plt.tight_layout()
    plt.show()


def plot_roc_curves(models_dict, X_test, y_test, figsize=(8, 6)):
    """
    Plot ROC curves for multiple models on a single chart.

    Args:
        models_dict (dict): Dictionary of {model_name: fitted_model}.
                           Each model must have a predict_proba method.
        X_test: Test features.
        y_test: True test labels.
        figsize (tuple): Figure size.

    Example:
        models = {
            "Logistic Regression": lr_model,
            "Random Forest": rf_model,
            "XGBoost": xgb_model,
        }
        plot_roc_curves(models, X_test, y_test)
    """
    plt.figure(figsize=figsize)

    colors = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0"]

    for i, (name, model) in enumerate(models_dict.items()):
        # Get probability predictions
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
        else:
            y_prob = model.predict(X_test)

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        auc = roc_auc_score(y_test, y_prob)

        color = colors[i % len(colors)]
        plt.plot(fpr, tpr, color=color, linewidth=2,
                 label=f"{name} (AUC = {auc:.4f})")

    # Diagonal reference line
    plt.plot([0, 1], [0, 1], "k--", alpha=0.4, linewidth=1)

    plt.xlabel("False Positive Rate", fontsize=12)
    plt.ylabel("True Positive Rate", fontsize=12)
    plt.title("ROC Curves — Model Comparison", fontsize=14, fontweight="bold")
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def print_metrics(y_true, y_pred, model_name="Model"):
    """
    Print key classification metrics for a model.

    Args:
        y_true: True labels.
        y_pred: Predicted labels.
        model_name (str): Name of the model.

    Returns:
        dict: Dictionary of metric values.

    Example:
        metrics = print_metrics(y_test, y_pred, model_name="XGBoost")
    """
    metrics = {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1-Score": f1_score(y_true, y_pred),
    }

    print(f"\n{'='*45}")
    print(f"  📊 {model_name} — Classification Metrics")
    print(f"{'='*45}")
    for metric_name, value in metrics.items():
        print(f"  {metric_name:>12}: {value:.4f}")
    print(f"{'='*45}\n")

    return metrics


def compare_models(results_dict):
    """
    Create a comparison DataFrame and bar chart for all models.

    Args:
        results_dict (dict): Dictionary of {model_name: metrics_dict}.
                            Each metrics_dict should have keys:
                            Accuracy, Precision, Recall, F1-Score.

    Returns:
        pd.DataFrame: Comparison table.

    Example:
        results = {
            "Logistic Regression": {"Accuracy": 0.80, "Precision": 0.65, ...},
            "Random Forest": {"Accuracy": 0.82, "Precision": 0.70, ...},
        }
        comparison_df = compare_models(results)
    """
    # Create comparison DataFrame
    df = pd.DataFrame(results_dict).T
    df.index.name = "Model"

    print("\n📊 Model Comparison Table:")
    print("=" * 65)
    print(df.to_string())
    print("=" * 65)

    # Plot comparison
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(df.index))
    width = 0.2
    metrics = df.columns.tolist()
    colors = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63"]

    for i, metric in enumerate(metrics):
        ax.bar(x + i * width, df[metric], width, label=metric,
               color=colors[i % len(colors)], edgecolor="white", linewidth=0.5)

    ax.set_xlabel("Model", fontsize=12)
    ax.set_ylabel("Score", fontsize=12)
    ax.set_title("Model Performance Comparison", fontsize=14, fontweight="bold")
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(df.index, rotation=15, ha="right")
    ax.legend(fontsize=10)
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

    return df


def plot_feature_importance(model, feature_names, top_n=15, figsize=(10, 6)):
    """
    Plot the top N most important features.

    Args:
        model: A fitted model with feature_importances_ attribute.
        feature_names (list): List of feature names.
        top_n (int): Number of top features to display.
        figsize (tuple): Figure size.

    Example:
        plot_feature_importance(rf_model, X_train.columns, top_n=15)
    """
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]

    plt.figure(figsize=figsize)
    plt.barh(
        range(top_n),
        importances[indices][::-1],
        color="#2196F3",
        edgecolor="white",
    )
    plt.yticks(range(top_n), [feature_names[i] for i in indices][::-1])
    plt.xlabel("Importance", fontsize=12)
    plt.title(f"Top {top_n} Feature Importances", fontsize=14, fontweight="bold")
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.show()
