let likeButtons = document.querySelectorAll("i.heart")

likeButtons.forEach((likeButton)=>{            
    likeButton.addEventListener("click", (event)=>{
        let postId = event.target.dataset.postId 
        let username = event.target.closest(".btn").dataset.username
        let category = event.target.closest(".btn").dataset.category
        likeRequest(event.target, postId, username, category)
    })
})

let likeRequest = async (button, postId, username, category) => {
    let likeURL = `/${username}/${category}/${postId}/likes-async/`
    let response = await fetch(likeURL)
    let result = await response.json()

    if (result.status) {
        button.classList.remove('bi-heart')
        button.classList.add('bi-heart-fill')
        button.style.color = 'red'
        
    } else {
        button.classList.remove('bi-heart-fill')
        button.classList.add('bi-heart')
        button.style.color = 'black'
    }
button.innerHTML = result.count;
}
