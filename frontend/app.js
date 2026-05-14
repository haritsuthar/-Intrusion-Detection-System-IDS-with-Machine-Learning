async function postJSON(url, data) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const json = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = json && json.error ? json.error : `Request failed: ${res.status}`;
    throw new Error(msg);
  }
  return json;
}

function showStatus(id, message, type = 'loading') {
  const el = document.getElementById(id);
  if (!el) return;
  
  el.style.display = 'block';
  el.textContent = message;
  el.className = `status ${type}`;
}

function hideStatus(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = 'none';
}

function setText(id, txt) {
  const el = document.getElementById(id);
  if (el) el.textContent = txt;
}

function setHTML(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

function renderPlot(imgName) {
  const plotsEl = document.getElementById('plots');
  if (!plotsEl) return;
  
  const plotItem = document.createElement('div');
  plotItem.className = 'plot-item';
  
  const title = document.createElement('div');
  title.className = 'plot-title';
  title.textContent = imgName.replace('_', ' ');
  
  const img = document.createElement('img');
  img.src = `/plots/${imgName}.png`;
  img.alt = imgName;
  img.onerror = () => {
    plotItem.innerHTML = `<div class="small">Failed to load ${imgName}</div>`;
  };
  
  plotItem.appendChild(title);
  plotItem.appendChild(img);
  plotsEl.appendChild(plotItem);
}

function getInputValue(id) {
  const el = document.getElementById(id);
  if (!el) return undefined;
  return el.value;
}

function toNumberOrZero(v) {
  const n = Number(v);
  return Number.isFinite(n) ? n : 0;
}

function buildFeaturesFromForm() {
  // Get all the remaining features with default values
  const features = {
    protocol_type: getInputValue('protocol_type'),
    service: getInputValue('service'),
    flag: getInputValue('flag'),
    duration: toNumberOrZero(getInputValue('duration')),
    src_bytes: toNumberOrZero(getInputValue('src_bytes')),
    dst_bytes: toNumberOrZero(getInputValue('dst_bytes')),
    
    // Set defaults for features not in the simple form
    land: 0,
    wrong_fragment: 0,
    urgent: 0,
    hot: 0,
    num_failed_logins: toNumberOrZero(getInputValue('num_failed_logins')),
    logged_in: 1, // Assume logged in for normal traffic
    num_compromised: 0,
    root_shell: 0,
    su_attempted: 0,
    num_root: 0,
    num_file_creations: 0,
    num_shells: 0,
    num_access_files: 0,
    num_outbound_cmds: 0,
    is_host_login: 0,
    is_guest_login: 0,
    count: toNumberOrZero(getInputValue('count')),
    srv_count: toNumberOrZero(getInputValue('count')), // Use same as count
    serror_rate: 0.0,
    srv_serror_rate: 0.0,
    rerror_rate: 0.0,
    srv_rerror_rate: 0.0,
    same_srv_rate: 1.0,
    diff_srv_rate: 0.0,
    srv_diff_host_rate: 0.0,
    dst_host_count: 9,
    dst_host_srv_count: 9,
    dst_host_same_srv_rate: 1.0,
    dst_host_diff_srv_rate: 0.0,
    dst_host_same_src_port_rate: 0.11,
    dst_host_srv_diff_host_rate: 0.0,
    dst_host_serror_rate: 0.0,
    dst_host_srv_serror_rate: 0.0,
    dst_host_rerror_rate: 0.0,
    dst_host_srv_rerror_rate: 0.0,
  };
  
  return features;
}

function renderPredictionResult(result) {
  const resultEl = document.getElementById('predictResult');
  if (!resultEl) return;
  
  const prediction = result.prediction || 'Unknown';
  const confidence = result.confidence || result.probability_attack || 0;
  
  const isAttack = prediction.toLowerCase().includes('attack');
  const confidencePercent = Math.round(confidence * 100);
  
  const html = `
    <div class="prediction-result">
      <h3>🔍 Analysis Result</h3>
      <div style="display: flex; align-items: center; gap: 15px; margin: 15px 0;">
        <div style="font-size: 2em;">
          ${isAttack ? '🚨' : '✅'}
        </div>
        <div>
          <div style="font-size: 1.2em; font-weight: bold; color: ${isAttack ? '#dc3545' : '#28a745'};">
            ${prediction}
          </div>
          <div class="small">
            Attack Probability: ${confidencePercent}%
          </div>
        </div>
      </div>
      <div class="confidence-bar">
        <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
      </div>
      <div class="small" style="margin-top: 10px;">
        ${isAttack ? 
          'This connection shows suspicious patterns that may indicate malicious activity.' : 
          'This connection appears to be normal network traffic.'}
      </div>
    </div>
  `;
  
  resultEl.innerHTML = html;
}

async function trainModel() {
  const trainBtn = document.getElementById('trainBtn');
  trainBtn.disabled = true;
  trainBtn.textContent = '🔄 Training...';
  
  showStatus('trainStatus', 'Initializing training process...', 'loading');
  setText('trainMetrics', '');
  hideStatus('predictStatus');
  setHTML('predictResult', '');
  
  const plotsEl = document.getElementById('plots');
  if (plotsEl) plotsEl.innerHTML = '';

  try {
    const data = await postJSON('/train', {});
    
    showStatus('trainStatus', `✅ Training completed successfully!`, 'success');
    
    if (data.metrics) {
      setText('trainMetrics', `Model accuracy: ${(data.metrics.accuracy * 100).toFixed(2)}%`);
    }
    
    if (data.plots) {
      // Render the plots
      ['confusion_matrix', 'roc_curve', 'feature_importance'].forEach(plotName => {
        setTimeout(() => renderPlot(plotName), 500); // Small delay for better UX
      });
    }
    
  } catch (e) {
    showStatus('trainStatus', `❌ Training failed: ${e.message}`, 'error');
    setText('trainMetrics', '');
  } finally {
    trainBtn.disabled = false;
    trainBtn.textContent = '🚀 Start Training';
  }
}

async function predictFromFeatures() {
  const predictBtn = document.getElementById('predictBtn');
  predictBtn.disabled = true;
  predictBtn.textContent = '🔄 Analyzing...';
  
  showStatus('predictStatus', 'Analyzing network traffic patterns...', 'loading');
  setHTML('predictResult', '');
  
  try {
    const features = buildFeaturesFromForm();
    const res = await postJSON('/predict', { features });

    showStatus('predictStatus', '✅ Analysis complete', 'success');
    renderPredictionResult(res);

    // Show plots if available
    if (res.plots) {
      const plotsEl = document.getElementById('plots');
      if (plotsEl && plotsEl.children.length === 0) {
        ['confusion_matrix', 'roc_curve', 'feature_importance'].forEach(renderPlot);
      }
    }
    
  } catch (e) {
    showStatus('predictStatus', `❌ Analysis failed: ${e.message}`, 'error');
    setHTML('predictResult', '');
  } finally {
    predictBtn.disabled = false;
    predictBtn.textContent = '🔮 Predict Threat';
  }
}

async function predictRawJSON() {
  const raw = document.getElementById('rawJson').value;
  if (!raw || !raw.trim()) {
    showStatus('predictStatus', '❌ Please paste JSON data first', 'error');
    return;
  }

  let payload;
  try {
    payload = JSON.parse(raw);
  } catch {
    showStatus('predictStatus', '❌ Invalid JSON format', 'error');
    return;
  }

  const predictRawBtn = document.getElementById('predictRawBtn');
  predictRawBtn.disabled = true;
  predictRawBtn.textContent = '🔄 Analyzing...';
  
  showStatus('predictStatus', 'Analyzing custom JSON data...', 'loading');
  setHTML('predictResult', '');
  
  try {
    const res = await postJSON('/predict', payload);
    showStatus('predictStatus', '✅ Analysis complete', 'success');
    renderPredictionResult(res);
  } catch (e) {
    showStatus('predictStatus', `❌ Analysis failed: ${e.message}`, 'error');
    setHTML('predictResult', '');
  } finally {
    predictRawBtn.disabled = false;
    predictRawBtn.textContent = '🔍 Analyze JSON';
  }
}

// Initialize the application
window.addEventListener('DOMContentLoaded', () => {
  const trainBtn = document.getElementById('trainBtn');
  if (trainBtn) trainBtn.addEventListener('click', trainModel);

  const predictBtn = document.getElementById('predictBtn');
  if (predictBtn) predictBtn.addEventListener('click', predictFromFeatures);

  const predictRawBtn = document.getElementById('predictRawBtn');
  if (predictRawBtn) predictRawBtn.addEventListener('click', predictRawJSON);
  
  // Hide status elements initially
  hideStatus('trainStatus');
  hideStatus('predictStatus');
});

