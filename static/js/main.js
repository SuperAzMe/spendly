// main.js — students will add JavaScript here as features are built

function initConfirmPasswordValidation() {
    const form = document.getElementById("register-form");
    if (!form) return;

    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm_password");
    const errorText = document.getElementById("confirm-password-error");

    function validateMatch() {
        const mismatch = confirmPassword.value !== "" && password.value !== confirmPassword.value;
        confirmPassword.classList.toggle("input-error", mismatch);
        errorText.hidden = !mismatch;
        return !mismatch;
    }

    confirmPassword.addEventListener("input", validateMatch);
    password.addEventListener("input", validateMatch);

    form.addEventListener("submit", function (event) {
        if (!validateMatch()) {
            event.preventDefault();
        }
    });
}

document.addEventListener("DOMContentLoaded", initConfirmPasswordValidation);
