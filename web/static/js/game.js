/**
 * Game Integration and Advanced Features
 */

class GameManager {
    constructor() {
        this.gameState = null;
        this.connectionStatus = 'disconnected';
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        
        this.initializeConnection();
        this.setupPeriodicUpdates();
    }
    
    async initializeConnection() {
        try {
            await this.checkConnection();
            this.connectionStatus = 'connected';
            this.reconnectAttempts = 0;
            
            if (window.uiManager) {
                window.uiManager.showNotification('Connected to game server', 'success');
            }
        } catch (error) {
            this.connectionStatus = 'error';
            this.handleConnectionError();
        }
    }
    
    async checkConnection() {
        const response = await fetch('/api/game/status');
        if (!response.ok) {
            throw new Error('Server not responding');
        }
        return response.json();
    }
    
    handleConnectionError() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            
            if (window.uiManager) {
                window.uiManager.showNotification(
                    `Connection lost. Retrying... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`,
                    'warning'
                );
            }
            
            setTimeout(() => {
                this.initializeConnection();
            }, 2000 * this.reconnectAttempts);
        } else {
            if (window.uiManager) {
                window.uiManager.showNotification(
                    'Unable to connect to game server. Please refresh the page.',
                    'error'
                );
            }
        }
    }
    
    setupPeriodicUpdates() {
        // Check game state every 5 seconds
        setInterval(async () => {
            if (this.connectionStatus === 'connected') {
                try {
                    await this.syncGameState();
                } catch (error) {
                    console.warn('Failed to sync game state:', error);
                }
            }
        }, 5000);
    }
    
    async syncGameState() {
        try {
            const response = await fetch('/api/game/status');
            const gameInfo = await response.json();
            
            // Update local game state if needed
            if (window.chessGame && this.hasGameStateChanged(gameInfo)) {
                await window.chessGame.loadGameState();
            }
            
            this.gameState = gameInfo;
        } catch (error) {
            throw error;
        }
    }
    
    hasGameStateChanged(newState) {
        if (!this.gameState) return true;
        
        return (
            this.gameState.fen !== newState.fen ||
            this.gameState.game_over !== newState.game_over ||
            this.gameState.current_turn !== newState.current_turn
        );
    }
    
    // Game analysis features
    async analyzePosition() {
        try {
            const response = await fetch('/api/game/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                const analysis = await response.json();
                this.displayAnalysis(analysis);
            }
        } catch (error) {
            console.error('Failed to analyze position:', error);
        }
    }
    
    displayAnalysis(analysis) {
        // This could be expanded to show position evaluation, best moves, etc.
        console.log('Position analysis:', analysis);
    }
    
    // Save/Load game features
    saveGameToLocalStorage() {
        if (window.chessGame) {
            const gameData = {
                moveHistory: window.chessGame.moveHistory,
                playerColor: window.chessGame.playerColor,
                timestamp: Date.now()
            };
            
            localStorage.setItem('chess_game_save', JSON.stringify(gameData));
            
            if (window.uiManager) {
                window.uiManager.showNotification('Game saved locally', 'success');
            }
        }
    }
    
    loadGameFromLocalStorage() {
        try {
            const savedData = localStorage.getItem('chess_game_save');
            if (savedData) {
                const gameData = JSON.parse(savedData);
                
                // This would need backend support to restore game state
                console.log('Saved game found:', gameData);
                
                if (window.uiManager) {
                    window.uiManager.showNotification('Saved game found', 'info');
                }
                
                return gameData;
            }
        } catch (error) {
            console.error('Failed to load saved game:', error);
        }
        return null;
    }
    
    // Export game in PGN format
    async exportGamePGN() {
        try {
            const response = await fetch('/api/game/export/pgn');
            if (response.ok) {
                const pgnData = await response.text();
                this.downloadFile(pgnData, 'chess_game.pgn', 'text/plain');
            }
        } catch (error) {
            console.error('Failed to export PGN:', error);
        }
    }
    
    downloadFile(content, filename, contentType) {
        const blob = new Blob([content], { type: contentType });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
    }
    
    // Performance monitoring
    trackPerformance() {
        // Track move response times
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            const startTime = performance.now();
            const response = await originalFetch(...args);
            const endTime = performance.now();
            
            if (args[0].includes('/api/game/move')) {
                console.log(`Move request took ${endTime - startTime}ms`);
            }
            
            return response;
        };
    }
    
    // Accessibility features
    setupAccessibility() {
        // Add keyboard navigation for board
        document.addEventListener('keydown', (e) => {
            if (e.target.classList.contains('square')) {
                this.handleSquareKeyboard(e);
            }
        });
        
        // Add ARIA labels
        this.addAriaLabels();
    }
    
    handleSquareKeyboard(e) {
        const currentSquare = e.target;
        const squares = Array.from(document.querySelectorAll('.square'));
        const currentIndex = squares.indexOf(currentSquare);
        
        let newIndex = currentIndex;
        
        switch (e.key) {
            case 'ArrowUp':
                newIndex = Math.max(0, currentIndex - 8);
                break;
            case 'ArrowDown':
                newIndex = Math.min(squares.length - 1, currentIndex + 8);
                break;
            case 'ArrowLeft':
                newIndex = Math.max(0, currentIndex - 1);
                break;
            case 'ArrowRight':
                newIndex = Math.min(squares.length - 1, currentIndex + 1);
                break;
            case 'Enter':
            case ' ':
                currentSquare.click();
                return;
        }
        
        if (newIndex !== currentIndex) {
            e.preventDefault();
            squares[newIndex].focus();
        }
    }
    
    addAriaLabels() {
        // Add labels to squares
        document.querySelectorAll('.square').forEach(square => {
            const squareName = square.dataset.square;
            square.setAttribute('aria-label', `Square ${squareName}`);
            square.setAttribute('tabindex', '0');
            square.setAttribute('role', 'button');
        });
        
        // Add labels to buttons
        const buttons = {
            'resetBtn': 'Reset game',
            'colorBtn': 'Switch player color',
            'newGameBtn': 'Start new game',
            'closeModalBtn': 'Close dialog'
        };
        
        Object.entries(buttons).forEach(([id, label]) => {
            const element = document.getElementById(id);
            if (element) {
                element.setAttribute('aria-label', label);
            }
        });
    }
}

// Initialize game manager
document.addEventListener('DOMContentLoaded', () => {
    window.gameManager = new GameManager();
    
    // Setup additional features
    window.gameManager.trackPerformance();
    window.gameManager.setupAccessibility();
    
    // Load saved game if available
    const savedGame = window.gameManager.loadGameFromLocalStorage();
    if (savedGame) {
        console.log('Saved game available:', savedGame);
    }
    
    // Auto-save game periodically
    setInterval(() => {
        if (window.chessGame && window.chessGame.moveHistory.length > 0) {
            window.gameManager.saveGameToLocalStorage();
        }
    }, 30000); // Save every 30 seconds
});