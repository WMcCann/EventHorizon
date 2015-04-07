var services_add = function () {
    var current = location.pathname;
    if(current.match('^/admin/services_social/facebookconnection/add/.*')){
        self.location = '/services/social/facebook-connection/add/';
    }

    if(current.match('^/admin/services_social/twitterconnection/add/.*')){
        self.location = '/services/social/twitter-connection/add/';
    }

    if(current.match('^/admin/services_social/youtubeconnection/add/.*')){
        self.location = '/services/social/youtube-connection/add/';
    }

    if(current.match('^/admin/social/analyticsyoutubechannel/add/.*')){
        self.location = '/social/analytics/youtube-channel/add/';
    }

    if(current.match('^/admin/services_media/adwordsconnection/add/.*')){
        self.location = '/services/media/adwords-connection/add/';
    }
};

jQuery(function(){
	services_add();
});