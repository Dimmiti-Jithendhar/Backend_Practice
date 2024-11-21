document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('booking-form');
    const resultsContainer = document.getElementById('search-results');

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        
        // For demonstration purposes, we will display the form values as search results.
        const departure = document.getElementById('departure').value;
        const destination = document.getElementById('destination').value;
        const departureDate = document.getElementById('departure-date').value;
        const returnDate = document.getElementById('return-date').value;

        // Clear previous results
        resultsContainer.innerHTML = '';

        // Display search results (In a real scenario, you would fetch data from a server here)
        const resultsHTML = `
            <h2>Available Buses</h2>
            <p><strong>Departure City:</strong> ${departure}</p>
            <p><strong>Destination City:</strong> ${destination}</p>
            <p><strong>Departure Date:</strong> ${departureDate}</p>
            <p><strong>Return Date:</strong> ${returnDate ? returnDate : 'N/A'}</p>
            <p>Here will be a list of available buses based on your search criteria.</p>
        `;

        resultsContainer.innerHTML = resultsHTML;
    });
});
