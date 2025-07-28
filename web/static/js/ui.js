/**
 * UI Helper Functions and Animations
 */

class UIManager {
    constructor() {
        this.initializeUI();
        this.setupAnimations();
    }
    
    initializeUI() {
        this.updateAIStatus();
        this.setupTooltips();
        this.setupKeyboardShortcuts();
    }
    
    async updateAIStatus() {
        const statusIndicator = document.querySelector('.status-indicator');
        const statusText = document.querySelector('.status-text');
        
        try {
            // Check if AI is available by making a test request
            const response = await fetch('/api/game/status');
            if (response.ok) {
                statusIndicator.className = 'status-indicator';
                statusText.textContent = 'AI Ready';
            } else {
                statusIndicator.className = 'status-indicator error';
                statusText.textContent = 'AI Unavailable';
            }
        } catch (error) {
            statusIndicator.className = 'status-indicator error';
            statusText.textContent = 'Connection Error';
        }
    }
    
    setupTooltips() {
        // Add tooltips to buttons and controls
        const tooltips = {
            'resetBtn': 'Start a new game',
            'colorBtn': 'Switch playing color',
            'soundEnabled': 'Toggle move sound effects',
            'highlightMoves': 'Show legal moves when piece is selected'
        };
        
        Object.entries(tooltips).forEach(([id, text]) => {
            const element = document.getElementById(id);
            if (element) {
                element.title = text;
            }
        });
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Prevent shortcuts when typing in inputs
            if (e.target.tagName === 'INPUT') return;
            
            switch (e.key.toLowerCase()) {
                case 'r':
                    if (e.ctrlKey || e.metaKey) {
                        e.preventDefault();
                        document.getElementById('resetBtn').click();
                    }
                    break;
                case 'escape':
                    // Clear selection
                    if (window.chessGame) {
                        window.chessGame.selectedSquare = null;
                        window.chessGame.updateBoardDisplay();
                    }
                    // Close modal
                    document.getElementById('gameOverModal').classList.add('hidden');
                    break;
                case 'h':
                    // Toggle highlight moves
                    const highlightCheckbox = document.getElementById('highlightMoves');
                    highlightCheckbox.checked = !highlightCheckbox.checked;
                    highlightCheckbox.dispatchEvent(new Event('change'));
                    break;
                case 's':
                    // Toggle sound
                    const soundCheckbox = document.getElementById('soundEnabled');
                    soundCheckbox.checked = !soundCheckbox.checked;
                    break;
            }
        });
    }
    
    setupAnimations() {
        // Add entrance animations
        this.animateOnLoad();
        
        // Setup hover effects
        this.setupHoverEffects();
    }
    
    animateOnLoad() {
        // Animate header
        const header = document.querySelector('.header');
        header.style.opacity = '0';
        header.style.transform = 'translateY(-20px)';
        
        setTimeout(() => {
            header.style.transition = 'all 0.6s ease';
            header.style.opacity = '1';
            header.style.transform = 'translateY(0)';
        }, 100);
        
        // Animate game area
        const gameArea = document.querySelector('.game-area');
        gameArea.style.opacity = '0';
        gameArea.style.transform = 'translateX(-20px)';
        
        setTimeout(() => {
            gameArea.style.transition = 'all 0.6s ease';
            gameArea.style.opacity = '1';
            gameArea.style.transform = 'translateX(0)';
        }, 200);
        
        // Animate sidebar
        const sidebar = document.querySelector('.sidebar');
        sidebar.style.opacity = '0';
        sidebar.style.transform = 'translateX(20px)';
        
        setTimeout(() => {
            sidebar.style.transition = 'all 0.6s ease';
            sidebar.style.opacity = '1';
            sidebar.style.transform = 'translateX(0)';
        }, 300);
    }
    
    setupHoverEffects() {
        // Add subtle hover effects to squares
        document.addEventListener('mouseover', (e) => {
            if (e.target.classList.contains('square')) {
                e.target.style.transition = 'transform 0.1s ease';
                e.target.style.transform = 'scale(1.02)';
            }
        });
        
        document.addEventListener('mouseout', (e) => {
            if (e.target.classList.contains('square')) {
                e.target.style.transform = 'scale(1)';
            }
        });
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '15px 20px',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '500',
            zIndex: '1001',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease',
            maxWidth: '300px'
        });
        
        // Set background color based on type
        const colors = {
            info: '#17a2b8',
            success: '#28a745',
            warning: '#ffc107',
            error: '#dc3545'
        };
        notification.style.backgroundColor = colors[type] || colors.info;
        
        // Add to DOM
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after delay
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    showLoading(show = true) {
        const overlay = document.getElementById('loadingOverlay');
        if (show) {
            overlay.classList.remove('hidden');
        } else {
            overlay.classList.add('hidden');
        }
    }
    
    updateCapturedPieces(capturedWhite, capturedBlack) {
        const whiteContainer = document.getElementById('capturedWhite');
        const blackContainer = document.getElementById('capturedBlack');
        
        whiteContainer.innerHTML = capturedWhite.map(piece => 
            `<span class="captured-piece">${piece}</span>`
        ).join('');
        
        blackContainer.innerHTML = capturedBlack.map(piece => 
            `<span class="captured-piece">${piece}</span>`
        ).join('');
    }
    
    highlightLastMove(fromSquare, toSquare) {
        // Remove previous highlights
        document.querySelectorAll('.last-move').forEach(el => {
            el.classList.remove('last-move');
        });
        
        // Add new highlights
        const fromEl = document.querySelector(`[data-square="${fromSquare}"]`);
        const toEl = document.querySelector(`[data-square="${toSquare}"]`);
        
        if (fromEl) fromEl.classList.add('last-move');
        if (toEl) toEl.classList.add('last-move');
    }
    
    animatePieceMove(fromSquare, toSquare, callback) {
        const fromEl = document.querySelector(`[data-square="${fromSquare}"]`);
        const toEl = document.querySelector(`[data-square="${toSquare}"]`);
        
        if (!fromEl || !toEl) {
            if (callback) callback();
            return;
        }
        
        // Create animated piece
        const piece = fromEl.textContent;
        const animatedPiece = document.createElement('div');
        animatedPiece.textContent = piece;
        animatedPiece.className = 'animated-piece';
        
        // Position at source
        const fromRect = fromEl.getBoundingClientRect();
        const toRect = toEl.getBoundingClientRect();
        
        Object.assign(animatedPiece.style, {
            position: 'fixed',
            left: fromRect.left + 'px',
            top: fromRect.top + 'px',
            width: fromRect.width + 'px',
            height: fromRect.height + 'px',
            fontSize: window.getComputedStyle(fromEl).fontSize,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: '1000',
            pointerEvents: 'none',
            transition: 'all 0.3s ease'
        });
        
        document.body.appendChild(animatedPiece);
        
        // Hide original piece
        fromEl.style.opacity = '0';
        
        // Animate to destination
        setTimeout(() => {
            animatedPiece.style.left = toRect.left + 'px';
            animatedPiece.style.top = toRect.top + 'px';
        }, 50);
        
        // Clean up after animation
        setTimeout(() => {
            document.body.removeChild(animatedPiece);
            fromEl.style.opacity = '1';
            if (callback) callback();
        }, 350);
    }
}

// Initialize UI manager
document.addEventListener('DOMContentLoaded', () => {
    window.uiManager = new UIManager();
});