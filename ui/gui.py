import pygame
import chess
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState
from ml.model import ChessAI

class ChessGUI:
    """Simple Pygame-based chess GUI"""
    
    def __init__(self):
        pygame.init()
        
        # Constants
        self.BOARD_SIZE = 640
        self.SQUARE_SIZE = self.BOARD_SIZE // 8
        self.WHITE = (240, 217, 181)
        self.BLACK = (181, 136, 99)
        self.HIGHLIGHT = (255, 255, 0, 128)
        self.SELECTED = (0, 255, 0, 128)
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.BOARD_SIZE, self.BOARD_SIZE + 100))
        pygame.display.set_caption("AI Chess Game")
        
        # Game state
        self.game = GameState(player_color=chess.WHITE)
        self.selected_square = None
        self.legal_moves = []
        
        # AI
        self.ai = None
        try:
            self.ai = ChessAI("models/chess_model.h5")
            print("✅ AI model loaded successfully!")
        except:
            print("⚠️ AI model not found. AI will make random moves.")
        
        # Font for text
        self.font = pygame.font.Font(None, 36)
        
        # Piece symbols (Unicode)
        self.piece_symbols = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
    
    def square_to_coords(self, square: int) -> tuple:
        """Convert chess square to screen coordinates"""
        row = 7 - (square // 8)
        col = square % 8
        return col * self.SQUARE_SIZE, row * self.SQUARE_SIZE
    
    def coords_to_square(self, x: int, y: int) -> int:
        """Convert screen coordinates to chess square"""
        col = x // self.SQUARE_SIZE
        row = 7 - (y // self.SQUARE_SIZE)
        return row * 8 + col
    
    def draw_board(self):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                rect = pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                                 self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
    
    def draw_pieces(self):
        """Draw chess pieces on the board"""
        for square in chess.SQUARES:
            piece = self.game.board.board.piece_at(square)
            if piece:
                x, y = self.square_to_coords(square)
                symbol = self.piece_symbols.get(piece.symbol(), '?')
                
                # Render piece
                text = self.font.render(symbol, True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + self.SQUARE_SIZE // 2, 
                                                y + self.SQUARE_SIZE // 2))
                self.screen.blit(text, text_rect)
    
    def draw_highlights(self):
        """Draw square highlights"""
        # Highlight selected square
        if self.selected_square is not None:
            x, y = self.square_to_coords(self.selected_square)
            highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
            highlight_surface.set_alpha(128)
            highlight_surface.fill((0, 255, 0))
            self.screen.blit(highlight_surface, (x, y))
        
        # Highlight legal moves
        for move_uci in self.legal_moves:
            try:
                move = chess.Move.from_uci(move_uci)
                if self.selected_square == move.from_square:
                    x, y = self.square_to_coords(move.to_square)
                    highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                    highlight_surface.set_alpha(64)
                    highlight_surface.fill((255, 255, 0))
                    self.screen.blit(highlight_surface, (x, y))
            except:
                continue
    
    def draw_status(self):
        """Draw game status"""
        y_offset = self.BOARD_SIZE + 10
        
        # Current turn
        turn_text = f"Turn: {'White' if self.game.board.board.turn else 'Black'}"
        if self.game.board.is_check():
            turn_text += " (CHECK!)"
        
        text = self.font.render(turn_text, True, (0, 0, 0))
        self.screen.blit(text, (10, y_offset))
        
        # Game status
        if self.game.game_over:
            status_text = f"Game Over: {self.game.game_result}"
            text = self.font.render(status_text, True, (255, 0, 0))
            self.screen.blit(text, (10, y_offset + 40))
    
    def handle_click(self, pos):
        """Handle mouse click on board"""
        if self.game.game_over or not self.game.is_player_turn():
            return
        
        x, y = pos
        if y >= self.BOARD_SIZE:  # Click below board
            return
        
        clicked_square = self.coords_to_square(x, y)
        
        if self.selected_square is None:
            # Select a square
            piece = self.game.board.board.piece_at(clicked_square)
            if piece and piece.color == self.game.player_color:
                self.selected_square = clicked_square
                self.legal_moves = self.game.board.get_legal_moves()
        else:
            # Try to make a move
            try:
                move_uci = chess.Move(self.selected_square, clicked_square).uci()
                result = self.game.make_player_move(move_uci)
                
                if result["success"]:
                    print(f"Player move: {move_uci}")
                    self.selected_square = None
                    self.legal_moves = []
                else:
                    # Invalid move, try selecting new square
                    piece = self.game.board.board.piece_at(clicked_square)
                    if piece and piece.color == self.game.player_color:
                        self.selected_square = clicked_square
                        self.legal_moves = self.game.board.get_legal_moves()
                    else:
                        self.selected_square = None
                        self.legal_moves = []
            except:
                self.selected_square = None
                self.legal_moves = []
    
    def make_ai_move(self):
        """Make AI move"""
        if self.game.game_over or not self.game.is_ai_turn():
            return
        
        if self.ai:
            try:
                ai_move = self.ai.predict_move(self.game.board.get_fen())
            except:
                # Fallback to random move
                import random
                legal_moves = self.game.board.get_legal_moves()
                ai_move = random.choice(legal_moves) if legal_moves else None
        else:
            # Random move
            import random
            legal_moves = self.game.board.get_legal_moves()
            ai_move = random.choice(legal_moves) if legal_moves else None
        
        if ai_move:
            result = self.game.make_ai_move(ai_move)
            if result["success"]:
                print(f"AI move: {ai_move}")
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reset game
                        self.game.reset_game()
                        self.selected_square = None
                        self.legal_moves = []
            
            # Make AI move if it's AI's turn
            self.make_ai_move()
            
            # Draw everything
            self.screen.fill((255, 255, 255))
            self.draw_board()
            self.draw_highlights()
            self.draw_pieces()
            self.draw_status()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = ChessGUI()
    game.run()