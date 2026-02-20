/**
 * Intel Terminal Frontend - Main Application
 * Features: Multi-theme, Category filtering, Feed management
 */

// Dynamic API URL detection:
// - In Docker/production: nginx proxies /api and /ws to backend
// - In development: direct connection to backend on port 8001
const isProduction = window.location.port === '' || window.location.port === '80' || window.location.port === '443';
const API_BASE = isProduction ? '' : 'http://127.0.0.1:8001';
const WS_PROTOCOL = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const WS_URL = isProduction ? WS_PROTOCOL + '//' + window.location.host + '/ws' : 'ws://127.0.0.1:8001/ws';

// Application State
let articles = [];
let sources = [];
let categories = [];
let activeCategories = new Set();
let ws = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 10;
let autoRefreshInterval = null;
let autoRefreshSeconds = 0; // 0 = disabled
let currentLayout = 'modern'; // 'modern' or 'irc'

// Default categories with colors
const DEFAULT_CATEGORIES = [
    { name: 'Cybersecurity', color: '#ff3333' },
    { name: 'Geopolitical', color: '#00ffff' },
    { name: 'Technology', color: '#ffff00' },
    { name: 'OSINT', color: '#00ff00' },
    { name: 'AI/ML', color: '#dd00ff' },
    { name: 'Privacy', color: '#ff9900' },
    { name: 'Science', color: '#00aaff' },
    { name: 'Investigation', color: '#ff1493' }
];

// ========================================
// Initialization
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    loadLayout();
    loadAutoRefreshSetting();
    loadCategoriesFromBackend();
    connectWebSocket();
    loadSources();
    loadArticles();
});

// ========================================
// Theme Management
// ========================================
let matrixRainInterval = null;

function loadTheme() {
    const saved = localStorage.getItem('intel-theme') || 'theme-terminal';
    // Preserve layout class when setting theme
    const layoutClass = currentLayout === 'irc' ? ' layout-irc' : '';
    document.body.className = saved + layoutClass;
    const select = document.getElementById('themeSelect');
    if (select) select.value = saved;
    handleThemeEffects(saved);
}

function changeTheme(theme) {
    // Preserve layout class when changing theme
    const layoutClass = currentLayout === 'irc' ? ' layout-irc' : '';
    document.body.className = theme + layoutClass;
    localStorage.setItem('intel-theme', theme);
    handleThemeEffects(theme);
}

function handleThemeEffects(theme) {
    // Clean up previous effects
    stopMatrixRain();
    
    // Start theme-specific effects
    if (theme === 'theme-matrix') {
        startMatrixRain();
    }
}

// ========================================
// Layout Management (Modern Cards / IRC Classic)
// ========================================
function loadLayout() {
    const saved = localStorage.getItem('intel-layout') || 'modern';
    currentLayout = saved;
    applyLayout(saved);
    const select = document.getElementById('layoutSelect');
    if (select) select.value = saved;
}

function changeLayout(layout) {
    currentLayout = layout;
    localStorage.setItem('intel-layout', layout);
    applyLayout(layout);
    renderArticles(); // Re-render with new layout
}

function applyLayout(layout) {
    const body = document.body;
    if (layout === 'irc') {
        body.classList.add('layout-irc');
    } else {
        body.classList.remove('layout-irc');
    }
}

// ========================================
// Matrix Digital Rain Effect
// ========================================
function startMatrixRain() {
    // Create canvas if it doesn't exist
    let canvas = document.getElementById('matrix-rain');
    if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'matrix-rain';
        document.body.insertBefore(canvas, document.body.firstChild);
    }
    
    const ctx = canvas.getContext('2d');
    
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);
    
    // Matrix characters (katakana + numbers + symbols)
    const chars = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%^&*()';
    const charArray = chars.split('');
    
    const fontSize = 14;
    const columns = Math.floor(canvas.width / fontSize);
    const drops = new Array(columns).fill(1);
    
    function draw() {
        // Semi-transparent black to create trail effect
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#00ff41';
        ctx.font = fontSize + 'px monospace';
        
        for (let i = 0; i < drops.length; i++) {
            const char = charArray[Math.floor(Math.random() * charArray.length)];
            const x = i * fontSize;
            const y = drops[i] * fontSize;
            
            // Brighter character at the head
            if (Math.random() > 0.98) {
                ctx.fillStyle = '#ffffff';
            } else {
                ctx.fillStyle = '#00ff41';
            }
            
            ctx.fillText(char, x, y);
            
            // Reset drop randomly or when it goes off screen
            if (y > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    
    matrixRainInterval = setInterval(draw, 50);
}

function stopMatrixRain() {
    if (matrixRainInterval) {
        clearInterval(matrixRainInterval);
        matrixRainInterval = null;
    }
    const canvas = document.getElementById('matrix-rain');
    if (canvas) {
        canvas.remove();
    }
}

// ========================================
// Category Management
// ========================================
async function loadCategoriesFromBackend() {
    try {
        const response = await fetch(API_BASE + '/api/categories');
        if (response.ok) {
            const backendCats = await response.json();
            if (backendCats.length > 0) {
                categories = backendCats.map(c => ({ name: c.name, color: c.color, id: c.id }));
            } else {
                // Use defaults if backend has none
                categories = DEFAULT_CATEGORIES.slice();
            }
        } else {
            categories = DEFAULT_CATEGORIES.slice();
        }
    } catch (error) {
        console.error('Failed to load categories:', error);
        categories = DEFAULT_CATEGORIES.slice();
    }
    
    // Load active categories from localStorage
    const savedActive = localStorage.getItem('intel-active-categories');
    if (savedActive) {
        activeCategories = new Set(JSON.parse(savedActive));
    } else {
        categories.forEach(c => activeCategories.add(c.name));
    }
    
    renderCategories();
    populateCategoryDropdown();
}

function initializeCategories() {
    // Load from localStorage or use defaults
    const saved = localStorage.getItem('intel-categories');
    if (saved) {
        categories = JSON.parse(saved);
    } else {
        categories = DEFAULT_CATEGORIES.slice();
        saveCategories();
    }
    
    // Initially all categories are active
    const savedActive = localStorage.getItem('intel-active-categories');
    if (savedActive) {
        activeCategories = new Set(JSON.parse(savedActive));
    } else {
        categories.forEach(c => activeCategories.add(c.name));
    }
    
    renderCategories();
    populateCategoryDropdown();
}

function saveCategories() {
    localStorage.setItem('intel-categories', JSON.stringify(categories));
}

function saveActiveCategories() {
    localStorage.setItem('intel-active-categories', JSON.stringify([...activeCategories]));
}

function renderCategories() {
    const container = document.getElementById('categoryList');
    if (!container) return;
    
    let html = '';
    categories.forEach(cat => {
        const isActive = activeCategories.has(cat.name);
        html += '<div class="category-item ' + (isActive ? 'active' : 'inactive') + '" ';
        html += 'style="border-left-color: ' + cat.color + ';" ';
        html += 'onclick="toggleCategory(\'' + escapeAttr(cat.name) + '\')">';
        html += '<input type="checkbox" ' + (isActive ? 'checked' : '') + ' ';
        html += 'onclick="event.stopPropagation(); toggleCategory(\'' + escapeAttr(cat.name) + '\')">';
        html += '<span style="color: ' + cat.color + '">' + escapeHtml(cat.name) + '</span>';
        html += '</div>';
    });
    container.innerHTML = html;
}

function toggleCategory(name) {
    if (activeCategories.has(name)) {
        activeCategories.delete(name);
    } else {
        activeCategories.add(name);
    }
    saveActiveCategories();
    renderCategories();
    renderArticles();
}

function populateCategoryDropdown() {
    const select = document.getElementById('feedCategory');
    if (!select) return;
    
    let html = '';
    categories.forEach(cat => {
        html += '<option value="' + escapeAttr(cat.name) + '">' + escapeHtml(cat.name) + '</option>';
    });
    select.innerHTML = html;
}

function showAddCategoryModal() {
    document.getElementById('categoryName').value = '';
    document.getElementById('categoryColor').value = '#00ffff';
    document.getElementById('addCategoryModal').style.display = 'flex';
}

async function submitAddCategory() {
    const name = document.getElementById('categoryName').value.trim();
    const color = document.getElementById('categoryColor').value;
    
    if (!name) {
        alert('Please enter a category name');
        return;
    }
    
    // Check for duplicate locally
    if (categories.some(c => c.name.toLowerCase() === name.toLowerCase())) {
        alert('Category already exists');
        return;
    }
    
    try {
        // Add to backend
        const response = await fetch(API_BASE + '/api/categories', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, color })
        });
        
        if (response.ok) {
            const result = await response.json();
            categories.push({ name, color, id: result.id });
            activeCategories.add(name);
            saveActiveCategories();
            renderCategories();
            populateCategoryDropdown();
            closeModal('addCategoryModal');
        } else {
            alert('Failed to add category');
        }
    } catch (error) {
        console.error('Error adding category:', error);
        // Add locally anyway
        categories.push({ name, color });
        activeCategories.add(name);
        saveCategories();
        saveActiveCategories();
        renderCategories();
        populateCategoryDropdown();
        closeModal('addCategoryModal');
    }
}

// ========================================
// WebSocket Connection
// ========================================
function connectWebSocket() {
    try {
        ws = new WebSocket(WS_URL);
        
        ws.onopen = () => {
            console.log('WebSocket connected');
            updateStatus('connected', '✓ Connected');
            reconnectAttempts = 0;
        };
        
        ws.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);
                if (msg.type === 'article') {
                    addArticle(msg.data);
                } else if (msg.type === 'status') {
                    console.log('Status:', msg.message);
                }
            } catch (e) {
                console.error('Parse error:', e);
            }
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            updateStatus('error', '✗ Error');
        };
        
        ws.onclose = () => {
            console.log('WebSocket closed');
            updateStatus('disconnected', '✗ Disconnected');
            
            if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                reconnectAttempts++;
                console.log('Reconnecting... (' + reconnectAttempts + '/' + MAX_RECONNECT_ATTEMPTS + ')');
                setTimeout(connectWebSocket, 3000);
            }
        };
    } catch (error) {
        console.error('WebSocket connection error:', error);
        updateStatus('error', '✗ Connection Failed');
    }
}

function updateStatus(className, text) {
    const el = document.getElementById('status');
    if (el) {
        el.className = 'status-indicator ' + className;
        el.textContent = text;
    }
}

// ========================================
// Source/Feed Management
// ========================================
async function loadSources() {
    try {
        const response = await fetch(API_BASE + '/api/sources');
        if (response.ok) {
            sources = await response.json();
            renderSources();
        }
    } catch (error) {
        console.error('Failed to load sources:', error);
    }
}

function renderSources() {
    const container = document.getElementById('sourceList');
    if (!container) return;
    
    if (sources.length === 0) {
        container.innerHTML = '<div style="color: var(--text-dim); padding: 10px; font-size: 13px;">No feeds configured</div>';
        return;
    }
    
    let html = '';
    sources.forEach(source => {
        const color = source.color || '#55ff55';
        html += '<div class="source-item">';
        html += '<span class="source-name">';
        html += '<span class="color-dot" style="background: ' + color + '"></span>';
        html += escapeHtml(source.name);
        html += '</span>';
        html += '<button class="delete-btn" onclick="deleteSource(' + source.id + ')" title="Remove">✕</button>';
        html += '</div>';
    });
    container.innerHTML = html;
}

function showAddFeedModal() {
    document.getElementById('feedName').value = '';
    document.getElementById('feedUrl').value = '';
    document.getElementById('feedColor').value = '#00ff00';
    populateCategoryDropdown();
    document.getElementById('addFeedModal').style.display = 'flex';
}

async function submitAddFeed() {
    const name = document.getElementById('feedName').value.trim();
    const url = document.getElementById('feedUrl').value.trim();
    const category = document.getElementById('feedCategory').value;
    const color = document.getElementById('feedColor').value;
    
    if (!name || !url) {
        alert('Please enter feed name and URL');
        return;
    }
    
    try {
        const response = await fetch(API_BASE + '/api/sources', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                url: url,
                category: category,
                color: color
            })
        });
        
        if (response.ok) {
            closeModal('addFeedModal');
            loadSources();
            // Trigger a fetch for the new feed
            refreshFeeds();
        } else {
            const err = await response.json();
            alert('Failed to add feed: ' + (err.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error adding feed:', error);
        alert('Error adding feed');
    }
}

async function deleteSource(sourceId) {
    if (!confirm('Remove this feed?')) return;
    
    try {
        const response = await fetch(API_BASE + '/api/sources/' + sourceId, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadSources();
        } else {
            alert('Failed to remove feed');
        }
    } catch (error) {
        console.error('Error removing feed:', error);
    }
}

async function refreshFeeds() {
    updateStatus('', '⟳ Fetching...');
    try {
        const response = await fetch(API_BASE + '/api/fetch', { method: 'POST' });
        if (response.ok) {
            console.log('RSS fetch triggered');
            // Wait a bit for backend to process, then reload
            setTimeout(async () => {
                await loadArticles();
                updateStatus('connected', '✓ Connected');
            }, 3000);
        } else {
            updateStatus('error', '✗ Fetch Failed');
        }
    } catch (error) {
        console.error('Failed to trigger RSS fetch:', error);
        updateStatus('error', '✗ Fetch Failed');
    }
}

// ========================================
// Auto-Refresh Management
// ========================================
function loadAutoRefreshSetting() {
    const saved = localStorage.getItem('intel-autorefresh');
    if (saved) {
        autoRefreshSeconds = parseInt(saved, 10);
    }
    const select = document.getElementById('refreshInterval');
    if (select) {
        select.value = autoRefreshSeconds.toString();
    }
    startAutoRefresh();
}

function changeRefreshInterval(seconds) {
    autoRefreshSeconds = parseInt(seconds, 10);
    localStorage.setItem('intel-autorefresh', autoRefreshSeconds.toString());
    startAutoRefresh();
}

function startAutoRefresh() {
    // Clear existing interval
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
    
    // Set new interval if enabled
    if (autoRefreshSeconds > 0) {
        console.log('Auto-refresh enabled: every ' + autoRefreshSeconds + ' seconds');
        autoRefreshInterval = setInterval(() => {
            console.log('Auto-refreshing articles...');
            loadArticles();
        }, autoRefreshSeconds * 1000);
    } else {
        console.log('Auto-refresh disabled');
    }
}

// ========================================
// Article Management
// ========================================
async function loadArticles() {
    try {
        const response = await fetch(API_BASE + '/api/articles?limit=200');
        if (response.ok) {
            articles = await response.json();
            updateArticleCount();
            renderArticles();
        }
    } catch (error) {
        console.error('Failed to load articles:', error);
    }
}

function addArticle(article) {
    // Add to beginning
    articles.unshift(article);
    if (articles.length > 1000) articles.pop();
    updateArticleCount();
    renderArticles();
}

function updateArticleCount() {
    const el = document.getElementById('articleCount');
    if (el) el.textContent = 'Articles: ' + articles.length;
}

function renderArticles() {
    const feed = document.getElementById('feed');
    if (!feed) return;
    
    // Filter by active categories
    const filtered = articles.filter(a => {
        // Category comes as a string name from the backend now
        const cat = a.category || 'Unknown';
        return activeCategories.has(cat);
    });
    
    if (filtered.length === 0) {
        feed.innerHTML = '<div class="no-articles">No articles match your filters. Try enabling more categories or wait for new articles...</div>';
        return;
    }
    
    let html = '';
    
    // Render based on current layout
    if (currentLayout === 'irc') {
        // IRC Classic Layout - chat room style
        filtered.forEach(article => {
            const sourceColor = article.source_color || article.color || '#55ff55';
            const categoryName = article.category || 'Unknown';
            const categoryColor = getCategoryColor(categoryName);
            const articleUrl = article.url || article.link || '#';
            const timestamp = article.published_at ? formatTimeShort(article.published_at) : '';
            
            html += '<div class="article-card">';
            html += '<span class="article-timestamp">' + timestamp + '</span>';
            html += '<span class="article-source" style="color: ' + sourceColor + '">' + escapeHtml(article.source || 'Unknown') + '</span>';
            html += '<span class="article-title"><a href="' + escapeAttr(articleUrl) + '" target="_blank">' + escapeHtml(article.title) + '</a></span>';
            html += '<span class="article-category" style="background: ' + categoryColor + '22; color: ' + categoryColor + '; border: 1px solid ' + categoryColor + '">' + escapeHtml(categoryName) + '</span>';
            html += '</div>';
        });
    } else {
        // Modern Cards Layout (default)
        filtered.forEach(article => {
            const severity = article.severity || 'low';
            const sourceColor = article.source_color || article.color || '#55ff55';
            const categoryName = article.category || 'Unknown';
            const categoryColor = getCategoryColor(categoryName);
            const articleUrl = article.url || article.link || '#';
            const summary = article.summary || 'No summary available';
            
            html += '<div class="article" data-severity="' + severity + '">';
            html += '<div class="article-header">';
            html += '<span class="source" style="color: ' + sourceColor + '">[' + escapeHtml(article.source || 'Unknown') + ']</span>';
            html += '<span class="category" style="border-left: 3px solid ' + categoryColor + '; padding-left: 8px;">' + escapeHtml(categoryName) + '</span>';
            html += '<span class="severity severity-' + severity + '">' + severity.toUpperCase() + '</span>';
            html += '</div>';
            html += '<div class="article-title">' + escapeHtml(article.title) + '</div>';
            html += '<div class="article-summary">' + escapeHtml(summary) + '</div>';
            html += '<div class="article-footer">';
            html += '<a href="' + escapeAttr(articleUrl) + '" target="_blank" class="article-link">Read More →</a>';
            if (article.published_at) {
                html += '<span class="timestamp">' + formatTime(article.published_at) + '</span>';
            }
            html += '</div>';
            html += '</div>';
        });
    }
    
    feed.innerHTML = html;
}

// Format time for IRC layout (short format)
function formatTimeShort(dateStr) {
    try {
        const date = new Date(dateStr);
        const hours = date.getHours().toString().padStart(2, '0');
        const mins = date.getMinutes().toString().padStart(2, '0');
        return hours + ':' + mins;
    } catch {
        return '';
    }
}

function getCategoryColor(name) {
    const cat = categories.find(c => c.name === name);
    return cat ? cat.color : '#888888';
}

// ========================================
// Modal Management
// ========================================
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Close modal on outside click
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal').forEach(m => m.style.display = 'none');
    }
});

// ========================================
// Utility Functions
// ========================================
function formatTime(isoString) {
    try {
        const date = new Date(isoString);
        return date.toLocaleString();
    } catch (e) {
        return '';
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function escapeAttr(text) {
    if (!text) return '';
    return text.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function clearFeed() {
    if (confirm('Clear all displayed articles?')) {
        articles = [];
        renderArticles();
        updateArticleCount();
    }
}

function exportArticles() {
    const data = JSON.stringify(articles, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'intel-articles-' + new Date().toISOString().slice(0, 10) + '.json';
    a.click();
    URL.revokeObjectURL(url);
}
