    document.getElementById('predictForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      const features = {};
      for (let [key, value] of formData.entries()) {
        features[key] = isNaN(value) ? value : parseFloat(value);
      }

      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ features })
      });

      const data = await response.json();
      const resultBox = document.getElementById('resultBox');
      if (data.stroke_prediction === 1) {
        resultBox.innerHTML = `🔴 High Stroke Risk<br>Confidence: ${data.confidence}`;
        resultBox.style.color = 'red';
      } else if (data.stroke_prediction === 0) {
        resultBox.innerHTML = `🟢 Low Stroke Risk<br>Confidence: ${data.confidence}`;
        resultBox.style.color = 'green';
      } else {
        resultBox.innerHTML = '⚠️ Error occurred';
        resultBox.style.color = 'orange';
      }
    });