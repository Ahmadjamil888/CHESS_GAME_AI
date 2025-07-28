import chess
from typing import Dict, List, Tuple

class ChessPiece:
    """Base class for chess pieces"""
    
    PIECE_VALUES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    
    PIECE_SYMBOLS = {
        chess.PAWN: '♟',
        chess.KNIGHT: '♞',
        chess.BISHOP: '♝',
        chess.ROOK: '♜',
        chess.QUEEN: '♛',
        chess.KING: '♚'
    }
    
    @staticmethod
    def get_piece_value(piece_type: int) -> int:
        """Get the value of a piece type"""
        return ChessPiece.PIECE_VALUES.get(piece_type, 0)
    
    @staticmethod
    def get_piece_symbol(piece_type: int) -> str:
        """Get the Unicode symbol for a piece type"""
        return ChessPiece.PIECE_SYMBOLS.get(piece_type, '?')
    
    @staticmethod
    def get_all_piece_positions(board: chess.Board, color: bool) -> Dict[int, List[int]]:
        """Get positions of all pieces for a given color"""
        pieces = {}
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == color:
                if piece.piece_type not in pieces:
                    pieces[piece.piece_type] = []
                pieces[piece.piece_type].append(square)
        return pieces
    
    @staticmethod
    def count_material(board: chess.Board, color: bool) -> int:
        """Count total material value for a color"""
        total = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == color:
                total += ChessPiece.get_piece_value(piece.piece_type)
        return total