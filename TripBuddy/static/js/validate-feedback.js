/*************************************************************************
TripBuddy.sg (c) 2016. All rights reserved.
*************************************************************************/

function validateForm() {
    $('.form-empty').css('display', 'none');
    $('.form-invalid-email').css('display', 'none');
    $('#name').removeClass('form-error');
    $('#email').removeClass('form-error');
    $('#feedback').removeClass('form-error');

    var name = document.forms["feedbackForm"]["name"].value;
    var email = document.forms["feedbackForm"]["email"].value;
    var email_atpos = email.indexOf("@");
    var email_dotpos = email.lastIndexOf(".");
    var feedback = document.forms["feedbackForm"]["feedback"].value;
    var valid = true;

    if (name == null || name == "") {
        $('#name').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (email == null || email == "") {
        $('#email').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (feedback == null || feedback == "") {
        $('#feedback').addClass('form-error');
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