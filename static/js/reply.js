// reply form toggle
$('.replybutton').click(function(){
$(this).next('.replyform_div').toggle();
});    

// reply create
let replyForms = document.querySelectorAll('.reply-Form')
replyForms.forEach(function(replyForm){
    replyForm.addEventListener('submit', function(event){
        event.preventDefault()
        const data = new FormData(event.target)
        axios.post(event.target.action, data)
            .then(function(response){
            const reply = response.data
            console.log(reply)
            const updatedAt = new Intl.DateTimeFormat('ko-KR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: 'numeric',
                minute: 'numeric',
                hour12: true
            }).format(reply.updated_at);
            const newReply = `
            <div class="ms-2">
                <div class="d-flex align-items-center" style="width: 100%;">
                    <div class="m-1" style="width: 30px; height: 30px; border-radius: 70%; overflow: hidden;">
                        <img src="${ reply.reply_user_profile_image_url }" alt="" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>

                    <div>
                        <p class="m-0" style="font-size: 1rem;">${ reply.reply_username }</p>
                        <p class="m-0" style="font-size: 0.75rem; color: rgb(143, 143, 143);">${updatedAt}</p>
                    </div>

                    <div class="dropdown ms-auto">
                        <button class="btn dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false"></button>
                        <ul class="dropdown-menu">
                            <li><button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#replyModal${ reply.number }-${ reply.comment_id }-${ reply.reply_id }">수정하기</button></li>
                            <li><button onclick="replyDelete('${reply.owner}','${reply.category}','${reply.number}','${reply.comment_id}','${reply.reply_id}');" class="dropdown-item" href="#">삭제하기</button></li>
                        </ul>
                    </div>
                </div>
                <p class="ms-3">${ reply.reply_content }</p>
            </div>
            `;
            const replyList = replyForm.closest('.reply_form')
            replyList.insertAdjacentHTML('beforebegin', newReply)
            event.target.reset()
            })
        })
    })

// reply_update
function showUpdateReplyForm(replyId, content) {
    $('[id^="reply-"][id$="-update-form"]').hide();
    $('#reply-' + replyId + '-update-form').show();
    $('#reply-' + replyId + '-update-content').val(content);
}

function updateReply(username, category, postId, commentId, replyId, content) {
    $.ajax({
        type: 'POST',
        url: `/${username}/${category}/${postId}/comments/${commentId}/replys/${replyId}/update/`,
        dataType: 'json',
        data: {
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
            'content': content,
        },
        success: function(response) {
            $('#reply-' + replyId + '-content').text(response.content);
            $('#reply-' + replyId + '-update-form').hide();
            location.reload()
        }
    });
}

// reply_delete
function replyDelete(username, category, number, comment_id, reply_id) {
    $.ajax({
        type : 'POST',
        url : `/${username}/${category}/${number}/comments/${comment_id}/replys/${reply_id}/delete/`,
        dataType : 'json',
        data : {
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        },
        success: function(response){
            location.reload()
        }
    })
}