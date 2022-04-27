function ReplyComment(pk){
    let value = document.getElementById(pk);
    if (value.classList.contains('d-none')){
        value.classList.remove('d-none');
    }
    else {
        value.classList.add('d-none');
    }
}

function Show(child){
    let value = document.getElementsByClassName(child)[0];
    if (value.classList.contains('d-none')){
        value.classList.remove('d-none');
    }
    else {
        value.classList.add('d-none');
    }

}
