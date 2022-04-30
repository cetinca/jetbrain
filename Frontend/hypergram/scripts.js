let image = new Image();
let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');

let fileInput = document.getElementById('file-input');
fileInput.addEventListener('change', function (ev) {
    if (ev.target.files) {
        let file = ev.target.files[0];
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function (e) {
            // let image = new Image();
            image.src = e.target["result"];
            image.onload = function (ev) {
                // let canvas = document.getElementById('canvas');
                canvas.width = image.width;
                canvas.height = image.height;
                let ctx = canvas.getContext('2d');
                ctx.drawImage(image, 0, 0);
            }
        }
        let element = document.getElementById("brightness")
        element.value = 0
        element = document.getElementById("contrast")
        element.value = 0
        element = document.getElementById("transparent")
        element.value = 1
    }
});

function truncate(value) {
    if (value < 0) {
        return 0
    } else if (value > 255) {
        return 255
    } else {
        return value
    }
}

document.getElementById('brightness').addEventListener('change', function (ev) {
    change()
});
document.getElementById('transparent').addEventListener('change', function (ev) {
    change()
});
document.getElementById('contrast').addEventListener('change', function (ev) {
    change()
});

function change() {
    let value1 = parseInt(document.getElementById("contrast").value)
    let value0 = parseInt(document.getElementById("brightness").value)
    let value2 = parseFloat(document.getElementById("transparent").value)

    ctx.drawImage(image, 0, 0)
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const pixels = imageData.data;

    let factor = 259 * (255 + value1) / (255 * (259 - value1))
    pixels.forEach(function (pixel, index) {

        if (index % 4 === 0) {
            pixels[index] = truncate(factor * (pixel - 128) + 128 + value0)
        }
        if (index % 4 === 1) {
            pixels[index] = truncate(factor * (pixel - 128) + 128 + value0)
        }
        if (index % 4 === 2) {
            pixels[index] = truncate(factor * (pixel - 128) + 128 + value0)
        }
    })

    if (value2 != 1) {
        pixels.forEach(function (pixel, index) {
            if (index % 4 === 3) {
                pixels[index] = pixel * value2
            }
        })
        pixels.forEach(function (pixel, index) {
            pixels[index] = truncate(pixel)
        })
    }
    imageData.data = pixels
    ctx.putImageData(imageData, 0, 0);
}

document.getElementById("save-button").addEventListener("click", downloadCanvas)

function downloadCanvas(){
    // get canvas data
    let image = canvas.toDataURL();

    // create temporary link
    let tmpLink = document.createElement( 'a' );
    tmpLink.download = 'result.png'; // set the name of the download file
    tmpLink.href = image;

    // temporarily add link to body and initiate the download
    document.body.appendChild( tmpLink );
    tmpLink.click();
    document.body.removeChild( tmpLink );
}
