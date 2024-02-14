// comment create
let commentForms = document.querySelectorAll('.comment-Form')
commentForms.forEach(function(commentForm){
    commentForm.addEventListener('submit', function(event){
        event.preventDefault()
        const data = new FormData(event.target)
        axios.post(event.target.action, data)
            .then(function(response){
            const comment = response.data
            const updatedAt = new Intl.DateTimeFormat('ko-KR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: 'numeric',
                minute: 'numeric',
                hour12: true
            }).format(comment.updated_at);

            const likeIcon = comment.like_users > 0 ?
            `<i class="bi bi-heart-fill comment_heart align-self-center" style="color:red; font-size: 1rem;" data-post-id="${comment.number}" data-comment-id="${comment.comment_id}">${comment.like_users}</i>` :
            `<i class="bi bi-heart comment_heart align-self-center" style="font-size: 1rem;" data-post-id="${comment.number}" data-comment-id="${comment.comment_id}">${comment.like_users}</i>`;


            const newComment = `
            <div class="d-flex align-items-center" style="width: 100%;">
                <div class="m-1" style="width: 30px; height: 30px; border-radius: 70%; overflow: hidden;">
                    <img src="${comment.comment_user_profile_image_url}" alt="" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <div class="mx-2">
                    <p class="m-0" style="font-size: 1rem;">${comment.comment_username}</p>
                    <p class="m-0" style="font-size: 0.75rem; color: rgb(143, 143, 143);">${updatedAt}</p>
                </div>
                <div class="ms-auto my-0 py-0">
                    <div class="ms-auto">
                        <div class="dropdown">
                            <button class="btn dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false"></button>
                            <ul class="dropdown-menu">
                                <li><button class="dropdown-item" data-bs-toggle="modal" data-bs-target="#commentModal${comment.number}-${comment.comment_id}">수정하기</button></li>
                                <li><button onclick="commentDelete('${comment.owner}','${comment.category}','${comment.number}','${comment.comment_id}');" class="dropdown-item" href="#">삭제하기</button></li>
                            </ul>
                        </div>
                    </div>

                    <div class="my-0 py-0 me-2">
                        ${likeIcon}
                    </div>
                </div>
            </div>
            <p class="mt-2 ms-1">${comment.comment_content}</p>
            <div class="d-flex align-items-center" style="width: 100%;">
                <button type="button" class="btn btn-outline-secondary" data-bs-toggle="collapse" data-bs-target="#reply-list-${comment.number}-${comment.comment_id}" aria-expanded="false" aria-controls="reply" style="--bs-btn-padding-y: 0rem; --bs-btn-padding-x: .3rem; --bs-btn-font-size: .75rem;">답글</button>
            </div>
            <hr>            
            `;
            const commentList = commentForm.closest('.comment_form');
            commentList.insertAdjacentHTML('beforebegin', newComment);
            event.target.reset()
        })
    })
})

// comment update
function showUpdateForm(commentId, content) {
    $('[id^="comment-"][id$="-update-form"]').hide();
    $('#comment-' + commentId + '-update-form').show();
    $('#comment-' + commentId + '-update-content').val(content);
}

function updateComment(username, category, number, commentId) {
    const content = $('#comment-' + commentId + '-update-content').val();
    $.ajax({
        type: 'POST',
        url: `/${username}/${category}/${number}/comments/${commentId}/update/`,
        dataType: 'json',
        data: {
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
            'content': content,
        },
        success: function(response) {
            $('#comment-' + commentId + '-content').text(response.content);
            $('#comment-' + commentId + '-update-form').hide();
            location.reload()
        }
    });
}


// comment_delete
function commentDelete(username, category, number, comment_id) {
    $.ajax({
        type : 'POST',
        url : `/${username}/${category}/${number}/comments/${comment_id}/delete/`,
        dataType : 'json',
        data : {
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        },
        success: function(response){
            location.reload()
        }
    })
}


// comment like 
let comment_likeButtons = document.querySelectorAll("i.comment_heart")
comment_likeButtons.forEach((comment_likeButton)=>{            
    comment_likeButton.addEventListener("click", (event)=>{
        let postId = event.target.dataset.postId
        let commentId = event.target.dataset.commentId 
        let username = event.target.dataset.username
        let category = event.target.dataset.category 
        comment_likeRequest(event.target, postId, username, category, commentId)
    })
})

let comment_likeRequest = async (button, postId, username, category, commentId) => {
    let comment_likeURL = `/${username}/${category}/${postId}/comments/${commentId}/likes-async/`;
    try {
        let response = await fetch(comment_likeURL);
        let result = await response.json();

        if (result.status) {
            button.classList.remove('bi-heart', 'comment_heart');
            button.classList.add('bi-heart-fill', 'comment_heart');
            button.style.color = 'red';
        } else {
            button.classList.remove('bi-heart-fill', 'comment_heart');
            button.classList.add('bi-heart', 'comment_heart');
            button.style.color = 'black';
        }

        button.innerHTML = result.count;
    } catch (error) {
        console.error('Error during like request:', error);
    }
};