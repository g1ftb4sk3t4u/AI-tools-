// Placeholder: Web-sanitized version. To be filled with dashboard/map only logic.
// ============ MODAL HELPERS ============
window.openModal = function(id) {
	document.getElementById(id).style.display = 'block';
}
window.closeModal = function(id) {
	document.getElementById(id).style.display = 'none';
}

// ============ LOGIN TOGGLE & SETTINGS VISIBILITY ============
let isAdmin = false;
window.toggleLogin = function() {
	isAdmin = !isAdmin;
	document.getElementById('loginToggle').textContent = isAdmin ? 'Log Out' : 'Admin Login';
	document.getElementById('settingsSidebar').style.display = isAdmin ? '' : 'none';
	// Optionally, show/hide dashboard edit buttons, etc.
}

// On load, hide settings sidebar unless admin
window.addEventListener('DOMContentLoaded', () => {
	document.getElementById('settingsSidebar').style.display = isAdmin ? '' : 'none';
});
// ============ CRITICAL ALERTS TICKER (ALWAYS ON) ============
let tickerInterval = null;
let tickerSpeed = 120;
let tickerCategory = 'critical';

async function startCriticalTicker() {
	await updateCriticalTicker();
	if (tickerInterval) clearInterval(tickerInterval);
	tickerInterval = setInterval(updateCriticalTicker, 30000);
}

async function updateCriticalTicker() {
	const ticker = document.getElementById('criticalTicker');
	try {
		// If the current dashboard has a master feed panel with a category filter, use that category
		let filters = { limit: 10 };
		const dashboard = state.currentDashboard;
		let masterFeed = null;
		if (dashboard && dashboard.panels) {
			masterFeed = dashboard.panels.find(p => p.module === 'feed' && p.filters && p.filters.category);
		}
		if (masterFeed && masterFeed.filters.category) {
			filters.category = masterFeed.filters.category;
		} else {
			filters.severity = 'critical';
		}
		const articles = await loadArticles(filters);
		if (!articles || articles.length === 0) {
			ticker.innerHTML = '<span class="ticker-content">No alerts at this time.</span>';
			return;
		}
		const items = articles.map(a => {
			const url = a.link ? escapeHtml(a.link) : '#';
			return `<span style="margin-right:32px;">🚨 <a href="${url}" target="_blank" rel="noopener" style="color:inherit;text-decoration:underline;"><strong>${escapeHtml(a.title)}</strong></a> (${escapeHtml(a.region || 'Global')})</span>`;
		}).join('');
		ticker.innerHTML = `<span class="ticker-content">${items}</span>`;
	} catch (e) {
		ticker.innerHTML = '<span class="ticker-content">Error loading alerts.</span>';
	}
}

window.addEventListener('DOMContentLoaded', () => {
	// Always show ticker at bottom
	document.getElementById('criticalTicker').style.display = '';
	tickerSpeed = parseInt(localStorage.getItem('tickerSpeed') || '120');
	document.body.style.setProperty('--ticker-speed', tickerSpeed + 's');
	startCriticalTicker();
});
// ============ THEME SWITCHER ============
function setTheme(themeClass) {
	document.body.classList.remove('theme-light', 'theme-fun', 'theme-terminal', 'theme-synthwave', 'theme-lcars', 'theme-half-life');
	if (themeClass) document.body.classList.add(themeClass);
	localStorage.setItem('theme', themeClass || '');
	// Force full dashboard re-render to apply theme everywhere
	if (typeof renderDashboard === 'function' && state.currentDashboard) {
		renderDashboard();
	}
}

window.setTheme = setTheme;

window.addEventListener('DOMContentLoaded', () => {
	// Restore theme from localStorage
	const savedTheme = localStorage.getItem('theme') || '';
	setTheme(savedTheme);
	// Theme selector event
	const themeSelector = document.getElementById('themeSelector');
	if (themeSelector) {
		themeSelector.value = savedTheme;
		themeSelector.addEventListener('change', (e) => setTheme(e.target.value));
	}
});
window.renderPanel = renderPanel;
window.renderSourcesList = renderSourcesList;
window.updateDashboardSelector = updateDashboardSelector;
// ...existing code...