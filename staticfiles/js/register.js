const password2 =document.querySelector("#password2")
const element = document.getElementById("error-message");
const registration_form = document.getElementById("registration_form");
if (element && element.textContent.trim() !== "") {
  setTimeout(() => {
    element.textContent = "";
  },10000);
}

function togglePasswordVisibility(inputId, icon) {
    const input = document.getElementById(inputId);
    if (input.type === "password") {
      input.type = "text";
      icon.src = "/static/images/closeeye.png"; 
    } else {
      input.type = "password";
      icon.src = "/static/images/openeye.png"; 
    }
  }

password2.addEventListener('keyup', (event) => {
    const password1 = document.querySelector("#password1").value;
    const password3 = password2.value;
    if (password1 === password3) {
        password2.classList.remove("focus:ring-red-600", "focus:border-red-600");
        password2.classList.add("focus:ring-green-600", "focus:border-green-600");
    } else {
        password2.classList.remove("focus:ring-green-600", "focus:border-green-600");
        password2.classList.add("focus:ring-red-600", "focus:border-red-600");
    } 
});

registration_form.addEventListener('submit', (event) => {
    const password1 = document.querySelector("#password1").value;
    const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!passwordRegex.test(password1)) {
        event.preventDefault();
        alert("Password must be at least 8 characters long., Password must include at least one uppercase letter, one lowercase letter, one digit, and one special character.");
    }
});