// Function to handle the file upload
document.getElementById("fileUploadForm").addEventListener("submit", function (event) {
    console.log("File upload form submitted"); // Add this line
    event.preventDefault();
    
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file.");
        return;
    }

    const formData = new FormData();
    formData.append("csv_file", file);

    // Log the formData to check if it's correct
    console.log("File Upload FormData:", formData);

    // Send POST request to the backend API for file upload
    fetch("http://127.0.0.1:5000/predict/csv", {
        method: "POST",
        body: formData,
    })
    .then((response) => {
        console.log("Response Status:", response.status);
        return response.json();
    })
    .then((json) => {
        console.log("Response JSON:", json);

        // Display prediction results for file upload
        const predictionResult = json.Prediction;
        const sampleNumbers = json["Sample No"];

        if (predictionResult.length === 0 || sampleNumbers.length === 0) {
            alert("No prediction results found.");
            return;
        }

        // Display prediction results for file upload
        const resultText = predictionResult.map((value, index) => {
            return `Sample No ${sampleNumbers[index]}: ${value === "0" ? "Negative" : "Positive"}`;
        }).join("\n");

        document.getElementById("predictionResult").textContent = resultText;
    })
    .catch((error) => {
        console.error("Error:", error);
    });
});

// Function to handle form submission
document.getElementById("predictionForm").addEventListener("submit", function (event) {
    event.preventDefault();

    // Get user input data and parse them as floats or integers
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        // Use parseInt() for specific fields
        if (["Sample No", "DIM( Days In Milk)", "Avg(7 days). Daily MY( L )", "Kg. milk 305 ( Kg )"].includes(key)) {
            data[key] = parseInt(value); // Parse as integer
        } else {
            data[key] = parseFloat(value); // Parse as float
        }
    });

    // Log the data to check if it's correct
    console.log("Form Data:", data);

    // Send POST request to the backend API for form data
    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
    .then((response) => {
        console.log("Response Status:", response.status);
        return response.json();
    })
    .then((json) => {
        console.log("Response JSON:", json);

        // Display prediction result for form input
        const predictionResult = json.Prediction[0];

        let resultText;
        if (predictionResult === "0") {
            resultText = "Negative";
        } else if (predictionResult === "1") {
            resultText = "Positive";
        } else {
            resultText = "Unknown"; // Handle other cases if needed
        }

        document.getElementById("predictionResult").textContent = resultText;
    })
    .catch((error) => {
        console.error("Error:", error);
    });
});

