/**
 * Chess Game Logic and Board Management
 */

class ChessGame {
    constructor() {
        this.board = {};
        this.currentTurn = 'white';
        this.selectedSquare = null;
        this.legalMoves = [];
        this.gameOver = false;
        this.playerColor = 'white';
        this.moveHistory = [];
        this.capturedPieces = { white: [], black: [] };
        
        // Piece symbols
        this.pieceSymbols = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        };
        
        this.initializeBoard();
        this.bindEvents();
    }
    
    initializeBoard() {
        const boardElement = document.getElementById('chessBoard');
        boardElement.innerHTML = '';
        
        // Create 64 squares
        for (let rank = 8; rank >= 1; rank--) {
            for (let file = 0; file < 8; file++) {
                const square = document.createElement('div');
                const squareName = String.fromCharCode(97 + file) + rank;
                
                square.className = `square ${(rank + file) % 2 === 0 ? 'dark' : 'light'}`;
                square.dataset.square = squareName;
                square.addEventListener('click', (e) => this.handleSquareClick(e));
                
                boardElement.appendChild(square);
            }
        }
        
        this.loadGameState();
    }
    
    async loadGameState() {
        try {
            const response = await fetch('/api/game/board');
            const data = await response.json();
            
            this.board = data.board;
            this.currentTurn = data.turn;
            this.gameOver = data.game_over;
            
            this.updateBoardDisplay();
            this.updateGameStatus(data);
            
        } catch (error) {
            console.error('Failed to load game state:', error);
            this.showError('Failed to connect to game server');
        }
    }
    
    updateBoardDisplay() {
        // Clear all squares
        document.querySelectorAll('.square').forEach(square => {
            square.textContent = '';
            square.classList.remove('selected', 'legal-move', 'has-piece');
        });
        
        // Place pieces
        Object.entries(this.board).forEach(([square, pieceData]) => {
            const squareElement = document.querySelector(`[data-square="${square}"]`);
            if (squareElement && pieceData) {
                squareElement.textContent = this.pieceSymbols[pieceData.piece] || pieceData.piece;
                squareElement.classList.add('has-piece');
                console.log(`Placed piece ${pieceData.piece} on ${square}`);
            }
        });
        
        // Highlight selected square
        if (this.selectedSquare) {
            const selectedElement = document.querySelector(`[data-square="${this.selectedSquare}"]`);
            if (selectedElement) {
                selectedElement.classList.add('selected');
                console.log(`Highlighted selected square: ${this.selectedSquare}`);
            }
        }
        
        // Highlight legal moves
        if (document.getElementById('highlightMoves') && document.getElementById('highlightMoves').checked) {
            this.highlightLegalMoves();
        }
        
        console.log('Board updated. Current board state:', this.board);
        console.log('Current turn:', this.currentTurn, 'Player color:', this.playerColor);
    }
    
    async highlightLegalMoves() {
        if (!this.selectedSquare) return;
        
        try {
            const response = await fetch('/api/game/legal-moves');
            const data = await response.json();
            
            data.legal_moves.forEach(moveUci => {
                if (moveUci.startsWith(this.selectedSquare)) {
                    const toSquare = moveUci.substring(2, 4);
                    const squareElement = document.querySelector(`[data-square="${toSquare}"]`);
                    if (squareElement) {
                        squareElement.classList.add('legal-move');
                        if (squareElement.classList.contains('has-piece')) {
                            squareElement.classList.add('has-piece');
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Failed to get legal moves:', error);
        }
    }
    
    async handleSquareClick(event) {
        if (this.gameOver) return;
        
        const square = event.target.dataset.square;
        const piece = this.board[square];
        
        console.log(`Clicked square: ${square}, piece:`, piece, `selected: ${this.selectedSquare}`);
        
        // If no square is selected
        if (!this.selectedSquare) {
            if (piece && piece.color === this.playerColor && this.currentTurn === this.playerColor) {
                this.selectedSquare = square;
                console.log(`Selected square: ${square}`);
                this.updateBoardDisplay();
            } else {
                console.log(`Cannot select: piece=${piece}, playerColor=${this.playerColor}, currentTurn=${this.currentTurn}`);
            }
            return;
        }
        
        // If clicking the same square, deselect
        if (this.selectedSquare === square) {
            this.selectedSquare = null;
            console.log('Deselected square');
            this.updateBoardDisplay();
            return;
        }
        
        // If clicking another piece of the same color, select it
        if (piece && piece.color === this.playerColor && this.currentTurn === this.playerColor) {
            this.selectedSquare = square;
            console.log(`Reselected square: ${square}`);
            this.updateBoardDisplay();
            return;
        }
        
        // Try to make a move
        const move = this.selectedSquare + square;
        console.log(`Attempting move: ${move}`);
        await this.makeMove(move);
    }
    
    async makeMove(moveUci) {
        console.log(`Making move: ${moveUci}`);
        
        if (this.currentTurn !== this.playerColor) {
            this.showError("It's not your turn!");
            return;
        }
        
        this.showAIThinking(false);
        
        try {
            console.log('Sending move to server...');
            const response = await fetch('/api/game/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ move: moveUci })
            });
            
            const result = await response.json();
            console.log('Server response:', result);
            
            if (result.success) {
                console.log('Move successful!');
                
                // Play move sound
                this.playMoveSound();
                
                // Add to move history
                this.addMoveToHistory(moveUci, result.ai_move);
                
                // Clear selection
                this.selectedSquare = null;
                
                // Update board
                await this.loadGameState();
                
                // Show AI thinking if AI made a move
                if (result.ai_move) {
                    console.log(`AI played: ${result.ai_move}`);
                    this.showAIThinking(true);
                    setTimeout(() => {
                        this.showAIThinking(false);
                        this.playMoveSound();
                    }, 1000);
                }
                
                // Check for game over
                if (result.game_over) {
                    this.handleGameOver(result.result);
                }
                
            } else {
                console.error('Move failed:', result.error);
                this.showError(result.error || 'Invalid move');
                this.selectedSquare = null;
                this.updateBoardDisplay();
            }
            
        } catch (error) {
            console.error('Failed to make move:', error);
            this.showError('Failed to make move: ' + error.message);
            this.selectedSquare = null;
            this.updateBoardDisplay();
        }
    }
    
    updateGameStatus(data) {
        const turnElement = document.getElementById('currentTurn');
        const checkElement = document.getElementById('checkIndicator');
        const statusElement = document.getElementById('gameStatus');
        
        // Update turn indicator
        turnElement.textContent = `${data.turn.charAt(0).toUpperCase() + data.turn.slice(1)} to move`;
        
        // Show check indicator
        if (data.is_check) {
            checkElement.classList.remove('hidden');
        } else {
            checkElement.classList.add('hidden');
        }
        
        // Update game status
        if (data.game_over) {
            statusElement.textContent = data.result || 'Game Over';
            statusElement.style.color = '#dc3545';
        } else {
            statusElement.textContent = 'Game in progress';
            statusElement.style.color = '#28a745';
        }
    }
    
    addMoveToHistory(playerMove, aiMove) {
        const moveList = document.getElementById('moveList');
        const moveNumber = Math.floor(this.moveHistory.length / 2) + 1;
        
        let moveText = '';
        if (this.playerColor === 'white') {
            moveText = `${moveNumber}. ${playerMove}`;
            if (aiMove) {
                moveText += ` ${aiMove}`;
            }
        } else {
            if (this.moveHistory.length % 2 === 0) {
                moveText = `${moveNumber}. ... ${playerMove}`;
            } else {
                moveText = `${moveNumber}. ${playerMove}`;
            }
            if (aiMove) {
                moveText += ` ${aiMove}`;
            }
        }
        
        const moveItem = document.createElement('div');
        moveItem.className = 'move-item';
        moveItem.innerHTML = `<span>${moveText}</span>`;
        
        moveList.appendChild(moveItem);
        moveList.scrollTop = moveList.scrollHeight;
        
        this.moveHistory.push(playerMove);
        if (aiMove) {
            this.moveHistory.push(aiMove);
        }
    }
    
    showAIThinking(show) {
        const aiThinking = document.getElementById('aiThinking');
        if (show) {
            aiThinking.classList.remove('hidden');
        } else {
            aiThinking.classList.add('hidden');
        }
    }
    
    playMoveSound() {
        if (document.getElementById('soundEnabled').checked) {
            // Create a simple beep sound
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.value = 800;
            oscillator.type = 'sine';
            
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.1);
        }
    }
    
    handleGameOver(result) {
        const modal = document.getElementById('gameOverModal');
        const title = document.getElementById('gameOverTitle');
        const message = document.getElementById('gameOverMessage');
        
        title.textContent = 'Game Over';
        message.textContent = result;
        
        modal.classList.remove('hidden');
    }
    
    showError(message) {
        console.error('Chess Error:', message);
        
        // Use UI manager if available, otherwise fallback to alert
        if (window.uiManager) {
            window.uiManager.showNotification(message, 'error');
        } else {
            alert(message);
        }
    }
    
    async resetGame(playerColor = 'white') {
        try {
            const response = await fetch('/api/game/reset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ player_color: playerColor })
            });
            
            if (response.ok) {
                this.playerColor = playerColor;
                this.selectedSquare = null;
                this.moveHistory = [];
                this.capturedPieces = { white: [], black: [] };
                
                // Clear move history
                document.getElementById('moveList').innerHTML = '';
                
                // Clear captured pieces
                document.getElementById('capturedWhite').innerHTML = '';
                document.getElementById('capturedBlack').innerHTML = '';
                
                // Hide modal
                document.getElementById('gameOverModal').classList.add('hidden');
                
                // Reload game state
                await this.loadGameState();
                
                // Update color button
                const colorBtn = document.getElementById('colorBtn');
                colorBtn.textContent = playerColor === 'white' ? 'Play as Black' : 'Play as White';
            }
        } catch (error) {
            console.error('Failed to reset game:', error);
            this.showError('Failed to reset game');
        }
    }
    
    bindEvents() {
        // Reset button
        document.getElementById('resetBtn').addEventListener('click', () => {
            this.resetGame(this.playerColor);
        });
        
        // Color switch button
        document.getElementById('colorBtn').addEventListener('click', () => {
            const newColor = this.playerColor === 'white' ? 'black' : 'white';
            this.resetGame(newColor);
        });
        
        // Modal buttons
        document.getElementById('newGameBtn').addEventListener('click', () => {
            this.resetGame(this.playerColor);
        });
        
        document.getElementById('closeModalBtn').addEventListener('click', () => {
            document.getElementById('gameOverModal').classList.add('hidden');
        });
        
        // Settings
        document.getElementById('highlightMoves').addEventListener('change', () => {
            this.updateBoardDisplay();
        });
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chessGame = new ChessGame();
});