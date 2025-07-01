const resend_otp = document.getElementById("resend_otp");

let countdown = 600; 
const timerInterval = setInterval(() => {
    if (countdown > 0) {
        resend_otp.textContent = `${countdown} seconds`;
        countdown--;
    } else {
        clearInterval(timerInterval); // Stop the timer when it reaches 0
        // Clear the countdown text and add the "Resend OTP" link
        resend_otp.innerHTML = `
            <a id="resend_otp_link"
               href="/resend_otp/"
               class="text-blue-500 hover:underline"
            >
               Resend OTP
            </a>`;
    }
}, 1000);
