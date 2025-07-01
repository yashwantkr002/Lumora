document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#select_file").addEventListener("click", () => {
    document.querySelector("#create-post-icon").click();
  });
});

document.querySelector("#create-post-icon").addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file.size >  1024 * 1024) {
    e.preventDefault();
    alert(`File size exceeds 10 MB. Please upload a smaller file.`);
    return;
}

  const select_file = document.querySelector("#select_file");
  select_file.style.display = "none";
  const file_preview = document.querySelector("#file_preview");
  if (file) {
    const mediaElement = file.type.startsWith("video")
      ? document.createElement("video")
      : document.createElement("img");
    mediaElement.src = URL.createObjectURL(file);
    mediaElement.controls = file.type.startsWith("video");
    mediaElement.className = "w-full h-full object-cover rounded-md";
    document.querySelector("#insert").innerHTML=""
    document.querySelector("#insert").appendChild(mediaElement)
    file_preview.classList.remove("hidden");
  }

  console.log(file);
});
