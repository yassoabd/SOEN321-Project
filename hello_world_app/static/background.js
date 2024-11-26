chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: extractAndAnalyzePolicy
    });
  });
  
  function extractAndAnalyzePolicy() {
    const policyText = document.body.innerText; // Extract the entire page's text
    if (!policyText) {
      alert("Could not extract text from the page.");
      return;
    }
  
    fetch('http://127.0.0.1:5000/analyze', { // Replace with your backend URL if deployed
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ policyText: policyText })
    })
      .then(response => response.json())
      .then(data => {
        if (data.summary) {
          alert(`Analysis Summary:\n${data.summary}`);
        } else {
          console.error('Error:', data.error || 'Unknown error occurred.');
          alert('Failed to analyze the policy.');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Failed to connect to the analysis server.');
      });
  }
  