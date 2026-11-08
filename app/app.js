const $ = id => document.getElementById(id);
$('resume-file').onchange = async () => {
  const file = $('resume-file').files[0];
  if (!file) return;
  if (!/\.(pdf|docx)$/i.test(file.name) || !file.size || file.size > 5 * 1024 * 1024) {
    $('upload-status').textContent = 'Choose a non-empty PDF or Word .docx file up to 5 MB.';
    $('resume-file').value = '';
    return;
  }
  $('results').hidden = true;
  for (const id of ['analyze', 'sample', 'resume-file', 'resume']) $(id).disabled = true;
  $('upload-status').textContent = 'Reading your document…';
  try {
    const response = await fetch('/api/extract', {method: 'POST', headers: {'Content-Type': 'application/octet-stream', 'X-Filename': encodeURIComponent(file.name)}, body: file});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Could not read the document.');
    $('resume').value = data.text;
    $('upload-status').textContent = 'Text extracted. Review and correct it below, then analyze. The uploaded file was not saved.';
  } catch (error) {
    $('upload-status').textContent = error.message + ' Your previous resume text has been kept.';
  } finally {
    for (const id of ['analyze', 'sample', 'resume-file', 'resume']) $(id).disabled = false;
    $('resume-file').value = '';
  }
};
$('sample').onclick = () => {
  $('resume').value = 'FICTIONAL DEMO — Alex Chen, NYU Stern MBA candidate.\nProduct analyst at ExampleCo, 2022–2025. Used SQL to analyze onboarding drop-off. Partnered with design and engineering to test a simpler signup flow, increasing activation from 40% to 47%. Interviewed 12 customers and presented findings to product leadership. Led weekly cross-functional project updates.';
  $('job').value = 'FICTIONAL DEMO — Associate Product Manager. Own product roadmap prioritization, define success metrics, and collaborate with engineering and design. Use SQL and customer research to identify opportunities. Experience with A/B testing, stakeholder communication, and competitive analysis preferred.';
  $('results').hidden = true;
  $('status').textContent = 'Fictional sample loaded. Choose a mode and analyze.';
};
fetch('/api/status').then(r => r.json()).then(data => {
  $('configuration').textContent = data.ai_configured ? 'API key is configured. Provider access is verified only when an analysis succeeds.' : 'AI setup needed: add a valid OPENROUTER_API_KEY to .env and restart. You can explicitly choose Non-AI keyword comparison now.';
}).catch(() => { $('configuration').textContent = 'Cannot reach the local server. Start it with python3 server.py.'; });
$('review-form').onsubmit = async event => {
  event.preventDefault();
  $('results').hidden = true;
  $('analyze').disabled = true;
  $('sample').disabled = true;
  $('resume-file').disabled = true;
  $('status').textContent = 'Analyzing… AI requests may take up to 60 seconds.';
  try {
    const response = await fetch('/api/analyze', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({resume:$('resume').value,job_description:$('job').value,mode:$('mode').value}) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Analysis failed. Try again.');
    for (const field of ['strengths','missing_evidence','improvements']) {
      $(field).replaceChildren(...data.result[field].map(text => { const item = document.createElement('li'); item.textContent = text; return item; }));
    }
    $('result-label').textContent = data.label;
    $('results').hidden = false;
    $('status').textContent = 'Analysis complete. Review your results below.';
  } catch (error) { $('status').textContent = error.message || 'Cannot reach the server. Check that it is running.'; }
  finally { $('analyze').disabled = false; $('sample').disabled = false; $('resume-file').disabled = false; }
};
