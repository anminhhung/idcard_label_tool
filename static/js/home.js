var mode = '';
var index = '';
var fname = '';

function onLoad(){
    var url = new URL(window.location.href);
    mode = url.searchParams.get("mode");
    if (mode.localeCompare('random')==0){
        getImgFileName('random','0');
    }else if (mode.localeCompare('index')==0){
        index = url.searchParams.get("index");
        getImgFileName('index',index);
    }
    console.log("onload done");
}
function getImgFileName(mode, index){
    $.ajax({
        url: '/get_img_name?mode='+mode+'&index='+index,
        type: 'get',
        dataType: 'json',
        contentType: 'application/json',  
        success: function (response) {
            if (response['code'] == 1001) {
                alert("[Lỗi] Không nhận được phản hồi từ server, vui lòng kiểm tra lại!");
            }
            console.log(response);
            fname = response['data']['fname'];
            var return_index = String(response['data']['index']);
            if (return_index.localeCompare('-1')==0){
                window.location.href = "home?mode=index&index=0";
            }
            drawImageOCR("/get_ori_img?filename="+fname);
            loadLabel(fname);
        }
    }).done(function() {
        
    }).fail(function() {
        alert('Fail!');
    });
}
function loadLabel(fname){
    $.ajax({
        url: '/get_label?fname='+fname,
        type: 'get',
        dataType: 'json',
        contentType: 'application/json',  
        success: function (response) {
            if (response['code'] == 1001) {
                alert("[Lỗi] Không nhận được phản hồi từ server, vui lòng kiểm tra lại!");
            }
            if (response['code'] != 1201){
                label = response['data']['label'];
                document.getElementById('input_label').value = label;
            }
        }
    }).done(function() {
        
    }).fail(function() {
        alert('Fail!');
    });
}
function drawImageOCR(src) {
    var canvas = document.getElementById("preview_img");
    IMGSRC = src;
    var context = canvas.getContext('2d');
    var imageObj = new Image();
    imageObj.onload = function() {
        canvas.width = this.width;
        canvas.height = this.height;
        context.drawImage(imageObj, 0, 0, this.width,this.height);
    };
    imageObj.src = src;
}
function sendResult(){
    var label = document.getElementById('input_label').value;
    $.ajax({
        url: '/send_result',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',  
        data: JSON.stringify({"version": "1.0", "fname": fname, 'label': label}),
        success: function (response) {
            if (response['code'] == 1001) {
                alert("[Lỗi] Không nhận được phản hồi từ server, vui lòng kiểm tra lại!");
            }
            console.log(response);
        }
    }).done(function() {
        
    }).fail(function() {
        alert('Fail!');
    });
}
$(document).ready(function() {
    $("#input_label").on('keyup', function (e) {
        if (e.keyCode === 13) {
            sendResult();
            if (mode.localeCompare('random')==0){
                window.location.href = "home?mode=random";
            }else if (mode.localeCompare('index')==0){
                window.location.href = "home?mode=index&index="+(parseInt(index)+1);
            }
            
        }else if (e.keyCode === 37){
            if (mode.localeCompare('random')==0){
                window.location.href = "home?mode=random";
            }else if (mode.localeCompare('index')==0){
                window.location.href = "home?mode=index&index="+(parseInt(index)-1);
            }
        }else if (e.keyCode === 39){
            if (mode.localeCompare('random')==0){
                window.location.href = "home?mode=random";
            }else if (mode.localeCompare('index')==0){
                window.location.href = "home?mode=index&index="+(parseInt(index)+1);
            }
        }
    });
});
