requirejs.config({
    baseUrl: 'js',
    shim : {
        "bootstrap" : { "deps" :['jquery'] },
        "bootbox" : { "deps" :['bootstrap'] }
    },
    paths: {
        "jquery" : "vendors/jquery",
        "bootstrap" :  "vendors/bootstrap",
        "bootbox" :  "vendors/bootbox"
    }
});

require(['jquery'], function ($) {
    //console.log($);
    require(['app/upload']);
});