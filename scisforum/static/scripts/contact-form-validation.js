$('#contact_form').submit(function(){
    let email = $('#email').val();
    let msg = $('#message').val();
    let flag=0;
    if(msg === ''){
      $('#message_error_block').html('Enter the message');
      flag += 1;
    }else{
      $('message_error_block').html('');
    }
    let pattern = /^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$/;
    if(!email.match(pattern)){
      $('#email_error_block').html('Enter valid email');
      flag += 1;
    }else{
      $('#email_error_block').html('');
    }
    if(flag > 0){
      return false;
    }
});