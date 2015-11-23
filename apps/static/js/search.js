$(function(){

    $('.ui.search').search({
        apiSettings: {
          url: '/search/{query}'
        },
        type: 'category'
    });

//    $('#site_search_icon').on('click', function(){
//        var sc = $('#site_search').val()
//        console.log(sc)
//    });

})