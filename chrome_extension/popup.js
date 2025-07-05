document.getElementById('askBtn').addEventListener('click', async () => {
  const videoId = document.getElementById('videoId').value.trim();
  const question = document.getElementById('question').value.trim();
  const answerDiv = document.getElementById('answer');

  if (!videoId || !question) {
    answerDiv.textContent = 'Please enter both Video ID and a question.';
    return;
  }

  answerDiv.textContent = 'Loading...';

  try {
    const response = await fetch('http://localhost:8000/ask', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({video_id: videoId, question: question})
    });
    if (!response.ok) {
      throw new Error('Backend error: ' + response.status);
    }
    const data = await response.json();
    answerDiv.textContent = data.answer;
  } catch (err) {
    answerDiv.textContent = 'Error: ' + err.message;
  }
}); 