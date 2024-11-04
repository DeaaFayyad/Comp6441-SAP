// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById("password-input");
    const toggleButton = document.querySelector(".password-checker button");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleButton.textContent = "HIDE";
    } else {
        passwordInput.type = "password";
        toggleButton.textContent = "SHOW";
    }
}

// Check password strength with detailed feedback
function checkPassword() {
    const password = document.getElementById("password-input").value;
    const feedback = document.getElementById("feedback");
    const strengthBar = document.getElementById("strength-bar");

    // Reset strength bar segments
    Array.from(strengthBar.children).forEach(segment => {
        segment.style.backgroundColor = "#e0e0e0"; // Reset color for all segments
    });

    // Password strength checks
    let issues = [];
    if (password.length < 8) issues.push("At least 8 characters");
    if (!/[A-Z]/.test(password)) issues.push("Uppercase letter");
    if (!/[a-z]/.test(password)) issues.push("Lowercase letter");
    if (!/[0-9]/.test(password)) issues.push("Number");
    if (!/[^A-Za-z0-9]/.test(password)) issues.push("Special character");

    // Update feedback and strength bar based on issues
    if (issues.length > 0) {
        feedback.textContent = "Weak: " + issues.join(", ");
        feedback.style.color = "#ff4b5c";
        strengthBar.children[0].style.backgroundColor = "#ff4b5c";
    } else {
        feedback.textContent = "Strong password!";
        feedback.style.color = "#28a745";
        strengthBar.children[0].style.backgroundColor = "#28a745";
        strengthBar.children[1].style.backgroundColor = "#28a745";
        strengthBar.children[2].style.backgroundColor = "#28a745";
    }
}

// Event listener for real-time strength check
document.getElementById("password-input").addEventListener("input", function () {
    const password = this.value;
    const strengthBar = document.getElementById("strength-bar");
    const feedback = document.getElementById("feedback");

    // Reset strength bar segments
    Array.from(strengthBar.children).forEach(segment => {
        segment.style.backgroundColor = "#e0e0e0"; // Reset color for all segments
    });

    // Determine password strength level
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    // Update strength bar and feedback based on calculated strength
    if (strength <= 2) {
        strengthBar.children[0].style.backgroundColor = "#ff4b5c";
        feedback.textContent = "Your password is weak";
        feedback.style.color = "#ff4b5c";
    } else if (strength === 3 || strength === 4) { // Moderate strength condition
        strengthBar.children[0].style.backgroundColor = "#ffaf3f";
        strengthBar.children[1].style.backgroundColor = "#ffaf3f";
        feedback.textContent = "Your password is moderate";
        feedback.style.color = "#ffaf3f";
    } else {
        strengthBar.children[0].style.backgroundColor = "#28a745";
        strengthBar.children[1].style.backgroundColor = "#28a745";
        strengthBar.children[2].style.backgroundColor = "#28a745";
        feedback.textContent = "Your password is strong!";
        feedback.style.color = "#28a745";
    }
});
