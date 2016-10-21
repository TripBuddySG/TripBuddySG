/*************************************************************************
TripBuddy.sg (c) 2016. All rights reserved.
*************************************************************************/

jQuery(document).ready(function () {
    jQuery('.legal-pills a').on('click', function (e) {
        var currentAttrValue = jQuery(this).attr('href');

        // Show & Hide Tabs:
        jQuery('.legal-content ' + currentAttrValue).show().siblings().hide();

        // Change .active Tab:
        jQuery('.legal-pills div li').removeClass('active');
        jQuery(this).parent('li').addClass('active');

        e.preventDefault();
    });
});