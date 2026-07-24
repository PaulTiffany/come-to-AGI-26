(() => {
  const initialBudget = 12;
  let budget = 0;
  let angle = 0;
  let timer = null;
  let events = [{ seq: 0, type: 'session.created', budget: 0, angle: 0 }];
  const controls = {
    grant: document.querySelector('#grant'),
    step: document.querySelector('#step'),
    run: document.querySelector('#run'),
    forbidden: document.querySelector('#forbidden'),
    stop: document.querySelector('#stop')
  };
  const field = document.querySelector('#agentField');
  const meter = document.querySelector('#meterFill');
  const budgetText = document.querySelector('#budgetText');
  const status = document.querySelector('#flowStatus');
  const trace = document.querySelector('#trace');
  const verdict = document.querySelector('#traceVerdict');

  function append(type, detail = {}) {
    events.push({ seq: events.length, type, budget, angle, ...detail });
    render();
  }
  function closeRun() {
    if (timer) window.clearInterval(timer);
    timer = null;
    controls.run.textContent = '2B. Run continuously';
  }
  function move() {
    if (budget <= 0) {
      closeRun();
      append('channel.closed', { reason: 'budget-exhausted' });
      status.textContent = 'The allowance ran out. The agent stopped.';
      return;
    }
    budget -= 1;
    angle = (angle + 17) % 360;
    append('agent.moved');
    status.textContent = 'The agent moved only the generated field.';
    if (budget === 0) move();
  }
  function render() {
    const open = budget > 0;
    controls.step.disabled = !open;
    controls.run.disabled = !open;
    controls.forbidden.disabled = !open;
    meter.style.width = `${(budget / initialBudget) * 100}%`;
    budgetText.textContent = open ? `${budget} of ${initialBudget} moves remain.` : 'Nothing granted.';
    field.style.transform = `rotate(${angle}deg) scale(${1 + (initialBudget - budget) * 0.008})`;
    trace.innerHTML = [...events].reverse().slice(0, 18).map(event => `<li><strong>${event.type}</strong> · b${event.budget} · a${event.angle}</li>`).join('');
    const valid = events.every((event, index) => event.seq === index && event.budget >= 0 && event.budget <= initialBudget);
    verdict.textContent = valid ? 'PASS' : 'FAIL';
    verdict.className = valid ? 'status-pass' : 'status-fail';
  }
  controls.grant.addEventListener('click', () => {
    closeRun(); budget = initialBudget; append('channel.opened'); status.textContent = 'The agent is allowed, but paused.';
  });
  controls.step.addEventListener('click', move);
  controls.run.addEventListener('click', () => {
    if (timer) { closeRun(); append('flow.paused'); status.textContent = 'The agent is paused.'; return; }
    append('flow.started'); controls.run.textContent = '2B. Pause'; status.textContent = 'The agent is moving inside the allowance.';
    timer = window.setInterval(move, 420);
  });
  controls.forbidden.addEventListener('click', () => {
    closeRun(); budget = 0; append('proposal.denied', { reason: 'human-origin-protected' }); status.textContent = 'Forbidden move blocked. Permission ended.';
  });
  controls.stop.addEventListener('click', () => {
    closeRun(); budget = 0; angle = 0; append('human.interrupt'); append('generated.rewound'); status.textContent = 'You stopped it and rewound generated work.';
  });
  document.querySelector('#downloadTrace').addEventListener('click', () => {
    const blob = new Blob([JSON.stringify({ schema: 'bgi-open-build.flow-trace.v1', events }, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'bgi-open-build-flow-trace.json'; a.click(); URL.revokeObjectURL(url);
  });
  render();

  const evidenceStatus = document.querySelector('#evidenceStatus');
  const evidenceCards = document.querySelector('#evidenceCards');
  const bundleHash = document.querySelector('#bundleHash');
  fetch('evidence/evidence-index.json', { cache: 'no-store' })
    .then(response => { if (!response.ok) throw new Error(`HTTP ${response.status}`); return response.json(); })
    .then(index => {
      if (index.schema !== 'bgi-open-build.evidence-index.v1') throw new Error('schema mismatch');
      evidenceStatus.textContent = `${index.items.length} certified artifacts loaded.`;
      bundleHash.textContent = index.bundle_sha256 || 'not recorded';
      evidenceCards.innerHTML = index.items.map(item => {
        const pass = item.policy_ok && item.source_ran && item.notebook_ran && item.validation_passed;
        const links = Object.entries(item.links || {}).map(([label, href]) => `<a href="evidence/${href}">${label}</a>`).join('');
        return `<article class="panel evidence-card"><span class="eyebrow">${item.kind || 'certificate'}</span><h3>${item.title}</h3><strong class="${pass ? 'status-pass' : 'status-fail'}">${pass ? 'PASS' : 'FAIL'}</strong><dl><div><dt>Policy</dt><dd>${String(item.policy_ok)}</dd></div><div><dt>Source ran</dt><dd>${String(item.source_ran)}</dd></div><div><dt>Notebook ran</dt><dd>${String(item.notebook_ran)}</dd></div><div><dt>Validation</dt><dd>${String(item.validation_passed)}</dd></div><div><dt>Source SHA-256</dt><dd>${item.source_sha256 || '—'}</dd></div><div><dt>Notebook SHA-256</dt><dd>${item.notebook_sha256 || '—'}</dd></div></dl><div class="evidence-links">${links}</div></article>`;
      }).join('');
    })
    .catch(error => {
      evidenceStatus.innerHTML = `Evidence upload surface is ready. Add <code>evidence/evidence-index.json</code> and the finalized Notebook Compiler files. <small>${String(error.message)}</small>`;
      evidenceCards.innerHTML = '<article class="panel evidence-card"><span class="eyebrow">Awaiting Codex upload</span><h3>Four green notebook certificates</h3><p>Continuation value · discrete shadow charge · online-optimal equivalence · belief-sensitive boundary.</p><a href="evidence/README.md">Open upload contract →</a></article>';
    });
})();
