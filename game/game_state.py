import chess
from .board import ChessBoard
from .rules import ChessRules
from typing import Optional, Dict, Any

class GameState:
    """Manages the overall game state and flow"""
    
    def __init__(self, player_color: bool = chess.WHITE):
        self.board = ChessBoard()
        self.player_color = player_color  # True for White, False for Black
        self.ai_color = not player_color
        self.game_over = False
        self.winner = None
        self.game_result = None
        
    def is_player_turn(self) -> bool:
        """Check if it's the player's turn"""
        return self.board.board.turn == self.player_color
    
    def is_ai_turn(self) -> bool:
        """Check if it's the AI's turn"""
        return self.board.board.turn == self.ai_color
    
    def make_player_move(self, move_uci: str) -> Dict[str, Any]:
        """Make a player move and return result"""
        if not self.is_player_turn():
            return {"success": False, "error": "Not player's turn"}
        
        if not ChessRules.is_legal_move(self.board.board, move_uci):
            return {"success": False, "error": "Illegal move"}
        
        success = self.board.make_move(move_uci)
        if success:
            self._check_game_over()
            return {
                "success": True,
                "move": move_uci,
                "fen": self.board.get_fen(),
                "is_check": self.board.is_check(),
                "game_over": self.game_over,
                "result": self.game_result
            }
        else:
            return {"success": False, "error": "Failed to make move"}
    
    def make_ai_move(self, move_uci: str) -> Dict[str, Any]:
        """Make an AI move and return result"""
        if not self.is_ai_turn():
            return {"success": False, "error": "Not AI's turn"}
        
        success = self.board.make_move(move_uci)
        if success:
            self._check_game_over()
            return {
                "success": True,
                "move": move_uci,
                "fen": self.board.get_fen(),
                "is_check": self.board.is_check(),
                "game_over": self.game_over,
                "result": self.game_result
            }
        else:
            return {"success": False, "error": "Failed to make AI move"}
    
    def _check_game_over(self):
        """Check if the game is over and update state"""
        if self.board.is_game_over():
            self.game_over = True
            self.game_result = self.board.get_game_result()
            
            if self.board.board.is_checkmate():
                # Winner is the opposite of current turn (who just got checkmated)
                self.winner = not self.board.board.turn
            else:
                self.winner = None  # Draw
    
    def get_game_info(self) -> Dict[str, Any]:
        """Get current game information"""
        return {
            "fen": self.board.get_fen(),
            "player_color": "White" if self.player_color else "Black",
            "ai_color": "Black" if self.ai_color else "White",
            "current_turn": "White" if self.board.board.turn else "Black",
            "is_player_turn": self.is_player_turn(),
            "is_check": self.board.is_check(),
            "legal_moves": self.board.get_legal_moves(),
            "move_history": self.board.move_history,
            "game_over": self.game_over,
            "result": self.game_result,
            "winner": "White" if self.winner else "Black" if self.winner is False else None
        }
    
    def reset_game(self, player_color: bool = chess.WHITE):
        """Reset the game to initial state"""
        self.board.reset()
        self.player_color = player_color
        self.ai_color = not player_color
        self.game_over = False
        self.winner = None
        self.game_result = None