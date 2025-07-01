function toggleMute(postId) {
  const video = document.getElementById(`video-${postId}`);
  const muteBtn = document.getElementById(`mute-btn-${postId}`);
  const icon = muteBtn.querySelector("i");

  if (video.muted) {
    video.muted = false;
    icon.classList.remove("fa-volume-mute");
    icon.classList.add("fa-volume-up");
  } else {
    video.muted = true;
    icon.classList.remove("fa-volume-up");
    icon.classList.add("fa-volume-mute");
  }
}

const like_unlike = async (id) => {
  const button = document.querySelector(
    `button[onclick="like_unlike('${id}')"]`
  );
  button.disabled = true;
  try {
    const csrfToken = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    ).value;
    const response = await fetch(`/like/${id}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    });
    if (response.ok) {
      const data = await response.json();
      const likeCountElement = document.getElementById(`like_${id}`);
      likeCountElement.textContent = data.likes_count;
      button.classList.toggle("text-red-500", data.liked);
      button.classList.toggle("text-gray-500", !data.liked);
      button.disabled = false;
    }
  } catch (error) {
    button.disabled = false;
  }
};



let currentPage = 2;
let isLoading = false;

const loadPosts = async () => {
  if (isLoading) return;
  isLoading = true;
  const loader= document.getElementById("loader")
  loader.classList.remove("hidden")
  try {
    const response = await fetch(`/?page=${currentPage}`, {
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    if (response.ok) {
      const data = await response.json();
      const postsContainer = document.getElementById("posts-container");

      data.posts.forEach((post) => {
        const postElement = document.createElement("div");
        postElement.className = "bg-white shadow-md rounded-lg mb-4";
        postElement.innerHTML = 
        `
        <div class="bg-white shadow-md rounded-lg">
            <!-- Post Header -->
            <div class="flex items-center p-4">
              <img
              src="${post.author_image}"
                alt="${post.author.username}"
                class="h-10 w-10 rounded-full border"
              />
              <div class="ml-4">
                <h2 class="font-bold text-gray-800">
                  ${post.author}
                </h2>
                <p class="text-sm text-gray-500">
                  ${post.created_at}
                </p>
              </div>
              <div class="ml-auto">
                <button class="text-gray-500 hover:text-gray-800">
                  <i class="fas fa-ellipsis-h"></i>
                </button>
              </div>
            </div>
            <!-- Post Image -->
            <div class="flex relative justify-center">

            ${
                post.image_url
                  ? `
              
               <img
                src="${post.image_url}"
                alt="Post Image"
                class="w-[95%] md:w-[400px] h-[450px] sm:w-[400px] object-contain rounded-lg"
              />`
                : `
                <div class="relative w-[95%] md:w-[400px] h-[450px] sm:w-[400px]">
             <video
              id="video-${post.id}"
              muted
              autoplay
                src="${post.video_url}"
                class="w-[95%] md:w-[380px] h-[450px] sm:w-[300px] object-cover rounded-lg"
              >
                Your browser does not support the video tag.
              </video>
             <button
              class="absolute bottom-4 right-4 bg-gray-800 text-white p-2 rounded-full hover:bg-gray-700"
              onclick="toggleMute(${post.id})"
              id="mute-btn-${post.id}"
          >
              <i class="fas fa-volume-mute"></i>
          </button>

                  </div>
                  `
            }

            </div>
            <!-- Post Actions -->
            <div
              class="flex items-center justify-between mt-1 px-4 py-2 border-t"
            >
              <div class="flex items-center space-x-4">
                <button
                  class="text-gray-500 outline-none border-none  flex items-center ${post.is_liked ? 'text-red-500' : ''}"
                  onclick="like_unlike('${post.id}')"  >
                  <i class="fas fa-heart mr-1"></i> Likes ( <span id="like_${post.id}" > ${post.like_count}</span>)
                </button>
                <input
                type="hidden"
                name="csrfmiddlewaretoken"
                value="{{ csrf_token }}"
           />
                <button
                  class="text-gray-500 hover:text-blue-500 flex items-center"
                >
                  <i class="fas fa-comment mr-1"></i> Comment
                </button>
                <button
                  class="text-gray-500 hover:text-green-500 flex items-center"
                >
                  <i class="fas fa-share mr-1"></i> Share
                </button>
              </div>
            </div>
            <!-- Comments Section -->
            <div class="px-4 py-2">
              <p>
                <span class="font-bold text-gray-800">Tinku</span>
                <span class="text-gray-600">Thank you</span>
              </p>

              <p>
                <a href="#" class="text-blue-500 hover:underline">
                  View All Comments
                </a>
              </p>
              <form method="post" class="mt-2">
                <input
                  type="text"
                  name="comment"
                  placeholder="Add a comment..."
                  class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 px-4 py-2"
                />
              </form>
            </div>
          </div>
        `;
        postsContainer.appendChild(postElement);
        loader.classList.add("hidden");
      });

      if (data.has_next) {
        currentPage++;
      } else {
        window.removeEventListener("scroll", handleScroll);
      }
    }
  } catch (error) {
    console.error("Error loading posts:", error);
  } finally {
    isLoading = false;
  }
};

const handleScroll = () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 10) {
    loadPosts();
  }
};

// Initialize
window.addEventListener("scroll", handleScroll);
