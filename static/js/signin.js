$(document).ready(function(){

    function showError(error){
        $('#error').html(String(error))
    }

    $('#submit').click(function(){
        var login = $('#login_text').val(),
            email = $('#email').val(),
            password = $('#password').val(),
            password2 = $('#password2').val();
        if(password === password2){

            if (login && email && password){
                $.post('sign-in', {'login': login, 'email': email, 'password': password}, function(data){

                    if (data.error){
                        showError(data.error)
                    }else{
                        window.location.href = '/'
                    }
                });
            }else{
                showError('Please fill all fields')
            }
        }else{
            showError('Passwords must be the same');
        }
        $('#password').val("");
        $('#password2').val("");
    });
});
