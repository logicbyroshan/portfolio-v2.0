// js/music.js - Enhanced Spotify Integration
document.addEventListener('DOMContentLoaded', () => {
    // Animation system is now handled by animations.js
    // No need for duplicate animation code here

    // Enhanced Playlist Loading
    loadPlaylistsFromAPI();

    // Handle playlist card clicks for better user experience
    setupPlaylistInteractions();
});

/**
 * Load playlists from the API and update the display
 */
async function loadPlaylistsFromAPI() {
    try {
        const response = await fetch('/music/api/playlists/');
        const data = await response.json();
        
        if (data.success && data.playlists.length > 0) {
            updatePlaylistGrid(data.playlists);
        } else {
            console.log('No playlists available, using default display');
        }
    } catch (error) {
        console.error('Failed to load playlists:', error);
        // Fallback to default template display
    }
}

/**
 * Update the playlist grid with API data
 */
function updatePlaylistGrid(playlists) {
    const playlistGrid = document.querySelector('.playlist-grid');
    if (!playlistGrid) return;

    // Create playlist cards
    const playlistCards = playlists.map(playlist => createPlaylistCard(playlist)).join('');
    
    // Update the grid
    playlistGrid.innerHTML = playlistCards;
    
    // Re-setup interactions
    setupPlaylistInteractions();
    
    // Re-trigger animations
    const newCards = playlistGrid.querySelectorAll('.playlist-card');
    newCards.forEach((card, index) => {
        setTimeout(() => card.classList.add('is-visible'), index * 100);
    });
}

/**
 * Create a playlist card HTML
 */
function createPlaylistCard(playlist) {
    const imageUrl = playlist.image_url || 'https://placehold.co/300x300/1a1a2e/16213e?text=No+Image';
    const description = playlist.description ? 
        (playlist.description.length > 50 ? playlist.description.substring(0, 50) + '...' : playlist.description) : 
        'No description available';
    
    return `
        <div class="playlist-card card" data-animation="zoom-in" data-playlist-id="${playlist.id}">
            <a href="/music/playlist/${playlist.id}/" class="playlist-image">
                <img src="${imageUrl}" alt="${playlist.name} playlist cover" loading="lazy">
                <div class="play-overlay">
                    <i class="fa-solid fa-play"></i>
                </div>
            </a>
            <div class="playlist-content">
                <h3>${playlist.name}</h3>
                <p class="playlist-description">${description}</p>
                <div class="playlist-meta">
                    <span class="track-count">${playlist.track_count} tracks</span>
                    ${playlist.last_synced ? `<span class="sync-time">Synced ${formatSyncTime(playlist.last_synced)}</span>` : ''}
                </div>
            </div>
            <div class="playlist-footer">
                <a href="/music/playlist/${playlist.id}/" class="outline-btn">
                    <i class="fa-solid fa-headphones-simple"></i> Listen
                </a>
                <button class="outline-btn spotify-redirect" data-spotify-url="https://open.spotify.com/playlist/${playlist.id}" data-playlist-name="${playlist.name}">
                    <i class="fa-brands fa-spotify"></i> Spotify
                </button>
            </div>
        </div>
    `;
}

/**
 * Setup playlist interactions
 */
function setupPlaylistInteractions() {
    // Handle Spotify redirect buttons
    document.querySelectorAll('.spotify-redirect').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const spotifyUrl = btn.dataset.spotifyUrl;
            const playlistName = btn.dataset.playlistName;
            
            // Show confirmation modal or directly open
            openSpotifyPlaylist(spotifyUrl, playlistName);
        });
    });

    // Handle playlist image clicks for preview
    document.querySelectorAll('.playlist-image').forEach(link => {
        link.addEventListener('click', (e) => {
            const playlistCard = link.closest('.playlist-card');
            playlistCard.classList.add('loading');
            
            // Remove loading class after navigation or timeout
            setTimeout(() => {
                playlistCard.classList.remove('loading');
            }, 2000);
        });
    });
}

/**
 * Open Spotify playlist with user feedback
 */
function openSpotifyPlaylist(spotifyUrl, playlistName) {
    // Create and show modal
    const modal = createSpotifyModal(spotifyUrl, playlistName);
    document.body.appendChild(modal);
    
    // Show modal
    setTimeout(() => modal.classList.add('show'), 10);
    
    // Auto-close after 5 seconds
    setTimeout(() => {
        closeSpotifyModal(modal);
    }, 5000);
}

/**
 * Create Spotify redirect modal
 */
function createSpotifyModal(spotifyUrl, playlistName) {
    const modal = document.createElement('div');
    modal.className = 'spotify-modal-overlay';
    modal.innerHTML = `
        <div class="spotify-modal">
            <div class="spotify-modal-header">
                <h3><i class="fa-brands fa-spotify"></i> Opening in Spotify</h3>
                <button class="close-btn" onclick="closeSpotifyModal(this.closest('.spotify-modal-overlay'))">
                    <i class="fa-solid fa-times"></i>
                </button>
            </div>
            <div class="spotify-modal-body">
                <p>Opening <strong>"${playlistName}"</strong> in Spotify...</p>
                <p class="note">If Spotify doesn't open automatically, click the button below:</p>
                <a href="${spotifyUrl}" target="_blank" rel="noopener noreferrer" class="filled-btn">
                    <i class="fa-brands fa-spotify"></i> Open in Spotify
                </a>
            </div>
        </div>
    `;
    
    // Open Spotify immediately
    window.open(spotifyUrl, '_blank', 'noopener,noreferrer');
    
    return modal;
}

/**
 * Close Spotify modal
 */
function closeSpotifyModal(modal) {
    modal.classList.add('hide');
    setTimeout(() => {
        if (modal.parentNode) {
            modal.parentNode.removeChild(modal);
        }
    }, 300);
}

/**
 * Format sync time for display
 */
function formatSyncTime(syncTime) {
    const date = new Date(syncTime);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    if (diffInHours < 48) return 'yesterday';
    return date.toLocaleDateString();
}

// Global function for modal closing
window.closeSpotifyModal = closeSpotifyModal;