
let data_path;
let dd = false;
let path;
function init(data){
    data_path = data;
}

function load_image() {
    var e = document.getElementById("img_list");
    var imageParent = document.getElementById("myimage");
    imageParent.src = data_path[e.value];
    path = data_path[e.value];
    imageZoom("myimage", "myresult");
}

function imageZoom(imgID, resultID) {
    dd = false;
    var img, lens, result, cx, cy;
    img = document.getElementById(imgID);
    result = document.getElementById(resultID);

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
    lens.addEventListener("mouseup", changeDD);

    img.addEventListener("mousemove", moveLens);
//    img.addEventListener("touchmove", moveLens);
    img.addEventListener("mouseup", changeDD);


    function changeDD(e){
        dd = !dd;
    }
    function moveLens(e) {
        if (dd) {
            return;
        }
        var pos, x, y;
        e.preventDefault();
        pos = getCursorPos(e);
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
        lens.style.left = x + "px";
        lens.style.top = y + "px";
        result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
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

function handler_image() {

    $.ajax('/handler_image', {
        type: 'POST',
        data: path,
        contentType: 'application/json',
        success: function(data, textStatus, jqXHR){
            response = JSON.parse(data);
            if (response['status'] === 'ok') {
                alert(23);
            }
            else {
                alert('Не удалось найти пост');
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert(errorThrown);
        },
        complete: function(){
            $('.loading').hide();
        }
    });

}