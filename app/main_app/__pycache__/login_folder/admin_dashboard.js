// Example JavaScript to populate the dashboard cards with dynamic data

document.addEventListener('DOMContentLoaded', function() {
    // Simulate data fetching with static values for demonstration
    const data = {
        totalRoutes: 15,
        activeBuses: 120,
        busStatus: 'All systems operational',
        busesPerRoute: {
            'Route 1': 5,
            'Route 2': 3,
            'Route 3': 8,
        },
        recentBookings: '50 recent bookings'
    };

    // Populate the dashboard cards
    document.getElementById('totalRoutes').textContent = data.totalRoutes;
    document.getElementById('activeBuses').textContent = data.activeBuses;
    document.getElementById('busStatus').textContent = data.busStatus;
    document.getElementById('busesPerRoute').textContent = Object.entries(data.busesPerRoute)
        .map(([route, count]) => `${route}: ${count} buses`).join(', ');
    document.getElementById('recentBookings').textContent = data.recentBookings;
});
