var total_of_images = 0

$('#btn-loadfile').click(function () {
        var mode = document.getElementById("mode").value;
        var index = document.getElementById("number_id").value;

        if (mode.localeCompare('random')==0){
            getImgFileName('random','0');
        }else if (mode.localeCompare('index')==0){
            getImgFileName('index',index);
        }
    }
)

function getImgFileName(mode, index){
    $.ajax({
        url: 'get_img_name?mode='+mode+'&index='+index,
        type: 'get',
        dataType: 'json',
        contentType: 'application/json',  
        success: function (response) {
            if (response['code'] == 1001) {
                alert("[Lỗi] Không nhận được phản hồi từ server, vui lòng kiểm tra lại!");
            }
            console.log(response);
            fname = response['data']['fname'];
            index = response['data']['index'];
            total = response['data']['total'];
            total_of_images = total;
            document.getElementById('number_id').value = index;
            var return_index = String(response['data']['index']);
            if (return_index.localeCompare('-1')==0){
                window.location.href = "idcard?mode=index&index=0";
            }
            drawImageOCR("/get_ori_img?filename="+fname, fname, index);
            loadLabel(fname);
        }
    }).done(function() {
        
    }).fail(function() {
        alert('Fail!');
    });
}

function loadLabel(fname){
    $.ajax({
        url: 'get_label?fname='+fname,
        type: 'get',
        dataType: 'json',
        contentType: 'application/json',  
        success: function (response) {
            if (response['code'] == 1001) {
                alert("[Lỗi] Không nhận được phản hồi từ server, vui lòng kiểm tra lại!");
            }
            if (response['code'] != 1201){
                idnum = response['data']['idnum'];
                idname = response['data']['idname'];
                iddob = response['data']['iddob'];
                idhome = response['data']['idhome'];
                idaddress = response['data']['idaddress'];
                document.getElementById('idnum').value = idnum;
                document.getElementById('idname').value = idname;
                document.getElementById('iddob').value = iddob;
                document.getElementById('idhome').value = idhome;
                document.getElementById('idaddress').value = idaddress
            }
        }
    }).done(function() {
    
    }).fail(function() {
        alert('Fail!');
    });
}

function drawImageOCR(src, fname, index) {
    console.log(src)
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

    document.getElementById("noti_index").innerHTML ="Index: " + index;
    document.getElementById("noti_number").innerHTML = "Image name: " + fname;
    document.getElementById('idcard_info').style.display = "block";
}

$('#btn-Save').click(function () {
    console.log("fname in Submitlabel: " + fname)
    var idnum = document.getElementById('idnum').value;
    var idname = document.getElementById('idname').value;
    var iddob = document.getElementById('iddob').value;
    var idhome = document.getElementById('idhome').value;
    var idaddress = document.getElementById('idaddress').value;

    $.ajax({
        url: '/send_result',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',  
        data: JSON.stringify({"version": "1.0", "fname": fname, 'idnum': idnum, 'idname': idname, 'iddob': iddob, 'idhome': idhome, 'idaddress': idaddress}),
        success: function (response) {
            if (response['code'] == 1001) {
                alert("[Lỗi] Không nhận được phản hồi từ server, vui lòng kiểm tra lại!");
            }
            console.log(response);
        }
    }).done(function() {
        document.getElementById("noti_save").innerHTML = "Done!";
    }).fail(function() {
        alert('Fail!');
    });
}
)

$('#btn-Next').click(function () {
    var index = document.getElementById("number_id").value;

    index = parseInt(index) ;

    if (index <  total_of_images-1){
        index += 1;
    }
    else{
        index = 0;
    }

    getImgFileName('index', String(index));
    document.getElementById("noti_save").innerHTML = "Not Save!";
}
)

$('#btn-Previous').click(function () {
    var index = document.getElementById("number_id").value;

    index = parseInt(index)
    if (index > 0) {
        index = index - 1;
    }

    getImgFileName('index', String(index));
    document.getElementById("noti_save").innerHTML = "Not Save!";
}
)

function save_info_idcard(){
    var idnum = document.getElementById('idnum').value;
    var idname = document.getElementById('idname').value;
    var iddob = document.getElementById('iddob').value;
    var idhome = document.getElementById('idhome').value;
    var idaddress = document.getElementById('idaddress').value;

    $.ajax({
        url: '/send_result',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',  
        data: JSON.stringify({"version": "1.0", "fname": fname, 'idnum': idnum, 'idname': idname, 'iddob': iddob, 'idhome': idhome, 'idaddress': idaddress}),
        success: function (response) {
            if (response['code'] == 1001) {
                alert("[Lỗi] Không nhận được phản hồi từ server, vui lòng kiểm tra lại!");
            }
            console.log(response);
        }
    }).done(function() {
        document.getElementById("noti_save").innerHTML = "Done!";
    }).fail(function() {
        alert('Fail!');
    });
}

function view_previous_image(){
    var index = document.getElementById("number_id").value;

    index = parseInt(index)
    if (index > 0) {
        index = index - 1;
    }

    getImgFileName('index', String(index));
    document.getElementById("noti_save").innerHTML = "Not Save!";
}

function view_next_image(){
    var index = document.getElementById("number_id").value;

    index = parseInt(index) ;

    if (index <  total_of_images-1){
        index += 1;
    }
    else{
        index = 0;
    }

    getImgFileName('index', String(index));
    document.getElementById("noti_save").innerHTML = "Not Save!";
}

function focus_field_down(){
    var index_text = $("input[type='text']").index(this);
    $("input[type='text']").eq(index_text + 1).focus();
}

function focus_field_top(){
    var index_text = $("input[type='text']").index(this);
    $("input[type='text']").eq(index_text + -1).focus();
}

document.onkeydown = function(evt) {
    evt = evt || window.event;
    switch (evt.keyCode) {
        case 13:
            save_info_idcard();
            break;
        case 37:
            view_previous_image();
            break;
        case 39:
            view_next_image();
            break;
    }
};