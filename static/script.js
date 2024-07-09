function handleSubmit(event) {
    event.preventDefault(); // Prevents the default form submission
    const successMessage = document.getElementById('success-message');
    successMessage.textContent = 'Success! You have been subscribed to Canvas Notify Me.';
    successMessage.style.display = 'block'; // Show the success message
}