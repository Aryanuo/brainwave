import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from model import (
    load_and_merge_datasets, 
    get_column_types, 
    get_preprocessor, 
    train_rf, 
    train_iso,
    SIMULATION_FEATURES
)

def run_training_pipeline():
    base_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.abspath(os.path.join(base_path, "..", "..", "dataset", "extracted"))
    
    # 1. Data Preparation
    print("Loading and merging data...")
    df = load_and_merge_datasets(dataset_path)
    
    target_col = 'Label' if 'Label' in df.columns else 'label'

    print(f"Original columns: {len(df.columns)}")
    available_features = [col for col in SIMULATION_FEATURES if col in df.columns]
    df = df[available_features + [target_col]]
    print(f"Filtered columns for simulation: {len(df.columns)}")
    
    # 2. Extract Column Types via model.py function
    num_cols, cat_cols = get_column_types(df, target_col)
    
    # 3. Split and Transform
    X = df.drop(columns=[target_col])
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=1)
    
    print("Preprocessing data...")
    preprocessor = get_preprocessor(num_cols, cat_cols)
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)
    
    # 4. Train Models via model.py functions
    print("Training Random Forest...")
    rf_model = train_rf(X_train_transformed, y_train)
    

    y_pred = rf_model.predict(X_test_transformed)
    print("Validation Report:")
    print(classification_report(y_test, y_pred))

    print("Training Isolation Forest...")
    iso_model = train_iso(X_train_transformed)
    
    # 5. Save Artifacts for API
    joblib.dump(rf_model, os.path.join(base_path, 'rf_model.pkl'))
    joblib.dump(iso_model, os.path.join(base_path, 'iso_model.pkl'))
    joblib.dump(preprocessor, os.path.join(base_path, 'preprocessor.pkl'))
    
    print("Training complete. Models saved successfully.")

if __name__ == "__main__":
    run_training_pipeline()
