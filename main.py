#!/usr/bin/env python3
"""
AI-Powered Chess Game with Machine Learning Opponent
Main entry point for the chess game
"""

import sys
import os
import argparse
from game.game_state import GameState
from ml.data_generator import ChessDataGenerator
import chess

def play_console_game():
    """Play chess in console mode"""
    print("🏁 Welcome to AI Chess!")
    print("You are playing as White. Enter moves in UCI format (e.g., e2e4)")
    print("Type 'quit' to exit, 'help' for commands\n")
    
    game = GameState(player_color=chess.WHITE)
    
    while not game.game_over:
        # Display current position
        print(f"\nCurrent position (FEN): {game.board.get_fen()}")
        print(f"Turn: {'White' if game.board.board.turn else 'Black'}")
        
        if game.board.is_check():
            print("⚠️  CHECK!")
        
        # Show board (simple ASCII representation)
        print("\n" + str(game.board.board))
        
        if game.is_player_turn():
            # Player's turn
            print(f"\nYour turn! Legal moves: {', '.join(game.board.get_legal_moves()[:10])}...")
            
            while True:
                move_input = input("Enter your move: ").strip().lower()
                
                if move_input == 'quit':
                    print("Thanks for playing!")
                    return
                elif move_input == 'help':
                    print("Commands: quit, help")
                    print("Move format: e2e4 (from square to square)")
                    continue
                
                result = game.make_player_move(move_input)
                if result["success"]:
                    print(f"✅ You played: {move_input}")
                    break
                else:
                    print(f"❌ {result['error']}. Try again.")
        
        else:
            # AI's turn - for now, make a random legal move
            legal_moves = game.board.get_legal_moves()
            if legal_moves:
                import random
                ai_move = random.choice(legal_moves)
                result = game.make_ai_move(ai_move)
                if result["success"]:
                    print(f"🤖 AI played: {ai_move}")
                else:
                    print("AI failed to make a move!")
                    break
    
    # Game over
    print(f"\n🎯 Game Over! Result: {game.game_result}")
    if game.winner is not None:
        winner_color = "White" if game.winner else "Black"
        print(f"🏆 Winner: {winner_color}")

def generate_training_data():
    """Generate training data for the ML model"""
    print("🔄 Generating training data...")
    
    generator = ChessDataGenerator()
    data = generator.generate_full_dataset(num_games=500, num_tactical=200)
    generator.save_dataset(data)
    
    print("✅ Training data generated successfully!")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AI-Powered Chess Game")
    parser.add_argument("--mode", choices=["play", "generate-data", "train"], 
                       default="play", help="Game mode")
    
    args = parser.parse_args()
    
    if args.mode == "play":
        play_console_game()
    elif args.mode == "generate-data":
        generate_training_data()
    elif args.mode == "train":
        print("🚧 Model training not implemented yet!")
        print("Run with --mode generate-data first to create training data")
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()