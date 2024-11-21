document.getElementById('addAdminForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Collect data from the form
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        // Send data to the backend using fetch
        const response = await fetch('http://127.0.0.1:5000/addadmin', { // Adjust the URL to your Flask endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        // Check if response is OK before parsing JSON
        if (!response.ok) {
            const errorResult = await response.json();
            alert("Error: " + (errorResult.message || "Unknown error"));
            return;
        }

        // Parse JSON response
        const result = await response.json();

        // If registration is successful, display a success message and clear the form
        alert(result.message);
        document.getElementById('addAdminForm').reset();

    } catch (error) {
        console.error('Error occurred:', error);
        alert('An error occurred: ' + error.message);
    }
});
