document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('forgot-password-form');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form submission

        const email = document.getElementById('email').value;

        try {
            const response = await fetch('/api/forgot-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });

            const result = await response.json();
            if (response.ok) {
                alert('A password reset link has been sent to your email address.');
            } else {
                alert(`Error: ${result.message}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred.');
        }
    });
});
