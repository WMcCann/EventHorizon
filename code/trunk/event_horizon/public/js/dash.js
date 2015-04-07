jQuery(function(){
    var current = location.pathname;
    if(current.match('^/dashboard/[0-9]+$')){
        jQuery('#menu-dashboard').addClass('active');
    }
});