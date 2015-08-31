"use strict";

(function initHeader($){
    $(document).ready(function(){
        var $subMenuItems = $('#top .container > div > ul > li');
        $subMenuItems.hover(function(){
            var $this = $(this);
            var $links = $this.children('a');
            if (!$links.hasClass('selected')) {
                $links.addClass('selected');
            }

            var $sub = $this.find('.sub');
            if ($sub.length) {
                $this.find('.sub').show();
            }
        }, function(){
            var $this = $(this);
            var $links = $this.children('a');
            if ($links.hasClass('selected')) {
                $links.removeClass('selected');
            }
            if ($this.find('.sub').length) {
                $this.find('.sub').hide();
            }
        });

        $('.navbar-nav .global').on('click', function(event){
            var $languagePanel =  $('.language-panel', $(this));
            $languagePanel.toggleClass('invisible');

            var $userInfo =  $('.user-info .dropdown');

            if(!$userInfo.hasClass('invisible')){
                $userInfo.addClass('invisible');
            }

            event.stopPropagation();
        });
       var url = window.location.pathname + window.location.search;
       console.log(url);
       if(url == '/' || url.substr(0,20) == '/bbs' || url == '/') {
           $('#mn_Nfaed').addClass('current');
           $('#mn_Nfaed > a').addClass('current');
       } else if (url == '/forum.php?gid=3') {
           $('#mn_N7cd3').addClass('current');
           $('#mn_N7cd3 > a').addClass('current');

       } else if (url == '/forum.php?gid=51') {
           $('#mn_Ne402').addClass('current');
           $('#mn_Ne402 > a').addClass('current');

       } else if (url == '/forum.php') {
           $('#mn_forum').addClass('current');
           $('#mn_forum > a').addClass('current');

       }

        $('.user-menu .arrow-down').on('click', function(event){
            var $userInfo =  $('.user-info .dropdown');
            $userInfo.toggleClass('invisible');


            var $languagePanel =  $('.navbar-nav .global .language-panel');

            if(!$languagePanel.hasClass('invisible')){
                $languagePanel.addClass('invisible');
            }

            event.stopPropagation();
        });

        //var $userInfo =  $('.user-info .dropdown');
        //
        //$('.user-menu').hover(function() {
        //    $userInfo.show();
        //}, function() {
        //    $userInfo.hide();
        //});


        $('.navbar-nav .search .search-button').on('click', function(event){
            var $this = $(this);

            var $languagePanel = $('.navbar-nav .global .language-panel');

            if(!$languagePanel.hasClass('invisible')) {
                $languagePanel.addClass('invisible');
            }

            var $search = $('.navbar-nav .search input');
            var $button = $('#scbar_btn');
            $this.hide();
            $search.show();
            $button.show();
            $("#top > div > div > div.collapse.navbar-collapse.bs-navbar-collapse > div > div.user-info.left > a").hide();
            event.stopPropagation();

        });


        $('.navbar-nav .search input').on('click', function(){
            return false;
        });

/*
        var $weixinPop = $('.weixin-pop');
        var $weixin = $('.weixin');

        $weixin.bind('click', function(event){
            event.preventDefault();
            $weixinPop.toggle({display: 'none'});
        });
*/

        var $maskLayer = $('.mask-layer');

        function showMaskLayer(show) {
            if (show === true) {
                $maskLayer.css({
                    display: 'block',
                    width: $(document).width(),
                    height: $(document).height()
                });
            }
            else {
                $maskLayer.css({display: 'none'});
            }
        }

        function showWindow(window, show) {
            var $window = $('.window' + '.' + window);
            if (show === true) {
                $window.css({
                    display: 'block',
                    left: ($(document).width() - $window.width()) / 2
                });
            }
            else {
                $window.css({
                    display: 'none'
                });
            }
        }

        $('.social > a.pop').on('click', function () {
            var $this = $(this);
            var buttonName = $this.attr('class').split(' ')[0];
            if (buttonName !== 'weibo') {
                showMaskLayer(true);
                showWindow(buttonName, true);
            }
        });

        $('.window .close').on('click', function () {
            showWindow($(this).parent('.window').attr('class').split(' ')[1], false);
            showMaskLayer(false);
        });

        $maskLayer.on('click', function () {
            $('.window').each(function () {
                var $this = $(this);
                if ($this.css('display') !== 'none') {
                    $this.css({
                        display: 'none'
                    });
                }
            });
            $('.video-frame').css({display: 'none'});
            showMaskLayer(false);
        });


        $(document.body).on('click', function(){
            var $languagePanel = $('.language-panel');
            var $searchButton = $('.navbar-nav .search .search-button');
            var $searchInput = $('.navbar-nav .search input');

            if(!$languagePanel.hasClass('invisible')) {
                $languagePanel.addClass('invisible');
            }

            if($searchButton.hasClass('clicked')){
                $searchButton.removeClass('clicked');
            }

            var $userInfo =  $('.user-info .dropdown');

            if(!$userInfo.hasClass('invisible')){
                $userInfo.addClass('invisible');
            }

            $searchInput.hide();
            $('#scbar_btn').hide();
            $('.navbar-nav .search .search-button').show();
            $("#top > div > div > div.collapse.navbar-collapse.bs-navbar-collapse > div > div.user-info.left > a").show();

        });

        if($(document.body).height() < $(window).height()) {
            $('#wp').height($(window).height() - $('#ft').outerHeight() - $('#hd').outerHeight());
        }

        $("#top > div > div > div.collapse.navbar-collapse.bs-navbar-collapse > ul > li:nth-child(1) > a").addClass('currentx');

        //if((window.location.href).indexOf('bbs')!=-1){
        //    $('#top > div > div > div.collapse.navbar-collapse.bs-navbar-collapse > ul > li > a').addClass('currentx');
        //
        //}
        $('.nvhm').html('');

    });
})(jQuery);

