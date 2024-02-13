$(document).ready(function(){
    $(".nav-link").click(function(){
        event.preventDefault(); // 새로고침 방지

        $(".nav-link").removeClass("active");
        $(this).addClass("active");
    });
});

function showContent(contentId) {
    // 모든 content를 숨김
    document.querySelectorAll('.content').forEach(function(element) {
        element.style.display = 'none';
    });

    // 클릭한 탭에 해당하는 content를 보이게 함
    document.getElementById(contentId + 'Content').style.display = 'block';
}