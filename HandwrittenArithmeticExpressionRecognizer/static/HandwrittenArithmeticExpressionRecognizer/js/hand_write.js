// 获取主画布
let my_canvas = document.getElementById("my_canvas");

window.onload = function () {
    // 获取主画布
    let my_canvas = document.getElementById("my_canvas");
    // 获取识别结果框
    let res1 = document.getElementById("res1");
    // 获取计算结果框
    let res2 = document.getElementById("res2");
    // 获取主画布2d接口的画笔
    let ctx = my_canvas.getContext("2d");

    function init_canvas() {
        my_canvas.width = 1000;
        my_canvas.height = 625;

        // 绘制画布背景为黑色（默认为透明色）
        ctx.fillStyle = "#FFFFFF";
        ctx.fillRect(0, 0, 1000, 625);

        res1.value = '';
        res2.value = '';
    }

    init_canvas();
    //获取画布的起点坐标位置
    let canvas_X = my_canvas.offsetLeft;
    let canvas_Y = my_canvas.offsetTop;

    //鼠标按下操作事件绑定
    my_canvas.onmousedown = function (event) {
        // window.event处理浏览器的兼容性
        let ev = event || window.event;
        // 获取落笔点的绝对坐标位置
        let left = ev.clientX;
        let top = ev.clientY;
        // 获取落笔点的相对于画布的相对坐标位置
        let x = left - canvas_X;
        let y = top - canvas_Y;
        // 定义画笔粗细
        ctx.lineCap = "round";
        ctx.lineWidth = 16;
        ctx.lineCap = "round";
        ctx.strokeStyle = '#000000';
        // 定义画笔的落笔点坐标位置
        ctx.beginPath();
        // ctx.moveTo(location.x, location.y);
        ctx.moveTo(x, y);
        //鼠标移动操作事件绑定
        my_canvas.onmousemove = function (event) {
            // window.event处理浏览器的兼容性
            let ev = event || window.event;
            // 获取起笔点的绝对坐标位置
            let left = ev.clientX;
            let top = ev.clientY;
            // 获取起笔点的相对于画布的相对坐标位置
            let x = left - canvas_X;
            let y = top - canvas_Y;
            // 定义画笔的落笔点坐标位置
            ctx.lineTo(x, y);
            ctx.stroke();

            my_canvas.onmouseup = function () {
                my_canvas.onmousemove = null;
            };
            my_canvas.onmouseout = function () {
                my_canvas.onmousemove = null;
            };
            my_canvas.onmouseleave = function () {
                my_canvas.onmousemove = null;
            }
        };
    };

    // 提交按钮绑定事件
    $("#submit").click(function () {
        // 弹出等待层
        loading();
        // 调用后端识别函数
        let my_canvas = document.getElementById('my_canvas');
        let img = new Image();
        img.src = my_canvas.toDataURL();
        let img_data = img.src.substring(22);
        // console.log(img_data);
        $.post('get_result', {"img_data": img_data.toLocaleString()}, function (json) {
            // console.log(json["expression"][0][0]);
            // console.log(json["result"][0][0]);
            for (let i = 0; i < json["expression"].length; i++) {
                let exp = res1.value;
                let res = res2.value;
                res1.value = exp + json["expression"][i][0] + "\n";
                res2.value = res + json["result"][i][0] + "\n";
            }
            loading_end();
        });
    });
    // 清除按钮绑定事件
    $("#clear").click(function () {
        init_canvas();
    });
};

function out_focus() {
    my_canvas.onmouseleave = null;
}

// 识别算式过程中的等待弹出层
function loading() {
    // 弹出层
    layer.open({
        type: 3,
        title: false,
        closeBtn: 0,
        skin: 'layui-layer-nobg', //没有背景色
    });
}

// 识别结束后关闭弹出层
function loading_end() {
    layer.closeAll('loading');
}