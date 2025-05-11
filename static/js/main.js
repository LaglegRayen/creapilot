document.addEventListener('DOMContentLoaded', function() {
  const loading = document.getElementById('loadingIndicator');
  const showLoading = () => loading.classList.remove('d-none');
  const hideLoading = () => loading.classList.add('d-none');

  // Video Idea Generator
  document.getElementById('videoIdeaForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const topic = document.getElementById('videoTopic').value;
    document.getElementById('videoIdeasResults').innerHTML = '';
    showLoading();
    try {
      const res = await fetch('/api/video_ideas/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ topic })
      });
      const data = await res.json();
      if (res.ok) {
        let html = '';
        data.ideas.forEach(item => {
          html += `<div class="card mb-2"><div class="card-body"><h5>${item.title}</h5><p>${item.description}</p><p><strong>${item.value}</strong></p></div></div>`;
        });
        document.getElementById('videoIdeasResults').innerHTML = html;
      } else {
        document.getElementById('videoIdeasResults').innerHTML = `<div class="alert alert-danger">${data.error || 'Error generating ideas.'}</div>`;
      }
    } catch (err) {
      document.getElementById('videoIdeasResults').innerHTML = `<div class="alert alert-danger">Network error.</div>`;
    }
    hideLoading();
  });

  // Transcript Analyzer
  document.getElementById('transcriptForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const text = document.getElementById('transcriptText').value;
    const fileInput = document.getElementById('transcriptFile');
    const formData = new FormData();
    if (text) formData.append('transcript', text);
    if (fileInput.files.length) formData.append('transcript_file', fileInput.files[0]);
    document.getElementById('transcriptResults').innerHTML = '';
    showLoading();
    try {
      const res = await fetch('/api/transcript_analyzer/', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (res.ok) {
        let html = '<h5>Key Topics:</h5><ul>';
        data.key_topics.forEach(t => { html += `<li>${t}</li>`; });
        html += '</ul><h5>Suggested Angles:</h5><ul>';
        data.angles.forEach(a => { html += `<li>${a}</li>`; });
        html += '</ul><h5>New Video Ideas:</h5>';
        data.new_ideas.forEach(item => {
          html += `<div class="card mb-2"><div class="card-body"><h5>${item.title}</h5><p>${item.description}</p><p><strong>${item.value}</strong></p></div></div>`;
        });
        if (data.quotes && data.quotes.length) {
          html += '<h5>Clip-worthy Quotes:</h5><ul>';
          data.quotes.forEach(q => { html += `<li>${q}</li>`; });
          html += '</ul>';
        }
        document.getElementById('transcriptResults').innerHTML = html;
      } else {
        document.getElementById('transcriptResults').innerHTML = `<div class="alert alert-danger">${data.error || 'Error analyzing transcript.'}</div>`;
      }
    } catch (err) {
      document.getElementById('transcriptResults').innerHTML = `<div class="alert alert-danger">Network error.</div>`;
    }
    hideLoading();
  });

  // Hashtag Assistant
  document.getElementById('hashtagForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const platform = document.getElementById('platformSelect').value;
    const topic = document.getElementById('hashtagTopic').value;
    document.getElementById('hashtagResults').innerHTML = '';
    showLoading();
    try {
      const res = await fetch('/api/hashtags/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ platform, topic })
      });
      const data = await res.json();
      if (res.ok) {
        let html = '<div class="d-flex flex-wrap">';
        data.hashtags.forEach(tag => { html += `<span class="badge bg-secondary me-1 mb-1">${tag}</span>`; });
        html += '</div>';
        document.getElementById('hashtagResults').innerHTML = html;
      } else {
        document.getElementById('hashtagResults').innerHTML = `<div class="alert alert-danger">${data.error || 'Error generating hashtags.'}</div>`;
      }
    } catch (err) {
      document.getElementById('hashtagResults').innerHTML = `<div class="alert alert-danger">Network error.</div>`;
    }
    hideLoading();
  });
}); 