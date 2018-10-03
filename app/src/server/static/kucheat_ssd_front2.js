const player = document.getElementById('player');
const snapshotCanvas = $('#snapshot');
const captureButton = document.getElementById('capture');
const sendButton = document.getElementById('send');
const img = document.getElementById('image');
let screwImageBlob;
let imageCapture;
const imageWidth = 320
const imageHeight = 240
const url = 'https://www.mawile.work/detect'
var handleSuccess = function(stream) {
    // Attach the video stream to the video element and autoplay.
    player.srcObject = stream;
    imageCapture = new ImageCapture(stream.getVideoTracks()[0]);
    getCapabilities();
};
function getCapabilities() {
    imageCapture.getPhotoCapabilities().then(function(capabilities) {
        console.log('Camera capabilities:', capabilities);
        if (capabilities.zoom.max > 0) {
            zoomInput.min = capabilities.zoom.min;
            zoomInput.max = capabilities.zoom.max;
            zoomInput.value = capabilities.zoom.current;
            zoomInput.classList.remove('hidden');
        }
    }).catch(function(error) {
        console.log('getCapabilities() error: ', error);
    });
}
captureButton.addEventListener('click', function() {
    imageCapture.takePhoto().then(function(blob) {
        screwImageBlob = blob
        console.log('Took photo:', blob);
        img.classList.remove('hidden');
        img.src = URL.createObjectURL(blob);
    }).catch(function(error) {
        console.log('takePhoto() error: ', error);
    });
});
sendButton.addEventListener('click', function() {
    var context = snapshotCanvas[0].getContext('2d');
    $("#response").text("送信！")
    console.log(url)
    fetch(url, {
        method: 'POST',
        body: screwImageBlob
    }).then(function(response) {
        return response.json();
    }).then(function(json) {
        var image = new Image();
        var reader = new FileReader();
        var results = json
        $("#response").text(JSON.stringify(json))
        reader.onload = function(evt) {
            image.onload = function() {
                let imageWidthRatio = image.width / imageWidth
                let imageHeightRatio = image.height / imageHeight
                snapshotCanvas[0].width = imageWidth
                snapshotCanvas[0].height = imageHeight
                context.drawImage(image, 0, 0,image.width,image.height,0,0,imageWidth,imageHeight); //canvasに画像を転写
                results.forEach(result => {
                    context.font = "20px gradient";
                    var resultXmin = result.xmin / imageWidthRatio;
                    var resultYmin = result.ymin / imageHeightRatio;
                    var resultXmax = result.xmax / imageWidthRatio;
                    var resultYmax = result.ymax / imageHeightRatio
                    context.fillText(result.class_name, resultXmin , resultYmin - 3);
                    context.strokeRect(resultXmin, resultYmin, resultXmax - resultXmin, resultYmax - resultYmin)
                });
            }
            image.src = evt.target.result;
        }
        reader.readAsDataURL(screwImageBlob);
    });
})
const constraints = {
    advanced: [{
        facingMode: "environment"
    }]
};
navigator.mediaDevices.getUserMedia({
    video: {
        facingMode: { ideal: "environment" }
    }
})
    .then(handleSuccess);