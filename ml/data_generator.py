import chess
import chess.engine
import json
import random
from typing import List, Dict, Tuple
from .utils import ChessEncoder

class ChessDataGenerator:
    """Generate training data from chess games"""
    
    def __init__(self):
        self.encoder = ChessEncoder()
    
    def generate_random_game_data(self, num_games: int = 1000) -> List[Dict]:
        """Generate training data from random games"""
        data = []
        
        for game_idx in range(num_games):
            board = chess.Board()
            game_moves = []
            
            # Play random moves until game ends or max moves reached
            max_moves = 100
            move_count = 0
            
            while not board.is_game_over() and move_count < max_moves:
                legal_moves = list(board.legal_moves)
                if not legal_moves:
                    break
                
                # Choose random legal move
                move = random.choice(legal_moves)
                
                # Store position and move
                data.append({
                    "fen": board.fen(),
                    "move": move.uci(),
                    "game_id": game_idx,
                    "move_number": move_count
                })
                
                board.push(move)
                move_count += 1
            
            if game_idx % 100 == 0:
                print(f"Generated {game_idx} games...")
        
        return data
    
    def generate_tactical_positions(self, num_positions: int = 500) -> List[Dict]:
        """Generate positions with tactical themes"""
        data = []
        
        # Common tactical patterns
        tactical_fens = [
            # Back rank mate threats
            "r5k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1",
            # Pin tactics
            "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 1",
            # Fork opportunities
            "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 2",
        ]
        
        for i in range(num_positions):
            # Use random tactical position
            fen = random.choice(tactical_fens)
            board = chess.Board(fen)
            
            if board.legal_moves:
                # Pick a random legal move as "best"
                move = random.choice(list(board.legal_moves))
                
                data.append({
                    "fen": fen,
                    "move": move.uci(),
                    "tactical": True,
                    "position_id": i
                })
        
        return data
    
    def save_dataset(self, data: List[Dict], filename: str = "data/chess_dataset.json"):
        """Save dataset to JSON file"""
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved {len(data)} positions to {filename}")
    
    def load_dataset(self, filename: str = "data/chess_dataset.json") -> List[Dict]:
        """Load dataset from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            print(f"Loaded {len(data)} positions from {filename}")
            return data
        except FileNotFoundError:
            print(f"Dataset file {filename} not found")
            return []
    
    def generate_full_dataset(self, num_games: int = 1000, num_tactical: int = 500) -> List[Dict]:
        """Generate complete dataset with random games and tactical positions"""
        print("Generating random game data...")
        game_data = self.generate_random_game_data(num_games)
        
        print("Generating tactical positions...")
        tactical_data = self.generate_tactical_positions(num_tactical)
        
        # Combine datasets
        full_data = game_data + tactical_data
        random.shuffle(full_data)
        
        return full_data