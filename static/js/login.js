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