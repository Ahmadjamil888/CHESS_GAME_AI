#!/usr/bin/env python3
"""
Flask web server for chess game
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState
from ml.model import ChessAI
import chess
import json

app = Flask(__name__)
CORS(app)

# Global game state
game = None
ai = None

def initialize_game():
    """Initialize game and AI"""
    global game, ai
    game = GameState(player_color=chess.WHITE)
    
    # Try to load AI model
    try:
        ai = ChessAI("../models/chess_model.h5")
        print("✅ AI model loaded successfully!")
    except:
        print("⚠️ AI model not found. AI will make random moves.")
        ai = None

@app.route('/')
def index():
    """Serve the main chess game page"""
    return render_template('index.html')

@app.route('/api/game/status')
def get_game_status():
    """Get current game status"""
    if not game:
        initialize_game()
    
    return jsonify(game.get_game_info())

@app.route('/api/game/reset', methods=['POST'])
def reset_game():
    """Reset the game"""
    global game
    data = request.get_json() or {}
    player_color = chess.WHITE if data.get('player_color', 'white') == 'white' else chess.BLACK
    
    game = GameState(player_color=player_color)
    return jsonify({"success": True, "message": "Game reset"})

@app.route('/api/game/move', methods=['POST'])
def make_move():
    """Make a player move"""
    if not game:
        initialize_game()
    
    data = request.get_json()
    move_uci = data.get('move')
    
    if not move_uci:
        return jsonify({"success": False, "error": "No move provided"})
    
    # Make player move
    result = game.make_player_move(move_uci)
    
    if not result["success"]:
        return jsonify(result)
    
    # If game is not over and it's AI's turn, make AI move
    if not game.game_over and game.is_ai_turn():
        ai_move = get_ai_move()
        if ai_move:
            ai_result = game.make_ai_move(ai_move)
            result["ai_move"] = ai_move
            result["ai_result"] = ai_result
    
    return jsonify(result)

def get_ai_move():
    """Get AI move"""
    if ai:
        try:
            return ai.predict_move(game.board.get_fen())
        except Exception as e:
            print(f"AI prediction failed: {e}")
    
    # Fallback to random move
    import random
    legal_moves = game.board.get_legal_moves()
    return random.choice(legal_moves) if legal_moves else None

@app.route('/api/game/legal-moves')
def get_legal_moves():
    """Get legal moves for current position"""
    if not game:
        initialize_game()
    
    return jsonify({
        "legal_moves": game.board.get_legal_moves(),
        "current_turn": "white" if game.board.board.turn else "black"
    })

@app.route('/api/game/board')
def get_board():
    """Get current board state"""
    if not game:
        initialize_game()
    
    # Convert board to JSON format
    board_data = {}
    for square in chess.SQUARES:
        piece = game.board.board.piece_at(square)
        if piece:
            square_name = chess.square_name(square)
            board_data[square_name] = {
                "piece": piece.symbol(),
                "color": "white" if piece.color else "black"
            }
    
    return jsonify({
        "board": board_data,
        "fen": game.board.get_fen(),
        "turn": "white" if game.board.board.turn else "black",
        "is_check": game.board.is_check(),
        "game_over": game.game_over,
        "result": game.game_result
    })

if __name__ == '__main__':
    initialize_game()
    app.run(debug=True, host='0.0.0.0', port=5000)