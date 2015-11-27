$(function() {
    $('.menu .item').tab();
    $('.ui.dropdown').dropdown();
    $('.ui.checkbox').checkbox();

    $('.relate_template').click(function() {
        var hostname = $(this).parents('tr').children('td:first-child').text();
        $('#hid').val(hostname);
        $('#host_templates').modal({
            closeable: false,
            onApprove: function() {
                $('#tform').submit();
                return true;
            }
        }).modal('setting', 'closable', false).modal('show');
    });

    $('#template_type').change(function() {
        var type = $('#template_type').val();
        if(type != '选择') {
            $('#template_name_id').empty();
            $('#template_name_id').append('<option selected=selected>选择</option>');
            $.getJSON('/monitor/m/get_template_name_by_type/', {'type': type}, function(result) {
            $.each(result.templates, function(inx, template) {
                $('#template_name_id').append('<option value=' + template.id +'>' + template.name + '</option>');
            });
        });
        };
    })
});