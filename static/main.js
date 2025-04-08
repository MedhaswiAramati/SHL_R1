async function getRecommendations() {
    const query = document.getElementById("queryInput").value;
    const url = document.getElementById("urlInput").value;
  
    const res = await fetch("/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query, url }),
    });
  
    const data = await res.json();
    const resultDiv = document.getElementById("results");
  
    if (data.error) {
      resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
      return;
    }
  
    if (!data.recommendations.length) {
      resultDiv.innerHTML = "<p>No recommendations found.</p>";
      return;
    }
  
    let html = `<table><tr><th>Name</th><th>URL</th><th>Remote Support</th></tr>`;
    data.recommendations.forEach(item => {
      html += `<tr><td>${item.name}</td><td><a href="${item.url}" target="_blank">Link</a></td><td>${item.remote}</td></tr>`;
    });
    html += "</table>";
    resultDiv.innerHTML = html;
  }
  