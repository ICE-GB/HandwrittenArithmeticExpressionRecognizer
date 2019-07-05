window.onload = function () {
    // 获取文件选择
    let fp = document.getElementById('file');
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
        res1.value = "(4 + 6)";
        res2.value = "10";
    });
    // 清除按钮绑定事件
    $("#clear").click(function () {
        img.src = "";
        clear();
    });
};

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
