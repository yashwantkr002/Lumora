document.getElementById('profile-picture-input').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
      const img = document.querySelector('#profile-picture-preview');
      img.src = URL.createObjectURL(file);
    }
  });