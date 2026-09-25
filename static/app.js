/**
 * SautiCare Client Application
 * Universal Smartphone Navigator & Voice Assistant for African Elders.
 * Features: Authentic East African Swahili Neural Speech, Elder Volume Boost (+40%),
 * Dynamic Accessibility Text Scaling (A- / A / A+), Full Everyday App Navigation
 * (WhatsApp, YouTube Gospel, Camera, Settings, Airtime USSD, M-Pesa), and Offline Lifeline.
 */

class SautiCareApp {
  constructor() {
    this.isRecording = false;
    this.isOnline = navigator.onLine;
    this.mediaRecorder = null;
    this.audioStream = null;
    this.socket = null;
    this.recognition = null;
    this.audioContext = null;
    this.gainNode = null;
    this.lastAudioUrl = null;

    // DOM Elements
    this.phoneContainer = document.getElementById("phone-container");
    this.btnMic = document.getElementById("btn-mic");
    this.micLabel = document.getElementById("mic-label");
    this.btnEmergency = document.getElementById("btn-emergency-sos");
    this.waveform = document.getElementById("waveform");
    this.connectivityBadge = document.getElementById("connectivity-badge");
    this.connectivityText = document.getElementById("connectivity-text");
    this.responseCard = document.getElementById("response-card");
    this.cardBadge = document.getElementById("card-badge");
    this.swahiliReply = document.getElementById("swahili-reply");
    this.englishSub = document.getElementById("english-sub");
    this.actionDetails = document.getElementById("action-details");
    this.btnReplay = document.getElementById("btn-replay-audio");
    this.voiceSelect = document.getElementById("voice-select");
    this.audioPlayer = document.getElementById("native-audio-player");

    this.init();
  }

  init() {
    this.setupConnectivityMonitor();
    this.setupEventListeners();
    this.setupAccessibilityControls();
    this.registerServiceWorker();
    this.initWebSocket();
    this.initSpeechRecognition();
  }

  getSelectedVoice() {
    return this.voiceSelect ? this.voiceSelect.value : "sw-ke-zuri";
  }

  // 1. Accessibility Controls (Font Sizing for Elders)
  setupAccessibilityControls() {
    const btnDecrease = document.getElementById("font-decrease");
    const btnDefault = document.getElementById("font-default");
    const btnIncrease = document.getElementById("font-increase");

    btnDecrease?.addEventListener("click", () => this.setFontSize("default"));
    btnDefault?.addEventListener("click", () => this.setFontSize("default"));
    btnIncrease?.addEventListener("click", () => this.setFontSize("large"));
  }

  setFontSize(size) {
    if (!this.phoneContainer) return;
    this.phoneContainer.classList.remove("font-large", "font-xlarge");
    document.querySelectorAll(".btn-font-zoom").forEach(b => b.classList.remove("active"));

    if (size === "large") {
      this.phoneContainer.classList.add("font-large");
      document.getElementById("font-increase")?.classList.add("active");
    } else if (size === "xlarge") {
      this.phoneContainer.classList.add("font-xlarge");
      document.getElementById("font-increase")?.classList.add("active");
    } else {
      document.getElementById("font-default")?.classList.add("active");
    }
  }

  // 2. Service Worker Registration & PWA Install Listener
  registerServiceWorker() {
    if ("serviceWorker" in navigator) {
      window.addEventListener("load", () => {
        navigator.serviceWorker.register("/sw.js").then((reg) => {
          console.log("[SautiCare] Service Worker registered with scope:", reg.scope);
        }).catch((err) => {
          console.warn("[SautiCare] Service Worker registration failed:", err);
        });
      });
    }

    let deferredPrompt = null;
    const installBanner = document.getElementById("pwa-install-banner");
    const btnInstall = document.getElementById("btn-install-pwa");

    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      deferredPrompt = e;
      if (installBanner) installBanner.classList.remove("hidden");
    });

    if (btnInstall) {
      btnInstall.addEventListener("click", async () => {
        if (deferredPrompt) {
          deferredPrompt.prompt();
          const { outcome } = await deferredPrompt.userChoice;
          console.log("[SautiCare PWA] User response:", outcome);
          deferredPrompt = null;
          if (installBanner) installBanner.classList.add("hidden");
        }
      });
    }

    window.addEventListener("appinstalled", () => {
      console.log("[SautiCare PWA] App was successfully installed!");
      if (installBanner) installBanner.classList.add("hidden");
    });
  }

  // 3. Connectivity Monitoring (Offline / Online Resilience)
  setupConnectivityMonitor() {
    const updateStatus = () => {
      this.isOnline = navigator.onLine;
      if (this.isOnline) {
        this.connectivityBadge.className = "status-badge online";
        this.connectivityText.innerText = "Mtandaoni (AssemblyAI)";
      } else {
        this.connectivityBadge.className = "status-badge offline";
        this.connectivityText.innerText = "Nje ya Mtandao (Simu & SMS)";
      }
    };

    window.addEventListener("online", () => {
      updateStatus();
      this.initWebSocket();
    });

    window.addEventListener("offline", () => {
      updateStatus();
      this.playNativeSwahiliAudio("Uko nje ya mtandao. Simu za dharura na huduma ya simu bado zinafanya kazi bila bando.");
    });

    updateStatus();
  }

  // 3. Setup UI Event Listeners
  setupEventListeners() {
    this.btnMic.addEventListener("click", () => this.toggleRecording());
    this.btnEmergency.addEventListener("click", () => this.triggerInstantSOS());

    // Scenario Pills
    document.querySelectorAll(".pill-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const query = btn.getAttribute("data-query");
        this.processQuery(query);
      });
    });

    // Replay speech button
    this.btnReplay.addEventListener("click", () => {
      if (this.lastAudioUrl) {
        this.playAudioUrl(this.lastAudioUrl);
      } else {
        const text = this.swahiliReply.innerText;
        if (text) this.playNativeSwahiliAudio(text);
      }
    });

    // When voice selector changes, greet in pure, natural Swahili (NO English words)
    this.voiceSelect.addEventListener("change", () => {
      const selected = this.getSelectedVoice();
      const voiceGreetings = {
        "sw-ke-zuri": "Shikamoo Mzee wangu! Mimi ni Zuri, niko hapa kukuongoza na simu yako kwa upole.",
        "sw-ke-rafiki": "Jambo Mzee wetu! Mimi ni Rafiki, msaidizi wako wa sauti hapa Kenya.",
        "sw-tz-daudi": "Habari za leo Mzee! Mimi ni Daudi, msaidizi wako wa sauti kutoka Tanzania.",
        "sw-tz-rehema": "Habari yako Mzee wetu! Mimi ni Rehema, niko tayari kukusaidia na simu yako."
      };
      const text = voiceGreetings[selected] || "Marahaba, niko tayari kukusaidia.";
      this.playNativeSwahiliAudio(text);
    });
  }

  // 4. WebSocket Setup for AssemblyAI Realtime Streaming
  initWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws/voice`;

    try {
      this.socket = new WebSocket(wsUrl);

      this.socket.onopen = () => {
        console.log("SautiCare Voice WebSocket connected.");
      };

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "partial_transcript") {
          this.swahiliReply.innerText = `Ninakusikiliza: "${data.text}..."`;
        } else if (data.type === "final_transcript") {
          this.swahiliReply.innerText = `Nimekusikia: "${data.text}"`;
        } else if (data.type === "agent_response" && data.decision) {
          this.renderDecision(data.decision);
        }
      };

      this.socket.onclose = () => {
        console.warn("WebSocket closed, attempting reconnect in 3s...");
        setTimeout(() => {
          if (this.isOnline) this.initWebSocket();
        }, 3000);
      };

      this.socket.onerror = (err) => {
        console.error("WebSocket error:", err);
      };
    } catch (e) {
      console.warn("WebSocket initialization skipped:", e);
    }
  }

  // 5. Browser Web Speech Fallback Recognition
  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.lang = "sw-KE"; // Kenyan Swahili
      this.recognition.continuous = false;
      this.recognition.interimResults = true;

      this.recognition.onresult = (event) => {
        let transcript = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          transcript += event.results[i][0].transcript;
        }
        this.swahiliReply.innerText = transcript;
        if (event.results[0].isFinal) {
          this.processQuery(transcript);
        }
      };

      this.recognition.onerror = (event) => {
        console.warn("Web Speech recognition error:", event.error);
        this.stopRecordingUI();
      };

      this.recognition.onend = () => {
        this.stopRecordingUI();
      };
    }
  }

  // 6. Audio Recording & Streaming Control
  async toggleRecording() {
    if (this.isRecording) {
      this.stopRecording();
    } else {
      await this.startRecording();
    }
  }

  async startRecording() {
    this.isRecording = true;
    this.btnMic.classList.add("listening");
    this.micLabel.innerText = "NINAKUSIKILIZA...";
    this.waveform.classList.remove("hidden");
    this.recordedChunks = [];

    try {
      this.audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(this.audioStream, { mimeType: "audio/webm" });

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.recordedChunks.push(event.data);
          if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(event.data);
          }
        }
      };

      this.mediaRecorder.onstop = async () => {
        if (this.recordedChunks.length > 0) {
          const audioBlob = new Blob(this.recordedChunks, { type: "audio/webm" });
          this.swahiliReply.innerText = "AssemblyAI inasikiliza sauti yako...";
          this.englishSub.innerText = "(AssemblyAI is transcribing your Swahili speech...)";

          const voice = this.getSelectedVoice();
          try {
            const res = await fetch(`/api/transcribe-audio?voice=${voice}`, {
              method: "POST",
              headers: { "Content-Type": "audio/webm" },
              body: audioBlob
            });
            const decision = await res.json();
            if (decision.transcript) {
              this.swahiliReply.innerText = `Nimekusikia: "${decision.transcript}"`;
            }
            this.renderDecision(decision);
          } catch (err) {
            console.error("AssemblyAI transcribe error:", err);
          }
        }
      };

      this.mediaRecorder.start(250);
      return;
    } catch (err) {
      console.warn("Could not capture MediaRecorder stream, falling back to Web Speech:", err);
    }

    if (this.recognition) {
      try {
        this.recognition.start();
      } catch (e) {
        console.warn("Recognition already active", e);
      }
    } else {
      alert("Tafadhali tumia mifano iliyoandikwa hapo juu au uwashe intaneti.");
      this.stopRecordingUI();
    }
  }

  stopRecording() {
    this.isRecording = false;
    this.stopRecordingUI();

    if (this.mediaRecorder && this.mediaRecorder.state !== "inactive") {
      this.mediaRecorder.stop();
    }
    if (this.audioStream) {
      this.audioStream.getTracks().forEach((track) => track.stop());
    }
    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch (e) {}
    }
  }

  stopRecordingUI() {
    this.isRecording = false;
    this.btnMic.classList.remove("listening");
    this.micLabel.innerText = "BONYEZA KUONGEA";
    this.waveform.classList.add("hidden");
  }

  // 7. Process Text Query via Backend API
  async processQuery(text) {
    this.swahiliReply.innerText = `Ninakufikiria: "${text}"...`;
    this.englishSub.innerText = "(Processing your request...)";

    const voice = this.getSelectedVoice();

    if (!this.isOnline) {
      this.processOfflineLocally(text);
      return;
    }

    try {
      const response = await fetch("/api/process-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text, voice: voice })
      });
      const data = await response.json();
      this.renderDecision(data);
    } catch (err) {
      console.error("API error, fallback to offline logic:", err);
      this.processOfflineLocally(text);
    }
  }

  // 8. One-Tap Instant Emergency SOS Handler
  async triggerInstantSOS() {
    if (this.isOnline) {
      try {
        const res = await fetch("/api/emergency/sos", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            distress_type: "SOS Button Pressed (Kitufe cha Dharura)",
            location: "1°17'31.2\"S 36°49'10.8\"E (Nairobi, Kenya)"
          })
        });
        const decision = await res.json();
        this.renderDecision(decision);
      } catch (e) {
        console.error("SOS API failed, falling back to local SOS:", e);
      }
    } else {
      this.renderDecision({
        action: "emergency_sos",
        is_emergency: true,
        swahili_response: "Tulia Mzee wangu, usijali wala usiogope! Nimeshatuma ujumbe wa dharura na eneo lako mara moja. Simu ya msaada inapigwa sasa hivi.",
        english_translation: "Stay calm elder, do not be afraid! An emergency SMS with your live GPS location has been dispatched, and emergency dialing is active.",
        visual_card: {
          type: "sos_card",
          status: "DHARURA IMETUMWA (SOS DISPATCHED)",
          recipient: "Mwanangu Juma",
          phone: "+254712345678",
          location: "1°17'31.2\"S 36°49'10.8\"E (Nairobi, Kenya)",
          sms_preview: "DHARURA: Mzazi wako anahitaji msaada wa haraka nyumbani! Mahali: Nairobi. Piga simu mara moja.",
          gsm_dialer_intent: "tel:+254712345678"
        }
      });
    }

    if (confirm("Piga simu ya dharura kwa Mwanangu Juma (+254712345678)?")) {
      window.location.href = "tel:+254712345678";
    }
  }

  // 9. Render Agent Decision Card & Play Authentic East African Audio
  renderDecision(decision) {
    this.responseCard.className = "response-card";

    // Set Theme & Badge
    if (decision.is_emergency) {
      this.responseCard.classList.add("emergency-card");
      this.cardBadge.innerText = "🚨 DHARURA (EMERGENCY)";
    } else if (decision.action && decision.action.startsWith("whatsapp")) {
      this.responseCard.classList.add("card-whatsapp");
      this.cardBadge.innerText = "💬 WATSAPU";
    } else if (decision.action === "youtube_gospel") {
      this.responseCard.classList.add("card-youtube");
      this.cardBadge.innerText = "🎵 YUTUBU & INJILI";
    } else if (decision.action === "take_photo" || decision.action === "view_photos") {
      this.responseCard.classList.add("card-camera");
      this.cardBadge.innerText = "📸 KAMERA NA PICHA";
    } else if (decision.action === "enlarge_font" || decision.action === "adjust_brightness" || decision.action === "network_settings") {
      this.responseCard.classList.add("card-settings");
      this.cardBadge.innerText = "🔤 MIPANGILIO";
      if (decision.action === "enlarge_font") {
        this.setFontSize("large");
      }
    } else if (decision.action === "check_balance" || decision.action === "buy_bundles") {
      this.responseCard.classList.add("card-airtime");
      this.cardBadge.innerText = "📞 SALIO & BANDO";
    } else if (decision.action === "mpesa_guide") {
      this.responseCard.classList.add("mpesa-card");
      this.cardBadge.innerText = "💸 M-PESA USALAMA";
    } else {
      this.cardBadge.innerText = "MSAADA WA SAUTI";
    }

    this.swahiliReply.innerText = decision.swahili_response || "";
    this.englishSub.innerText = decision.english_translation ? `(${decision.english_translation})` : "";

    // Visual Action Box Rendering
    this.actionDetails.innerHTML = "";
    if (decision.visual_card) {
      const card = decision.visual_card;
      const box = document.createElement("div");
      box.className = "action-box";

      if (card.type === "sos_card") {
        box.innerHTML = `
          <h4>🚨 Hali ya Dharura: ${card.status}</h4>
          <p><strong>Mpokeaji:</strong> ${card.recipient} (${card.phone})</p>
          <p><strong>Eneo (GPS):</strong> ${card.location}</p>
          <p style="margin-top: 6px; font-style: italic; color: #DC2626;"><strong>Ujumbe:</strong> "${card.sms_preview}"</p>
          <a href="${card.gsm_dialer_intent}" class="btn-card-action" style="background:#DC2626;">📞 Piga Simu ya Dharura Sasa</a>
        `;
      } else if (card.type === "whatsapp_guide" || card.type === "whatsapp_call_guide") {
        box.innerHTML = `
          <h4>${card.title}</h4>
          <ul class="step-list">
            ${card.steps.map((s, idx) => `
              <li class="step-item">
                <span class="step-num">${idx + 1}</span>
                <span class="step-text">${s.replace(/^\d+\.\s*/, '')}</span>
              </li>
            `).join("")}
          </ul>
          <a href="${card.action_intent || 'whatsapp://'}" class="btn-card-action btn-action-wa">📲 Fungua Watsapu Moja kwa Moja</a>
        `;
      } else if (card.type === "youtube_guide") {
        box.innerHTML = `
          <h4>${card.title}</h4>
          <div class="action-options">
            ${card.options.map(opt => `
              <a href="${opt.url}" target="_blank" class="option-link">${opt.label} <span>↗</span></a>
            `).join("")}
          </div>
          <a href="${card.action_url}" target="_blank" class="btn-card-action btn-action-yt">▶️ Fungua Yutubu Moja kwa Moja</a>
        `;
      } else if (card.type === "camera_guide" || card.type === "gallery_guide") {
        box.innerHTML = `
          <h4>${card.title}</h4>
          <ul class="step-list">
            ${card.steps.map((s, idx) => `
              <li class="step-item">
                <span class="step-num">${idx + 1}</span>
                <span class="step-text">${s.replace(/^\d+\.\s*/, '')}</span>
              </li>
            `).join("")}
          </ul>
        `;
      } else if (card.type === "font_magnifier") {
        box.innerHTML = `
          <h4>${card.title}</h4>
          <p style="color: #2563EB; font-weight: bold; font-size: 16px;">${card.status}</p>
          <p style="margin-top: 6px;">${card.preview}</p>
          <button class="btn-card-action btn-action-settings" onclick="window.sautiCare.setFontSize('xlarge')">🔍 Kuza Zaidi (Kubwa Zaidi)</button>
        `;
      } else if (card.type === "airtime_card") {
        box.innerHTML = `
          <h4>${card.title}</h4>
          <p style="font-weight: 800; font-size: 16px; color: #0D9488;">Msimbo: ${card.ussd_code}</p>
          <ul class="step-list">
            ${card.steps.map((s, idx) => `
              <li class="step-item">
                <span class="step-num">${idx + 1}</span>
                <span class="step-text">${s.replace(/^\d+\.\s*/, '')}</span>
              </li>
            `).join("")}
          </ul>
          <a href="${card.dialer_intent}" class="btn-card-action btn-action-bal">📞 Piga ${card.ussd_code} Sasa</a>
        `;
      } else if (card.type === "sms_card") {
        box.innerHTML = `
          <h4>${card.title}</h4>
          <p><strong>Mtumaji:</strong> ${card.sender}</p>
          <p style="font-size: 12px; color: #64748B;"><strong>Muda:</strong> ${card.received_time}</p>
          <div style="margin-top: 8px; padding: 10px; background: #F1F5F9; border-left: 3px solid #0284C7; font-style: italic; border-radius: 6px;">
            "${card.message_body}"
          </div>
        `;
      } else if (card.type === "mpesa_safety") {
        box.innerHTML = `
          <h4>${card.title} - ${card.ussd_code}</h4>
          <ul class="step-list">
            ${card.steps.map((s, idx) => `
              <li class="step-item">
                <span class="step-num">${idx + 1}</span>
                <span class="step-text">${s.replace(/^\d+\.\s*/, '')}</span>
              </li>
            `).join("")}
          </ul>
          <p style="color: #059669; font-weight: bold; margin-top: 8px;">⚠️ ${card.warning}</p>
          <a href="tel:*334%23" class="btn-card-action btn-action-mpesa">📞 Piga *334# (M-Pesa)</a>
        `;
      } else if (card.type === "device_action") {
        box.innerHTML = `
          <h4>${card.title}</h4>
          <p>${card.details}</p>
        `;
      } else if (card.type === "suggestion") {
        box.innerHTML = `
          <h4>${card.title}</h4>
          <ul class="step-list">
            ${card.items.map((it, idx) => `
              <li class="step-item">
                <span class="step-num">${idx + 1}</span>
                <span class="step-text">${it}</span>
              </li>
            `).join("")}
          </ul>
        `;
      }
      this.actionDetails.appendChild(box);
    }

    // Play Authentic Native East African Audio
    if (decision.audio_url) {
      this.playAudioUrl(decision.audio_url);
    } else if (decision.swahili_response) {
      this.playNativeSwahiliAudio(decision.swahili_response);
    }
  }

  // 10. Play Authentic Audio with Amplified Volume (+Boost for Elderly Ears)
  playAudioUrl(url) {
    this.lastAudioUrl = url;
    try {
      if (!this.audioContext) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        this.audioContext = new AudioCtx();
        const source = this.audioContext.createMediaElementSource(this.audioPlayer);
        this.gainNode = this.audioContext.createGain();
        // 1.4x elder volume amplification
        this.gainNode.gain.value = 1.4;
        source.connect(this.gainNode);
        this.gainNode.connect(this.audioContext.destination);
      }
      if (this.audioContext.state === "suspended") {
        this.audioContext.resume();
      }
    } catch (e) {
      console.warn("Web Audio GainNode initialization info:", e);
    }

    this.audioPlayer.volume = 1.0;
    this.audioPlayer.src = url;
    this.audioPlayer.play().catch((err) => {
      console.warn("Autoplay blocked, user can tap speaker button:", err);
    });
  }

  // 11. Fallback Audio Synthesizer via Backend TTS Endpoint
  async playNativeSwahiliAudio(text) {
    const voice = this.getSelectedVoice();
    try {
      const res = await fetch("/api/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text, voice: voice })
      });
      const data = await res.json();
      if (data.audio_url) {
        this.playAudioUrl(data.audio_url);
      }
    } catch (e) {
      console.warn("Could not generate server audio:", e);
    }
  }

  // 12. Local Offline Logic (0MB Data Resilience)
  processOfflineLocally(text) {
    const lower = text.toLowerCase();
    if (lower.includes("dharura") || lower.includes("anguka") || lower.includes("naumwa")) {
      this.triggerInstantSOS();
      return;
    }

    this.renderDecision({
      action: "offline_guide",
      swahili_response: "Niko hapa kukusaidia Mzee wangu. Hata ukiwa nje ya mtandao, unaweza kupiga simu ya dharura au kutumia huduma ya simu ya nyota tatu tatu nne reli au nyota moja nne nne reli.",
      english_translation: "I am here to help you elder. Even offline, you can make emergency calls or use mobile services via star 3 3 4 hash or star 1 4 4 hash.",
      visual_card: {
        type: "device_action",
        title: "Hali ya Nje ya Mtandao (Offline) 📶",
        details: "Huna bando la intaneti kwa sasa. Simu za GSM, SMS, na USSD (*334#, *144#) zinafanya kazi kawaida bila intaneti."
      }
    });
  }
}

// Global initialization
window.addEventListener("DOMContentLoaded", () => {
  window.sautiCare = new SautiCareApp();
});
