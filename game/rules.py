import chess
from typing import List, Optional

class ChessRules:
    """Chess rules validation and special move handling"""
    
    @staticmethod
    def is_legal_move(board: chess.Board, move_uci: str) -> bool:
        """Check if a move is legal"""
        try:
            move = chess.Move.from_uci(move_uci)
            return move in board.legal_moves
        except:
            return False
    
    @staticmethod
    def is_castling_move(board: chess.Board, move_uci: str) -> bool:
        """Check if move is castling"""
        try:
            move = chess.Move.from_uci(move_uci)
            return board.is_castling(move)
        except:
            return False
    
    @staticmethod
    def is_en_passant_move(board: chess.Board, move_uci: str) -> bool:
        """Check if move is en passant"""
        try:
            move = chess.Move.from_uci(move_uci)
            return board.is_en_passant(move)
        except:
            return False
    
    @staticmethod
    def is_promotion_move(move_uci: str) -> bool:
        """Check if move is pawn promotion"""
        return len(move_uci) == 5 and move_uci[4] in 'qrbn'
    
    @staticmethod
    def get_promotion_piece(move_uci: str) -> Optional[int]:
        """Get promotion piece type from UCI move"""
        if ChessRules.is_promotion_move(move_uci):
            piece_map = {'q': chess.QUEEN, 'r': chess.ROOK, 'b': chess.BISHOP, 'n': chess.KNIGHT}
            return piece_map.get(move_uci[4].lower())
        return None
    
    @staticmethod
    def can_castle_kingside(board: chess.Board, color: bool) -> bool:
        """Check if kingside castling is possible"""
        return board.has_kingside_castling_rights(color)
    
    @staticmethod
    def can_castle_queenside(board: chess.Board, color: bool) -> bool:
        """Check if queenside castling is possible"""
        return board.has_queenside_castling_rights(color)
    
    @staticmethod
    def is_in_check(board: chess.Board, color: bool) -> bool:
        """Check if the given color is in check"""
        return board.is_check() and board.turn == color
    
    @staticmethod
    def is_checkmate(board: chess.Board) -> bool:
        """Check if current position is checkmate"""
        return board.is_checkmate()
    
    @staticmethod
    def is_stalemate(board: chess.Board) -> bool:
        """Check if current position is stalemate"""
        return board.is_stalemate()
    
    @staticmethod
    def get_attacking_squares(board: chess.Board, square: int, color: bool) -> List[int]:
        """Get all squares attacking the given square by the given color"""
        attacking_squares = []
        for attacker_square in chess.SQUARES:
            piece = board.piece_at(attacker_square)
            if piece and piece.color == color:
                if board.is_attacked_by(color, square):
                    attacking_squares.append(attacker_square)
        return attacking_squares