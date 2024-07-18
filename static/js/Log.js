var is_visiable = false;

function see(){
    var input = document.getElementById("password");
    var eye = document.getElementById("eye");

    if(is_visiable){
        input.type = 'password';
        is_visiable = false;
        eye.style.color = 'gray';
    }else{
        input.type = 'text';
        is_visiable = true;
        eye.style.color = '#262626'
    }
}