$(document).ready(function() {
    // 수정 버튼 클릭 이벤트
    $(document).on('click', '.edit-btn', function() {
        var introduceText = $(this).siblings('p').text().trim();
        $(this).siblings('textarea').val(introduceText).show().removeAttr('readonly').focus();
        $(this).siblings('p').hide();
        $(this).hide();
        $(this).siblings('.submit-btn').show();
    });

    // 제출 버튼 클릭 이벤트
    $(document).on('click', '.submit-btn', function() {
        var newText = $(this).siblings('textarea').val().trim();
        var url = $(this).siblings('textarea').data('url');
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                'introduce': newText,
            },
            success: function(response) {
                $('.editable-text p').text(newText).show();
                $('.editable-text textarea').hide();
                $('.edit-btn').show();
                $('.submit-btn').hide();
            },
            error: function(xhr, errmsg, err) {
                console.error(xhr.status + ': ' + xhr.responseText);
            }
        });
    });
});
