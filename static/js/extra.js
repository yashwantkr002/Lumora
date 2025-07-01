document.addEventListener("DOMContentLoaded", function () {
    const videos = document.querySelectorAll(".reel-video");
  
    const handleIntersection = (entries) => {
      entries.forEach((entry) => {
        const video = entry.target;
        if (entry.isIntersecting) {
          video.play();
        } else {
          video.pause();
        }
      });
    };
  
    const observer = new IntersectionObserver(handleIntersection, {
      root: null,
      threshold: 0.8, // Play when 80% visible
    });
  
    videos.forEach((video) => observer.observe(video));
  });
  fetch("/api/get-reels/")
  .then((response) => response.json())
  .then((reels) => {
    const container = document.querySelector(".reels-container");
    reels.forEach((reel) => {
      const reelDiv = document.createElement("div");
      reelDiv.className = "reel-container h-screen w-full relative bg-black text-white";
      reelDiv.innerHTML = `
        <video class="reel-video h-full w-full object-cover" src="${reel.video_url}" muted autoplay loop></video>
        <div class="absolute bottom-20 left-4 space-y-2">
          <p class="text-lg font-bold text-yellow-400">${reel.caption}</p>
        </div>
        <div class="absolute bottom-4 right-4 flex flex-col space-y-4">
          <button class="flex flex-col items-center">
            <i class="fas fa-heart text-2xl"></i>
            <span>${reel.likes}</span>
          </button>
          <button class="flex flex-col items-center">
            <i class="fas fa-comment text-2xl"></i>
            <span>${reel.comments}</span>
          </button>
        </div>
      `;
      container.appendChild(reelDiv);
    });
  });
  