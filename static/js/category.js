function categoryAddCheckFrom(){
    if($('#categoryName').val().length <= 0){
        alert('추가할 카테고리 이름을 입력해주세요.')
        $('#categoryName').focus()
        return false;
    }
    else{
        return true;
    }
}

function categoryFrom(){
    if ($('#resTitle').val().length <= 0){
        alert("카테고리 이름을 입력해주세요.")
        $('#resTitle').focus()
        return false
    }else{
        return true
    }
}