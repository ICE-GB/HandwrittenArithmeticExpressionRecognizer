let s = document.getElementById("show");
    // 获取主画布
    let my_canvas = document.getElementById("my_canvas");
    // 获取识别结果框
    let res1 = document.getElementById("res1");
    // 获取计算结果框
    let res2 = document.getElementById("res2");
    // 获取提交按钮
    let btn1 = document.getElementById("submit");
    // 获取清除按钮
    let btn2 = document.getElementById("clear");
    // 获取主画布2d接口的画笔
    let ctx1 = my_canvas.getContext("2d");

    function init_canvas() {
        my_canvas.width = 777;
        my_canvas.height = 300;

        // 绘制画布背景为白色（默认为透明色）
        ctx1.fillStyle = "#000000";
        ctx1.fillRect(0, 0, 777, 300);
        // // 绘制画布边框为黑色
        // ctx1.strokeStyle = "#000000";
        ctx1.lineWidth = 1;
        ctx1.strokeRect(0, 0, 777, 300);

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

        // 定义画笔粗细 粗些较易识别
        ctx1.lineWidth = 5;
        ctx1.strokeStyle = '#ffffff';
        // 定义画笔的落笔点坐标位置
        ctx1.beginPath();
        // ctx1.moveTo(location.x, location.y);
        ctx1.moveTo(x, y);
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
            ctx1.lineTo(x, y);
            ctx1.stroke();

            my_canvas.onmouseup = function () {
                my_canvas.onmouseup = null;
                my_canvas.onmousemove = null;
            };
            my_canvas.onmouseout = function () {
                my_canvas.onmouseout = null;
                my_canvas.onmouseup = null;
                my_canvas.onmousemove = null;
            };
        };
    };


    btn1.onclick = function () {
        res1.value = "(4 + 6) * 3";
        res2.value = "30";
    };
    btn2.onclick = function () {
        init_canvas();
    };