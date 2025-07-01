const likeunlike = async(id)=>{
    const button = document.querySelector(`button[onclick="likeunlike('${id}')"]`);
    button.disabled=true
    try {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const response = await fetch(`/like/${id}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            }
        });
        if (response.ok) {
            const data = await response.json();
            const likeCountElement = document.getElementById("like");
            likeCountElement.textContent = data.likes_count;
            button.classList.toggle("text-red-500", data.liked);
            button.classList.toggle("text-gray-500", !data.liked);
            button.disabled=false;  
        }

    } catch (error) {
        console.log(error);  
        button.disabled = false;      
    }
}
