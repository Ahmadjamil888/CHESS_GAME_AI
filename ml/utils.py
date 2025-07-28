import chess
import numpy as np
from typing import List, Tuple, Dict

class ChessEncoder:
    """Utilities for encoding chess positions and moves"""
    
    @staticmethod
    def fen_to_tensor(fen: str) -> np.ndarray:
        """Convert FEN string to neural network input tensor"""
        board = chess.Board(fen)
        
        # Create 8x8x12 tensor (12 piece types for each square)
        tensor = np.zeros((8, 8, 12), dtype=np.float32)
        
        piece_to_index = {
            chess.PAWN: 0, chess.KNIGHT: 1, chess.BISHOP: 2,
            chess.ROOK: 3, chess.QUEEN: 4, chess.KING: 5
        }
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                row = 7 - (square // 8)  # Flip for proper orientation
                col = square % 8
                piece_idx = piece_to_index[piece.piece_type]
                
                # White pieces: indices 0-5, Black pieces: indices 6-11
                if piece.color == chess.WHITE:
                    tensor[row, col, piece_idx] = 1.0
                else:
                    tensor[row, col, piece_idx + 6] = 1.0
        
        return tensor
    
    @staticmethod
    def move_to_index(move_uci: str) -> int:
        """Convert UCI move to index for classification"""
        # Simple encoding: from_square * 64 + to_square
        try:
            move = chess.Move.from_uci(move_uci)
            return move.from_square * 64 + move.to_square
        except:
            return 0
    
    @staticmethod
    def index_to_move(index: int) -> str:
        """Convert index back to UCI move"""
        from_square = index // 64
        to_square = index % 64
        
        try:
            move = chess.Move(from_square, to_square)
            return move.uci()
        except:
            return "a1a1"
    
    @staticmethod
    def get_all_possible_moves() -> List[str]:
        """Get all possible UCI moves (for output layer size)"""
        moves = []
        for from_sq in range(64):
            for to_sq in range(64):
                if from_sq != to_sq:
                    try:
                        move = chess.Move(from_sq, to_sq)
                        moves.append(move.uci())
                    except:
                        continue
        return moves
    
    @staticmethod
    def filter_legal_moves(board: chess.Board, predicted_moves: List[Tuple[str, float]]) -> str:
        """Filter predicted moves to only legal ones and return best"""
        legal_moves = [move.uci() for move in board.legal_moves]
        
        # Filter and sort by probability
        legal_predictions = [(move, prob) for move, prob in predicted_moves if move in legal_moves]
        
        if legal_predictions:
            # Return move with highest probability
            return max(legal_predictions, key=lambda x: x[1])[0]
        else:
            # Fallback to random legal move
            return np.random.choice(legal_moves) if legal_moves else "a1a1"