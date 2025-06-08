// Console.log when DOM is loaded.
document.addEventListener("DOMContentLoaded", () => {
  console.log("Loaded!");
});

// Get cookie by name //
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
      // Check if this cookie string begins with the name we want.
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

///// POST-RELATED FUNCTIONALITY /////
function edit_post(button) {
  // Ensure button is within a post container
  const postContainer = button.closest(".post-container");
  const postID = postContainer.dataset.postid;
  const postContentElem = postContainer.querySelector(".post-content");
  const originalContent = postContentElem.innerText;

  // Prevent duplicate edit //
  if (postContainer.querySelector("textarea")) return;

  // Create textarea //
  const textarea = document.createElement("textarea");
  textarea.classList.add("form-control", "mb-2");
  textarea.value = originalContent;

  // Create Save button //
  const saveButton = document.createElement("button");
  saveButton.innerText = "Save";
  saveButton.className = "btn btn-success btn-sm me-2";

  // Save button functionality //
  saveButton.onclick = () => {
    fetch(`/edit_post/${postID}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        content: textarea.value,
      }),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Failed to update post.");

        return response.json();
      })
      .then(() => {
        postContentElem.innerText = textarea.value;
        textarea.remove();
        saveButton.remove();
        cancelButton.remove();
      })
      .catch((error) => {
        console.error(error);
        alert("Failed to save post.");
      });
  };

  // Create Cancel button
  const cancelButton = document.createElement("button");
  cancelButton.innerText = "Cancel";
  cancelButton.className = "btn btn-secondary btn-sm";

  cancelButton.onclick = () => {
    postContentElem.innerText = originalContent;
    textarea.remove();
    saveButton.remove();
    cancelButton.remove();
  };

  // Replace content with textarea + buttons
  postContentElem.innerHTML = "";
  postContentElem.appendChild(textarea);
  postContentElem.appendChild(saveButton);
  postContentElem.appendChild(cancelButton);

  setTimeout(() => textarea.classList.add("show"), 10);
}

// Fetch post from ID and delete it.
function delete_post(button) {
  try {
    const postContainer = button.closest(".post-container");
    const postID = postContainer.dataset.postid;

    fetch(`/delete_post/${postID}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        postContainer.remove();
        setTimeout(() => textarea.classList.add("hide"), 10);
      });
  } catch (err) {
    console.error(err);
  }
}

// SOCIAL-RELATED FUNCTIONALITY //
function toggle_follow(button) {
  const username = button.getAttribute("data-author");
  fetch(`/follow/${username}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (typeof data.buttonContext != "undefined") {
        button.innerHTML = data.buttonContext;
      }
    });
}

// Get like count and update button with like count and status.
function toggle_like(button) {
  try {
    const postContainer = button.closest(".post-container");
    const postID = postContainer.getAttribute("data-postId");
    const likeCount = postContainer.querySelector(".like-button");

    fetch(`/like/${postID}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);

        if (data["liked"]) {
          button.classList.remove("bi-hand-thumbs-up");
          button.classList.remove("btn-primary");
          button.classList.add("bi-hand-thumbs-up-fill");
          button.classList.add("btn-secondary");
        } else {
          button.classList.remove("bi-hand-thumbs-up-fill");
          button.classList.remove("btn-secondary");
          button.classList.add("btn-primary");
          button.classList.add("bi-hand-thumbs-up");
        }

        likeCount.innerHTML = data["like_count"];
      });
  } catch (err) {
    console.error(err);
  }
}
