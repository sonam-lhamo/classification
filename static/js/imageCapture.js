document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video-feed');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture-btn');
    const submitButton = document.getElementById('submit-btn');
    const retakeButton = document.getElementById('retake-btn');
    const capturedImage = document.getElementById('captured-image');
    const cameraContainer = document.querySelector('.camera-container');
    const clickWrapper = document.querySelector('.click-wrapper');

    // Access the camera
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (error) {
            console.error('Error accessing the camera:', error);
        });

    captureButton.addEventListener('click', function () {
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Show the captured image
        capturedImage.src = canvas.toDataURL('image/png');
        capturedImage.style.display = 'block';
        submitButton.style.display = 'block';
        retakeButton.style.display = 'block';
        cameraContainer.style.display = 'none';
        clickWrapper.style.display = 'flex';
    });

    // Submit the captured image
    submitButton.addEventListener('click', function () {
        alert('Image submitted!');
        resetInterface();
    });

    // Retake the picture
    retakeButton.addEventListener('click', function () {
        capturedImage.style.display = 'none';
        submitButton.style.display = 'none';
        retakeButton.style.display = 'none';
        cameraContainer.style.display = 'flex';
        clickWrapper.style.display = 'none';
    });

    // Function to reset the interface
    function resetInterface() {
        capturedImage.style.display = 'none';
        submitButton.style.display = 'none';
        retakeButton.style.display = 'none';
        cameraContainer.style.display = 'flex';
        clickWrapper.style.display = 'none';
    }
});
