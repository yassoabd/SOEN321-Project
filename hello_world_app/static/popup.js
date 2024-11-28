//popup
document.addEventListener("DOMContentLoaded", function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        const tab = tabs[0];
        extractAndAnalyzePolicy(tab);
    });
});

function extractAndAnalyzePolicy(tab) {
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: extractTextFromPage
    }, (results) => {
        const policyText = results[0].result;
        const analysisSummaryElement = document.getElementById('analysis-summary');
        const loadingTextElement = document.getElementById('loading-text');
        
        // If no text was extracted, show an error
        if (!policyText) {
            analysisSummaryElement.innerHTML = "<p class='error'>Could not extract Policy text.</p>";
            return;
        }

        // Show loading text while waiting for analysis
        loadingTextElement.textContent = "Analyzing policy...";

        // Send the extracted text server
        fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ policyText: policyText })
        })
        .then(response => response.json())
        .then(data => {
            if (data.summary) {
                analysisSummaryElement.textContent = data.summary;
            } else if (data.error) {
                analysisSummaryElement.innerHTML = `<p class='error'>Error: ${data.error}</p>`;
            } else {
                analysisSummaryElement.innerHTML = "<p class='error'>Failed to analyze the policy.</p>";
            }
        })
        .catch(error => {
            console.error('Error:', error);
            analysisSummaryElement.innerHTML = "<p class='error'>Failed to connect to the analysis server.</p>";
        });
    });
}

// Extract the text from the current webpage
function extractTextFromPage() {
    return document.body.innerText;
}
