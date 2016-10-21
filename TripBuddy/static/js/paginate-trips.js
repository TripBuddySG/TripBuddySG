/*************************************************************************
TripBuddy.sg (c) 2016. All rights reserved.
*************************************************************************/

$(document).ready(function () {
    var show_per_page = 6; // items to show per page
    var number_of_items = $('#trips-grid').find('.trip-grid-link').size(); // total number of items
    var number_of_pages = Math.ceil(number_of_items / show_per_page); // total number of pages

    // Set the value of hidden input fields:
    $('#current_page').val(0);
    $('#show_per_page').val(show_per_page);


    // Creating the navigation buttons:
    var navigation_html = '<ul class="pagination pagination-lg">';
    var current_link = 0;
    while (number_of_pages > current_link) {
        navigation_html += '<li longdesc="' + current_link + '"><a class="page-link" href="javascript:go_to_page(' + current_link + ')">' + (current_link + 1) + '</a></li>';
        current_link = current_link + 1;
    }
    navigation_html += '</ul>';

    $('#trip_page_nav').html(navigation_html);

    // Add "active" class to first page link:
    $('#trip_page_nav li:first').addClass('active');


    // Hide all elements inside grid:
    $('#trips-grid').children().css('display', 'none');

    // Show the first n (show_per_page) elements:
    $('#trips-grid').children().slice(0, show_per_page).css('display', 'block');
});

function go_to_page(page_num) {
    // Get the number of items shown per page:
    var show_per_page = parseInt($('#show_per_page').val(), 10);

    // Get element numbers for slice:
    var start_from = page_num * show_per_page;
    var end_on = start_from + show_per_page;

    // Hide all the children elements of .trips-grid and then show the specific slice:
    $('#trips-grid').children().css('display', 'none').slice(start_from, end_on).css('display', 'block');

    // Update the .active page:
    $('li[longdesc=' + page_num + ']').addClass('active').siblings('.active').removeClass('active');

    // Update the current page input field:
    $('#current_page').val(page_num);

    scroll_to_start();
}

function scroll_to_start() {
    $(document).scrollTop($("#trips-grid").offset().top);
}