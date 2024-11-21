document.getElementById('signupForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Collect data from the form
    const firstName = document.getElementById('firstname').value;
    const lastName = document.getElementById('lastname').value;
    const mobile = document.getElementById('mobile').value;
    const email = document.getElementById('email').value;
    const gender = document.getElementById('gender').value;
    const password = document.getElementById('password').value;

    try {
        // Send data to the backend using fetch
        const response = await fetch('http://127.0.0.1:5000/usersignup', { // Full URL to your Flask endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                mobile: mobile,
                email: email,
                gender: gender,
                password: password
            })
        });

        // Check if response is OK before parsing JSON
        if (!response.ok) {
            const errorResult = await response.json();
            alert("Registration failed: " + (errorResult.message || "Unknown error"));
            return;
        }

        // Parse JSON response
        const result = await response.json();

        // If registration is successful, display a success message and redirect
        alert(result.message);
        window.location.href = 'login.html'; // Redirect to home.html

    } catch (error) {
        console.error('Error occurred:', error);
        alert('An error occurred during registration: ' + error.message);
    }
});
