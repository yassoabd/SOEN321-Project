document.addEventListener("DOMContentLoaded", function () {
    const analyzeButton = document.getElementById("analyzeBtn");
    const expandButton = document.getElementById("expandBtn");
    const statusMessage = document.getElementById("statusMessage");
    const tosContent = document.getElementById("tosContent");
  
    let fullContent = ""; // To store the full analysis content
  
    // Analyze TOS Button
    analyzeButton.addEventListener("click", function () {
      statusMessage.textContent = "Analyzing...";
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const tab = tabs[0];
        chrome.scripting.executeScript(
          {
            target: { tabId: tab.id },
            function: extractTextFromPage,
          },
          (results) => {
            const policyText = results[0]?.result;
            if (!policyText) {
              statusMessage.textContent = "Error: Could not extract policy text.";
              return;
            }
  
            // Send extracted text to the backend server for analysis
            fetch("http://127.0.0.1:5000/analyze", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ policyText: policyText }),
            })
              .then((response) => response.json())
              .then((data) => {
                if (data.summary) {
                  fullContent = data.summary.replace(/\*\*/g, ""); // Remove markdown `**`
                  const bulletPoints = fullContent
                    .split("- ") // Split text into bullet points
                    .filter((point) => point.trim() !== "") // Remove empty items
                    .map((point) => `<li>${point.trim()}</li>`); // Wrap each point in <li>
                  const truncatedPoints = bulletPoints.slice(0, 3); // Show the first 3 points initially
  
                  tosContent.innerHTML = `<ul>${truncatedPoints.join("")}</ul>`; // Wrap in <ul>
                  tosContent.style.display = "block"; // Show ToS content
                  expandButton.style.display = "inline-block"; // Show the Expand button
                  statusMessage.textContent = "Analysis complete!";
                } else if (data.error) {
                  statusMessage.textContent = `Error: ${data.error}`;
                } else {
                  statusMessage.textContent = "Failed to analyze the policy.";
                }
              })
              .catch((error) => {
                console.error("Error:", error);
                statusMessage.textContent =
                  "Failed to connect to the analysis server.";
              });
          }
        );
      });
    });
  
    // Expand Button
    expandButton.addEventListener("click", function () {
      const bullet_points = fullContent
      // Split text -> bullet points
        .split("- ") 
        // Remove empty space
        .filter((point) => point.trim() !== "") 
        // Wrap each point 
        .map((point) => `<li>${point.trim()}</li>`); 
      tosContent.innerHTML = `<ul>${bullet_points.join("")}</ul>`; 
      // Hide the Expand button after using expand 
      expandButton.style.display = "none"; 
    });
  
    // Function to extract text from the current page
    function extractTextFromPage() {
      return document.body.innerText;
    }
  });