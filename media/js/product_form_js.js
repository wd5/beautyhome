$(function() {
    var selected_set = $('select[name="life_events"] option:selected');
    var selected_ids = [];
    for (var i=0;i<=selected_set.length-1;i++){
        selected_ids.push(selected_set.eq(i).val());
    }
    selected_ids = selected_ids.join(',');
    var selected_subcat_set = $('select[name="le_category"] option:selected');

    $.ajax({
        url: "/load_le_subcat/",
        data: {
            selected_ids:selected_ids
        },
        type: "POST",
        success: function(data) {
            $('select[name="le_category"]').html(data);
            for (var i = 0; i <= selected_subcat_set.length-1; i++)
                {
                    var val = selected_subcat_set.eq(i).val();
                    if ($('select[name="le_category"] option[value="'+val+'"]'))
                        {   // если объект уже был выделен - то оставляем выделение
                            $('select[name="le_category"] option[value="'+val+'"]').attr('selected','selected')
                        }
                }
        },
        error:function(jqXHR,textStatus,errorThrown) {
            /*$('.feature_name select').html('<option value="" selected="selected">---------</option>');*/
        }
    });

    $('select[name="life_events"]').live('change',function(){
        var selected_options_set = $('select[name="life_events"] option:selected');
        var selected_options_ids = [];
        for (var i=0;i<=selected_options_set.length-1;i++){
            selected_options_ids.push(selected_options_set.eq(i).val());
        }
        selected_options_ids = selected_options_ids.join(',');
        $.ajax({
            url: "/load_le_subcat/",
            data: {
                selected_ids:selected_options_ids
            },
            type: "POST",
            success: function(data) {
                $('select[name="le_category"]').html(data);
            },
            error:function(jqXHR,textStatus,errorThrown) {
                /*$('.feature_name select').html('<option value="" selected="selected">---------</option>');*/
            }
        });
    });
});