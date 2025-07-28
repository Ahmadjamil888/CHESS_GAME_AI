#!/usr/bin/env python3
"""
Quick test of the chess game functionality
"""

from game.game_state import GameState
from ml.data_generator import ChessDataGenerator
import chess

def test_basic_game():
    """Test basic game functionality"""
    print("🧪 Testing basic game functionality...")
    
    # Create game
    game = GameState(player_color=chess.WHITE)
    
    # Test initial state
    assert not game.game_over
    assert game.is_player_turn()
    assert not game.is_ai_turn()
    
    # Make a move
    result = game.make_player_move("e2e4")
    assert result["success"]
    assert result["move"] == "e2e4"
    
    # Now it should be AI's turn
    assert not game.is_player_turn()
    assert game.is_ai_turn()
    
    # Make AI move
    legal_moves = game.board.get_legal_moves()
    ai_move = legal_moves[0]  # Pick first legal move
    result = game.make_ai_move(ai_move)
    assert result["success"]
    
    print("✅ Basic game functionality works!")

def test_data_generation():
    """Test data generation"""
    print("🧪 Testing data generation...")
    
    generator = ChessDataGenerator()
    
    # Generate small dataset
    data = generator.generate_random_game_data(num_games=2)
    assert len(data) > 0
    
    # Check data format
    example = data[0]
    assert "fen" in example
    assert "move" in example
    
    print(f"✅ Generated {len(data)} training examples!")

def test_chess_encoding():
    """Test chess position encoding"""
    print("🧪 Testing chess encoding...")
    
    from ml.utils import ChessEncoder
    
    encoder = ChessEncoder()
    
    # Test FEN encoding
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    tensor = encoder.fen_to_tensor(fen)
    
    assert tensor.shape == (8, 8, 12)
    assert tensor.dtype == 'float32'
    
    # Test move encoding
    move_index = encoder.move_to_index("e2e4")
    assert isinstance(move_index, int)
    
    # Test reverse encoding
    move_uci = encoder.index_to_move(move_index)
    assert isinstance(move_uci, str)
    
    print("✅ Chess encoding works!")

if __name__ == "__main__":
    print("🚀 Running chess game tests...\n")
    
    try:
        test_basic_game()
        test_data_generation()
        test_chess_encoding()
        
        print("\n🎉 All tests passed! The chess game is ready to play!")
        print("\nNext steps:")
        print("1. Run: python main.py --mode play (console game)")
        print("2. Run: python ui/gui.py (GUI game)")
        print("3. Run: python scripts/train_model.py (train AI)")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()