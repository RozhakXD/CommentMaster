function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('id-ID', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDate(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleDateString('id-ID', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
    });
}

function updateLastUpdated() {
    document.getElementById('last-updated').textContent =
        `Terakhir diperbarui: ${formatTime(new Date())}`;
}

async function loadDashboardData() {
    try {
        updateLastUpdated();

        const [historyRes, predictRes, devicesRes, realtimeRes] = await Promise.all([
            fetch('/api/usage/history'),
            fetch('/api/predict'),
            fetch('/api/device_breakdown'),
            fetch('/api/usage/realtime')
        ]);

        const historyData = await historyRes.json();
        const predictData = await predictRes.json();
        const devicesData = await devicesRes.json();
        const realtimeData = await realtimeRes.json();

        document.getElementById('loading-chart').style.display = 'none';
        document.getElementById('loading-devices').style.display = 'none';
        document.getElementById('loading-realtime').style.display = 'none';

        renderChart(historyData, predictData);
        renderDeviceStatus(devicesData);
        renderRealtimeStatus(realtimeData);

    } catch (error) {
        console.error('Failed to load dashboard data:', error);
        document.getElementById('loading-chart').innerHTML =
            '<i class="fas fa-exclamation-triangle"></i> Gagal memuat data grafik';
        document.getElementById('loading-devices').innerHTML =
            '<i class="fas fa-exclamation-triangle"></i> Gagal memuat status perangkat';
        document.getElementById('loading-realtime').innerHTML =
            '<i class="fas fa-exclamation-triangle"></i> Gagal memuat data real-time';
    }
}

function renderChart(history, prediction) {
    const ctx = document.getElementById('energyChart').getContext('2d');

    const historyLabels = Object.keys(history).map(label =>
        new Date(label).toLocaleTimeString('id-ID', {
            hour: '2-digit',
            minute: '2-digit'
        }));
    const historyValues = Object.values(history);

    const predictionLabels = Object.keys(prediction).map(label =>
        new Date(label).toLocaleTimeString('id-ID', {
            hour: '2-digit',
            minute: '2-digit'
        }));
    const predictionValues = Object.values(prediction);

    const historyDates = Object.keys(history);
    const predictionDates = Object.keys(prediction);

    if (historyDates.length > 0 && predictionDates.length > 0) {
        const startDate = formatDate(historyDates[0]);
        const endDate = formatDate(predictionDates[predictionDates.length - 1]);

        document.getElementById('chart-date-range').textContent =
            `${startDate} - ${endDate} | ${historyDates.length} jam data historis + ${predictionDates.length} jam prediksi`;
    }

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: [...historyLabels, ...predictionLabels],
            datasets: [{
                    label: 'Konsumsi Aktual',
                    data: [...historyValues, ...Array(predictionLabels.length).fill(null)],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                },
                {
                    label: 'Prediksi Energi',
                    data: [...Array(historyLabels.length).fill(null), ...predictionValues],
                    borderColor: 'rgba(0, 168, 132, 1)',
                    backgroundColor: 'rgba(0, 168, 132, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    tension: 0.3,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += context.parsed.y.toFixed(2) + ' kW';
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Waktu'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Konsumsi (kW)'
                    },
                    beginAtZero: true
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

function renderDeviceStatus(devices) {
    const container = document.getElementById('device-status');
    container.innerHTML = '';

    const deviceIcons = {
        'Dapur (Sub_metering_1)': 'utensils',
        'Laundry (Sub_metering_2)': 'tshirt',
        'AC & Pemanas (Sub_metering_3)': 'snowflake'
    };

    for (const [device, status] of Object.entries(devices)) {
        const statusClass = status === 'Aktif' ? 'status-active' : 'status-inactive';
        const statusIcon = status === 'Aktif' ? 'check-circle' : 'times-circle';

        const item = document.createElement('div');
        item.className = 'status-item';
        item.innerHTML = `
                    <i class="fas fa-${deviceIcons[device]} status-icon"></i>
                    <div class="status-info">
                        <div class="status-name">${device.replace(' (Sub_metering_', ' - ').replace(')', '')}</div>
                        <div class="status-value ${statusClass}">
                            <i class="fas fa-${statusIcon}"></i> ${status}
                        </div>
                    </div>
                `;
        container.appendChild(item);
    }
}

function renderRealtimeStatus(realtime) {
    const container = document.getElementById('realtime-status');
    container.innerHTML = `
                <div class="realtime-value">${realtime.konsumsi_kw.toFixed(2)} kW</div>
                <div class="realtime-time">${formatTime(realtime.timestamp)}</div>
            `;
}

document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
    setInterval(loadDashboardData, 300000);
});