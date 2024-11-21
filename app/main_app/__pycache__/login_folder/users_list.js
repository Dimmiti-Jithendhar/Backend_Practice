document.addEventListener('DOMContentLoaded', () => {
    // Fetch and display user data
    async function fetchUsers() {
        try {
            const response = await fetch('http://127.0.0.1:5000/userlist'); // Adjust URL as needed
            if (!response.ok) {
                throw new Error('Failed to fetch user data');
            }

            const data = await response.json();
            
            if (data.message === 'Users fetched successfully') {
                const userTableBody = document.querySelector('#userTable tbody');
                userTableBody.innerHTML = '';

                data.users.forEach(user => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${user.first_name}</td>
                        <td>${user.last_name}</td>
                        <td>${user.mobile}</td>
                        <td>${user.email}</td>
                        <td>${user.gender}</td>
                    `;
                    userTableBody.appendChild(row);
                });
            }
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    }

    fetchUsers();

    // Get modal elements
    const addUserModal = document.getElementById('addUserModal');
    const updateUserModal = document.getElementById('updateUserModal');
    const deleteUserModal = document.getElementById('deleteUserModal');

    // Get button elements
    const addUserBtn = document.getElementById('addUserBtn');
    const updateUserBtn = document.getElementById('updateUserBtn');
    const deleteUserBtn = document.getElementById('deleteUserBtn');

    // Get close elements
    const closeAddUserModal = document.getElementById('closeAddUserModal');
    const closeUpdateUserModal = document.getElementById('closeUpdateUserModal');
    const closeDeleteUserModal = document.getElementById('closeDeleteUserModal');

    // Function to open a modal
    function openModal(modal) {
        modal.style.display = 'block';
    }

    // Function to close a modal
    function closeModal(modal) {
        modal.style.display = 'none';
    }

    // Event listeners for buttons
    addUserBtn.addEventListener('click', () => openModal(addUserModal));
    updateUserBtn.addEventListener('click', () => openModal(updateUserModal));
    deleteUserBtn.addEventListener('click', () => openModal(deleteUserModal));

    // Event listeners for close buttons
    closeAddUserModal.addEventListener('click', () => closeModal(addUserModal));
    closeUpdateUserModal.addEventListener('click', () => closeModal(updateUserModal));
    closeDeleteUserModal.addEventListener('click', () => closeModal(deleteUserModal));

    // Event listeners for clicking outside the modal content
    window.addEventListener('click', (event) => {
        if (event.target === addUserModal) {
            closeModal(addUserModal);
        }
        if (event.target === updateUserModal) {
            closeModal(updateUserModal);
        }
        if (event.target === deleteUserModal) {
            closeModal(deleteUserModal);
        }
    });

    // Add User Form submission
    document.getElementById('addUserForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = {
            email: document.getElementById('addEmail').value,
            first_name :document.getElementById('addFirstName').value,
            last_name :document.getElementById('addLastName').value,
            password :document.getElementById('addPassword').value,
            gender : document.getElementById('addGender').value,
            mobile: document.getElementById('addMobile').value
        };
        console.log(data)
        try {
            const response = await fetch('http://127.0.0.1:5000/usersignup', { // Adjust URL as needed
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            alert(result.message);
            if (result.message === 'User added successfully') {
                fetchUsers(); // Refresh user list
                closeModal(addUserModal);
            }
        } catch (error) {
            console.error('Error adding user:', error);
        }
    });
    // Update User Form submission
    document.getElementById('updateUserForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
    
        const data = {
            new_email: document.getElementById('updateEmail').value,  // Only include new_email if provided
            email: document.getElementById('Email').value,
            first_name :document.getElementById('updateFirstName').value,
            last_name :document.getElementById('updateLastName').value,
            password :document.getElementById('updatePassword').value,
            gender : document.getElementById('updateGender').value,
            mobile: document.getElementById('updateMobile').value
        };
    
        try {
            const response = await fetch('http://127.0.0.1:5000/updateuser', { // Adjust URL as needed
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            alert(result.message);
            if (response.ok) {
                fetchUsers(); // Refresh user list or handle UI update
            }
        } catch (error) {
            console.error('Error updating user:', error);
        }
    });

    // Update User Form submission
    document.getElementById('updateUserForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = {
            email: formData.get('updateEmail'),
            firstName: formData.get('updateFirstName'),
            lastName: formData.get('updateLastName'),
            mobile: formData.get('updateMobile'),
            gender: formData.get('updateGender'),
            newPassword: formData.get('updatePassword'),
            currentPassword: formData.get('currentPassword')
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/updateuse', { // Adjust URL as needed
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            alert(result.message);
            if (result.message === 'User updated successfully') {
                fetchUsers(); // Refresh user list
                closeModal(updateUserModal);
            }
        } catch (error) {
            console.error('Error updating user:', error);
        }
    });

    // Delete User Form submission
    document.getElementById('deleteUserForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        const mobile = document.getElementById('deleteMobile').value;

        try {
            const response = await fetch('http://127.0.0.1:5000/deleteuser', { // Adjust URL as needed
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mobile })
            });
            const result = await response.json();
            alert(result.message);
            if (result.message === 'User deleted successfully') {
                fetchUsers(); // Refresh user list
                closeModal(deleteUserModal);
            }
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    });
});
