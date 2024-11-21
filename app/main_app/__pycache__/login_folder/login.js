document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent the form from submitting the default way
 
    const formData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };
 
    try {
        const response = await fetch('http://127.0.0.1:5000/userlogin', { // Adjust the URL as per your backend configuration
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
 
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.message || 'Something went wrong');
        }
 
        const data = await response.json(); // Parse the JSON response
 
        // Handle admin login success
        if (data.message.trim() === 'Admin login successful') {
            alert('Admin login successful!');
            console.log('Admin Details:', data.admin_details);
 
            // Store the admin email in local storage or session storage
            localStorage.setItem('adminEmail', formData.email);
 
            // Redirect to the admin dashboard
            window.location.href = 'admin_dashboard.html';
 
        } else if (data.message.trim() === 'User login successful') {
            alert('User login successful!');
            console.log('User Details:', data.user_details);
 
            // Redirect to the user dashboard
            window.location.href = 'home.html';
 
        } else {
            alert('Login failed: ' + data.message);
        }
 
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred: ' + error.message);
    }
});
 
 