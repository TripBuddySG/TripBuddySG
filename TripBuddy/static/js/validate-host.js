/*************************************************************************
TripBuddy.sg (c) 2016. All rights reserved.
*************************************************************************/

function validateForm() {
    $('.form-empty').css('display', 'none');
    $('.form-invalid-email').css('display', 'none');
    $('#university').removeClass('form-error');
    $('#school').removeClass('form-error');
    $('#course').removeClass('form-error');
    $('#study_year').removeClass('form-error');
    $('#univ_email').removeClass('form-error');
    $('#univ_matric').removeClass('form-error');
    $('#tagline').removeClass('form-error');
    $('#descr').removeClass('form-error');

    var university = document.forms["editProfileForm"]["university"].value;
    var school = document.forms["editProfileForm"]["school"].value;
    var course = document.forms["editProfileForm"]["course"].value;
    var study_year = document.forms["editProfileForm"]["study_year"].value;
    var email = document.forms["editProfileForm"]["univ_email"].value;
    var email_atpos = email.indexOf("@");
    var email_dotpos = email.lastIndexOf(".");
    var matric = document.forms["editProfileForm"]["univ_matric"].value;
    var tagline = document.forms["editProfileForm"]["tagline"].value;
    var descr = document.forms["editProfileForm"]["descr"].value;
    var valid = true;


    if (university == null || university == "") {
        $('#university').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (school == null || school == "") {
        $('#school').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (course == null || course == "") {
        $('#course').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (study_year == null || study_year == "") {
        $('#study_year').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (email == null || email == "") {
        $('#univ_email').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (matric == null || matric == "") {
        $('#univ_matric').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (tagline == null || tagline == "") {
        $('#tagline').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (descr == null || descr == "") {
        $('#descr').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (valid == true) {
        if (email_atpos < 1 || email_dotpos < email_atpos + 2 || email_dotpos + 2 >= email.length) {
            $('#univ_email').addClass('form-error');
            $('.form-invalid-email').css('display', 'block');
            valid = false;
        }

        if (email.substr(email.length - 7) != ".edu.sg") {
            $('#univ_email').addClass('form-error');
            $('.form-invalid-email').css('display', 'block');
            valid = false;
        }
    }

    if (valid == true) {
        $('.form-success').css('display', 'block');
    }

    return valid;
}