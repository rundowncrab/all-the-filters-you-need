//Function to display the images selected 
async function loadImage(imageNumber) {
    var input = document.getElementById('image' + imageNumber);
    var displayDiv = document.getElementById('imageDisplay' + imageNumber);
    var file = input.files[0]; // Get the file selected

    if (file) {
        var reader = new FileReader();
        
        // Set up what happens when the image is loaded
        reader.onload = function(e) {
            var img = new Image();
            img.src = e.target.result;
            img.alt = "Selected Image " + imageNumber;
            
            // Clear any previous images and display the new one
            displayDiv.innerHTML = ''; // Clear previous image
            displayDiv.appendChild(img);
        };
        
        reader.readAsDataURL(file); // Read the file as a data URL
    } else {
        displayDiv.innerHTML = "No image selected.";
    }
}


// Function to handle the form submission and image mixing
async function submitImages() {
    const image1 = document.getElementById('image1').files[0];
    const image2 = document.getElementById('image2').files[0];

    // Validate that both images are selected
    if (!image1 || !image2) {
        alert('Please select both images to mix.');
        return;
    }

    // Prepare form data to send the images to the backend
    const formData = new FormData();
    formData.append('image1', image1);
    formData.append('image2', image2);
    console.log("beforeAPI");
    
    // Send images to FastAPI for blending
    const response = await fetch('http://127.0.0.1:8000/mix-images/', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    // Display the blended image
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `<h3>${data.message}</h3><img src="data:image/png;base64,${data.blended_image}" />`;
    
    // Optionally, display the uploaded images
    const imageDisplay1 = document.getElementById('imageDisplay1');
    const imageDisplay2 = document.getElementById('imageDisplay2');
    imageDisplay1.innerHTML = `<img src="${URL.createObjectURL(image1)}" />`;
    imageDisplay2.innerHTML = `<img src="${URL.createObjectURL(image2)}" />`;
}
