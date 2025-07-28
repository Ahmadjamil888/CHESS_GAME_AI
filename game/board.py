import chess
import chess.engine
from typing import List, Optional, Tuple

class ChessBoard:
    """Chess board representation and basic operations"""
    
    def __init__(self):
        self.board = chess.Board()
        self.move_history = []
        
    def get_fen(self) -> str:
        """Get current board state in FEN format"""
        return self.board.fen()
    
    def get_legal_moves(self) -> List[str]:
        """Get all legal moves in UCI format"""
        return [move.uci() for move in self.board.legal_moves]
    
    def make_move(self, move_uci: str) -> bool:
        """Make a move and return success status"""
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history.append(move_uci)
                return True
            return False
        except:
            return False
    
    def undo_move(self) -> bool:
        """Undo the last move"""
        if self.board.move_stack:
            self.board.pop()
            if self.move_history:
                self.move_history.pop()
            return True
        return False
    
    def is_game_over(self) -> bool:
        """Check if game is over"""
        return self.board.is_game_over()
    
    def get_game_result(self) -> str:
        """Get game result"""
        if self.board.is_checkmate():
            return "Checkmate"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_insufficient_material():
            return "Draw - Insufficient Material"
        elif self.board.is_seventyfive_moves():
            return "Draw - 75 Move Rule"
        elif self.board.is_fivefold_repetition():
            return "Draw - Repetition"
        return "Game in progress"
    
    def is_check(self) -> bool:
        """Check if current player is in check"""
        return self.board.is_check()
    
    def get_piece_at(self, square: str) -> Optional[str]:
        """Get piece at square (e.g., 'e4')"""
        try:
            square_idx = chess.parse_square(square)
            piece = self.board.piece_at(square_idx)
            return piece.symbol() if piece else None
        except:
            return None
    
    def reset(self):
        """Reset board to starting position"""
        self.board = chess.Board()
        self.move_history = []