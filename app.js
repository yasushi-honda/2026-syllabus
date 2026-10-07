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

// ========================================
// ふりがなトグル（<body data-furigana="辞書のJSON"> があるページだけ）
// 辞書は tools/furigana/build_dict.py が作る。オンにしたときだけ読み込み、オフの間はDOMを変えない
// （Chromeの翻訳とも競合しない）。選んだ状態は端末に覚えさせる（保存できない環境では毎回オフ）。
// ========================================
(function () {
  'use strict';

  const STORAGE_KEY = 'syllabus-furigana';
  const KANJI = /[㐀-䶿一-鿿々〆]/;
  const SKIP = 'script,style,textarea,svg,ruby,code,pre,title,noscript,[data-no-furigana],.furigana-toggle';

  // build_dict.py の node_key と同じ（FNV-1a 32bit、UTF-16の単位）
  function nodeKey(text) {
    let h = 0x811c9dc5;
    for (let i = 0; i < text.length; i++) {
      h ^= text.charCodeAt(i);
      h = Math.imul(h, 0x01000193) >>> 0;
    }
    return h.toString(16).padStart(8, '0') + '.' + text.length;
  }

  function readSaved() {
    try { return localStorage.getItem(STORAGE_KEY) === 'on'; } catch (e) { return false; }
  }
  function writeSaved(on) {
    try { localStorage.setItem(STORAGE_KEY, on ? 'on' : 'off'); } catch (e) { /* 保存できない環境では毎回オフ */ }
  }

  function init() {
    const src = document.body && document.body.dataset.furigana;
    if (!src) return;

    let dictPromise = null;
    let records = [];   // 置き換えた記録（オフで元に戻す）
    let isOn = false;
    let busy = false;

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'furigana-toggle';
    btn.setAttribute('aria-pressed', 'false');
    btn.title = '漢字にふりがなをつけます（オン／オフ）';
    const icon = document.createElement('span');
    icon.className = 'furigana-toggle-icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = 'あ';
    const label = document.createElement('span');
    label.className = 'furigana-toggle-label';
    label.textContent = 'ふりがな';
    const state = document.createElement('span');
    state.className = 'furigana-toggle-state';
    state.textContent = 'オフ';
    const status = document.createElement('span');
    status.className = 'furigana-status';
    status.setAttribute('role', 'status');
    btn.append(icon, label, state, status);
    document.body.appendChild(btn);
    document.body.classList.add('has-furigana-toggle');

    function render() {
      btn.setAttribute('aria-pressed', isOn ? 'true' : 'false');
      state.textContent = isOn ? 'オン' : 'オフ';
      document.documentElement.classList.toggle('furigana-on', isOn);
    }

    function loadDict() {
      if (!dictPromise) {
        dictPromise = fetch(new URL(src, location.href), { cache: 'default' })
          .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
          .catch(err => { dictPromise = null; throw err; });
      }
      return dictPromise;
    }

    function apply(dict) {
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
        acceptNode(n) {
          if (!KANJI.test(n.nodeValue)) return NodeFilter.FILTER_REJECT;
          const p = n.parentElement;
          return p && p.closest(SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
        }
      });
      const nodes = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      const layoutCache = new Map();
      nodes.forEach(node => {
        const text = node.nodeValue;
        const spans = dict.n[nodeKey(text)];
        if (!spans) return;
        const frag = document.createDocumentFragment();
        let pos = 0;
        spans.forEach(sp => {
          const s = sp[0], l = sp[1], r = sp[2];
          if (s < pos || s + l > text.length) return;
          if (s > pos) frag.appendChild(document.createTextNode(text.slice(pos, s)));
          const ruby = document.createElement('ruby');
          ruby.appendChild(document.createTextNode(text.slice(s, s + l)));
          const rt = document.createElement('rt');
          rt.textContent = r;
          ruby.appendChild(rt);
          frag.appendChild(ruby);
          pos = s + l;
        });
        if (pos === 0) return;
        if (pos < text.length) frag.appendChild(document.createTextNode(text.slice(pos)));
        // 親が flex/grid だと、ルビが別々の項目になって折り返せない。1つの span にまとめて1項目にする
        const parent = node.parentNode;
        if (!layoutCache.has(parent)) layoutCache.set(parent, /flex|grid/.test(getComputedStyle(parent).display));
        let inserted;
        if (layoutCache.get(parent)) {
          const wrap = document.createElement('span');
          wrap.appendChild(frag);
          inserted = [wrap];
          parent.replaceChild(wrap, node);
        } else {
          inserted = Array.from(frag.childNodes);
          parent.replaceChild(frag, node);
        }
        records.push({ node, inserted });
      });
    }

    function remove() {
      records.forEach(rec => {
        const first = rec.inserted.find(n => n.parentNode);
        if (!first) return;
        first.parentNode.insertBefore(rec.node, first);
        rec.inserted.forEach(n => { if (n.parentNode) n.parentNode.removeChild(n); });
      });
      records = [];
    }

    async function setOn(on, persist) {
      if (busy || on === isOn) return;
      busy = true;
      try {
        if (on) {
          apply(await loadDict());
        } else {
          remove();
        }
        isOn = on;
        status.textContent = on ? 'ふりがなをつけました' : 'ふりがなをなくしました';
        if (persist) writeSaved(on);
      } catch (e) {
        status.textContent = 'ふりがなを読み込めませんでした。あとでもう一度お試しください';
        btn.title = status.textContent;
      } finally {
        busy = false;
        render();
      }
    }

    btn.addEventListener('click', () => setOn(!isOn, true));
    render();
    if (readSaved()) setOn(true, false);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
