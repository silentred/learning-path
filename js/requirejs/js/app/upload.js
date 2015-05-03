define(['jquery', 'bootbox'], function ($, bootbox) {

    $('#uploadBtn').click(function(){
        var formData = new FormData($('#uploadForm')[0]);
        $.ajax({
            url: '/upload',  //Server script to process data
            type: 'POST',
            // Form data
            data: formData,
            //Options to tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false,

            xhr: function() {  // Custom XMLHttpRequest
                var myXhr = $.ajaxSettings.xhr();
                console.log(myXhr);
                if(myXhr.upload){ // Check if uploads property exists
                    myXhr.upload.addEventListener('progress',function(e){
                        console.log(e);
                        if(e.lengthComputable){
                            $('progress').attr({value:e.loaded,max:e.total});
                        }
                    }, false); // For handling the progress of the uploads
                }
                return myXhr;
            },
            //Ajax events
            beforeSend: function(){
                console.log('before');
            },
            success: function(data){
                console.log(data);
            },
            error: function(e){
                console.log('error');
                console.log(e);
            }
        });
        return false;
    });



    console.log(bootbox);
    $(function () {
        bootbox.alert({
            size: 'large',
            message: "Your message here…",
            callback: function(){  /*your callback code */ }
        })
    })
});

