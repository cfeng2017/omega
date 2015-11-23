$(function() {

    $('.menu .item').tab();
    $('.ui.dropdown').dropdown();
    $('.ui.checkbox').checkbox();

//    $('.add_ds').on('click', function() {
//        var tr_num = $('#ds_table tbody tr').length;             //已有数据源行总数
//
//        var i=0;
//        for(; i<=tr_num; i++) {
//            if($('#tr_' + i).length==0) break;
//        }
//
//        var tr_id = 'tr_' + i;
//
//        var tr="<tr id=" + tr_id + ">" +
//                "<td><input type='text' name=" + tr_id + "_ds_name id=" + tr_id + "_ds_name></td>" +
//                "<td><textarea name=" +  tr_id + "_ds_desc id=" + tr_id + "_ds_desc></textarea></td>" +
//                "<td><a class='ui red button del_ds'>删除</a></td></tr>";
//
//        $('.add_ds').parents('tbody').append(tr);
//    });
//
//    $('tbody').on('click', '.del_ds', function() {
//        $(this).parents('tr').remove();
//    })

    $('.add_template').click(function() {
        $('#template_name_modal').modal({
            closeable: false,
            onApprove: function() {
                if($('#new_template_name').val().trim().length != 0) {
                    $('#tnform').submit();
                } else {
                    console.log('模板名不能为空！');
                }
                return true;
            }
        }).modal('setting', 'closable', false).modal('show');
    })

    $('.add_ds').click(function() {
        var change_button = "<a class='modify_ds content-line-btn'>修改</a>";
        var del_button = "<a class='del content-line-btn ui red tiny button'>删除</a>";

        $('#ds_name_modal').modal({
            closeable: false,
            onApprove: function() {
                var ds_name = "<div class='content-line-text' name='ds_name'>" + $('#ds_name').val() + "</div>";
                var ds_desc = "<div class='content-line-text' name='ds_desc'>" + $('#ds_desc').val() + "</div>";
                var h_ds_name = "<input type='hidden' name='ds_name' value=" + $('#ds_name').val() +">";
                var h_ds_desc = "<input type='hidden' name='ds_desc' value=" + $('#ds_desc').val() +">";

                var line = "<div class=content-line>" +
                            change_button + del_button +
                            ds_name +
                            ds_desc +
                            h_ds_name +
                            h_ds_desc +
                            "</div>";
                $('#add_ds_items').parent().before(line);

                return true;
            }
        }).modal('setting', 'closable', false).modal('show');
    });

    $('.form-content').on('click', '.del', function() {
        $(this).parent().remove()
    });

    $('.form-content').on('click', '.modify_ds', function() {
        var target_ds = $(this).closest('div').children('div');
        var hidden_ds = $(this).closest('div').children('input');
        var ds_name = target_ds.eq(0).text();
        var ds_desc = target_ds.eq(1).text();
        $('#modify_ds_name').val(ds_name);
        $('#modify_ds_desc').val(ds_desc);
        $('#modify_ds_name_modal').modal({
            closeable: false,
            onApprove: function() {
                var new_ds_name = $('#modify_ds_name').val();
                var new_ds_desc = $('#modify_ds_desc').val();
                target_ds.eq(0).text(new_ds_name);
                target_ds.eq(1).text(new_ds_desc);
                hidden_ds.eq(0).val(new_ds_name);
                hidden_ds.eq(1).val(new_ds_name);
                return true;
            }
        }).modal('setting', 'closable', false).modal('show');
    });

    $('.form-content').on('click', '.modify_rule', function() {
        console.log('111');
    });


    $('#add_rule').click(function() {
        var ds_list = $('#ds-list').children('.content-line');
        var options = '';
        for(var i=0; i<ds_list.length-1; i++) {
            options += "<option>" + ds_list.eq(i).children('div').eq(0).text() + "</option>";
        }
        $('#modal_ds').empty().append(options);
        var change_button = "<a class='modify_rule content-line-btn'>修改</a>";
        var del_button = "<a class='del content-line-btn  ui red tiny button'>删除</a>";
        $('#alarm_rule_modal').modal({
            closeable: false,
            onApprove: function() {
                var mode=$('#threshold_type').val();
                var rule = '';
                var r1 = ',&emsp;警告&nbsp;';
                var r2 = ',&emsp;灾难&nbsp;';
                var r3 = '&nbsp;~&nbsp;';

                rule += $('#modal_ds').val();

                var warn_lower = $('#warn_lower').val();
                if(!warn_lower) {
                    warn_lower = 0;
                }
                var dis_lower = $('#disaster_lower').val();
                if(!dis_lower) {
                    dis_lower = 0;
                }

                if(mode==1) {
                    rule += '上限模式' + r1 + warn_lower + r2 + dis_lower;
                } else if (mode==2) {
                    rule += '下限模式' + r1 + warn_lower + r2 + dis_lower;
                } else if (mode==3) {
                    var warn_upper = $('#warn_upper').val();
                    var dis_upper = $('#disaster_upper').val();
                    if(!warn_upper) {
                        warn_upper = 0;
                    }
                    if(!dis_upper) {
                        dis_upper = 0;
                    }
                    if(parseInt(warn_upper)<parseInt(warn_lower) || parseInt(dis_upper)<parseInt(warn_lower)) {
                        $('#msg').css('display', 'block');
                        return false;
                    }
                    rule += '范围模式' + r1 + warn_lower + r3 + warn_upper + '%' +
                                        r2 + dis_lower + r3 + dis_upper + '%';
                } else {
                    rule += '斜率模式' + r1 + warn_lower + r2 + dis_lower;
                }

                rule += ',&emsp;持续&nbsp;' + $('#last_time').val() + '&nbsp;分钟,&emsp;间隔&nbsp;' +
                        $('#interval_time').val() + '&nbsp;分钟,&emsp;' +
                        $('#begin_time').val() + ' ~ ' + $('#end_time').val();

                var h_ds = "<input type='hidden' name='selected_ds' value=" + $('#modal_ds').val() + ">";
                var h_mode = "<input type='hidden' name='mode' value=" + mode + ">";
                var h_warn_lower = "<input type='hidden' name='warn_lower' value=" + warn_lower + ">";
                var h_warn_upper = "<input type='hidden' name='warn_upper' value=" + warn_upper + ">";
                var h_dis_lower = "<input type='hidden' name='dis_lower' value=" + dis_lower + ">";
                var h_dis_upper = "<input type='hidden' name='dis_upper' value=" + dis_upper + ">";
                var h_last_time = "<input type='hidden' name='last_time' value=" + $('#last_time').val() + ">";
                var h_inter_time = "<input type='hidden' name='interval_time' value=" + $('#interval_time').val() + ">";
                var h_begin_time = "<input type='hidden' name='begin_time' value=" + $('#begin_time').val() + ">";
                var h_end_time = "<input type='hidden' name='end_time' value=" + $('#end_time').val() + ">";

                var line = "<div class=content-line>" +
                            change_button + del_button + rule + h_ds + h_mode + h_warn_lower + h_warn_upper +
                            h_dis_lower + h_dis_upper + h_last_time + h_inter_time + h_begin_time + h_end_time +
                            "</div>";
                $('#add_rule').parent().before(line);
                return true;
            }
        }).modal('setting', 'closable', false).modal('show');
    });

//    $('.time-picker').datetimepicker({
//        datepicker: false,
//        defaultTime: '00:00',
//        format: 'H:i'
//    });

    $('#begin_time').datetimepicker({
        format:'H:i',
        defaultTime: '00:00',
        onShow:function( ct ){
            this.setOptions({
                maxTime:jQuery('#end_time').val()?jQuery('#end_time').val():false
            });
        },
        datepicker:false
    });

    $('#end_time').datetimepicker({
        format:'H:i',
        defaultTime: '00:00',
        onShow:function( ct ){
            this.setOptions({
                minTime:jQuery('#begin_time').val()?jQuery('#begin_time').val():false
            })
        },
        datepicker:false
 });


    $('#threshold_type').change(function() {
        var mode = $(this).val();
        if(mode==3) {
            var warn = "<input type='text' class='ui-modal test' name='warn_upper' id='warn_upper'><span class='rank-percent'>(百分比)</span>";
            var dis = "<input type='text' class='ui-modal' name='disaster_upper' id='disaster_upper'><span class='rank-percent'>(百分比)</span>";
            $('#warn').append(warn);
            $('#disaster').append(dis);
        } else {
            if($('#warn_upper').length > 0){
                $('#warn_upper').remove();
                $('#disaster_upper').remove();
                $('.rank-percent').remove();
            }
        }

    })

//    $('#ds_template_name').change(function() {
//        var ds_template_name = $('#ds_template_name').val();
//        if(ds_template_name=="选择") {
//            $('#alarm_template_show').css("display", "none");
//            return false;
//        }
//        $('#alarm_template_show').css("display", "block");
//        $('#template_infos').empty();
//        $.getJSON('/config/t/get_monitor_template/', {'template_name': ds_template_name}, function(result) {
//            var data = result['template_infos']
//            var tr=''
//            for(var i in data) {
//                var ds_num = data[i]['ds'].length;
//                tr=tr+"<tr>" +
//                    "<td rowspan=" + ds_num + ">" + data[i]['chart_name'] + "</td>" +
//                    "<td rowspan=" + ds_num + ">" + data[i]['chart_desc'] + "</td>";
//                var ds_arr = data[i]['ds'];
//                for(var j in ds_arr) {
//                    if(j==0) pre_tr='';
//                    else pre_tr="<tr>"
//
//                    var tds = "<td>" + ds_arr[j]['ds_name'] + "</td>" +
//                             "<td>" + ds_arr[j]['ds_desc'] + "</td>" +
//                             "<td></td>"+
//                             "<td class='add_alarm_condition'><a class='ui blue button'>添加报警</a></td>";
//                    tr+=pre_tr + tds + "</tr>";
//                }
//            }
//
//            $("#template_infos").html(tr);
//        });
//    });
//
//    $('form').on('click', '.add_alarm_condition', function() {
//        $('#alarm_template_modal').
//            modal({
//            closeable : false,
//            onApprove:function() {
//                var c_name = $('#modal_chart_name').val();
//                var t_type = $('#threshold_type').val();
////                if (t_type == 1) {
////                    var
////                }
//
//                return false;
//            }
//        }).modal('setting', 'closable', false).modal('show');
//    });


//    $('form').on('change', '#threshold_type', function() {
//        var tt = $('#threshold_type').val()
//        var warning_tr = ''
//        var disaster_tr = ''
//        if(tt == 1) {
//            warning_tr= "<td>上限警告阈值:</td><td><input type='text' id='warnging_upper' name='warnging_upper'></td>";
//            disaster_tr = "<td>上限灾难阈值:</td><td><input type='text' id='disaster_upper' name='disaster_upper'></td>";
//        } else if(tt == 2) {
//            warning_tr = "<td>下限警告阈值:</td><td><input type='text' id='warnging_lower' name='warnging_lower'></td>";
//            disaster_tr = "<td>报警灾难阈值:</td><td><input type='text' id='disaster_lower' name='disaster_lower'></td>";
//        } else if(tt == 3) {
//            warning_tr = "<td>范围警告阈值:</td>" +
//                         "<td><input style='width: 47%' type='text' id='warnging_lower' name='warnging_lower'> - " +
//                               "<input style='width: 47%' type='text' id='warnging_upper' name='warnging_upper'></td>";
//            disaster_tr = "<td>范围灾难阈值:</td>" +
//                          "<td><input style='width: 47%' type='text' id='disaster_lower' name='disaster_lower'> - " +
//                             "<input style='width: 47%' type='text' id='disaster_upper' name='disaster_upper'></td>";
//        } else if(tt == 4) {
//            warning_tr = "<td>斜率警告阈值:</td><td><input type='text' id='warnging_slope' name='warnging_slope'></td>";
//            disaster_tr = "<td>斜率灾难阈值:</td><td><input type='text' id='disaster_slope' name='disaster_slope'></td>";
//        }
//        $("#warning_threshold").html(warning_tr);
//        $('#disaster_threshold').html(disaster_tr);
//
//    });
//
});