const dummyData = {
    labels: ['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5'],
    datasets: [{
        label: 'Dummy Data',
        data: [10, 20, 15, 25, 18],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
    }]
};

const ctx = document.getElementById('realtimeChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: dummyData,
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
            }
        }
    }
});