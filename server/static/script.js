let data_path;
let dd = false;
let path;
let handler_img_path = null;
let global_x = null, global_y = null;

let super_info = {
    'status': false,
    'data': null
}

function init(data){
    data_path = data;
    $('.loader').hide();
}

function load_image() {
    var e = document.getElementById("img_list");
    var imageParent = document.getElementById("myimage");
    path = data_path[e.value];
    imageParent.src = path;
//    handler_img_path = null;
    imageZoom("myimage", "myresult");
}

function imageZoom(imgID, resultID) {
    dd = false;
    var img, lens, result, cx, cy;
    img = document.getElementById(imgID);
    result = document.getElementById(resultID);

    let blockImage = document.getElementById("block_image");
    blockImage.addEventListener("scroll", (e) => {
        console.log(cx + " " + cy);
        console.log(global_x + " " + global_y);
        console.log(blockImage.scrollLeft + " " + blockImage.scrollTop)
        console.log(result.style.backgroundPosition)
        result.style.backgroundPosition = "-" + (global_x * cx - blockImage.scrollLeft) + "px -" + (global_y * cy - blockImage.scrollTop) + "px";
    })

    document.querySelectorAll('.img-zoom-lens').forEach(function(a){
        a.remove();
    })

    lens = document.createElement("DIV");
    lens.setAttribute("class", "img-zoom-lens");
    img.parentElement.insertBefore(lens, img);

    cx = result.offsetWidth / lens.offsetWidth;
    cy = result.offsetHeight / lens.offsetHeight;
    result.style.backgroundImage = "url('" + img.src + "')";
    result.style.backgroundSize = (img.width * cx) + "px " + (img.height * cy) + "px";

    lens.addEventListener("mousemove", moveLens);
//    lens.addEventListener("touchmove", moveLens);
    lens.addEventListener("mouseup", clearDD);
    lens.addEventListener("mousedown", setDD);

    img.addEventListener("mousemove", moveLens);
//    img.addEventListener("touchmove", moveLens);
    img.addEventListener("mouseup", clearDD);
    img.addEventListener("mousedown", setDD);


    function changeDD(e){
        console.log(super_info['data'])
        dd = !dd;
    }
    function clearDD(e){
        dd = 0;
    }
    function setDD(e){
        dd = 1;
    }
    function moveLens(e) {
        if (!dd) {
            return;
        }
        var pos, x, y;
        e.preventDefault();
        pos = getCursorPos(e);

        let blockImg = document.getElementById("block_image");

        x = pos.x - 1;
        y = pos.y - 1;


        if (x > img.width - lens.offsetWidth) {
            x = img.width - lens.offsetWidth;
        }
        if (x < 0) {
            x = 0;
        }
        if (y > img.height - lens.offsetHeight) {
            y = img.height - lens.offsetHeight;
        }
        if (y < 0) {
            y = 0;
        }

        lens.style.left = (Math.round(x) - blockImg.scrollLeft) + "px";
        lens.style.top = (Math.round(y) - blockImg.scrollTop) + "px";
        result.style.backgroundPosition = "-" + (Math.round(x) * cx) + "px -" + (Math.round(y) * cy) + "px";

        global_x = Math.round(x);
        global_y = Math.round(y);
        show_info();
    }
    function getCursorPos(e) {
        var a, x = 0, y = 0;
        e = e || window.event;
        a = img.getBoundingClientRect();
        x = e.pageX - a.left;
        y = e.pageY - a.top;
        x = x - window.pageXOffset;
        y = y - window.pageYOffset;
        return {x : x, y : y};
    }
}

function show_info() {
    // console.log(global_x + " " + global_y);
    $('#coordinates').text(global_x + " ; " + global_y);
    show_info_helper('B');
    show_info_helper('C');

    H = super_info['data']['h']['(' + global_y + ', ' + global_x + ')'];
    $('.H_INFO').empty();
    let z = 40; // масштаб
    let c = document.querySelector('canvas');
    let ctx = c.getContext('2d');
    ctx.clearRect(0, 0, c.width, c.height);
    if (!H) return;
    let info = '';
    for (let i = 0; i < H.length; i++) {
        info += (H[i]).toFixed(5) + ", ";
    }
    $('.H_INFO').append(info);


    // let y = x => x*x; // функция
    let y = x => H[1] + 2 * H[2] * x + 3 * H[3] * (x ** 2) + 4 * H[4] * (x ** 3) + 5 * H[5] * (x ** 4) + 6 * H[6] * (x ** 5);
    

    
    // центровочка
    ctx.translate(c.width/2, c.height/2)

    // сетка
    ctx.strokeStyle = "black";
    ctx.lineWidth = 1;
    ctx.beginPath();
    from_to = super_info['data']['l_max']['(' + global_y + ', ' + global_x + ')'];
    for (let x1 = -3; x1 < 3; x1 += 1) {
        ctx.moveTo(x1*z, -c.height/2);
        ctx.lineTo(x1*z, c.height/2);
        ctx.moveTo(-c.width/2, x1*z);
        ctx.lineTo(c.width/2, x1*z);
    }
    ctx.stroke();
    // график функции
    ctx.strokeStyle = "red";
    ctx.lineWidth = 3;
    ctx.beginPath();

    
    console.log(from_to);
    for (let q = -2; q <= 2; q += 0.01) {
        ctx[q?'lineTo':'moveTo'](q*z, -y(q)*z);
    }
    ctx.stroke();
    ctx.translate(-c.width/2, -c.height/2)
}

function show_info_helper(letter) {
    $('.' + letter + '_INFO').empty();
    my_data_b = super_info['data'][letter]['(' + global_y + ', ' + global_x + ')'];
    if (!my_data_b) return;
    let str = "<table>";



    // $('.' + letter + '_INFO').append('<table>');
    for (let i = 0; i < 4; i++) {
        str += "<tr>"
        // $('.' + letter + '_INFO').append('');
        for (let j = 0; j < 4; j++) {
            str += '<td>' + (my_data_b[i][j]).toFixed(5) + '</td>';
            // $('.' + letter + '_INFO').append('<th>' + my_data_b[i][j] + '</th>');
        }
        str += "</tr>"
        // $('.' + letter + '_INFO').append('</tr>');
    }
    str += "</table>";
    $('.' + letter + '_INFO').append(str);

}

function handler_image() {
    $('.loader').show();
    $.ajax('/handler_image', {
        type: 'POST',
        data: JSON.stringify({'path': path, 'angle': parseInt(document.getElementById('numb_angle').value)}),
        contentType: 'application/json',
        dataType: 'json',
        success: function(data, textStatus, jqXHR){
            console.log(data);
            // response = JSON.parse(data);
            response = data;
            if (response['status'] === 'ok') {
                alert(response['handler_img']);
                handler_img_path = response['handler_img'];
                console.log(response['data']);
                super_info['status'] = true;
                super_info['data'] = response['data'];
            }
            else {
                alert('Не удалось найти пост');
                super_info['status'] = false;
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert(errorThrown);
            super_info['status'] = false;
        },
        complete: function(){
            $('.loader').hide();
        }
    });

}

function changeImage() {
    if (handler_img_path != null) {
        var imageParent = document.getElementById("myimage");
        imageParent.src = handler_img_path+ "?" + new Date().getTime();;
        imageZoom("myimage", "myresult");
    }


    

}



