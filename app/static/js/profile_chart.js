document.addEventListener('DOMContentLoaded', function() {
    
    const chartElement = document.getElementById('learningChart');
    if (!chartElement) return;
    
    const ctx = chartElement.getContext('2d');
    
    const box1 = Number(chartElement.dataset.box1) || 0;
    const box2 = Number(chartElement.dataset.box2) || 0;
    const box3 = Number(chartElement.dataset.box3) || 0;

    const dataStats = window.chartData || { box1: 0, box2: 0, box3: 0 };

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Учу', 'Средне', 'Мастер'],
            datasets: [{
                data: [box1, box2, box3],
                backgroundColor: [
                    '#dc3545',
                    '#ffc107',
                    '#198754'
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            let value = context.raw;
                            let total = context.chart._metasets[context.datasetIndex].total;
                            let percentage = Math.round((value / total) * 100) + '%';
                            return label + value + ' (' + percentage + ')';
                        }
                    }
                }
            }
        }
    });
});
