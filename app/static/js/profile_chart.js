document.addEventListener('DOMContentLoaded', function() {
    const chartCanvas = document.getElementById('learningChart');
    const deckSelector = document.getElementById('deckSelector');
    
    if (!chartCanvas || !deckSelector) return;

    const fullStats = JSON.parse(chartCanvas.dataset.stats);
    
    const elBox1 = document.getElementById('stat-box1');
    const elBox2 = document.getElementById('stat-box2');
    const elBox3 = document.getElementById('stat-box3');
    const elTotal = document.getElementById('stat-total-cards');
    
    const ctx = chartCanvas.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Учу', 'Средне', 'Мастер'],
            datasets: [{
                data: [fullStats.total.box1, fullStats.total.box2, fullStats.total.box3],
                backgroundColor: ['#dc3545', '#ffc107', '#198754'],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });

    deckSelector.addEventListener('change', function() {
        const selectedId = this.value;
        let currentData;

        if (selectedId === 'all') {
            currentData = fullStats.total;
        } else {
            currentData = fullStats.decks[selectedId];
        }

        chart.data.datasets[0].data = [
            currentData.box1, 
            currentData.box2, 
            currentData.box3
        ];
        chart.update();

        elBox1.textContent = currentData.box1;
        elBox2.textContent = currentData.box2;
        elBox3.textContent = currentData.box3;
        elTotal.textContent = currentData.total;
    });
});
