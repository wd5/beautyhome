// карусель
function mycarousel_initCallback(carousel) {
    //$('.carousel_ctrls li').bind('click', function() {
    $('.carousel_ctrls li').live('click',function(){
        carousel.scroll(jQuery.jcarousel.intval($(this).index('.carousel_ctrls li')+1));
		$('.carousel_ctrls li').removeClass('curr');
        $(this).addClass('curr');
    });
}

$(function() {
    if ($('.carousel_actions').html()) { // если нашли элемент - то делаем карусели
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

        $('.carousel_actions').jcarousel('stopAuto');
        $('.carousel_daily').jcarousel('stopAuto');
        $('.carousel_hit').jcarousel('stopAuto');
        $('.carousel_new').jcarousel('stopAuto');
        $('.carousel_unique').jcarousel('stopAuto');

        $('.jcarousel-container').hide();
        $('.jcarousel-container').eq(2).show();
        $('.jcarousel-container').eq(2).find('.jcarousel-list').jcarousel('startAuto');
        var cont = '';
        for (var i=1;i<=$('.jcarousel-container').eq(2).find('li').length;i++){
            cont += '<li></li>';
        }
        $('.carousel_ctrls').html(cont);
        $('.carousel_ctrls li:first').addClass('curr');

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

            $('.carousel_actions').jcarousel('stopAuto');
            $('.carousel_daily').jcarousel('stopAuto');
            $('.carousel_hit').jcarousel('stopAuto');
            $('.carousel_new').jcarousel('stopAuto');
            $('.carousel_unique').jcarousel('stopAuto');

            target.jcarousel('reload');
            target.jcarousel('scroll',0);
            target.jcarousel('startAuto');
            return false;
        });
    }
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

    $('div.product div.pagemenu a').live('click',function(){
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

    function animate_later_cart(){
        $('.cart_later').animate({
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

    // кабинет
    $('div.personal input,select').live('change',function(){
        if ($(this).attr('type') == 'checkbox'){
            ChangePersonalInfo($(this).attr('name'),$(this).attr('checked'));
        } else {
            ChangePersonalInfo($(this).attr('name'),$(this).attr('value'));
        }
    });

    $('div.personal input').live('keypress',function(e){
        /*if(e.which == 13)
            $(this).change();*/
    });

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

    $('.cart_qty_btn').live('click',function(){
        $('.cart_qty_btn').attr('disabled', true);
        $(this).attr('disabled', false);
        $(this).parents('.cart_qty').find('.cart_qty_modal').show();
        $(this).parents('.cart_qty').find('.cart_qty_modal').find('.cart_qty_modal_ok').attr('disabled', false);
        $('.cart_submit_btn').attr('disabled', true);
        $('.cart_back').attr('disabled', true);
        $('.delete_cart_id').attr('disabled', true);
    });

    $('.cart_qty_modal_text').live('keypress',function(e){
        if(e.which == 13)
            $('.cart_qty_modal_ok').trigger("click");
        else
        if( e.which!=8 && e.which!=0 && (e.which<48 || e.which>57))
        {
            alert("Только цифры");
            return false;
        }
    });

    //Подсчёт стоимости
    $('.cart_qty_modal_text').live('keyup',function(){
        var el = $(this)
        var count = el.val();
        if (count){
            count = parseInt(count);
            if (count==0){
                $('.cart_qty_modal_text').val('1');
                count = 1;
            }
            if (count > 999){
                $('.cart_qty_modal_text').val('999');
                count = 999;
            }

            var product_price = el.parent().find('.cart_qty_price span').html();

            product_price = parseFloat(product_price);
            var sum = product_price*count;
            if ((sum % 1)==0){
                sum = sum.toFixed(0);
            }
            else{
                sum = sum.toFixed(2);
            }
            el.parent().find('.cart_qty_total_price span').text(sum);
        }
    });

        //Кнопка Созранить в изменении количества в корзине
    $('.cart_qty_modal_ok').live('click', function(){
        var el = $(this);
        var parent = el.parents('.cart_qty_modal');
        var cart_item = el.parents('.cart_item');
        var initial_count = parent.find('.initial_count').val();
        var new_count = parent.find('.cart_qty_modal_text').val();
        var cart_product_id = parent.find('.cart_qty_item_id').val();

        if (new_count && cart_product_id && initial_count){
            if (new_count != initial_count){
                $.ajax({
                    type:'post',
                    url:'/change_cart_product_count/',
                    data:{
                        'cart_product_id':cart_product_id,
                        'new_count':new_count
                    },
                    success:function(data){
                        data = eval('(' + data + ')');
                        cart_item.find('.cart_price>.item_price').html(data.tr_str_total+' <i>руб.</i>');
                        cart_item.find('.cart_qty_btn').html(new_count);
                        parent.find('.initial_count').val(new_count);
                        parent.find('.cart_qty_modal_text').val(new_count);
                        parent.find('.cart_qty_total_price span').text(data.tr_str_total);
                        $('.cart_summary .cart_total span').html(data.cart_str_total);
                        if (data.cart_str_total=='0')
                            {$('.cart_submit_btn').attr('disabled', true);}
                        else
                            {$('.cart_submit_btn').attr('disabled', false);}
                        $('.cart_qty_btn').attr('disabled', false);
                        $('.cart_back').attr('disabled', false);
                        parent.hide();
                        getCartboxHtml();
                    },
                    error:function(data){
                        $('.cart_submit_btn').attr('disabled', false);
                        $('.cart_qty_btn').attr('disabled', false);
                        $('.cart_back').attr('disabled', false);
                    }
                });
            }

        }
        $('.cart_submit_btn').attr('disabled', false);
        return false;

    });

    $('.cart_qty_modal_cancel').live('click', function(){
        var el = $(this)
        var parent = el.parents('.cart_qty_modal')
        parent.hide();
        parent.find('.cart_qty_modal_ok').attr('disabled', true);
        $('.cart_submit_btn').attr('disabled', false);
        $('.cart_qty_btn').attr('disabled', false);
        $('.delete_cart_id').attr('disabled', false);
        $('.cart_back').attr('disabled', false);
    });

    $('.delete_cart_id').live('click', function(){
        var el = $(this);
        var cart_product_id = el.attr('name');
        var parent = el.parents('.cart_item');
        if (cart_product_id){
            $.ajax({
                type:'post',
                url:'/delete_product_from_cart/',
                data:{
                    'cart_product_id':cart_product_id
                },
                success:function(data){
                    data = eval('(' + data + ')');
                    $('.cart_summary .cart_total span').html(data.cart_total);
                    if (data.cart_total=='0')
                        {$('.cart_submit_btn').attr('disabled', true);}
                    else
                        {$('.cart_submit_btn').attr('disabled', false);}
                    parent.append('<div class="cart_item_deleted"><a class="cart_back" name="'+data.cart_product_id+'" href="#">Вернуть</a></div>')
                },
                error:function(data){
                }
            });
        }
        return false;
    });

    $('.cart_back').live('click', function(){
        var el = $(this);
        var cart_product_id = el.attr('name');
        var parent = el.parents('.cart_item');
        if (cart_product_id){
            $.ajax({
                type:'post',
                url:'/restore_product_to_cart/',
                data:{
                    'cart_product_id':cart_product_id
                },
                success:function(data){
                    data = eval('(' + data + ')');
                    $('.cart_summary .cart_total span').html(data.cart_total);
                    if (data.cart_total=='0')
                        {$('.cart_submit_btn').attr('disabled', true);}
                    else
                        {$('.cart_submit_btn').attr('disabled', false);}
                    parent.find('.cart_item_deleted').remove()
                },
                error:function(data){
                }
            });
        }
        return false;
    });

    $('.later_cart_id').live('click', function(){
        var el = $(this);
        var cart_product_id = el.attr('name');
        var parent = el.parents('.cart_item');
        if (cart_product_id){
            $.ajax({
                type:'post',
                url:'/set_product_later_from_cart/',
                data:{
                    'cart_product_id':cart_product_id
                },
                success:function(data){
                    data = eval('(' + data + ')');
                    $('.cart_summary .cart_total span').html(data.cart_str_total);
                    if (data.cart_str_total=='0')
                        {$('.cart_submit_btn').attr('disabled', true);
                        $('.cart_in').remove();
                        $('.cart h1').html('Ваша косметичка пока пуста');}
                    else
                        {$('.cart_submit_btn').attr('disabled', false);}
                    parent.remove();
                    // вытащим later_cart и вставим в cart
                    getLaterCartHtml();
                    getCartboxHtml();
                    setTimeout(function(){
                        animate_later_cart();
                        animate_cart();
                    } ,600);

                },
                error:function(data){
                }
            });
        }
        return false;
    });

    $('.later_buy_now').live('click',function(){
        var product_id = $(this).attr('name')
        var parent_blk = $(this).parents('.later_item')

        if (product_id){
            $.ajax({
                type:'post',
                url:'/add_product_to_cart/',
                data:{
                    'product_id':product_id
                },
                success:function(data){
                    parent_blk.remove();
                    if ($('.later_item').length==0){
                        $('.cart_later').remove();
                    }
                    $('.cartbox').replaceWith(data);

                    setTimeout(function(){
                        animate_cart();
                    } ,600);
                    getCartInHtml();
                },
                error:function(jqXHR,textStatus,errorThrown){

                }
            });
        }

    });

    function getLaterCartHtml(){
        $.ajax({
            type:'post',
            url:'/get_later_list/',
            success:function(data){
                if ($('.cart_later').html()){
                    $('.cart_later').replaceWith(data);
                } else {
                    $('.cart').append(data);
                }
            },
            error:function(data){
            }
        });
    }

    function getCartboxHtml(){
        $.ajax({
            type:'post',
            url:'/get_cartbox_html/',
            success:function(data){
                $('.cartbox').replaceWith(data);
            }
        });
    }

    function getCartInHtml(){
        $.ajax({
            type:'post',
            url:'/get_cartin_html/',
            success:function(data){
                if ($('.cart_in').html()) {
                    $('.cart_in').replaceWith(data);
                } else {
                    $('.cart h1').html('Косметичка');
                    $('.cart h1').after(data);
                }
            }
        });
    }

});

function ChangePersonalInfo(type,value){
    if (value==undefined){
        value = false;
    }
    $.ajax({
        type:'post',
        url:'/edt_profile_info/',
        data:{
            'type':type,
            'value':value,
            'id': $('#profile_id').val()
        },
        success:function(data){
            $('.sysmess').html(data);
            setTimeout( function(){
                $('.sysmess').html('');
            },2000);
        },
        error:function(jqXHR,textStatus,errorThrown){
            $('.sysmess').html(jqXHR.responseText);
        }
    });
}
