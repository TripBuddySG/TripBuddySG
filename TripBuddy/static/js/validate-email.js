/*************************************************************************
TripBuddy.sg (c) 2016. All rights reserved.
*************************************************************************/

function validateForm() {
    $('.form-empty').css('display', 'none');
    $('.form-invalid-email').css('display', 'none');
    $('#email').removeClass('form-error');

    var email = document.forms["emailForm"]["email"].value;
    var email_atpos = email.indexOf("@");
    var email_dotpos = email.lastIndexOf(".");
    
    var valid = true;

    if (email == null || email == "") {
        $('#email').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (valid == true) {
        if (email_atpos < 1 || email_dotpos < email_atpos + 2 || email_dotpos + 2 >= email.length) {
            $('#email').addClass('form-error');
            $('.form-invalid-email').css('display', 'block');
            valid = false;
        }
    }
    
    if (valid == true) {
        $('.form-success').css('display', 'block');
    }
    
    return valid;
}