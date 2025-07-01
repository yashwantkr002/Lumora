const q = document.getElementById("q");
const searchResults = document.getElementById("search-results");

let currentPage = 1; // Track the current page
let isLoading = false; // Prevent multiple requests

const fetchUsers = async (value, page) => {
  try {
    const response = await fetch(
      `?q=${encodeURIComponent(value)}&page=${page}`,
      {
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
        },
      }
    );

    if (response.ok) {
      const data = await response.json();

      if (data.users.length === 0 && page === 1) {
        searchResults.innerHTML =
          "<p class='text-gray-600'>No users found.</p>";
      } else {
        data.users.forEach((user) => {
          const userElement = document.createElement("div");
          userElement.innerHTML = `
            <div class="flex items-center space-x-2">
              <a href="/profile/${user.username}">
                <img src="${
                  user.profile_picture
                }" alt="Profile Picture" class="w-10 h-10 rounded-full">
                <div>
                  <p class="font-semibold">${user.username}</p>
                  <p class="text-gray-600">${user.bio}</p>
                </div>
              </a>
              ${
                data.followed_users.includes(user.username)
                  ? `<button onclick="follow_unfollow('${user.username}')" type="submit" class="bg-red-500 text-white font-semibold px-4 py-2 rounded-lg shadow hover:bg-red-600">Unfollow</button>`
                  : `<button onclick="follow_unfollow('${user.username}')" type="submit" class="bg-blue-500 text-white font-semibold px-4 py-2 rounded-lg shadow hover:bg-blue-600">Follow</button>`
              }
            </div>`;
          searchResults.appendChild(userElement);
        });

        if (!data.has_next) {
          window.removeEventListener("scroll", handleScroll);
        }
      }
    }
  } catch (error) {
    console.error("Error fetching users:", error);
    searchResults.innerHTML =
      "<p class='text-red-600'>Error fetching users. Please try again later.</p>";
  } finally {
    isLoading = false;
  }
};

const myfunc = async (e) => {
  let value = e.target.value.trim();
  currentPage = 1; // Reset to the first page
  searchResults.innerHTML = ""; // Clear previous results

  if (value === "") {
    searchResults.innerHTML =
      "<p class='text-gray-600'>Start typing to search...</p>";
    return;
  }

  fetchUsers(value, currentPage);
};

const handleScroll = () => {
  if (
    window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 &&
    !isLoading
  ) {
    isLoading = true;
    currentPage++;
    fetchUsers(q.value.trim(), currentPage);
  }
};

const debounce = (func, wait) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

const mydebounce = debounce(myfunc, 1000);

q.addEventListener("input", mydebounce);
window.addEventListener("scroll", handleScroll);

const follow_unfollow = (user) => {
  const btn = document.querySelector(
    `button[onclick="follow_unfollow('${user}')"]`
  );
  btn.disabled = true;
  try {
    const csrfToken = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    ).value;
    fetch(`/follow/${user}/`, {
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
          btn.textContent = data.is_following ? "Unfollow" : "Follow";
          btn.classList.toggle("bg-red-500", data.is_following);
          btn.classList.toggle("hover:bg-red-600", data.is_following);

          btn.classList.toggle("bg-blue-500", !data.is_following);
          btn.classList.toggle("hover:bg-blue-600", !data.is_following);
        }
      });

    btn.disabled = false;
  } catch (error) {
    console.log(error);
    btn.disabled = false;
  }
};
