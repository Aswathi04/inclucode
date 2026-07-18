/* ============================================================
   Vazhikaatti Voice Mode
   Lets a user go through the entire site by voice: filling the
   form, submitting it, hearing results, opening a scheme, and
   navigating back — without touching the screen.

   How it works across page loads:
   Each page load is a fresh JS context (this is a multi-page
   Flask app, not a single-page app), so listening state can't
   literally persist in memory across navigation. Instead, any
   voice-triggered navigation appends `?voice=1` to the target
   URL. On load, each page checks for that flag and, if present,
   auto-starts Voice Mode and speaks its own command list — so
   from the user's perspective the voice session feels continuous
   even though it's technically being handed off page to page.
   ============================================================ */

const VoiceMode = (() => {
  let recognition = null;
  let listening = false;
  let speaking = false;
  let commandList = [];
  let fallbackFn = null;
  let statusEl = null;
  let toggleBtn = null;

  function supported() {
    return ('webkitSpeechRecognition' in window) || ('SpeechRecognition' in window);
  }

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text;
  }

  // Speaks text aloud. Pauses listening first (so the mic doesn't hear
  // its own voice and misfire a command), and resumes listening only
  // after the utterance has genuinely finished — the `speaking` flag
  // stops the recognizer's own onend from restarting it prematurely.
  function speak(text, afterSpeak) {
    speaking = true;
    if (recognition) { try { recognition.abort(); } catch (e) {} }
    window.speechSynthesis.cancel();
    setStatus('🔊 Speaking · സംസാരിക്കുന്നു');
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-IN';
    utterance.rate = 0.95;
    utterance.onend = function () {
      speaking = false;
      if (afterSpeak) afterSpeak();
      // small pause lets any speaker/mic echo tail off before listening resumes
      if (listening) setTimeout(runRecognition, 350);
    };
    window.speechSynthesis.speak(utterance);
  }

  function stopSpeaking() {
    window.speechSynthesis.cancel();
  }

  function runRecognition() {
    if (!listening) return;
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = function (event) {
      const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase().trim();
      handleTranscript(transcript);
    };

    recognition.onerror = function (e) {
      // 'no-speech' fires often during normal silence between commands — not a real error.
      if (e.error === 'no-speech' || e.error === 'aborted') return;
      console.warn('Voice recognition error:', e.error);
    };

    recognition.onend = function () {
      if (listening && !speaking) runRecognition(); // auto-restart, Chrome stops after each utterance
    };

    setStatus('🎙️ Listening · കേൾക്കുന്നു');
    recognition.start();
  }

  function handleTranscript(transcript) {
    if (/^stop$/.test(transcript) || transcript.includes('stop reading') || transcript.includes('stop talking')) {
      stopSpeaking();
      return;
    }
    for (const cmd of commandList) {
      if (cmd.test(transcript)) {
        cmd.action(transcript);
        return;
      }
    }
    if (fallbackFn) fallbackFn(transcript);
  }

  // Extracts a 1-based number from speech: "scheme two", "scheme 2", "open the second one"
  function extractNumber(text) {
    const digitMatch = text.match(/\d+/);
    if (digitMatch) return parseInt(digitMatch[0], 10);
    const words = {
      one: 1, first: 1, two: 2, second: 2, three: 3, third: 3,
      four: 4, fourth: 4, five: 5, fifth: 5, six: 6, sixth: 6,
      seven: 7, seventh: 7, eight: 8, eighth: 8, nine: 9, ninth: 9, ten: 10, tenth: 10
    };
    for (const [word, num] of Object.entries(words)) {
      if (text.includes(word)) return num;
    }
    return null;
  }

  function commands(list, fallback) {
    commandList = list;
    fallbackFn = fallback || null;
  }

  function start() {
    if (!supported()) {
      alert('Voice mode only works in Chrome.');
      return;
    }
    listening = true;
    if (toggleBtn) toggleBtn.textContent = '🎙️ Voice mode: ON · ഓൺ';
    runRecognition();
  }

  function stop() {
    listening = false;
    speaking = false;
    if (recognition) { try { recognition.abort(); } catch (e) {} }
    stopSpeaking();
    setStatus('');
    if (toggleBtn) toggleBtn.textContent = '🎙️ Voice mode · ശബ്ദ മോഡ്';
  }

  function toggle() {
    if (listening) stop(); else start();
  }

  function init(toggleButtonEl, statusElement) {
    toggleBtn = toggleButtonEl;
    statusEl = statusElement;
    toggleBtn.addEventListener('click', toggle);
  }

  function isListening() {
    return listening;
  }

  // Navigates while preserving voice mode across the page load.
  function navigate(url) {
    const sep = url.includes('?') ? '&' : '?';
    window.location.href = url + sep + 'voice=1';
  }

  function cameFromVoice() {
    return new URLSearchParams(window.location.search).get('voice') === '1';
  }

  return {
    init, commands, start, stop, toggle,
    speak, stopSpeaking, navigate, extractNumber,
    supported, isListening, cameFromVoice
  };
})();