document.addEventListener("DOMContentLoaded", function () {
  const uploadForm = document.getElementById("upload-form");
  const imageUpload = document.getElementById("image-upload");
  const previewPlaceholder = document.getElementById("preview-placeholder");
  const resultsPlaceholder = document.getElementById("results-placeholder");

  uploadForm.addEventListener("submit", function (e) {
    e.preventDefault();

    if (imageUpload.files.length === 0) {
      alert("Please upload an image.");
      return;
    }

    const file = imageUpload.files[0];
    const formData = new FormData();
    formData.append("file", file);

    // Display uploaded image in the preview box
    const reader = new FileReader();
    reader.onload = function (e) {
      previewPlaceholder.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image" style="max-width: 100%; max-height: 200px;">`;
    };
    reader.readAsDataURL(file);

    // Send image to Flask for classification
    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          resultsPlaceholder.textContent = data.error;
        } else {
          const { result } = data;
          resultsPlaceholder.innerHTML = `
            <p><strong>Class:</strong> ${result.class}</p>
            <p><strong>Confidence:</strong> ${result.confidence}</p>
          `;
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        resultsPlaceholder.textContent = "An error occurred while classifying the image.";
      });
  });
});
