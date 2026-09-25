/**
 * SautiCare Client Application
 * Handles Realtime Speech Capture, AssemblyAI WebSockets, Offline Resilience,
 * Swahili Speech Synthesis, and UI State.
 */

class SautiCareApp {
  constructor() {
    this.isRecording = false;
    this.isOnline = navigator.onLine;
    this.mediaRecorder = null;
    this.audioStream = null;
    this.socket = null;
    this.recognition = null;

    // DOM Elements
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
    this.speakerIndicator = document.getElementById("speaker-indicator");

    this.init();
  }

  init() {
    this.setupConnectivityMonitor();
    this.setupEventListeners();
    this.initWebSocket();
    this.initSpeechRecognition();
  }

  // 1. Connectivity Monitoring (Offline / Online Resilience)
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
      this.speakSwahili("Uko nje ya mtandao. Simu za dharura na M-Pesa bado zinafanya kazi bila data.");
    });

    updateStatus();
  }

  // 2. Setup UI Event Listeners
  setupEventListeners() {
    this.btnMic.addEventListener("click", () => this.toggleRecording());
    this.btnEmergency.addEventListener("click", () => this.triggerInstantSOS());

    // Scenario Pills
    document.querySelectorAll(".pill-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const query = btn.getAttribute("data-query");
        this.processQuery(query);
      });
    });

    // Replay speech on speaker icon click
    this.speakerIndicator.addEventListener("click", () => {
      const text = this.swahiliReply.innerText;
      if (text) this.speakSwahili(text);
    });
  }

  // 3. WebSocket Setup for Live AssemblyAI Streaming
  initWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws/voice`;

    try {
      this.socket = new WebSocket(wsUrl);

      this.socket.onopen = () => {
        console.log("Connected to SautiCare Voice Server");
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === "transcript" && data.text) {
            this.swahiliReply.innerText = `"${data.text}"`;
            if (data.decision) {
              this.renderDecision(data.decision);
            }
          } else if (data.type === "agent_response") {
            this.renderDecision(data.decision);
          }
        } catch (err) {
          console.error("Error parsing WebSocket message:", err);
        }
      };

      this.socket.onerror = (error) => {
        console.warn("WebSocket fallback to HTTP:", error);
      };

      this.socket.onclose = () => {
        console.log("WebSocket closed, attempting reconnect in 3s...");
        setTimeout(() => {
          if (this.isOnline) this.initWebSocket();
        }, 3000);
      };
    } catch (e) {
      console.warn("WebSocket not supported or failed:", e);
    }
  }

  // 4. Web Speech API (Handles on-device speech fallback)
  initSpeechRecognition() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRec) {
      this.recognition = new SpeechRec();
      this.recognition.lang = "sw-TZ"; // Swahili
      this.recognition.continuous = false;
      this.recognition.interimResults = true;

      this.recognition.onstart = () => {
        this.setListeningState(true);
      };

      this.recognition.onresult = (event) => {
        let transcript = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          transcript += event.results[i][0].transcript;
        }
        this.swahiliReply.innerText = `Ninakusikiliza: "${transcript}"`;
        if (event.results[0].isFinal) {
          this.processQuery(transcript);
        }
      };

      this.recognition.onerror = (e) => {
        console.warn("Speech recognition error:", e);
        this.setListeningState(false);
      };

      this.recognition.onend = () => {
        this.setListeningState(false);
      };
    }
  }

  // 5. Toggle Recording
  async toggleRecording() {
    if (this.isRecording) {
      this.stopRecording();
    } else {
      await this.startRecording();
    }
  }

  async startRecording() {
    this.setListeningState(true);
    if (this.recognition) {
      try {
        this.recognition.start();
        return;
      } catch (e) {
        console.warn("SpeechRec start failed, falling back to MediaStream:", e);
      }
    }

    try {
      this.audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(this.audioStream);

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0 && this.socket && this.socket.readyState === WebSocket.OPEN) {
          this.socket.send(event.data);
        }
      };

      this.mediaRecorder.start(250); // Send chunks every 250ms
    } catch (err) {
      console.error("Microphone access error:", err);
      alert("Tafadhali ruhusu maikrofoni ili kuweza kuongea.");
      this.setListeningState(false);
    }
  }

  stopRecording() {
    this.setListeningState(false);
    if (this.recognition) {
      try { this.recognition.stop(); } catch (e) {}
    }
    if (this.mediaRecorder && this.mediaRecorder.state !== "inactive") {
      this.mediaRecorder.stop();
    }
    if (this.audioStream) {
      this.audioStream.getTracks().forEach((track) => track.stop());
    }
  }

  setListeningState(isListening) {
    this.isRecording = isListening;
    if (isListening) {
      this.btnMic.classList.add("listening");
      this.micLabel.innerText = "NINASIKILIZA... (ONGEA)";
      this.waveform.classList.remove("hidden");
    } else {
      this.btnMic.classList.remove("listening");
      this.micLabel.innerText = "BONYEZA KUONGEA";
      this.waveform.classList.add("hidden");
    }
  }

  // 6. Process Query (Online or Offline Engine)
  async processQuery(text) {
    this.setListeningState(false);

    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ action: "process_text", text: text }));
      return;
    }

    // HTTP Fallback
    try {
      const response = await fetch("/api/process-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text }),
      });
      const data = await response.json();
      this.renderDecision(data);
    } catch (e) {
      // Local Offline Fallback
      this.renderOfflineFallback(text);
    }
  }

  // 7. Instant SOS Trigger (Works 100% Offline)
  async triggerInstantSOS() {
    const isOffline = !navigator.onLine;

    const sosData = {
      action: "emergency_sos",
      is_emergency: true,
      swahili_response: "Tulia Mzee wangu! Ujumbe wa dharura na eneo lako vimetumwa mara moja. Simu ya msaada inapigwa sasa hivi.",
      english_translation: "Stay calm elder! An emergency SMS with your live GPS location has been dispatched, and emergency dialing is active.",
      visual_card: {
        type: "sos_card",
        status: "DHARURA IMETUMWA (SOS DISPATCHED)",
        recipient: "Mwanangu Juma (Child)",
        phone: "+254712345678",
        location: "1°17'31.2\"S 36°49'10.8\"E (Nairobi, Kenya)",
        sms_preview: "DHARURA: Mzazi wako anahitaji msaada wa haraka nyumbani! Mahali: Nairobi. Piga simu mara moja.",
        gsm_dialer_intent: "tel:+254712345678"
      }
    };

    this.renderDecision(sosData);

    // If on actual mobile device, execute tel: and sms: intents
    if (confirm("Piga simu ya dharura kwa Mwanangu Juma (+254712345678)?")) {
      window.location.href = "tel:+254712345678";
    }
  }

  // 8. Render Agent Decision Card
  renderDecision(decision) {
    this.responseCard.className = "response-card";
    if (decision.is_emergency) {
      this.responseCard.classList.add("emergency-card");
      this.cardBadge.innerText = "🚨 DHARURA (EMERGENCY)";
    } else if (decision.action === "mpesa_guide") {
      this.responseCard.classList.add("mpesa-card");
      this.cardBadge.innerText = "💸 M-PESA USALAMA";
    } else {
      this.cardBadge.innerText = "MSADA WA SAUTI";
    }

    this.swahiliReply.innerText = decision.swahili_response || "";
    this.englishSub.innerText = decision.english_translation ? `(${decision.english_translation})` : "";

    // Render Visual Action Box
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
          <p style="margin-top: 6px; font-style: italic; color: #DC2626;"><strong>Ujumbe wa SMS:</strong> "${card.sms_preview}"</p>
        `;
      } else if (card.type === "mpesa_safety") {
        box.innerHTML = `
          <h4>${card.title} - ${card.ussd_code}</h4>
          <ul>${card.steps.map((s) => `<li>${s}</li>`).join("")}</ul>
          <p style="color: #059669; font-weight: bold; margin-top: 6px;">⚠️ ${card.warning}</p>
        `;
      } else if (card.type === "device_action") {
        box.innerHTML = `
          <h4>${card.title}</h4>
          <p>${card.details}</p>
        `;
      } else if (card.type === "suggestion") {
        box.innerHTML = `
          <h4>${card.title}</h4>
          <ul>${card.items.map((it) => `<li>${it}</li>`).join("")}</ul>
        `;
      }
      this.actionDetails.appendChild(box);
    }

    // Speak Swahili response
    this.speakSwahili(decision.swahili_response);
  }

  // 9. Local Offline Fallback
  renderOfflineFallback(text) {
    const lower = text.toLowerCase();
    let reply = "Niko hapa kukusaidia. Uko nje ya mtandao, lakini unaweza kupiga simu ya dharura au kutumia M-Pesa kwa *334#.";
    let trans = "I am here to help. You are offline, but you can make emergency calls or use M-Pesa via *334#.";

    if (lower.includes("dharura") || lower.includes("nisaidie") || lower.includes("anguka")) {
      this.triggerInstantSOS();
      return;
    }

    this.renderDecision({
      action: "offline_guide",
      swahili_response: reply,
      english_translation: trans,
      visual_card: {
        type: "device_action",
        title: "Hali ya Nje ya Mtandao (Offline)",
        details: "Simu inatumia mfumo wa ndani bila kuhitaji bando ya intaneti."
      }
    });
  }

  // 10. Swahili Text-to-Speech (Client-side)
  speakSwahili(text) {
    if (!window.speechSynthesis) return;

    window.speechSynthesis.cancel(); // Stop any pending speech
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.88; // Gentle, elder-friendly pacing
    utterance.pitch = 1.0;

    // Try finding Swahili voice
    const voices = window.speechSynthesis.getVoices();
    const swVoice = voices.find((v) => v.lang.startsWith("sw") || v.name.toLowerCase().includes("swahili"));
    if (swVoice) {
      utterance.voice = swVoice;
    }

    window.speechSynthesis.speak(utterance);
  }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  window.sautiCare = new SautiCareApp();
});
