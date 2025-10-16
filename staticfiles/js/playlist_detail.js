// js/playlist_detail.js
document.addEventListener('DOMContentLoaded', () => {
    // This function will be defined below
    initEnhancedMusicPlayer();
    
    // Animation system is now handled by animations.js
    // No need for duplicate animation code here
});

// Global state variables
let currentPlaylist = [];
let currentTrackIndex = 0;
let isPlaying = false;
let audioPlayer = null;
let isMuted = false;
let loopMode = 'off'; // 'off', 'loop-all', 'loop-one', 'shuffle'
let originalPlaylist = [];
let shuffledPlaylist = [];

function initEnhancedMusicPlayer() {
    audioPlayer = document.getElementById('audio-player');
    if (!audioPlayer || !window.playlistData) return;

    currentPlaylist = window.playlistData.tracks;
    originalPlaylist = [...currentPlaylist]; // Store original order
    if (currentPlaylist.length === 0) return;

    // Element selectors
    const player = document.getElementById('music-player');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const muteBtn = document.getElementById('mute-btn');
    const loopShuffleBtn = document.getElementById('loop-shuffle-btn');
    const closePlayerBtn = document.getElementById('close-player-btn');
    const progressBar = document.getElementById('progress-bar');
    const playAllCoverBtn = document.getElementById('play-all-cover-btn');
    const playAllBtn = document.getElementById('play-all-btn');
    const trackItems = document.querySelectorAll('.track-item');

    // Event listeners for player controls
    playPauseBtn?.addEventListener('click', togglePlayPause);
    prevBtn?.addEventListener('click', playPrevious);
    nextBtn?.addEventListener('click', playNext);
    muteBtn?.addEventListener('click', toggleMute);
    loopShuffleBtn?.addEventListener('click', toggleLoopShuffle);
    closePlayerBtn?.addEventListener('click', closePlayer);
    progressBar?.addEventListener('click', seekTrack);
    playAllCoverBtn?.addEventListener('click', () => playTrack(0));
    playAllBtn?.addEventListener('click', () => playTrack(0));

    // Event listeners for each track in the list
    trackItems.forEach(item => {
        item.addEventListener('click', () => {
            const trackIndex = parseInt(item.dataset.trackIndex, 10);
            playTrack(trackIndex);
        });
    });
    
    // Event listeners for the audio element
    audioPlayer.addEventListener('timeupdate', updateProgress);
    audioPlayer.addEventListener('ended', playNext); // Handle end based on loop mode
    audioPlayer.addEventListener('loadedmetadata', updateDuration);

    // Set default volume
    audioPlayer.volume = 0.7; // 70% volume
}

function playTrack(index) {
    if (index < 0 || index >= currentPlaylist.length) return;

    currentTrackIndex = index;
    const track = currentPlaylist[index];

    // Handle demo tracks differently
    if (track.preview_url === 'demo') {
        // Simulate playback for demo tracks
        isPlaying = true;
        updatePlayerUI(track);
        updateTrackListUI();
        document.getElementById('music-player').classList.remove('hidden');
        simulateDemo();
        return;
    }

    if (!track.preview_url) {
        console.warn("No preview URL for this track.");
        // Show player anyway but indicate no preview
        isPlaying = false;
        updatePlayerUI(track);
        updateTrackListUI();
        document.getElementById('music-player').classList.remove('hidden');
        document.getElementById('current-track-name').textContent = track.name + ' (No Preview Available)';
        return;
    }

    audioPlayer.src = track.preview_url;
    audioPlayer.play().then(() => {
        isPlaying = true;
        updatePlayerUI(track);
        updateTrackListUI();
        document.getElementById('music-player').classList.remove('hidden');
    }).catch(error => {
        console.error("Playback error:", error);
        isPlaying = false;
        updatePlayerUI();
    });
}

function togglePlayPause() {
    const track = currentPlaylist[currentTrackIndex];
    
    if (track && track.preview_url === 'demo') {
        // Handle demo mode
        isPlaying = !isPlaying;
        if (!isPlaying) {
            stopDemo();
        } else {
            simulateDemo();
        }
        updatePlayerUI();
    } else {
        // Handle real audio
        if (isPlaying) {
            audioPlayer.pause();
        } else {
            audioPlayer.play();
        }
        isPlaying = !isPlaying;
        updatePlayerUI();
    }
}

function playNext() {
    let nextIndex;
    
    switch (loopMode) {
        case 'loop-one':
            // Stay on same track
            nextIndex = currentTrackIndex;
            break;
        case 'loop-all':
        case 'shuffle':
            // Go to next track, loop back to start if at end
            nextIndex = (currentTrackIndex + 1) % currentPlaylist.length;
            break;
        case 'off':
        default:
            // Go to next track, stop if at end
            nextIndex = currentTrackIndex + 1;
            if (nextIndex >= currentPlaylist.length) {
                // Stop playing when reaching the end
                closePlayer();
                return;
            }
            break;
    }
    
    playTrack(nextIndex);
}

function playPrevious() {
    let prevIndex = (currentTrackIndex - 1 + currentPlaylist.length) % currentPlaylist.length;
    playTrack(prevIndex);
}

function closePlayer() {
    audioPlayer.pause();
    stopDemo(); // Stop demo simulation if running
    isPlaying = false;
    document.getElementById('music-player').classList.add('hidden');
    document.querySelector('.track-item.playing')?.classList.remove('playing');
}

function seekTrack(e) {
    if (!audioPlayer.duration) return;
    const progressBar = document.getElementById('progress-bar');
    const seekTime = (e.offsetX / progressBar.offsetWidth) * audioPlayer.duration;
    audioPlayer.currentTime = seekTime;
}

function updateProgress() {
    if (!audioPlayer.duration) return;
    const progressFill = document.getElementById('progress-fill');
    const currentTimeEl = document.getElementById('current-time');
    const progressPercent = (audioPlayer.currentTime / audioPlayer.duration) * 100;
    
    progressFill.style.width = `${progressPercent}%`;
    currentTimeEl.textContent = formatTime(audioPlayer.currentTime);
}

function updateDuration() {
    const durationEl = document.getElementById('duration-time');
    durationEl.textContent = formatTime(audioPlayer.duration);
}

function updatePlayerUI(track) {
    const playPauseIcon = document.querySelector('#play-pause-btn i');
    if (track) {
        document.getElementById('current-track-name').textContent = track.name;
        document.getElementById('current-track-artist').textContent = track.artist;
        document.getElementById('current-track-cover').src = window.playlistData.coverUrl;
    }
    playPauseIcon.className = isPlaying ? 'fa-solid fa-pause' : 'fa-solid fa-play';
}

function updateTrackListUI() {
    document.querySelectorAll('.track-item').forEach(item => {
        item.classList.remove('playing');
    });
    const activeTrackEl = document.querySelector(`[data-track-index="${currentTrackIndex}"]`);
    activeTrackEl?.classList.add('playing');
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

// Demo simulation variables
let demoInterval = null;
let demoCurrentTime = 0;
let demoDuration = 30; // 30 seconds demo

function simulateDemo() {
    const track = currentPlaylist[currentTrackIndex];
    demoDuration = track.duration_ms ? track.duration_ms / 1000 : 30;
    demoCurrentTime = 0;
    
    // Update duration immediately
    document.getElementById('duration-time').textContent = formatTime(demoDuration);
    
    // Start demo progress simulation
    if (demoInterval) clearInterval(demoInterval);
    demoInterval = setInterval(() => {
        if (!isPlaying) return;
        
        demoCurrentTime += 1;
        const progressPercent = (demoCurrentTime / demoDuration) * 100;
        
        document.getElementById('progress-fill').style.width = `${progressPercent}%`;
        document.getElementById('current-time').textContent = formatTime(demoCurrentTime);
        
        if (demoCurrentTime >= demoDuration) {
            clearInterval(demoInterval);
            playNext();
        }
    }, 1000);
}

function stopDemo() {
    if (demoInterval) {
        clearInterval(demoInterval);
        demoInterval = null;
    }
    demoCurrentTime = 0;
}

// New control functions
function toggleMute() {
    isMuted = !isMuted;
    audioPlayer.muted = isMuted;
    
    const muteIcon = document.querySelector('#mute-btn i');
    muteIcon.className = isMuted ? 'fa-solid fa-volume-mute' : 'fa-solid fa-volume-high';
}

function toggleLoopShuffle() {
    const btn = document.getElementById('loop-shuffle-btn');
    const icon = btn.querySelector('i');
    
    // Cycle through modes: off -> loop-all -> loop-one -> shuffle -> off
    switch (loopMode) {
        case 'off':
            loopMode = 'loop-all';
            btn.setAttribute('data-mode', 'loop-all');
            btn.title = 'Loop All';
            icon.className = 'fa-solid fa-repeat';
            break;
        case 'loop-all':
            loopMode = 'loop-one';
            btn.setAttribute('data-mode', 'loop-one');
            btn.title = 'Loop One';
            icon.className = 'fa-solid fa-repeat';
            // Add a "1" indicator - you could use a pseudo-element or different icon
            break;
        case 'loop-one':
            loopMode = 'shuffle';
            btn.setAttribute('data-mode', 'shuffle');
            btn.title = 'Shuffle';
            icon.className = 'fa-solid fa-shuffle';
            // Create shuffled playlist
            shufflePlaylist();
            break;
        case 'shuffle':
            loopMode = 'off';
            btn.setAttribute('data-mode', 'off');
            btn.title = 'Loop Mode';
            icon.className = 'fa-solid fa-arrows-rotate';
            // Restore original playlist
            currentPlaylist = [...originalPlaylist];
            break;
    }
}

function shufflePlaylist() {
    // Store original if not already stored
    if (originalPlaylist.length === 0) {
        originalPlaylist = [...currentPlaylist];
    }
    
    // Create shuffled copy
    shuffledPlaylist = [...currentPlaylist];
    
    // Fisher-Yates shuffle algorithm
    for (let i = shuffledPlaylist.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledPlaylist[i], shuffledPlaylist[j]] = [shuffledPlaylist[j], shuffledPlaylist[i]];
    }
    
    // Update current playlist to shuffled version
    currentPlaylist = shuffledPlaylist;
    
    // Find current track in new shuffled playlist
    const currentTrack = originalPlaylist[currentTrackIndex];
    currentTrackIndex = currentPlaylist.findIndex(track => track.name === currentTrack.name);
}