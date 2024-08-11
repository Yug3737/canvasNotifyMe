//
// file: script.js
// author: Yug Patel
// last modified: 17 July 2024

function isValidForm() {
    let phoneNumber = document.getElementById("phone-no").value;
    if (!phoneNumber.match(/^\d{10}$/)) {
        alert("Please enter a valid 10-digit US phone number.");
        return false;
    } else if (phoneNumber.length !== 10) {
        alert("Phone number must be 10 digit length");
        return false;
    }

    let firstName = document.getElementById("first-name").value();
    let lastName = document.getElementById("last-name").value();
    if (!firstName.match(/^[a-zA-Z0-9]+$/)) {
        alert("Please enter valid first/last name only consisting of letters or numbers.");
        return false;
    }
    else if (firstName.length > 30) {
        alert("First Name cannot be longer than 30 characters.");
        return false;
    }
    else if (lastName.length > 30) {
        alert("Last Name cannot be longer than 30 characters.");
        return false;
    }
    return true;
}

function handleSubmit(event) {
    event.preventDefault(); // Prevents the default form submission
    const successMessage = document.getElementById('success-message');
    successMessage.textContent = 'Success! You have been subscribed to Canvas Notify Me.';
    successMessage.style.display = 'block'; // Show the success message
}

document.addEventListener('DOMContentLoaded', () => {
    const inputTime = document.getElementById('notification-time');

    // Console Log the time that user chose
    const form = document.querySelector('form');
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        console.log('Chose notification Time: ', inputTime.value);
    })
})