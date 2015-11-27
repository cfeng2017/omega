$(function(){

    $('.menu .item').tab();
    $('.ui.dropdown').dropdown();
    $('.ui.checkbox').checkbox();

    $('#gdb_gname-gtype-gtype').change(function() {
        tid = $('#gdb_gname-gtype-gtype').val();
        $('#gdb_gname-gname').empty();
        $.getJSON('/asset/g/get_group_by_type/', {'tid': tid}, function(data) {
            $.each(data.groups, function(ind, group) {
                $('#gdb_gname-gname').append('<option value=' + group.id + '>' + group.name + '</option>');
            });
        });
    });

    $('#group_type').change(function() {
        tid = $('#group_type').val();
        $('#group_list tbody').empty();
        $.getJSON('/asset/g/get_group_by_type/', {'tid': tid}, function(data) {
            $.each(data.groups, function(inx, group) {
                $('#group_list tbody').append('<tr>' +
                                        '<td>' + group.name + '</td>' +
                                        '<td>' + group.description + '</td>' +
                                        '<td>' + group.contacts + '</td></tr>');
            });
        });
    });

    $('#h_brt').datetimepicker({

//        defaultDate: new Date(1000, 12, 30),
//       formatDate: 'Y-m-d',

        defaultTime: '00:00',
        formatTime: 'H:i',
        format: 'Y-m-d H:i'

    });

})
