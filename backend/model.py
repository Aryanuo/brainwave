import os
import glob
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import OrdinalEncoder, RobustScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, IsolationForest

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    for col in df.select_dtypes(include=[np.number]).columns:
        if not np.isfinite(df[col]).all():
            max_val = df[col].dropna().max() if not df[col].dropna().empty else 0
            df[col] = df[col].fillna(max_val)
    return df

def reduce_memory_usage(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        col_type = df[col].dtype
        if pd.api.types.is_numeric_dtype(col_type):
            col_min, col_max = df[col].min(), df[col].max()
            if pd.api.types.is_integer_dtype(col_type):
                if col_min >= 0:
                    if col_max <= np.iinfo(np.uint8).max: df[col] = df[col].astype(np.uint8)
                    elif col_max <= np.iinfo(np.uint16).max: df[col] = df[col].astype(np.uint16)
                    else: df[col] = df[col].astype(np.uint32)
                else:
                    if col_min >= np.iinfo(np.int8).min and col_max <= np.iinfo(np.int8).max: df[col] = df[col].astype(np.int8)
                    else: df[col] = df[col].astype(np.int32)
            elif pd.api.types.is_float_dtype(col_type):
                df[col] = df[col].astype(np.float32)
    return df

SIMULATION_FEATURES = [
    'Destination Port', 'Flow Duration', 'Total Fwd Packets', 
    'Total Backward Packets', 'Total Length of Fwd Packets', 
    'Total Length of Bwd Packets', 'Protocol'
]

def get_column_types(df: pd.DataFrame, target_col: str):
    available = [col for col in SIMULATION_FEATURES if col in df.columns]
    X = df[available]
    num_cols = X.select_dtypes(include=['number']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    return num_cols, cat_cols

def load_and_merge_datasets(directory_path: str) -> pd.DataFrame:
    all_files = glob.glob(os.path.join(directory_path, "*.csv"))
    df_list = []
    for filename in all_files:
        temp_df = pd.read_csv(filename).rename(columns=lambda x: x.strip())
        temp_df = clean_dataset(temp_df)
        temp_df = reduce_memory_usage(temp_df)
        df_list.append(temp_df)
    full_df = pd.concat(df_list, ignore_index=True)
    return full_df.loc[:, ~full_df.columns.duplicated()]

def get_preprocessor(num_cols, cat_cols):
    num_pipe = Pipeline([
        ('impute', SimpleImputer(strategy='median')),
        ('var', VarianceThreshold(threshold=0)),
        ('scaler', RobustScaler())
    ])
    cat_pipe = Pipeline([
        ('impute', SimpleImputer(strategy='most_frequent')),
        ('encode', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
    ])
    return ColumnTransformer([
        ('num', num_pipe, num_cols),
        ('cat', cat_pipe, cat_cols)
    ])

def train_rf(X, y):
    model = RandomForestClassifier(n_estimators=100, n_jobs=-1, class_weight = 'balanced_subsample', random_state=42)
    model.fit(X, y)
    return model

def train_iso(X):
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    return model

def compute_risk_score(rf_model, iso_model, preprocessor, df, benign_label='BENIGN'):
    X_t = preprocessor.transform(df)
    
    # 1. Get probabilities for EVERY class
    rf_proba = rf_model.predict_proba(X_t)
    classes = rf_model.classes_
    
    # 2. Isolation Forest prediction
    iso_raw = iso_model.predict(X_t)
    iso_pred = np.where(iso_raw == -1, 1, 0)

    results = []
    # SET CERTAINTY THRESHOLD (95%)
    BENIGN_THRESHOLD = 0.95

    for i in range(len(rf_proba)):
        # Find the index for Benign
        benign_idx = list(classes).index(next(c for c in classes if str(c).upper() == benign_label.upper()))
        prob_benign = rf_proba[i][benign_idx]
        
        # Find the best class that IS NOT benign
        attack_probs = np.delete(rf_proba[i], benign_idx)
        attack_classes = np.delete(classes, benign_idx)
        best_attack_idx = np.argmax(attack_probs)
        best_attack_name = attack_classes[best_attack_idx]
        best_attack_conf = attack_probs[best_attack_idx]

        # LOGIC: If model is NOT 95% sure it's benign OR IsoForest sees an anomaly
        if prob_benign < BENIGN_THRESHOLD or iso_pred[i] == 1:
            # Even if 'Benign' is the #1 choice, if it's below 95%, 
            # we report the name of the most likely attack.
            final_type = best_attack_name
            
            # Determine score based on how strong the attack signal is
            if iso_pred[i] == 1 and prob_benign < 0.5:
                score = 0.8 + (0.2 * best_attack_conf)
                label = 'High-Risk'
            else:
                score = 0.5 + (0.3 * (1 - prob_benign))
                label = 'Attack'
        else:
            # Extremely sure it is benign
            final_type = "BENIGN"
            score = 0.1 * prob_benign
            label = 'Benign'

        results.append({
            "attack_type": final_type, 
            "threat_score": float(score), 
            "risk_label": label
        })
    return results
