// карусель
function mycarousel_initCallback(carousel) {
    $('.carousel_ctrls li').bind('click', function() {
        carousel.scroll(jQuery.jcarousel.intval($(this).index('.carousel_ctrls li')+1));
		$('.carousel_ctrls li').removeClass('curr');
        $(this).addClass('curr');
    });
};
$(function() {
	$('.carousel_ctrls li:first').addClass('curr');
	jQuery('.carousels').jcarousel({
        scroll: 1,
        wrap: "both",
		visible: 1,
		initCallback: mycarousel_initCallback,
        itemVisibleInCallback: {
            onAfterAnimation: mycarousel_itemVisibleInCallbackAfterAnimation
        }
	});
		
	function mycarousel_itemVisibleInCallbackAfterAnimation(carousel, item, idx, state) {
		$('.carousel_ctrls li').removeClass('curr');
		$($('.carousel_ctrls li').get(idx - 1)).addClass('curr');
	};
});



// плашка брендов
$(function() {
	$(".brands_btn").click(function() {
		$(this).toggleClass("brands_btn_curr");
		$(".brands_list").toggle();
		return false;
	});
	$(".brands_shade_t, .brands_shade_b, .brands_shade_lr").click(function() {
		$(".brands_list").hide();
		return false;
	});
});
$(document).click(function(e) {
	if ($(e.target).parents().filter('.brands_list:visible').length != 1)
	$('.brands_list').hide();
});




// фильтр цены
function SetPriceSlider(min, max, start)
{
    $( "#filter_price" ).slider({
		range: "min",
		value: start,
		min: min,
		max: max,
		slide: function( event, ui ) {
            $( ".filter_price_inpt" ).val( ui.value );
		},
        stop: function( event, ui ) {
/*            var val = $(this).slider( "option", "value" )
            var exist = false
            var curr_send_link = $('a.filter_submit_btn').attr('href')
            if (curr_send_link=='#')
                {$('a.filter_submit_btn').attr('href','?price_filter='+val)}
            else
                {
                    var get_param_array = curr_send_link.split('&');
                    length = get_param_array.length
                    for (var i = 0; i <= length-1; i++)
                        {
                            part = get_param_array[i].split('=')
                            if (part[0].substring(0, 1) == "?")
                                {
                                    part[0] = part[0].substring(1)
                                }
                            if (part[0]=='price_filter')
                                {
                                    exist = true
                                    part[1]=val
                                }
                            get_param_array[i] = part.join('=')
                        }
                    if (!exist)
                        {get_param_array.push('price_filter='+val);}
                    var curr_send_link = get_param_array.join('&')
                    if (curr_send_link != "?")
                        {
                            curr_send_link = '?' + curr_send_link
                        }
                    $('a.filter_submit_btn').attr('href',curr_send_link)
                }*/

        }
	});
	$( ".filter_price_inpt" ).val( start );
}


// выпадашка фильтров
$(function() {
	$(".select_label").click(function() {
		$(".select").removeClass("select_curr");
		$(this).parent().toggleClass("select_curr");
		return false;
	});
	$(".select_drop_h").click(function() {
		$(".select").removeClass("select_curr");
	});
});
$(document).click(function(e) {
	if ($(e.target).parents().filter('.select_drop:visible').length != 1)
		$(".select").removeClass("select_curr");
});


$(function() {
    $('.fancybox').fancybox();

    var myTimer = 0

    function HideMenu(){
      clearTimeout(myTimer);
       myTimer = setTimeout( function(){
           $(".submenu").hide();
           $('.menu_arr').hide();
           menu_opened = false;
           console.log('123');
       } , 7000);
    }

    var menu_opened = false;

    $('div.menu a').live('hover',function(){
        clearTimeout(myTimer);
        $(this).parents('ul').find('li').removeClass('curr');
        $(this).parent().toggleClass('curr');
        if (menu_opened){
            $(".submenu").hide();
            $('.menu_arr').hide();
            menu_opened = false;
        }
        var id = $(this).attr('name');
        $(this).parent().find('.menu_arr').show();
        $(".smenu_"+id).show()
        menu_opened = true;
    });

    $('div.menu a').live('mouseleave',function(){
        HideMenu();
    });

    $('div.submenu_content').live('mouseover',function(){
        clearTimeout(myTimer);
    });

    $('div.submenu_content').live('mouseleave', function() {
        $(".submenu").hide();
        $('.menu_arr').hide();
        menu_opened = false;
        clearTimeout(myTimer);
    });

    // карусель
    $('div.carousel_filter a').live('click',function(){
        $(this).parents('ul').find('li').removeClass('curr');
        $(this).parent().addClass('curr');

        return false;
    });

    $('div.item_specs').live('click',function(){
        $(this).parent().find('.item_gift_blob').toggle();
    });

});

