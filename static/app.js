/**
 * SautiCare Client Application
 * Universal Smartphone Navigator & Voice Assistant for African Elders.
 * Supports 4 African Regions: Kiswahili (East Africa), Nigerian Pidgin (West Africa),
 * isiZulu (Southern Africa), and Amharic (Horn of Africa).
 */

const PAN_AFRICAN_UI = {
  sw: {
    region: "East Africa (Kiswahili)",
    greetingTitle: "Shikamoo Mzee wetu!",
    greetingSub: "SautiCare inakuongoza kutumia simu yako yote kwa Kiswahili fasaha na sauti kubwa.",
    welcomeBadge: "KARIBU",
    welcomeText: "Bonyeza kitufe kikubwa cha kijani hapa chini na uzungumze kwa Kiswahili. SautiCare itakusaidia na Watsapu, Yutubu, picha, salio, au dharura.",
    welcomeEn: "(Press the big green button below and speak in Swahili. SautiCare will assist with WhatsApp, YouTube gospel, photos, airtime, or emergencies.)",
    sosTitle: "MSAADA WA DHARURA (SOS)",
    sosSub: "Piga simu na tuma ujumbe wa eneo mara moja",
    scenariosTitle: "Chagua huduma unayotaka kuelekezwa:",
    speakerLabel: "Sikiliza",
    micIdle: "BONYEZA KUONGEA",
    micListening: "NINAKUSIKILIZA...",
    voices: [
      { id: "sw-ke-zuri", label: "🇰🇪 Zuri (Mwanamke - Kenya)" },
      { id: "sw-ke-rafiki", label: "🇰🇪 Rafiki (Mwanaume - Kenya)" },
      { id: "sw-tz-daudi", label: "🇹🇿 Daudi (Mwanaume - Tanzania)" },
      { id: "sw-tz-rehema", label: "🇹🇿 Rehema (Mwanamke - Tanzania)" }
    ],
    defaultVoice: "sw-ke-zuri",
    recognitionLang: "sw-KE",
    pills: [
      { cls: "app-pill-wa", icon: "💬", title: "Watsapu:", subtitle: "Sauti", query: "Nataka kutuma ujumbe wa sauti kwa Watsapu" },
      { cls: "app-pill-yt", icon: "🎵", title: "Yutubu:", subtitle: "Nyimbo za Injili", query: "Fungua nyimbo za injili kwenye Yutubu" },
      { cls: "app-pill-cam", icon: "📸", title: "Kamera:", subtitle: "Piga Picha", query: "Nataka kupiga picha ya wajukuu" },
      { cls: "app-pill-set", icon: "🔤", title: "Kuza Maandishi", subtitle: "", query: "Maandishi ni madogo, ongeza ukubwa wa maandishi" },
      { cls: "app-pill-bal", icon: "📞", title: "Salio:", subtitle: "Piga *144#", query: "Salio langu la simu limebaki ngapi" },
      { cls: "app-pill-mpesa", icon: "💸", title: "M-Pesa:", subtitle: "Tuma Pesa", query: "Nataka kutuma pesa kwa M-Pesa" },
      { cls: "app-pill-torch", icon: "🔦", title: "Tochi:", subtitle: "Washa Mwanga", query: "Washa tochi ya simu kuko giza" },
      { cls: "app-pill-sos", icon: "🚑", title: "Dharura:", subtitle: "Msaada", query: "Nisaidie nimeanguka chini naumwa" }
    ]
  },
  ng: {
    region: "West Africa (Nigerian Pidgin)",
    greetingTitle: "Kedu / Salama Elder!",
    greetingSub: "SautiCare dey guide you use your phone well well with clear voice and loud sound.",
    welcomeBadge: "WELCOME",
    welcomeText: "Press this big green button for ground make you talk. SautiCare go help you send WhatsApp voice note, open YouTube gospel, snap photo, or call emergency.",
    welcomeEn: "(Press the big green button below and speak in Pidgin. SautiCare will assist with WhatsApp, YouTube gospel, photos, airtime, or emergencies.)",
    sosTitle: "EMERGENCY SOS HELP 🚨",
    sosSub: "Dial family phone and send your GPS location sharp sharp",
    scenariosTitle: "Choose wetin you wan do for your phone:",
    speakerLabel: "Listen",
    micIdle: "PRESS TO TALK",
    micListening: "DEY LISTEN TO YOU...",
    voices: [
      { id: "ng-ezinne", label: "🇳🇬 Ezinne (Female - Nigeria)" },
      { id: "ng-abeo", label: "🇳🇬 Abeo (Male - Nigeria)" }
    ],
    defaultVoice: "ng-ezinne",
    recognitionLang: "en-NG",
    pills: [
      { cls: "app-pill-wa", icon: "💬", title: "WhatsApp:", subtitle: "Voice Note", query: "I wan send voice note for WhatsApp" },
      { cls: "app-pill-yt", icon: "🎵", title: "YouTube:", subtitle: "Gospel Songs", query: "Play Nigerian gospel worship songs on YouTube" },
      { cls: "app-pill-cam", icon: "📸", title: "Camera:", subtitle: "Snap Photo", query: "I wan snap photo with my camera" },
      { cls: "app-pill-set", icon: "🔤", title: "Make Words Big", subtitle: "", query: "The words too small make am big" },
      { cls: "app-pill-bal", icon: "📞", title: "Airtime:", subtitle: "Dial *310#", query: "How much airtime balance remain" },
      { cls: "app-pill-mpesa", icon: "💸", title: "OPay / Transfer:", subtitle: "Send Money", query: "I wan transfer money with OPay" },
      { cls: "app-pill-torch", icon: "🔦", title: "Flashlight:", subtitle: "Put Light", query: "Turn on torchlight everywhere dark" },
      { cls: "app-pill-sos", icon: "🚑", title: "Emergency:", subtitle: "Help Me", query: "Help me abeg I don fall down" }
    ]
  },
  zu: {
    region: "Southern Africa (isiZulu)",
    greetingTitle: "Sawubona Mkhulu / Gogo!",
    greetingSub: "I-SautiCare ikusiza ukusebenzisa ifoni yakho ngesiZulu esicacile nevolumu ephezulu.",
    welcomeBadge: "SIYAKWEMUKELA",
    welcomeText: "Cindezela inkinobho enkulu eluhlaza ngezansi bese ukhuluma ngesiZulu. I-SautiCare izokusiza nge-WhatsApp, umculo wokholo ku-YouTube, izithombe, noma usizo lwesimo esiphuthumayo.",
    welcomeEn: "(Press the big green button below and speak in isiZulu. SautiCare will assist with WhatsApp, YouTube gospel, photos, airtime, or emergencies.)",
    sosTitle: "USIZO LWESIMO ESIPHUTHUMAYO (SOS) 🚨",
    sosSub: "Shaya ucingo futhi uthumele indawo yakho ngokushesha",
    scenariosTitle: "Khetha lokho ofuna ukukwenza:",
    speakerLabel: "Lalela",
    micIdle: "CINDEZELA UKUKHULUMA",
    micListening: "NGIYAKULALELA...",
    voices: [
      { id: "zu-thando", label: "🇿🇦 Thando (Owesifazane - South Africa)" },
      { id: "zu-themba", label: "🇿🇦 Themba (Owesilisa - South Africa)" }
    ],
    defaultVoice: "zu-thando",
    recognitionLang: "zu-ZA",
    pills: [
      { cls: "app-pill-wa", icon: "💬", title: "WhatsApp:", subtitle: "Ilizwi", query: "Ngifuna ukuthumela umyalezo wezwi ku-WhatsApp" },
      { cls: "app-pill-yt", icon: "🎵", title: "YouTube:", subtitle: "Umculo Wokholo", query: "Dlala umculo wokholo ku-YouTube" },
      { cls: "app-pill-cam", icon: "📸", title: "Ikhamera:", subtitle: "Thatha Isithombe", query: "Ngifuna ukuthatha isithombe" },
      { cls: "app-pill-set", icon: "🔤", title: "Khulisa Amagama", subtitle: "", query: "Amagama mancane kakhulu khulisa" },
      { cls: "app-pill-bal", icon: "📞", title: "Ibhalansi:", subtitle: "Shaya *136#", query: "Ibhalansi yami ingakanani" },
      { cls: "app-pill-mpesa", icon: "💸", title: "eWallet / Imali:", subtitle: "Thumela", query: "Ngifuna ukuthumela imali" },
      { cls: "app-pill-torch", icon: "🔦", title: "Ithoshi:", subtitle: "Khanyisa", query: "Khanyisa ithoshi kumnyama" },
      { cls: "app-pill-sos", icon: "🚑", title: "Isimo Esiphuthumayo:", subtitle: "Usizo", query: "Ngifuna usizo ngiwe phansi" }
    ]
  },
  am: {
    region: "Horn of Africa (አማርኛ / Amharic)",
    greetingTitle: "ጤና ይስጥልኝ አያቴ!",
    greetingSub: "ሳውቲኬር ስልክዎን በቀላሉ በአማርኛ እና በከፍተኛ ድምፅ እንዲጠቀሙ ይመራዎታል::",
    welcomeBadge: "እንኳን ደህና መጡ",
    welcomeText: "ከታች ያለውን ትልቅ አረንጓዴ ቁልፍ ተጭነው በአማርኛ ይናገሩ። ሳውቲኬር በዋትስአፕ፣ በዩቲዩብ መዝሙር፣ በፎቶ፣ ወይም በአደጋ ጊዜ ይረዳዎታል::",
    welcomeEn: "(Press the big green button below and speak in Amharic. SautiCare will assist with WhatsApp, YouTube gospel, photos, airtime, or emergencies.)",
    sosTitle: "የአደጋ ጊዜ እርዳታ (SOS) 🚨",
    sosSub: "ወዲያውኑ ስልክ ይደውሉ እና ያለዎትን ቦታ መልእክት ይላኩ",
    scenariosTitle: "የሚፈልጉትን አገልግሎት ይምረጡ:",
    speakerLabel: "አዳምጥ",
    micIdle: "ለመናገር ይጫኑ",
    micListening: "እያዳመጥኩ ነው...",
    voices: [
      { id: "am-mekdes", label: "🇪🇹 መቅደስ (ሴት - Ethiopia)" },
      { id: "am-ameha", label: "🇪🇹 አመሃ (ወንድ - Ethiopia)" }
    ],
    defaultVoice: "am-mekdes",
    recognitionLang: "am-ET",
    pills: [
      { cls: "app-pill-wa", icon: "💬", title: "ዋትስአፕ፡", subtitle: "የድምፅ መልእክት", query: "በዋትስአፕ የድምፅ መልእክት መላክ እፈልጋለሁ" },
      { cls: "app-pill-yt", icon: "🎵", title: "ዩቲዩብ፡", subtitle: "የኢትዮጵያ መዝሙር", query: "በዩቲዩብ ላይ የኦርቶዶክስ እና ፕሮቴስታንት መዝሙር ክፈት" },
      { cls: "app-pill-cam", icon: "📸", title: "ካሜራ፡", subtitle: "ፎቶ አንሳ", query: "በስልኬ ፎቶ ማንሳት እፈልጋለሁ" },
      { cls: "app-pill-set", icon: "🔤", title: "የጽሑፍ መጠን ጨምር", subtitle: "", query: "የስክሪኑ ጽሑፍ በጣም አነሰ አግዝፈው" },
      { cls: "app-pill-bal", icon: "📞", title: "ቀሪ ሂሳብ፡", subtitle: "ደውል *804#", query: "የስልኬን ቀሪ ሂሳብ ማወቅ እፈልጋለሁ" },
      { cls: "app-pill-mpesa", icon: "💸", title: "ቴሌብር፡", subtitle: "ገንዘብ ላክ", query: "በቴሌብር ገንዘብ መላክ እፈልጋለሁ" },
      { cls: "app-pill-torch", icon: "🔦", title: "የእጅ ባትሪ፡", subtitle: "አብራ", query: "ጨልሟል የእጅ ባትሪውን አብራ" },
      { cls: "app-pill-sos", icon: "🚑", title: "የአደጋ ጊዜ፡", subtitle: "እርዳኝ", query: "ወድቄያለሁ እባክዎን በአስቸኳይ እርዱኝ" }
    ]
  }
};

class SautiCareApp {
  constructor() {
    this.currentLang = "sw";
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
    this.setupLanguageSwitcher();
    this.setupConnectivityMonitor();
    this.setupEventListeners();
    this.setupAccessibilityControls();
    this.registerServiceWorker();
    this.initWebSocket();
    this.initSpeechRecognition();
  }

  getSelectedVoice() {
    return this.voiceSelect ? this.voiceSelect.value : (PAN_AFRICAN_UI[this.currentLang]?.defaultVoice || "sw-ke-zuri");
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

  // 3. Pan-African Regional Language Switcher
  setupLanguageSwitcher() {
    const tabs = document.querySelectorAll(".lang-tab");
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        const lang = tab.getAttribute("data-lang");
        if (lang && lang !== this.currentLang) {
          this.setLanguage(lang);
        }
      });
    });
  }

  setLanguage(lang, announce = true) {
    if (!PAN_AFRICAN_UI[lang]) return;
    this.currentLang = lang;
    const config = PAN_AFRICAN_UI[lang];

    // Update active tab styles
    document.querySelectorAll(".lang-tab").forEach(tab => {
      const isCurrent = tab.getAttribute("data-lang") === lang;
      tab.classList.toggle("active", isCurrent);
      tab.setAttribute("aria-selected", isCurrent ? "true" : "false");
    });

    // Populate voice dropdown
    if (this.voiceSelect) {
      this.voiceSelect.innerHTML = config.voices.map(v => 
        `<option value="${v.id}">${v.label}</option>`
      ).join("");
      this.voiceSelect.value = config.defaultVoice;
    }

    // Update greeting banner
    const greetingTitle = document.getElementById("greeting-title");
    const greetingSub = document.getElementById("greeting-sub");
    if (greetingTitle) greetingTitle.innerText = config.greetingTitle;
    if (greetingSub) greetingSub.innerText = config.greetingSub;

    // Update welcome card text
    if (this.cardBadge) this.cardBadge.innerText = config.welcomeBadge;
    if (this.swahiliReply) this.swahiliReply.innerText = config.welcomeText;
    if (this.englishSub) this.englishSub.innerText = config.welcomeEn;
    if (this.actionDetails) this.actionDetails.innerHTML = "";

    // Update SOS button text
    const sosTitle = document.getElementById("sos-title");
    const sosSub = document.getElementById("sos-sub");
    if (sosTitle) sosTitle.innerText = config.sosTitle;
    if (sosSub) sosSub.innerText = config.sosSub;

    // Update scenarios title
    const scenariosTitle = document.getElementById("scenarios-title");
    if (scenariosTitle) scenariosTitle.innerText = config.scenariosTitle;

    // Update speaker & mic button labels
    const speakerLabel = document.getElementById("speaker-label");
    if (speakerLabel) speakerLabel.innerText = config.speakerLabel;
    if (this.micLabel) this.micLabel.innerText = this.isRecording ? config.micListening : config.micIdle;

    // Update scenario pills
    const pillsGrid = document.getElementById("pills-grid");
    if (pillsGrid) {
      pillsGrid.innerHTML = config.pills.map(p => `
        <button class="pill-btn ${p.cls}" data-query="${p.query}">
          ${p.icon} <strong>${p.title}</strong> ${p.subtitle}
        </button>
      `).join("");

      // Re-attach click events
      pillsGrid.querySelectorAll(".pill-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          const query = btn.getAttribute("data-query");
          this.processQuery(query);
        });
      });
    }

    // Update speech recognition language
    if (this.recognition) {
      this.recognition.lang = config.recognitionLang;
    }

    // Announce in native regional voice
    if (announce) {
      const voiceGreetings = {
        "sw": "Habari Mzee wangu! SautiCare iko tayari kukusaidia kwa Kiswahili.",
        "ng": "How you dey Elder! SautiCare dey here to help you well well.",
        "zu": "Sawubona Mkhulu! I-SautiCare isilungele ukukusiza ngesiZulu.",
        "am": "ጤና ይስጥልኝ አያቴ! ሳውቲኬር በአማርኛ ሊረዳዎት ዝግጁ ነው::"
      };
      const text = voiceGreetings[lang] || config.greetingTitle;
      this.playNativeSwahiliAudio(text);
    }
  }

  // 4. Setup UI Event Listeners
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

    // When voice selector changes, greet in chosen dialect
    this.voiceSelect.addEventListener("change", () => {
      const selected = this.getSelectedVoice();
      const voiceGreetings = {
        "sw-ke-zuri": "Shikamoo Mzee wangu! Mimi ni Zuri, niko hapa kukuongoza na simu yako kwa upole.",
        "sw-ke-rafiki": "Jambo Mzee wetu! Mimi ni Rafiki, msaidizi wako wa sauti hapa Kenya.",
        "sw-tz-daudi": "Habari za leo Mzee! Mimi ni Daudi, msaidizi wako wa sauti kutoka Tanzania.",
        "sw-tz-rehema": "Habari yako Mzee wetu! Mimi ni Rehema, niko tayari kukusaidia na simu yako.",
        "ng-ezinne": "How you dey Elder! Na Ezinne be your voice assistant for Naija.",
        "ng-abeo": "Salama Elder! Na Abeo dey here to guide you well well.",
        "zu-thando": "Sawubona Mkhulu! Igama lami nguThando, ngizokusiza ngefoni yakho.",
        "zu-themba": "Sawubona Gogo! NginguThemba, ngilapha ukukusiza njalo.",
        "am-mekdes": "ጤና ይስጥልኝ አያቴ! እኔ መቅደስ ነኝ፣ ስልክዎን እንዲጠቀሙ በደስታ እረዳዎታለሁ::",
        "am-ameha": "ጤና ይስጥልኝ አያቴ! እኔ አመሃ ነኝ፣ የሚያስፈልግዎትን ሁሉ እረዳዎታለሁ::"
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
            const res = await fetch(`/api/transcribe-audio?voice=${voice}&lang=${this.currentLang}`, {
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
    const config = PAN_AFRICAN_UI[this.currentLang] || PAN_AFRICAN_UI.sw;
    this.micLabel.innerText = config.micIdle;
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
        body: JSON.stringify({ text: text, voice: voice, lang: this.currentLang })
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
    const voice = this.getSelectedVoice();
    if (this.isOnline) {
      try {
        const res = await fetch(`/api/emergency/sos?voice=${voice}&lang=${this.currentLang}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            distress_type: "SOS Button Pressed (Kitufe cha Dharura)",
            location: "1°17'31.2\"S 36°49'10.8\"E (Africa)"
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
        body: JSON.stringify({ text: text, voice: voice, lang: this.currentLang })
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
