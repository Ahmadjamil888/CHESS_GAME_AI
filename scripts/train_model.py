#!/usr/bin/env python3
"""
Train the chess AI model
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from sklearn.model_selection import train_test_split
from ml.model import ChessAI
from ml.data_generator import ChessDataGenerator
from ml.utils import ChessEncoder

def prepare_training_data(dataset_path: str = "data/chess_dataset.json"):
    """Prepare training data from dataset"""
    print("📊 Loading and preparing training data...")
    
    # Load dataset
    generator = ChessDataGenerator()
    data = generator.load_dataset(dataset_path)
    
    if not data:
        print("❌ No dataset found. Generate data first with: python main.py --mode generate-data")
        return None, None, None, None
    
    print(f"Loaded {len(data)} training examples")
    
    # Prepare features and labels
    encoder = ChessEncoder()
    X = []
    y = []
    
    print("🔄 Converting positions to tensors...")
    for i, example in enumerate(data):
        try:
            # Convert FEN to tensor
            board_tensor = encoder.fen_to_tensor(example['fen'])
            X.append(board_tensor)
            
            # Convert move to index
            move_index = encoder.move_to_index(example['move'])
            y.append(move_index)
            
            if i % 1000 == 0:
                print(f"Processed {i}/{len(data)} examples...")
                
        except Exception as e:
            print(f"Error processing example {i}: {e}")
            continue
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"✅ Prepared {len(X)} training examples")
    print(f"Input shape: {X.shape}")
    print(f"Output shape: {y.shape}")
    
    # Split into train/validation/test sets
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    
    print(f"Training set: {len(X_train)} examples")
    print(f"Validation set: {len(X_val)} examples")
    print(f"Test set: {len(X_test)} examples")
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def train_model():
    """Train the chess AI model"""
    print("🚀 Starting model training...")
    
    # Prepare data
    X_train, X_val, X_test, y_train, y_val, y_test = prepare_training_data()
    
    if X_train is None:
        return
    
    # Create and train model
    ai = ChessAI()
    
    print("🏋️ Training model...")
    history = ai.train(
        X_train, y_train,
        X_val, y_val,
        epochs=20,
        batch_size=64
    )
    
    # Evaluate model
    print("📈 Evaluating model...")
    ai.evaluate(X_test, y_test)
    
    # Save model
    ai.save_model("models/chess_model.h5")
    
    print("✅ Training completed successfully!")

if __name__ == "__main__":
    # Create models directory
    os.makedirs("models", exist_ok=True)
    train_model()