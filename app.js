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
  // build_dict.py の EXCLUDE_TAGS と同じ（＋ボタン自身）
  const SKIP = 'script,style,textarea,svg,ruby,code,pre,title,noscript,option,[data-no-furigana],.furigana-toggle,.furigana-notice';

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
    let applying = false;
    let observer = null;
    let noticeTimer = null;
    const layoutCache = new Map();

    // ボタン（名前は固定。状態は aria-pressed だけで伝える）
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'furigana-toggle';
    btn.setAttribute('aria-pressed', 'false');
    btn.setAttribute('aria-label', 'ふりがな');
    btn.title = '漢字にふりがなをつけます（オン／オフ）';
    const icon = document.createElement('span');
    icon.className = 'furigana-toggle-icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = 'あ';
    const label = document.createElement('span');
    label.className = 'furigana-toggle-label';
    label.setAttribute('aria-hidden', 'true');
    label.textContent = 'ふりがな';
    const state = document.createElement('span');
    state.className = 'furigana-toggle-state';
    state.setAttribute('aria-hidden', 'true');
    state.textContent = 'オフ';
    btn.append(icon, label, state);

    // 画面に見えるお知らせ（読み込みの失敗など）と、読み上げ用の状態通知。どちらもボタンの外に置く
    const notice = document.createElement('div');
    notice.className = 'furigana-notice';
    notice.setAttribute('role', 'status');
    document.body.append(btn, notice);
    document.body.classList.add('has-furigana-toggle');

    function say(message, visible) {
      notice.textContent = message;
      notice.classList.toggle('is-visible', !!visible);   // 見えない通知は読み上げ専用
      clearTimeout(noticeTimer);
      if (visible) noticeTimer = setTimeout(() => { notice.classList.remove('is-visible'); }, 6000);
    }

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

    // 1つのテキストノードをルビに置き換える
    function annotate(node, dict) {
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
    }

    function eligible(n) {
      if (n.nodeType !== 3 || !KANJI.test(n.nodeValue)) return false;
      const p = n.parentElement;
      return !!p && !p.closest(SKIP);
    }

    function apply(dict) {
      applying = true;
      try {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
          acceptNode(n) { return eligible(n) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT; }
        });
        const nodes = [];
        while (walker.nextNode()) nodes.push(walker.currentNode);
        nodes.forEach(n => annotate(n, dict));
      } finally {
        applying = false;
      }
      // 操作のあとに作られる文字（クイズの結果、「すべて開く／閉じる」など）にも付ける
      observer = new MutationObserver(muts => {
        if (applying) return;
        applying = true;
        try {
          muts.forEach(m => m.addedNodes.forEach(n => { if (eligible(n)) annotate(n, dict); }));
        } finally {
          applying = false;
        }
      });
      observer.observe(document.body, { childList: true, subtree: true });
    }

    function remove() {
      if (observer) { observer.disconnect(); observer = null; }
      applying = true;
      try {
        records.forEach(rec => {
          const first = rec.inserted.find(n => n.parentNode);
          if (!first) return;   // 操作で消えた文字は戻さない
          first.parentNode.insertBefore(rec.node, first);
          rec.inserted.forEach(n => { if (n.parentNode) n.parentNode.removeChild(n); });
        });
      } finally {
        applying = false;
      }
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
        say(on ? 'ふりがなをつけました' : 'ふりがなをなくしました', false);
        if (persist) writeSaved(on);
      } catch (e) {
        remove();   // 途中まで置き換えていたら元に戻す
        isOn = false;
        say('ふりがなを読み込めませんでした。時間をおいて、もう一度おしてください', true);
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
