let img_url_base64 = "";

window.onload = function () {
    // 获取文件上传组件
    let fp = document.getElementById("file");
    // 获取识别结果框
    let res1 = document.getElementById("res1");
    // 获取计算结果框
    let res2 = document.getElementById("res2");
    // 获取图片显示img
    let img = document.getElementById("show");

    function clear() {
        res1.value = "";
        res2.value = "";
    }

    // 提交按钮绑定事件
    $("#submit").click(function () {
        // 调用后端识别函数
        let img_data = img_url_base64.substring(22);
        // console.log(img_data);
        $.post('get_result', {"img_data": img_data.toLocaleString()}, function (json_response) {
            let json = JSON.parse(json_response);
            // console.log(json["expression"][0][0]);
            // console.log(json["result"][0][0]);
            for (let i = 0; i < json["expression"].length; i++) {
                let exp = res1.value;
                let res = res2.value;
                res1.value = exp + json["expression"][i][0] + "\n";
                res2.value = res + json["result"][i][0] + "\n";
            }
        });
    });
    // 清除按钮绑定事件
    $("#clear").click(function () {
        fp.value = "";
        img.src = "";
        clear();
    });
};

function url_base64(obj) {
    let reader = new FileReader();
    // filses就是input[type=file]文件列表，files[0]就是第一个文件
    // 这里就是将选择的第一个图片文件转化为base64的码
    reader.readAsDataURL(obj.files[0]);
    reader.onload = function () {
        // console.log(reader.result);  // reader.result是base64码
        img_url_base64 = reader.result;
    };
}

// 图片位置居中
function img_center(obj) {
    let margin_h = 625 - obj.height;
    let margin_w = 1000 - obj.width;
    obj.style.marginLeft = margin_w / 2 + 20 + "px";
    obj.style.marginTop = margin_h / 2 + 10 + "px";
}

// 显示选择的图片
function show_image(obj) {
    document.getElementById("show").src = getObjectURL(obj.files[0]);
}

function getObjectURL(file) {
    let url = null;
    // 下面函数执行的效果是一样的，只是需要针对不同的浏览器执行不同的 js 函数而已
    if (window.createObjectURL != undefined) { // basic
        url = window.createObjectURL(file);
    } else if (window.URL != undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file);
    } else if (window.webkitURL != undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file);
    }
    return url;
}
