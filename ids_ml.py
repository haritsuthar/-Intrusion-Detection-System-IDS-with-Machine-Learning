# ids_ml.py — Full Intrusion Detection System using NSL-KDD Dataset

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    roc_curve,
    auc
)
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from typing import Any, Dict, Tuple, List
import os
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 1. COLUMN DEFINITIONS (41 features + label + difficulty)
# =============================================================================
COLUMNS = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes',
    'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
    'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
    'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
    'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate',
    'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
    'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
    'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
    'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
    'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate', 'label', 'difficulty'
]

CATEGORICAL = ['protocol_type', 'service', 'flag']

# Attack type mapping
ATTACK_MAP = {
    'normal': 'normal',
    'back': 'dos', 'land': 'dos', 'neptune': 'dos', 'pod': 'dos',
    'smurf': 'dos', 'teardrop': 'dos', 'mailbomb': 'dos',
    'apache2': 'dos', 'processtable': 'dos', 'udpstorm': 'dos',
    'ipsweep': 'probe', 'nmap': 'probe', 'portsweep': 'probe',
    'satan': 'probe', 'mscan': 'probe', 'saint': 'probe',
    'ftp_write': 'r2l', 'guess_passwd': 'r2l', 'imap': 'r2l',
    'multihop': 'r2l', 'phf': 'r2l', 'spy': 'r2l',
    'warezclient': 'r2l', 'warezmaster': 'r2l', 'sendmail': 'r2l',
    'named': 'r2l', 'snmpgetattack': 'r2l', 'snmpguess': 'r2l',
    'xlock': 'r2l', 'xsnoop': 'r2l', 'worm': 'r2l',
    'buffer_overflow': 'u2r', 'loadmodule': 'u2r', 'perl': 'u2r',
    'rootkit': 'u2r', 'httptunnel': 'u2r', 'ps': 'u2r',
    'sqlattack': 'u2r', 'xterm': 'u2r'
}

# =============================================================================
# 2. LOAD DATASET
# =============================================================================
def load_data():
    # Check both current directory and parent directory for dataset files
    train_paths = ['KDDTrain+.txt', '../KDDTrain+.txt']
    test_paths = ['KDDTest+.txt', '../KDDTest+.txt']
    
    train_path = None
    test_path = None
    
    for path in train_paths:
        if os.path.exists(path):
            train_path = path
            break
    
    for path in test_paths:
        if os.path.exists(path):
            test_path = path
            break

    if not train_path:
        print("ERROR: KDDTrain+.txt not found!")
        print("Download from: https://www.unb.ca/cic/datasets/nsl.html")
        print("Place KDDTrain+.txt and KDDTest+.txt in this folder.")
        exit(1)

    df_train = pd.read_csv(train_path, header=None, names=COLUMNS)
    df_test = pd.read_csv(test_path, header=None, names=COLUMNS)

    print(f"[+] Training samples: {len(df_train)}")
    print(f"[+] Testing samples:  {len(df_test)}")

    return df_train, df_test

# =============================================================================
# 3. PREPROCESS
# =============================================================================
def preprocess(df_train, df_test):
    # Map attack names to categories
    df_train['attack_cat'] = df_train['label'].map(
        lambda x: ATTACK_MAP.get(x, 'unknown')
    )
    df_test['attack_cat'] = df_test['label'].map(
        lambda x: ATTACK_MAP.get(x, 'unknown')
    )

    # Binary label: 0 = normal, 1 = attack
    df_train['binary_label'] = df_train['attack_cat'].apply(
        lambda x: 0 if x == 'normal' else 1
    )
    df_test['binary_label'] = df_test['attack_cat'].apply(
        lambda x: 0 if x == 'normal' else 1
    )

    print(f"\n[+] Training class distribution:")
    print(df_train['binary_label'].value_counts().to_string())
    print(f"\n[+] Attack category distribution:")
    print(df_train['attack_cat'].value_counts().to_string())

    # Encode categorical columns
    encoders = {}
    for col in CATEGORICAL:
        le = LabelEncoder()
        combined = pd.concat([df_train[col], df_test[col]], axis=0)
        le.fit(combined)
        df_train[col] = le.transform(df_train[col])
        df_test[col] = le.transform(df_test[col])
        encoders[col] = le

    # Drop non-feature columns
    drop_cols = ['label', 'difficulty', 'attack_cat', 'binary_label']

    X_train = df_train.drop(drop_cols, axis=1)
    y_train = df_train['binary_label']
    X_test = df_test.drop(drop_cols, axis=1)
    y_test = df_test['binary_label']

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"\n[+] Feature count: {X_train_scaled.shape[1]}")

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, encoders

# =============================================================================
# 4. TRAIN MODEL
# =============================================================================
def train_model(X_train, y_train):
    print("\n[+] Training Random Forest Classifier...")
    clf = RandomForestClassifier(
        n_estimators=150,
        max_depth=25,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)
    print("[+] Training complete.")
    return clf

# =============================================================================
# 5. EVALUATE MODEL
# =============================================================================
def evaluate(clf, X_test, y_test):
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    print(f"\n{'='*60}")
    print(f"  RESULTS")
    print(f"{'='*60}")
    print(f"  Accuracy: {acc:.4f} ({acc*100:.2f}%)")
    print(f"{'='*60}")
    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred, target_names=['Normal', 'Attack']
    ))

    return y_pred, y_prob

# =============================================================================
# 6. VISUALIZATIONS
# =============================================================================
def plot_confusion_matrix(y_test, y_pred, show: bool = False):
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=['Normal', 'Attack'],
        yticklabels=['Normal', 'Attack']
    )
    plt.title('Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=150)
    plt.close()  # Close the figure to free memory
    print("[+] Saved: confusion_matrix.png")

def plot_roc_curve(y_test, y_prob, show: bool = False):
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2,
             label=f'ROC Curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig('roc_curve.png', dpi=150)
    plt.close()  # Close the figure to free memory
    print("[+] Saved: roc_curve.png")

def plot_feature_importance(clf, n_top=15, show: bool = False):
    feature_names = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes',
        'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
        'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
        'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
        'num_access_files', 'num_outbound_cmds', 'is_host_login',
        'is_guest_login', 'count', 'srv_count', 'serror_rate',
        'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
        'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
        'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
        'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
        'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
        'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
        'dst_host_srv_rerror_rate'
    ]
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1][:n_top]

    plt.figure(figsize=(10, 6))
    plt.title(f'Top {n_top} Feature Importances')
    plt.barh(
        range(n_top),
        importances[indices][::-1],
        color='steelblue'
    )
    plt.yticks(range(n_top), [feature_names[i] for i in indices][::-1])
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=150)
    plt.close()  # Close the figure to free memory
    print("[+] Saved: feature_importance.png")

# =============================================================================
# 7. MAIN
# =============================================================================
def main():
    print("=" * 60)
    print("  INTRUSION DETECTION SYSTEM — ML Pipeline")
    print("=" * 60)

    # Load
    df_train, df_test = load_data()

    # Preprocess
    X_train, X_test, y_train, y_test, scaler, encoders = preprocess(
        df_train, df_test
    )

    # Train
    clf = train_model(X_train, y_train)

    # Evaluate
    y_pred, y_prob = evaluate(clf, X_test, y_test)

    # Visualize
    plot_confusion_matrix(y_test, y_pred)
    plot_roc_curve(y_test, y_prob)
    plot_feature_importance(clf)

    print("\n[+] All done. Check generated PNG files.")

def feature_order() -> list[str]:
    # Order must match the columns after preprocess/drop.
    return [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes',
        'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
        'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
        'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
        'num_access_files', 'num_outbound_cmds', 'is_host_login',
        'is_guest_login', 'count', 'srv_count', 'serror_rate',
        'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
        'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
        'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
        'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
        'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
        'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
        'dst_host_srv_rerror_rate'
    ]


def train_and_save_artifacts(
    model_path: str,
    scaler_path: str,
    encoders_path: str,
    config_path: str,
    plots_dir: str,
):
    # Train using the existing pipeline
    df_train, df_test = load_data()
    X_train, X_test, y_train, y_test, scaler, encoders = preprocess(df_train, df_test)
    clf = train_model(X_train, y_train)

    y_pred, y_prob = evaluate(clf, X_test, y_test)

    # Generate plots (matplotlib Agg backend)
    plot_confusion_matrix(y_test, y_pred)
    plot_roc_curve(y_test, y_prob)
    plot_feature_importance(clf)

    # Ensure artifacts directory exists
    os.makedirs(os.path.dirname(model_path) or '.', exist_ok=True)

    joblib.dump(clf, model_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(encoders, encoders_path)

    # Save config (feature order)
    import json
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump({"feature_order": feature_order()}, f)

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "plots_generated": True,
    }
    return clf, scaler, encoders, feature_order(), metrics


def _encode_single_record(raw_features: Dict[str, Any], encoders: Dict[str, LabelEncoder]) -> Dict[str, Any]:
    # Copy and encode categorical fields
    out = dict(raw_features)
    for col in CATEGORICAL:
        if col not in out:
            raise KeyError(f"Missing feature: {col}")
        le = encoders[col]
        out[col] = int(le.transform([out[col]])[0])
    return out


def predict_from_features(
    model: Any,
    scaler: Any,
    encoders: Dict[str, LabelEncoder],
    feature_order: list[str],
    raw_features: Dict[str, Any],
):
    # Encode & order
    encoded = _encode_single_record(raw_features, encoders)

    row = []
    for f in feature_order:
        if f not in encoded:
            raise KeyError(f"Missing feature: {f}")
        row.append(encoded[f])

    X = np.array([row], dtype=float)
    X_scaled = scaler.transform(X)

    pred = int(model.predict(X_scaled)[0])
    prob_attack = float(model.predict_proba(X_scaled)[0][1])

    return {
        "prediction": "Attack" if pred == 1 else "Normal",
        "predicted_binary": pred,
        "confidence": prob_attack,
        "probability_attack": prob_attack,
    }


if __name__ == '__main__':
    main()
