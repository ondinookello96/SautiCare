# 🎙️ SautiCare — Sauti ya Wazee (Pan-African Voice Navigator for Elders)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-sauticare.onrender.com-brightgreen?style=for-the-badge&logo=render)](https://sauticare.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Technology](https://img.shields.io/badge/Powered%20By-AssemblyAI-blue)](https://www.assemblyai.com/)
[![Languages](https://img.shields.io/badge/Languages-Kiswahili%20%7C%20Pidgin%20%7C%20isiZulu%20%7C%20Amharic-orange)](#)

🌐 **Live Application URL:** [https://sauticare.onrender.com](https://sauticare.onrender.com)  
📱 **PWA Installable:** Open the link in mobile Chrome/Safari and tap *"Add to Home Screen"*.

> **An oral-first voice navigator and lifeline for African elders using smartphones. Empowers seniors across Africa to navigate everyday smartphone apps (WhatsApp voice notes, YouTube gospel, Camera, phone settings), manage mobile money safely (M-Pesa, OPay, eWallet, Telebirr), and summon 24/7 emergency help—in 4 major African languages with offline resilience.**

Built for the **AssemblyAI - Voice Agent Hackathon** on [lablab.ai](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon).

---

## 🌍 Supported African Regions & Languages

SautiCare bridges the digital literacy divide for over 100 million African elders across 4 key regional zones:

| Region | Primary Language & Dialect | Flag | Neural Voices | Supported Mobile Money & USSD |
| :--- | :--- | :---: | :--- | :--- |
| **East Africa** | **Kiswahili** (Kenya, Tanzania) | 🇰🇪 🇹🇿 | `Zuri`, `Rafiki`, `Daudi`, `Rehema` | M-Pesa (`*334#`), Safaricom (`*144#`) |
| **West Africa** | **Nigerian Pidgin** (Nigeria) | 🇳🇬 | `Ezinne`, `Abeo` | OPay / Transfers, MTN / Airtel (`*310#`) |
| **Southern Africa** | **isiZulu** (South Africa) | 🇿🇦 | `Thando`, `Themba` | eWallet, Vodacom / MTN (`*136#`) |
| **Horn of Africa** | **አማርኛ / Amharic** (Ethiopia) | 🇪🇹 | `Mekdes (መቅደስ)`, `Ameha (አመሃ)` | Telebirr (`*127#`), Ethio Telecom (`*804#`) |

---

## 🌍 The Problem in Africa

1. **Digital Exclusion of the Elderly:** Rapid smartphone adoption across Africa has flooded the market with affordable Android devices. However, digital literacy among aging parents and grandparents remains low. Complex nested menus, tiny text, and unfamiliar icons create anxiety.
2. **Oral-First Communication:** African elders overwhelmingly communicate through voice notes (e.g. WhatsApp audio) rather than typing text messages.
3. **Mobile Money Anxiety:** Elders frequently rely on remittances from children in the city, but fear sending money to the wrong recipient or being scammed via complex USSD prompts (`*334#`, `*127#`).
4. **Alone During Emergencies:** In medical crises (falls, hypertension, sudden illness), elders often cannot unlock their phone or find contacts in time.
5. **The "Zero Bundle" Reality (Offline Need):** Cellular data bundles run out frequently or drop in rural areas. Emergencies and mobile money operations cannot rely solely on active 4G data.

---

## 💡 The SautiCare Solution

SautiCare solves these challenges through a **Hybrid Dual-Engine Architecture**:

* **🟢 Online Engine (Powered by AssemblyAI):**
  * Real-time streaming Speech-to-Text over WebSockets.
  * Robust understanding of East African Swahili accents and natural code-switching (Swahili + Sheng / English).
  * Culturally respectful persona (*Heshima kwa Wazee*) greeting elders properly (*"Shikamoo Mzee/Mama"*).
  * Automated tool calling for device control, M-Pesa verification, and emergency dispatch.

* **🟡 Offline Safety Fail-Safe (Zero Data / Rural Mode):**
  * When mobile internet is disconnected, SautiCare automatically switches to **Offline Safety Mode**.
  * **Emergency SOS:** Direct hardware trigger for **GSM voice dialing (`tel:`)** and **SMS with GPS coordinates** with 0MB data required.
  * **M-Pesa USSD Guide:** Uses pre-cached Swahili voice prompts to guide elders step-by-step through offline USSD codes (`*334#` / SIM Toolkit).

---

## 🏗️ Architecture

```
                    ┌──────────────────────────────────────────────┐
                    │     Elderly-Friendly Smartphone Client       │
                    │  • Giant "BONYEZA KUONGEA" Mic Button        │
                    │  • High-Contrast AAA Accessibility UI        │
                    │  • One-Touch "DHARURA (SOS)" Button          │
                    └───────────────────────┬──────────────────────┘
                                            │
                             [Network Connectivity Check]
                                   ┌────────┴────────┐
                (Online / Data OK) ▼                 ▼ (Offline / No Data)
┌───────────────────────────────────────────┐    ┌───────────────────────────┐
│ Cloud Voice Engine (AssemblyAI)           │    │ Offline Safety Engine     │
│ • Sub-second WebSocket Streaming STT      │    │ • Pre-cached Swahili Audio│
│ • Universal-3 Pro Accent Resilience       │    │ • Direct GSM Cellular SOS │
│ • Conversational Tool Router:             │    │ • Direct GPS SMS Intent   │
│   - `trigger_emergency_sos`               │    │ • USSD *334# Step Guide   │
│   - `guide_mpesa_transfer`                │    └───────────────────────────┘
│   - `control_phone_feature` (Torch, Call) │                  │
└─────────────────────┬─────────────────────┘                  │
                      │                                        │
                      └──────────────────┬─────────────────────┘
                                         ▼
                     [Culturally Respectful Swahili Speech &
                         Visual Confirmation Cards]
```

---

## 🎯 Demo Scenarios

### 1. 🚨 Emergency Fall / Illness Scenario
* **User says:** *"Nisaidie, nimeanguka chini na siwezi kusimama"* (Help, I fell down and cannot stand)
* **Agent responds:** *"Tulia Mzee wangu, usijali. Nimeshatuma ujumbe wa dharura pamoja na mahali ulipo kwa mwanao Juma, na sasa ninapiga simu ya msaada mara moja."*
* **Action:** Dispatches emergency SMS with live GPS coordinates and initiates direct cellular phone call.

### 2. 💸 Safe M-Pesa Remittance Scenario
* **User says:** *"Nataka kutuma pesa kwa mtoto wangu Mary"* (I want to send money to my child Mary)
* **Agent responds:** *"Shikamoo Mama. Kwenye M-Pesa, usalama wako ni muhimu sana. Kabla hujaweka nambari yako ya siri, hakikisha jina la mpokeaji linaonekana wazi..."*
* **Action:** Displays high-contrast step-by-step verification card and guides them through safe USSD (`*334#`).

### 3. 🔦 Everyday Accessibility (Flashlight & Phone Features)
* **User says:** *"Washa tochi, kuko giza"* (Turn on the torch, it's dark)
* **Agent responds:** *"Tayari nimewasha tochi ya simu yako ili uweze kuona vizuri gizani."*
* **Action:** Toggles device flashlight simulation and confirms orally.

---

## 🚀 Quickstart & Setup

### Prerequisites
* Python 3.10+
* Free AssemblyAI API Key ([Claim Hackathon Credits](https://www.assemblyai.com/dashboard/signup?utm_source=event&utm_medium=credit-grant&utm_campaign=lablab_virtual_hackathon))

### Installation
```bash
# Clone the repository
git clone https://github.com/ondinookello96/SautiCare.git
cd SautiCare

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure your API key
cp .env.example .env
# Edit .env and paste your ASSEMBLYAI_API_KEY
```

### Running the Application
```bash
python main.py
```
Open your browser at: **`http://localhost:8000`**

### Running the Tests
```bash
python -m unittest discover tests
```

---

## 🏆 Hackathon Evaluation Alignment

| Judging Criteria (25% each) | How SautiCare Excels |
| :--- | :--- |
| **Application of Technology** | Deep integration of AssemblyAI Realtime Streaming STT, sub-second latency, voice session management, and JSON tool calling. |
| **Originality** | An oral-first Swahili voice agent specifically engineered around the African elder digital divide, code-switching, and cultural honorifics. |
| **Business Value** | Solves a massive humanitarian and fintech inclusion problem for 50M+ aging Africans and their diaspora families. |
| **Presentation** | High-contrast elder-accessible UI, clear bilingual subtitles for global judges, and comprehensive documentation. |

---

## 📄 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
