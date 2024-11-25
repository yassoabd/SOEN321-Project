// Select elements
const analyzeButton = document.getElementById("analyze-button");
const policyText = document.getElementById("policy-text");
const policyURL = document.getElementById("policy-url");
const resultContainer = document.getElementById("result-container");

// Analyze Button
analyzeButton.addEventListener("click", () => {
    const text = policyText.value.trim();
    const url = policyURL.value.trim();

    if (!text && !url) {
        alert("Please enter either the privacy policy text or a URL.");
        return;
    }

    resultContainer.innerHTML = "<p>Processing...</p>";

    // Determine input type (text or URL)
    const inputType = text ? "text" : "url";
    const inputData = text || url;

    // Send the request to the unified /analyze endpoint
    fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: inputType, data: inputData })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultContainer.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            } else {
                resultContainer.innerHTML = `<h3>Analysis Result:</h3><p>${data.analysis}</p>`;
            }
        })
        .catch(error => {
            console.error("Error:", error);
            resultContainer.innerHTML = `<p style="color: red;">An error occurred. Please try again later.</p>`;
        });
});
