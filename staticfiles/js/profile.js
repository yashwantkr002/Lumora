const followBtn = document.getElementById("follow-btn");
let page = 2; // Start from the second page
let isLoading = false;

if (followBtn) {
  followBtn.addEventListener("click", function () {
    this.disabled = true;
    try {
      const username = followBtn.getAttribute("data-username");
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;
      fetch(`/follow/${username}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            alert(data.error);
          } else {
            // Update button text
            followBtn.textContent = data.is_following ? "Unfollow" : "Follow";
            // Update follower count
            const followerCountElement =
              document.querySelector("#follower_count");
            if (followerCountElement) {
              followerCountElement.textContent = data.follower_count;
            }
            this.disabled = false;
          }
        })
        .catch((error) => console.error("Error:", error));
    } catch (error) {
      this.disabled = false;
    }
  });
}

// load morepost
const loadMorePosts = () => {
  if (isLoading) return;

  const loader = document.getElementById("loader");
  loader.classList.remove("hidden");
  isLoading = true;

  fetch(`?page=${page}`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.posts.length > 0) {
        const postContainer = document.getElementById("post-container");
        data.posts.forEach((post) => {
          const postElement = document.createElement("div");
          postElement.className = "relative";
          postElement.setAttribute("data-post-id", post.id);
          postElement.setAttribute("onclick", `openPostDetail('${post.id}')`);

          if (post.image_url) {
            postElement.innerHTML = `
                <img
                  src="${post.image_url}"
                  alt="Post Image"
                  class="w-full h-52 md:h-72 object-cover rounded-lg cursor-pointer"
                />
              `;
          } else if (post.video_url) {
            postElement.innerHTML = `
                <video
                  autoplay
                  muted
                  playsinline
                  src="${post.video_url}"
                  class="w-full h-52 md:h-72 object-cover rounded-lg cursor-pointer"
                >
                  Your browser does not support the video tag.
                </video>
                <div
                  class="absolute top-0 right-0 bg-black bg-opacity-50 text-white text-sm p-2"
                >
                  <img class="w-6 h-6" src="/static/images/reels.png" alt="reels" />
                </div>
              `;
          }

          postContainer.appendChild(postElement);
        });
        page++;
        isLoading = false;
      }
    })
    .catch(() => {
      console.error("Error loading more posts.");
      isLoading = false;
    });
  loader.classList.add("hidden");
};

// scroll event
window.addEventListener("scroll", () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 10) {
    loadMorePosts();
  }
});

window.openPostDetail = (postId) => {
  console.log(postId);
  window.location.href = `/post/${postId}/`;
};
