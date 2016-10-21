/*************************************************************************
TripBuddy.sg (c) 2016. All rights reserved.
*************************************************************************/

function validateForm() {
    $('.form-empty').css('display', 'none');
    $('.form-invalid-title').css('display', 'none');
    $('.form-invalid-tagline').css('display', 'none');
    $('.form-invalid-date').css('display', 'none');
    $('.form-invalid-time').css('display', 'none');
    $('.form-invalid-group-size').css('display', 'none');
    $('.form-invalid-price').css('display', 'none');
    $('.form-invalid-checkbox').css('display', 'none');

    $('#title').removeClass('form-error');
    $('#tagline').removeClass('form-error');
    $('#overview').removeClass('form-error');
    $('#pic').removeClass('form-error');
    $('#itinerary').removeClass('form-error');
    $('#date').removeClass('form-error');
    $('#time_start').removeClass('form-error');
    $('#time_end').removeClass('form-error');
    $('#location').removeClass('form-error');
    $('#min_group').removeClass('form-error');
    $('#max_group').removeClass('form-error');
    $('#price').removeClass('form-error');
    $('[id=items]').removeClass('form-error');
    $('[id=includes]').removeClass('form-error');
    $('[id=excludes]').removeClass('form-error');
    $('#theme').removeClass('form-error');


    var title = document.forms["tripForm"]["title"].value;
    var tagline = document.forms["tripForm"]["tagline"].value;
    var overview = document.forms["tripForm"]["overview"].value;
    var pic = document.forms["tripForm"]["pic"].value;
    var itinerary = document.forms["tripForm"]["itinerary"].value;
    var date = document.forms["tripForm"]["date"].value;
    var time_start = document.forms["tripForm"]["time_start"].value;
    var time_end = document.forms["tripForm"]["time_end"].value;
    var location = document.forms["tripForm"]["location"].value;
    var min_group = document.forms["tripForm"]["min_group"].value;
    var max_group = document.forms["tripForm"]["max_group"].value;
    var price = document.forms["tripForm"]["price"].value;
    var items = $('#items').first().val();
    var includes = $('#includes').first().val();
    var excludes = $('#excludes').first().val();
    var theme = document.forms["tripForm"]["theme"].value;

    var valid = true;

    var today = new Date();


    if (title == null || title == "") {
        $('#title').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (tagline == null || tagline == "") {
        $('#tagline').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (overview == null || overview == "") {
        $('#overview').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (pic.length <= 0) {
        $('#pic').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (itinerary == null || itinerary == "") {
        $('#itinerary').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (date == null || date == "") {
        $('#date').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (time_start == null || time_start == "") {
        $('#time_start').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (time_end == null || time_end == "") {
        $('#time_end').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (location == null || location == "") {
        $('#location').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (min_group == null || min_group == "") {
        $('#min_group').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (max_group == null || max_group == "") {
        $('#max_group').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (price == null || price == "") {
        $('#price').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }
    
    if (items == null || items == "") {
        $('#items').first().addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (includes == null || includes == "") {
        $('#includes').first().addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (excludes == null || excludes == "") {
        $('#excludes').first().addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (theme == null || theme == "") {
        $('#theme').addClass('form-error');
        $('.form-empty').css('display', 'block');
        valid = false;
    }

    if (valid == true) {
        if (title.length > 30) {
            $('#title').addClass('form-error');
            $('.form-invalid-title').css('display', 'block');
            valid = false;
        }
        if (tagline.length > 100) {
            $('#tagline').addClass('form-error');
            $('.form-invalid-tagline').css('display', 'block');
            valid = false;
        }
        if (Date.parse(date) <= today) {
            $('#date').addClass('form-error');
            $('.form-invalid-date').css('display', 'block');
            valid = false;
        }
        if (time_start >= time_end) {
            $('#time_start').addClass('form-error');
            $('#time_end').addClass('form-error');
            $('.form-invalid-time').css('display', 'block');
            valid = false;
        }
        if (min_group > max_group) {
            $('#min_group').addClass('form-error');
            $('#max_group').addClass('form-error');
            $('.form-invalid-group-size').css('display', 'block');
            valid = false;
        }
        if (price > 500) {
            $('#price').addClass('form-error');
            $('.form-invalid-price').css('display', 'block');
            valid = false;
        }
        if ($('input[type=checkbox]:checked').length <= 0) {
            $('.form-invalid-checkbox').css('display', 'block');
            valid = false;
        }
    }

    if (valid == true) {
        $('.form-success').css('display', 'block');
    }

    return valid;
}