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

var is_visiable_2 = false;

function see_2(){
    var input1 = document.getElementById("pass1");
    var input2 = document.getElementById("pass2");
    var eye = document.getElementById("eye");

    if(is_visiable_2){
        input1.type = 'password';
        input2.type = 'password';
        is_visiable_2 = false;
        eye.style.color = 'gray';
    }else{
        input1.type = 'text';
        input2.type = 'text';
        is_visiable_2 = true;
        eye.style.color = '#262626'
    }
}