jQuery(document).ready(function($){

    $(window).scroll(function(){
        $('.bd-navbar').toggleClass('scrollednav', $(this).scrollTop() > 50);
        });

    //object cover fix for stupid internet explorer
    if (document.documentMode || /Edge/.test(navigator.userAgent)) {
      jQuery('.cardthumb').each(function(){
          var t = jQuery(this),
              s = 'url(' + t.attr('src') + ')',
              p = t.parent(),
              d = jQuery('<div></div>');
  
          p.append(d);
          d.css({
              'height'                : '197',
              'background-size'       : 'cover',
              'background-repeat'     : 'no-repeat',
              'background-position'   : '50% 20%',
              'background-image'      : s
          });
          t.hide();
      });
    }

    if (document.documentMode || /Edge/.test(navigator.userAgent)) {
      jQuery('.featuredthumb').each(function(){
        var t = jQuery(this),
            s = 'url(' + t.attr('src') + ')',
            p = t.parent(),
            d = jQuery('<div></div>');

        p.append(d);
        d.css({
            'height'                : '86',
            'width'                 : '86',
            'background-size'       : 'cover',
            'dispalay'              : 'inline-block',
            'background-repeat'     : 'no-repeat',
            'background-position'   : '50% 20%',
            'background-image'      : s
        });
        t.hide();
    });
  }
    

    // alertbar later
    $('#alertbar').delay(2000).fadeTo("800", 1);

    $(".closealert").click(function(){
    $(".alertbar").removeClass("active");
    });


    // Smooth on external page
    $(function() {
      setTimeout(function() {
        if (location.hash) {
          /* we need to scroll to the top of the window first, because the browser will always jump to the anchor first before JavaScript is ready, thanks Stack Overflow: http://stackoverflow.com/a/3659116 */
          window.scrollTo(0, 0);
          target = location.hash.split('#');
          smoothScrollTo($('#'+target[1]));
        }
      }, 1);

      // taken from: https://css-tricks.com/snippets/jquery/smooth-scrolling/
      $('a[href*=\\#]:not([href=\\#])').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
          smoothScrollTo($(this.hash));
          return false;
        }
      });

      function smoothScrollTo(target) {
        target = target.length ? target : $('[name=' + this.hash.slice(1) +']');

        if (target.length) {
          $('html,body').animate({
            scrollTop: target.offset().top - 100
          }, 1000);
        }
      }
    });

    // footnotes
    $.bigfoot();
    
    $(function()  {

      // get's all video wrapper divs
      var youtube = document.querySelectorAll(".youtube");

      // iterates through all the divs
      for (var i = 0; i < youtube.length; i++) {

        /* 
        gets the video id we mentioned in the data-embed attribute
        to generate image thumbnail urls, youtube has several
        resolutions.
        - mqdefault 320 x 180
        - hqdefault 480 x 360
        - sddefault - 640 x 480
        - maxresdefault - 1920 x 1080
        */
        var source = "https://img.youtube.com/vi/" + youtube[i].dataset.embed + "/sddefault.jpg";

        /*
        creates new image and sets the source attribute to the thumbnail
        url we generated above and sets it to load the image on page load
        */
        var image = new Image();
        image.src = source;
        image.addEventListener("load", function() {
          youtube[i].appendChild(image);
        }(i));

        /*
        below is where the magic happens, we attach click listeners to the 
        video embed divs and when clicked we create a new iframe and sets
        it inside the video wrapper div and only then will the js files
        associated with the embedded video be loaded
        */

        youtube[i].addEventListener("click", function() {

          var iframe = document.createElement("iframe");

          iframe.setAttribute("frameborder", "0");
          iframe.setAttribute("allowfullscreen", "");
          iframe.setAttribute("src", "https://www.youtube.com/embed/" + this.dataset.embed + "?rel=0&showinfo=0&autoplay=1");

          this.innerHTML = "";
          this.appendChild(iframe);
        });
      };  
    });//youtube lazy loading
       
 });   



 /*global jQuery */
/*jshint multistr:true browser:true */
/*!
* FitVids 1.0.3
*
* Copyright 2013, Chris Coyier - http://css-tricks.com + Dave Rupert - http://daverupert.com
* Credit to Thierry Koblentz - http://www.alistapart.com/articles/creating-intrinsic-ratios-for-video/
* Released under the WTFPL license - http://sam.zoy.org/wtfpl/
*
* Date: Thu Sept 01 18:00:00 2011 -0500
*/

(function( $ ){

  "use strict";

  $.fn.fitVids = function( options ) {
    var settings = {
      customSelector: null
    };

    if(!document.getElementById('fit-vids-style')) {

      var div = document.createElement('div'),
          ref = document.getElementsByTagName('base')[0] || document.getElementsByTagName('script')[0],
          cssStyles = '&shy;<style>.fluid-width-video-wrapper{width:100%;position:relative;padding:0;}.fluid-width-video-wrapper iframe,.fluid-width-video-wrapper object,.fluid-width-video-wrapper embed {position:absolute;top:0;left:0;width:100%;height:100%;}</style>';

      div.className = 'fit-vids-style';
      div.id = 'fit-vids-style';
      div.style.display = 'none';
      div.innerHTML = cssStyles;

      ref.parentNode.insertBefore(div,ref);

    }

    if ( options ) {
      $.extend( settings, options );
    }

    return this.each(function(){
      var selectors = [
        "iframe[src*='player.vimeo.com']",
        "iframe[src*='youtube.com']",
        "iframe[src*='youtube-nocookie.com']",
        "iframe[src*='kickstarter.com'][src*='video.html']",
        "object",
        "embed"
      ];

      if (settings.customSelector) {
        selectors.push(settings.customSelector);
      }

      var $allVideos = $(this).find(selectors.join(','));
      $allVideos = $allVideos.not("object object"); // SwfObj conflict patch

      $allVideos.each(function(){
        var $this = $(this);
        if (this.tagName.toLowerCase() === 'embed' && $this.parent('object').length || $this.parent('.fluid-width-video-wrapper').length) { return; }
        var height = ( this.tagName.toLowerCase() === 'object' || ($this.attr('height') && !isNaN(parseInt($this.attr('height'), 10))) ) ? parseInt($this.attr('height'), 10) : $this.height(),
            width = !isNaN(parseInt($this.attr('width'), 10)) ? parseInt($this.attr('width'), 10) : $this.width(),
            aspectRatio = height / width;
        if(!$this.attr('id')){
          var videoID = 'fitvid' + Math.floor(Math.random()*999999);
          $this.attr('id', videoID);
        }
        $this.wrap('<div class="fluid-width-video-wrapper"></div>').parent('.fluid-width-video-wrapper').css('padding-top', (aspectRatio * 100)+"%");
        $this.removeAttr('height').removeAttr('width');
      });
    });
  };
// Works with either jQuery or Zepto
})( window.jQuery || window.Zepto );

// Wrap and make Videos responsive
$("iframe").wrap("<div class='content_vid'/>");

$(document).ready(function(){
  
  $(".content_vid").fitVids();

});


