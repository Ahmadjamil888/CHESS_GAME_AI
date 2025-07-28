# 🏁 AI-Powered Chess Game with Machine Learning

A fully functional chess game where you play against an AI opponent powered by machine learning. Features complete chess rules, a neural network trained on thousands of positions, and both console and GUI interfaces.

## ✨ Features

- ✅ **Complete Chess Rules**: All FIDE rules including castling, en passant, promotion, check, checkmate, and stalemate
- 🤖 **AI Opponent**: Neural network trained on chess positions to predict the best moves
- 🎮 **Multiple Interfaces**: Play in console mode or with a graphical interface
- 📊 **Training Pipeline**: Generate training data and train your own chess AI
- 🎯 **FEN Support**: Uses standard chess notation for position representation

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd chess-ml-game
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Playing the Game

**Console Mode** (recommended for first run):
```bash
python main.py --mode play
```

**GUI Mode**:
```bash
python ui/gui.py
```

### Training Your Own AI

1. **Generate training data**:
   ```bash
   python main.py --mode generate-data
   ```

2. **Train the model**:
   ```bash
   python scripts/train_model.py
   ```

3. **Play against your trained AI**:
   ```bash
   python ui/gui.py
   ```

## 📂 Project Structure

```
chess-ml-game/
├── game/                   # Chess game engine
│   ├── board.py           # Board representation and operations
│   ├── pieces.py          # Piece types and values
│   ├── rules.py           # Chess rules validation
│   └── game_state.py      # Game flow management
├── ml/                    # Machine learning components
│   ├── model.py           # Neural network architecture
│   ├── data_generator.py  # Training data generation
│   └── utils.py           # ML utilities and encoding
├── ui/                    # User interfaces
│   └── gui.py             # Pygame-based GUI
├── scripts/               # Utility scripts
│   └── train_model.py     # Model training script
├── data/                  # Generated datasets
├── models/                # Trained models
├── main.py                # Main entry point
└── requirements.txt       # Dependencies
```

## 🎮 How to Play

### Console Mode
- Enter moves in UCI format (e.g., `e2e4` to move pawn from e2 to e4)
- Type `quit` to exit or `help` for commands
- The AI will automatically respond after your move

### GUI Mode
- Click on a piece to select it
- Click on a destination square to move
- Press `R` to reset the game
- The AI moves automatically after your turn

## 🤖 AI Architecture

The chess AI uses a convolutional neural network:

- **Input**: 8×8×12 tensor representing the board state
  - 12 channels for different piece types (6 white + 6 black)
- **Architecture**: 
  - 3 convolutional layers with batch normalization
  - 2 dense layers with dropout
  - Softmax output layer for move probabilities
- **Training**: Supervised learning on generated chess positions
- **Output**: UCI move format (e.g., "e2e4")

## 📊 Training Data

The system generates training data through:

1. **Random Games**: Simulated games with random legal moves
2. **Tactical Positions**: Common chess patterns and tactics
3. **Format**: JSON with FEN positions and corresponding moves

Example data point:
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
  "move": "e7e5",
  "game_id": 42,
  "move_number": 1
}
```

## 🔧 Configuration

### Model Parameters
- **Epochs**: 20 (adjustable in `train_model.py`)
- **Batch Size**: 64
- **Learning Rate**: 0.001
- **Architecture**: CNN + Dense layers

### Data Generation
- **Random Games**: 500 games by default
- **Tactical Positions**: 200 positions
- **Total Dataset**: ~700 training examples

## 🎯 Performance

The AI's strength depends on training data quality and quantity. With the default dataset:
- **Beginner Level**: Makes legal moves consistently
- **Improvement**: Train on more data or use chess engine games for stronger play

## 🚧 Future Enhancements

- [ ] **Reinforcement Learning**: AlphaZero-style self-play training
- [ ] **Opening Book**: Database of common opening moves
- [ ] **Endgame Tablebase**: Perfect endgame play
- [ ] **Position Evaluation**: Board evaluation function
- [ ] **Difficulty Levels**: Adjustable AI strength
- [ ] **Move Hints**: Suggest moves to human player
- [ ] **Game Analysis**: Post-game move analysis

## 🛠️ Development

### Adding New Features

1. **Game Logic**: Modify files in `game/` directory
2. **AI Improvements**: Update `ml/model.py` or training pipeline
3. **UI Changes**: Edit `ui/gui.py` for interface modifications

### Testing

Run the console version to test game logic:
```bash
python main.py --mode play
```

### Debugging

Enable verbose output in training:
```python
# In train_model.py
history = ai.train(..., verbose=2)
```

## 📝 Dependencies

- `python-chess`: Chess game logic and validation
- `tensorflow`: Neural network framework
- `pygame`: GUI interface
- `numpy`: Numerical computations
- `scikit-learn`: Data preprocessing
- `pandas`: Data manipulation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🎉 Acknowledgments

- Uses the excellent `python-chess` library for game logic
- Inspired by classical chess engines and modern AI approaches
- Built with educational purposes in mind

---

**Happy Chess Playing! 🏆**