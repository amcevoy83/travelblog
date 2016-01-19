$(document).ready(function() {

  $('.imagegallery').hide();
  $('.imagegallery').fadeIn(400);
$('.blogcontent').fadeIn('slow');

    //Image gallery//
        $(".thumb").mouseover(function(){
            $(this).addClass("gal_hover");
        });
        $(".thumb").mouseout(function(){
            $(this).removeClass("gal_hover");
        });

        $(".galImg").click(function() {
            var image = $(this).attr("rel");
            $('#feature').fadeOut('fast');
            $('#feature').fadeIn('slow');
            $('#feature').html('<img src="' + image + '"/>');

        })

//intro page
     if ($.cookie('noShowHerobar')) {
         $('.herobar').hide();
         $('.fader').each(function () {
             $(this).fadeIn(Math.random() * 3500);
         })
         setTimeout($('.hometopbar').slideDown(600) , 800);
     }
    else {
        $("#button").click(function() {
            $(".herobar").fadeOut(1000);
            //$('.hometopbar').slideDown(600);
            $.cookie('noShowHerobar', true);
             $('.fader').each(function () {
                $(this).fadeIn(Math.random()*3500);
                    });
        });
    }

    //$('#button').on("click", function(){
   	//		$('.herobar').slideUp(500);
    //
    //        $('.fader').each(function () {
    //            $(this).fadeIn(Math.random()*3500);
    //                });
    //})
    //navigation

    $("#activatenav").click(function() {
            $('nav').slideToggle(200)
        $('nav').addClass('mobilenav');
        });

    })


