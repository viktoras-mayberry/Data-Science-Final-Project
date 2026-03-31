"""
Preprocessing Utilities
=======================
Reusable functions for data cleaning, encoding, scaling,
and feature engineering.

Usage:
    from src.preprocessing import handle_missing, encode_categoricals,
                                   scale_features, create_tenure_groups
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler


def handle_missing(df, strategy="median"):
    """
    Handle missing values in the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        strategy (str): Strategy for numerical columns —
                        'median', 'mean', or 'drop'.

    Returns:
        pd.DataFrame: DataFrame with missing values handled.

    Example:
        df_clean = handle_missing(df, strategy="median")
    """
    df = df.copy()

    # Report missing values
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) > 0:
        print(f"📊 Missing values found:")
        for col, count in missing.items():
            print(f"   {col}: {count} ({count/len(df)*100:.1f}%)")
    else:
        print("✅ No missing values found.")
        return df

    # Handle numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        if df[col].isnull().sum() > 0:
            if strategy == "median":
                df[col].fillna(df[col].median(), inplace=True)
            elif strategy == "mean":
                df[col].fillna(df[col].mean(), inplace=True)
            elif strategy == "drop":
                df.dropna(subset=[col], inplace=True)

    # Handle categorical columns — fill with mode
    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    print(f"✅ Missing values handled using '{strategy}' strategy.")
    return df


def encode_categoricals(df, method="label", columns=None):
    """
    Encode categorical variables.

    Args:
        df (pd.DataFrame): Input DataFrame.
        method (str): 'label' for Label Encoding, 'onehot' for One-Hot Encoding.
        columns (list): Specific columns to encode. If None, encodes all
                        object-type columns.

    Returns:
        pd.DataFrame: DataFrame with encoded columns.
        dict: Mapping of encoders (for label encoding) or None (for one-hot).

    Example:
        df_encoded, encoders = encode_categoricals(df, method="label")
        df_encoded, _ = encode_categoricals(df, method="onehot")
    """
    df = df.copy()

    if columns is None:
        columns = df.select_dtypes(include=["object"]).columns.tolist()

    # Remove ID columns from encoding
    columns = [c for c in columns if "id" not in c.lower()]

    if method == "label":
        encoders = {}
        for col in columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
        print(f"✅ Label-encoded {len(columns)} columns: {columns}")
        return df, encoders

    elif method == "onehot":
        df = pd.get_dummies(df, columns=columns, drop_first=True, dtype=int)
        print(f"✅ One-Hot encoded {len(columns)} columns.")
        print(f"   New shape: {df.shape}")
        return df, None

    else:
        raise ValueError(f"Unknown method: {method}. Use 'label' or 'onehot'.")


def scale_features(df, columns=None, scaler=None):
    """
    Scale numerical features using StandardScaler.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns (list): Columns to scale. If None, scales all numerical columns.
        scaler: Pre-fitted scaler. If None, creates and fits a new one.

    Returns:
        pd.DataFrame: DataFrame with scaled features.
        StandardScaler: The fitted scaler (for reuse on test data).

    Example:
        df_scaled, scaler = scale_features(df_train, columns=["tenure", "monthly_charges"])
        df_test_scaled, _ = scale_features(df_test, columns=["tenure", "monthly_charges"],
                                            scaler=scaler)
    """
    df = df.copy()

    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
        # Remove target column if present
        columns = [c for c in columns if c.lower() != "churn"]

    if scaler is None:
        scaler = StandardScaler()
        df[columns] = scaler.fit_transform(df[columns])
        print(f"✅ Fitted and scaled {len(columns)} features.")
    else:
        df[columns] = scaler.transform(df[columns])
        print(f"✅ Transformed {len(columns)} features using existing scaler.")

    return df, scaler


def create_tenure_groups(df, column="tenure"):
    """
    Create tenure groups from the tenure column.

    Groups:
        - 0-12 months:  'New'
        - 13-24 months: 'Growing'
        - 25-48 months: 'Established'
        - 49-60 months: 'Loyal'
        - 61+ months:   'Long-term'

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Name of the tenure column.

    Returns:
        pd.DataFrame: DataFrame with a new 'tenure_group' column.

    Example:
        df = create_tenure_groups(df)
        print(df["tenure_group"].value_counts())
    """
    df = df.copy()

    bins = [0, 12, 24, 48, 60, float("inf")]
    labels = ["New", "Growing", "Established", "Loyal", "Long-term"]

    df["tenure_group"] = pd.cut(df[column], bins=bins, labels=labels, right=True)
    print(f"✅ Created 'tenure_group' column with {len(labels)} groups.")

    return df


def prepare_features_target(df, target_column="churn"):
    """
    Split DataFrame into features (X) and target (y).

    Automatically drops ID columns and the target column from features.

    Args:
        df (pd.DataFrame): Input DataFrame.
        target_column (str): Name of the target column.

    Returns:
        tuple: (X, y) — features DataFrame and target Series.

    Example:
        X, y = prepare_features_target(df, target_column="churn")
    """
    # Drop ID columns
    id_cols = [c for c in df.columns if "id" in c.lower()]
    drop_cols = id_cols + [target_column]
    drop_cols = [c for c in drop_cols if c in df.columns]

    X = df.drop(columns=drop_cols)
    y = df[target_column]

    # Ensure target is numeric
    if y.dtype == "object":
        y = y.map({"Yes": 1, "No": 0})

    print(f"✅ Features shape: {X.shape}")
    print(f"   Target distribution: {dict(y.value_counts())}")

    return X, y
