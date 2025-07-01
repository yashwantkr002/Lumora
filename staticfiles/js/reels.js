let currentPage = 2;
let isLoading = false;

const likeunlike = async (id) => {
  const button = document.querySelector(`button[onclick="likeunlike('${id}')"]`);

  button.disabled = true;
  try {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const response = await fetch(`/like/${id}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    });
    if (response.ok) {
      const data = await response.json();
      const likeCountElement = document.getElementById(`like-${id}`);
      likeCountElement.textContent = data.likes_count;
      const btn = document.getElementById(`btn-${id}`);
      if (data.liked) {
        btn.classList.add("text-red-500");
      } else {
        btn.classList.remove("text-red-500");
      }
      button.disabled = false;
    }
  } catch (error) {
    console.log(error);
    button.disabled = false;
  }
};

const loadReels = async () => {
  if (isLoading) return;

  isLoading = true;
  try {
    const response = await fetch(`/reels/?page=${currentPage}`, {
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    if (response.ok) {
      const data = await response.json();
      const reelsContainer = document.getElementById("reels-container");

      data.reels.forEach((reel) => {
        const reelElement = document.createElement("div");
        reelElement.className = "bg-white shadow-md rounded-lg";
        reelElement.innerHTML = `
        <div class="h-full w-full relative bg-black text-white">
          <!-- Video Section -->
          <video
            class="reel-video h-full w-full object-cover"
            src="${reel.video_url}"
            loop
            onclick="toggleMute('${reel.id}')"
            ondblclick="likeunlike('${reel.id}')"
          >${reel.id}</video>
          <!-- Caption -->
          <div class="absolute bottom-20 left-4 space-y-2">
            <p class="text-sm">${reel.caption}</p>
          </div>

          <!-- Action Buttons -->
          <div class="absolute bottom-4 right-4 flex flex-col space-y-4">
            <a href="/profile/${reel.author}" class="flex flex-col items-center">
              <img
                src="${reel.author_image}"
                alt="JioCinema"
                class="h-6 w-6 rounded-full"
              />
            </a>
            <button onclick="likeunlike('${reel.id}')" class="flex flex-col items-center">
              <i id="btn-${reel.id}" class="fas fa-heart text-2xl ${reel.is_liked ? 'text-red-500' : ''}"></i>
              <span id="like-${reel.id}">${reel.likes_count}</span>
            </button>
            <button class="flex flex-col items-center">
              <i class="fas fa-comment text-2xl"></i>
              <span>4</span>
            </button>
            <button class="flex flex-col items-center">
              <i class="fas fa-share text-2xl"></i>
              <span>Share</span>
            </button>
            <div class="flex flex-col items-center">
              <i id="mute-icon-${reel.id}" class="fas fa-volume-up text-xl"></i>
            </div>
          </div>
        </div>
      `;
        reelsContainer.appendChild(reelElement);
      });

      if (data.has_next) {
        currentPage++;
      } else {
        window.removeEventListener("scroll", handleScroll);
      }

      // Attach IntersectionObserver to new videos
      observeVideos();
    }
  } catch (error) {
    console.error("Error loading reels:", error);
  } finally {
    isLoading = false;
  }
};
// mute 
const toggleMute = (postId) => {
  const video = document.querySelector(`video[onclick="toggleMute('${postId}')"]`);
  const muteIcon = document.getElementById(`mute-icon-${postId}`);

  video.muted = !video.muted;

  if (video.muted) {
    muteIcon.classList.remove("fa-volume-up");
    muteIcon.classList.add("fa-volume-mute");
  } else {
    muteIcon.classList.remove("fa-volume-mute");
    muteIcon.classList.add("fa-volume-up");
  }

};

const handleScroll = () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 10) {
    loadReels();
  }
};

// Auto-play logic using IntersectionObserver
const observeVideos = () => {
  const videos = document.querySelectorAll(".reel-video");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const video = entry.target;
        if (entry.isIntersecting) {
          video.play();
          video.muted = false;
          const muteIcon = document.getElementById(`mute-icon-${video.innerHTML}`);
          muteIcon.classList.remove("fa-volume-mute");
          muteIcon.classList.add("fa-volume-up");
          // Play the video when in view
        } else {
          video.pause(); // Pause the video when out of view
        }
      });
    },
    { threshold: 0.5 } // Play video when 50% of it is visible
  );

  videos.forEach((video) => observer.observe(video));
};

// Initialize
window.addEventListener("scroll", handleScroll);
observeVideos();



// like unlike 




// ${reel.comments.map(comment => `
//   <p>
//     <span class="font-bold text-gray-800">${comment.author}</span>
//     <span class="text-gray-600">${comment.text}</span>
//   </p>
// `).join('')}


// const loadingSpinner = document.getElementById("loading");
//   loadingSpinner.classList.remove("hidden");