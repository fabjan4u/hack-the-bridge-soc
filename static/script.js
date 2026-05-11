// Update the digital clock
function updateClock() {
    const now = new Date();
    document.getElementById('clock').innerText = now.toLocaleTimeString();
}
setInterval(updateClock, 1000);
updateClock();

// Fetch PLC Status
async function fetchPLCStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        const statusText = document.getElementById('plc-status');
        const orb = document.getElementById('plc-orb');
        const speed = document.getElementById('plc-speed');
        const temp = document.getElementById('plc-temp');
        const lastUpdate = document.getElementById('plc-last-update');

        // Update Text
        statusText.innerText = data.status;
        speed.innerText = data.speed + " RPM";
        temp.innerText = data.temperature + " °C";
        lastUpdate.innerText = data.last_update;

        // Update Colors
        statusText.className = '';
        orb.className = 'glow-orb';
        
        if (data.status === 'RUN') {
            statusText.classList.add('state-run');
            orb.classList.add('state-run');
        } else if (data.status === 'STOP') {
            statusText.classList.add('state-stop');
            orb.classList.add('state-stop');
        } else {
            statusText.classList.add('state-error');
            orb.classList.add('state-error');
        }

    } catch (error) {
        console.error("Error fetching PLC status:", error);
    }
}

// Keep track of alert IDs to avoid re-animating existing ones
let knownAlertIds = new Set();

// Fetch Security Alerts
async function fetchAlerts() {
    try {
        const response = await fetch('/api/alerts');
        const alerts = await response.json();
        
        const feed = document.getElementById('alert-feed');
        
        if (alerts.length === 0) return;

        // Clear empty state if exists
        const emptyState = feed.querySelector('.empty-state');
        if (emptyState) emptyState.remove();

        // Check if there are new alerts
        let hasNew = false;

        // To keep the feed ordered (newest top), we will clear and rebuild
        // A real app might just prepend, but rebuilding is fine for 50 items
        // We just use CSS animations for new ones.
        
        feed.innerHTML = ''; // Clear feed

        alerts.forEach(alert => {
            const isNew = !knownAlertIds.has(alert.id);
            if (isNew) knownAlertIds.add(alert.id);

            const div = document.createElement('div');
            div.className = `alert-item severity-${alert.severity.toLowerCase()}`;
            // If it's not new, disable animation so it doesn't flash every poll
            if (!isNew) {
                div.style.animation = 'none';
                div.style.opacity = '1';
                div.style.transform = 'translateX(0)';
            }

            div.innerHTML = `
                <div class="alert-meta">
                    <span class="alert-source">[${alert.source}]</span>
                    <span class="alert-time">${alert.timestamp}</span>
                </div>
                <div class="alert-message">${alert.message}</div>
            `;
            
            feed.appendChild(div);
        });

    } catch (error) {
        console.error("Error fetching alerts:", error);
    }
}

// Polling intervals
setInterval(fetchPLCStatus, 1000);
setInterval(fetchAlerts, 1000);

// Initial fetches
fetchPLCStatus();
fetchAlerts();
