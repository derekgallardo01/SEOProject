
if (!$) {
    $ = django.jQuery;	
}

$(document).ready(function() {
    //django.jQuery("input[name='_addanother']").attr('type','hidden');
    django.jQuery("input[name='_addanother']").css('display','none');
});
