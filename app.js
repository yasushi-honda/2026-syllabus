// ========================================
// Markdown Copy & Page Interactions
// ========================================

document.addEventListener('DOMContentLoaded', () => {
  const COPY_ICON = '<svg viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>';
  const CHECK_ICON = '<svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>';

  document.querySelectorAll('.copy-md-btn').forEach(btn => {
    // Store original label safely
    const originalLabel = btn.textContent.trim();

    btn.addEventListener('click', async () => {
      const mdId = btn.dataset.mdSource;
      const mdEl = document.getElementById(mdId);
      if (!mdEl) return;

      try {
        await navigator.clipboard.writeText(mdEl.textContent);
        showCopied(btn, originalLabel);
      } catch {
        // Fallback for older browsers
        const ta = document.createElement('textarea');
        ta.value = mdEl.textContent;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        showCopied(btn, originalLabel);
      }
    });
  });

  function showCopied(btn, originalLabel) {
    btn.classList.add('copied');
    // Clear existing content safely
    while (btn.firstChild) btn.removeChild(btn.firstChild);
    // Add check icon via DOM
    const iconSpan = document.createElement('span');
    iconSpan.className = 'btn-icon';
    btn.appendChild(iconSpan);
    btn.appendChild(document.createTextNode(' Copied!'));

    setTimeout(() => {
      btn.classList.remove('copied');
      while (btn.firstChild) btn.removeChild(btn.firstChild);
      const copyIconSpan = document.createElement('span');
      copyIconSpan.className = 'btn-icon';
      btn.appendChild(copyIconSpan);
      btn.appendChild(document.createTextNode(' ' + originalLabel));
    }, 2000);
  }

  // Self-check quiz: answers are judged in the page only. Nothing is stored or sent.
  document.querySelectorAll('.quiz').forEach(quiz => {
    const answer = quiz.dataset.answer;
    const choices = quiz.querySelectorAll('.quiz-choice');
    const feedback = quiz.querySelector('.quiz-feedback');
    const result = quiz.querySelector('.quiz-result');
    const retry = quiz.querySelector('.quiz-retry');

    choices.forEach(choice => {
      choice.addEventListener('click', () => {
        const isCorrect = choice.dataset.choice === answer;
        choices.forEach(c => {
          c.disabled = true;
          if (c.dataset.choice === answer) c.classList.add('is-correct');
        });
        if (!isCorrect) choice.classList.add('is-wrong');
        result.textContent = isCorrect ? '正解です' : '不正解です（正解: ' + answer + '）';
        feedback.hidden = false;
      });
    });

    retry.addEventListener('click', () => {
      choices.forEach(c => {
        c.disabled = false;
        c.classList.remove('is-correct', 'is-wrong');
      });
      feedback.hidden = true;
      choices[0].focus();
    });
  });
});
