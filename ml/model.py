import tensorflow as tf
import numpy as np
import chess
from typing import List, Tuple
from .utils import ChessEncoder

class ChessAI:
    """Neural network model for chess move prediction"""
    
    def __init__(self, model_path: str = None):
        self.encoder = ChessEncoder()
        self.model = None
        self.model_path = model_path or "models/chess_model.h5"
        
        if model_path:
            self.load_model(model_path)
        else:
            self.build_model()
    
    def build_model(self):
        """Build the neural network architecture"""
        # Input: 8x8x12 board representation
        inputs = tf.keras.Input(shape=(8, 8, 12), name='board_input')
        
        # Convolutional layers for spatial pattern recognition
        x = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        
        # Flatten for dense layers
        x = tf.keras.layers.Flatten()(x)
        
        # Dense layers for move evaluation
        x = tf.keras.layers.Dense(512, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        
        # Output layer: probability distribution over all possible moves
        # Using 4096 outputs (64*64 possible from-to combinations)
        outputs = tf.keras.layers.Dense(4096, activation='softmax', name='move_output')(x)
        
        self.model = tf.keras.Model(inputs=inputs, outputs=outputs)
        
        # Compile model
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("✅ Model architecture built successfully!")
        print(f"Model parameters: {self.model.count_params():,}")
    
    def predict_move(self, fen: str) -> str:
        """Predict the best move for a given position"""
        if not self.model:
            raise ValueError("Model not loaded or built")
        
        # Convert FEN to tensor
        board_tensor = self.encoder.fen_to_tensor(fen)
        board_tensor = np.expand_dims(board_tensor, axis=0)  # Add batch dimension
        
        # Get model prediction
        predictions = self.model.predict(board_tensor, verbose=0)[0]
        
        # Convert predictions to move probabilities
        move_probs = []
        for i, prob in enumerate(predictions):
            move_uci = self.encoder.index_to_move(i)
            move_probs.append((move_uci, prob))
        
        # Sort by probability and filter legal moves
        move_probs.sort(key=lambda x: x[1], reverse=True)
        
        # Filter to only legal moves
        board = chess.Board(fen)
        best_move = self.encoder.filter_legal_moves(board, move_probs)
        
        return best_move
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, 
              X_val: np.ndarray = None, y_val: np.ndarray = None,
              epochs: int = 10, batch_size: int = 32):
        """Train the model"""
        if not self.model:
            self.build_model()
        
        # Prepare validation data
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        
        # Callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
            tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=2),
        ]
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        return history
    
    def save_model(self, path: str = None):
        """Save the trained model"""
        if not self.model:
            raise ValueError("No model to save")
        
        save_path = path or self.model_path
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        self.model.save(save_path)
        print(f"✅ Model saved to {save_path}")
    
    def load_model(self, path: str):
        """Load a trained model"""
        try:
            self.model = tf.keras.models.load_model(path)
            print(f"✅ Model loaded from {path}")
        except Exception as e:
            print(f"❌ Failed to load model from {path}: {e}")
            self.build_model()
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray):
        """Evaluate model performance"""
        if not self.model:
            raise ValueError("No model to evaluate")
        
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Loss: {loss:.4f}")
        print(f"Test Accuracy: {accuracy:.4f}")
        
        return loss, accuracy