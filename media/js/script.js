// карусель
function mycarousel_initCallback(carousel) {
    $('.carousel_ctrls li').bind('click', function() {
        carousel.scroll(jQuery.jcarousel.intval($(this).index('.carousel_ctrls li')+1));
		$('.carousel_ctrls li').removeClass('curr');
        $(this).addClass('curr');
    });
}


$(function() {
	$('.carousel_ctrls li:first').addClass('curr');
    var params_dict = {
        scroll: 1,
        wrap: "both",
        visible: 1,
        start:1,
        auto: 6,
        initCallback: mycarousel_initCallback,
        itemVisibleInCallback: {
            onAfterAnimation: mycarousel_itemVisibleInCallbackAfterAnimation
        }
    };

	jQuery('.carousel_actions').jcarousel(params_dict);
	jQuery('.carousel_daily').jcarousel(params_dict);
	jQuery('.carousel_hit').jcarousel(params_dict);
	jQuery('.carousel_new').jcarousel(params_dict);
	jQuery('.carousel_unique').jcarousel(params_dict);

    $('.jcarousel-container').hide();
    $('.jcarousel-container').eq(2).show();

	function mycarousel_itemVisibleInCallbackAfterAnimation(carousel, item, idx, state) {
        $('.carousel_ctrls li').removeClass('curr');
		$($('.carousel_ctrls li').get(idx - 1)).addClass('curr');
	}

    $('div.carousel_filter a').live('click',function(){
        $(this).parents('ul').find('li').removeClass('curr');
        $(this).parent().addClass('curr');
        var slider_type = $(this).attr('name');
        var target = $('ul.'+slider_type);
        $('.jcarousel-container').hide();
        target.parents('.jcarousel-container').show();
        var content = ''
        for (var i=1;i<=target.find('li').length;i++){
            content += '<li></li>';
        }
        $('.carousel_ctrls').html(content);
        $('.carousel_ctrls li:first').addClass('curr');

        target.jcarousel('reload');
        return false;
    });
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
            var val = $(this).slider( "option", "value" );
            var exist = false;
            var curr_send_link = $('input.curr_send_link').val();

            if (curr_send_link=='#') {
                window.location = '?price_filter='+val;
            } else {
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
                window.location = curr_send_link;
            }

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
       } , 2000);
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

    $('div.item_specs').live('click',function(){
        $(this).parent().find('.item_gift_blob').toggle();
    });

    $('.product_gal li').live('click',function(){
        var el = $(this);
        var link = el.find('div.replace_img a').clone();
        var rel = $('.product_gal a').attr('rel');
        el.parent().find('a').attr('rel',rel);
        el.find('div.replace_img a').removeAttr('rel');
        el.parent().find('li').removeClass('curr');
        el.toggleClass('curr');
        link.attr('rel',rel);
        $('.product_img a').replaceWith(link);
        $('.product_gal').append('<script type="text/javascript">$(".fancybox").fancybox()</script>');
        return false;
    });

    $('div.pagemenu a').live('click',function(){
        $(this).parents('ul').find('li').removeClass('curr');
        var type = $(this).attr('name');
        $(this).parent().addClass('curr');
        $('div.product_des .text').hide();
        $('div.product_des .'+type).show();
        return false;
    });




    //Анимация корзины при изменении
    function animate_cart(){
        $('.cartbox').animate({
                opacity: 0.25
            }, 200, function() {
                $(this).animate({
                    opacity: 1
                },200);
            }
        );
    }

    function create_img_fly(el)
    {
        var img = el.html();
        var offset = el.find('img').offset();
        element = "<div class='img_fly'>"+img+"</div>";
        $('body').append(element);
        $('.img_fly').css({
            'position': "absolute",
            'z-index': "1000",
            'left': offset.left,
            'top': offset.top
        });

    }

    //Добавление товара в корзину

    $('.buy_btn').live('click',function(){
        var product_id = $(this).attr('name')
        var parent_blk = $(this).parents('.product')

        if (product_id){
            $.ajax({
                type:'post',
                url:'/add_product_to_cart/',
                data:{
                    'product_id':product_id
                },
                success:function(data){
                    $('.img_fly').remove();
                    create_img_fly(parent_blk.find('.product_img'));

                    $('.cartbox').replaceWith(data);

                    var fly = $('.img_fly');
                    var left_end = $('.cartbox').offset().left;
                    var top_end = $('.cartbox').offset().top;

                    fly.animate(
                        {
                            left: left_end,
                            top: top_end
                        },
                        {
                            queue: false,
                            duration: 600,
                            easing: "swing"
                        }
                    ).fadeOut(600);

                    setTimeout(function(){
                        animate_cart();
                    } ,600);

                },
                error:function(jqXHR,textStatus,errorThrown){

                }
            });
        }

    });

});

