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
	jQuery('#carousel').jcarousel({
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
$(function() {
	$( "#filter_price" ).slider({
		range: "min",
		min: 100,
		max: 10000
	});
});



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


