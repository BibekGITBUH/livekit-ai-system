-API Key
AQ.Ab8RN6LsAIP7KQyL9LUg0IUR1aLZ-xf7DkuLmzcX5r6pUawlXw
-Name
Gemini API Key
-Project name
projects/389126732081
-Project number
389126732081


curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: AQ.Ab8RN6LsAIP7KQyL9LUg0IUR1aLZ-xf7DkuLmzcX5r6pUawlXw' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explain how AI works in a few words"
          }
        ]
      }
    ]
  }'

# LiveKit Voice AI Assistant System

A real-time voice AI assistant powered by **LiveKit Agents** and **Google Gemini Live (Realtime Audio API)**, featuring automated two-way voice conversations with custom Knowledge Base, WebRTC web client support, and SIP telephony integration.

---

## 📋 System Architecture

| Component | Container | Ports | Purpose |
| :--- | :--- | :--- | :--- |
| **LiveKit Server** | `livekit-server` | `7880` (HTTP/WS), `7881` (TCP), `50000-50100/udp` (WebRTC) | Real-time audio routing & room management |
| **LiveKit Agent** | `livekit-agent` | Internal | Voice AI worker running Gemini Live real-time audio |
| **LiveKit SIP** | `livekit-sip` | `5060/udp+tcp` (SIP), `10000-10050/udp` (RTP) | Inbound SIP phone call bridging into LiveKit rooms |
| **Redis** | `livekit-redis` | `6379` | State coordination & message broker |

---

## 📌 Version Control & Environment Specifications

To ensure consistency and avoid version conflicts during development and deployment, all component, container, and library versions are locked and documented below:

### 1. Docker Images & Container Stack (`docker-compose.yaml`)

To inspect and freeze the pure image versions (avoiding `:latest` drifts), run the following docker commands:

| Service | Tag in Compose | Pure / Pinned Version | Docker Version Check Command | Role & Description |
| :--- | :--- | :--- | :--- | :--- |
| **LiveKit Server** | `livekit/livekit-server:latest` | **`v1.13.7`** | `docker run --rm livekit/livekit-server:latest --version` | WebRTC SFU media server (ports 7880, 7881, 50000-50100/udp) |
| **LiveKit SIP Gateway** | `livekit/sip:latest` | **`v1.17.0`** | `docker run --rm livekit/sip:latest --version` | SIP inbound trunk & dispatch bridge (port 5060, RTP 10000-10050/udp) |
| **Redis** | `redis:7-alpine` | **`7.4.11-alpine`** | `docker run --rm redis:7-alpine redis-server --version` | Distributed key-value store & pub/sub coordinator |
| **LiveKit CLI** | `livekit/livekit-cli:latest` | **`v2.18.8`** | `docker run --rm livekit/livekit-cli:latest --version` | CLI tool used for trunk & dispatch rule provisioning |
| **Compose Spec** | `3.9` | `3.9` | - | Docker Compose schema version |

> **Tip for Production Pinning**: In `docker-compose.yaml`, replace `:latest` with the pure tags (e.g. `livekit/livekit-server:v1.13.7` and `livekit/sip:v1.17.0`) to prevent breaking changes when images update upstream.

### 2. Agent Container Environment (`agent/Dockerfile`)
| Component | Version / Specification | Details |
| :--- | :--- | :--- |
| **Base Docker Image** | `python:3.11-slim` (Pure: **`3.11.17`**) | Check via: `docker run --rm python:3.11-slim python --version` |
| **Debian Audio & Build Deps**| `gcc`, `build-essential`, `curl`, `ca-certificates`, `portaudio19-dev`, `ffmpeg` | OS-level compilation and audio codecs |
| **Silero VAD ONNX Binary** | `snakers4/silero-vad` (master branch ONNX) | Placed at `/usr/local/lib/python3.11/site-packages/livekit/plugins/silero/resources/silero_vad.onnx` |

### 3. Python Dependencies (`agent/requirements.txt` & Scripts)
| Library | Version Constraint | Role in System |
| :--- | :--- | :--- |
| **`livekit-agents`** | `>=1.8.0` | LiveKit Multimodal Agents framework (`AgentSession`, `Agent`, `JobContext`, `cli`) |
| **`livekit-plugins-google`** | `>=1.8.0` | Google Gemini Live Realtime API plugin (`google.realtime.RealtimeModel`) |
| **`livekit-plugins-silero`** | `>=1.8.0` | Real-time Silero Voice Activity Detection (VAD) |
| **`python-dotenv`** | Latest (`>=1.0.0`) | `.env` configuration file loader |
| **`livekit-api`** | Compatible with `livekit-agents` | JWT Token & VideoGrants generator (`generate_token.py`) |

### 4. AI Models & Voice Engine Configuration
| Parameter | Setting | Usage |
| :--- | :--- | :--- |
| **Realtime Model** | `gemini-3.8-live` | Bidirectional real-time voice streaming model in [`agent/agent.py`](agent/agent.py) |
| **Voice Preset** | `Kore` | Natural conversational voice timbre |
| **REST Generation Model**| `gemini-flash-latest` (v1beta API) | Endpoint used for curl/API verification |

### 5. Host Development Machine (Verified Baseline)
| Tool / Runtime | Tested Host Version |
| :--- | :--- |
| **Operating System** | Windows 11 (Build 10.0.26200, 64-bit) |
| **Python** | `3.12.3` (Host) / `pip 26.1.2` |
| **Docker Engine** | Docker Desktop `29.1.3` (API `1.52`, Build `f52814d`) |
| **Docker Compose** | `v2.40.3-desktop.1` |
| **Git** | `2.43.0.windows.1` |
| **Node.js / npm** | Node `v24.12.0` / npm `9.7.2` |

---

## 🚀 Quickstart: Run the System

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd livekit-ai-system
```

### Step 2: Configure Your API Key & Host IP, Here Given is dummy.
Open [`docker-compose.yaml`](docker-compose.yaml) and ensure the following are configured:

1. **`GEMINI_API_KEY`** (under `livekit-agent` service):
   Set your Google Gemini API key:
   ```yaml
   - GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
   ```
2. **`external_ip` & `node_ip`** (if testing across LAN or SIP):
   - In [`docker-compose.yaml`](docker-compose.yaml) under `livekit-sip`: set `external_ip: YOUR_LAN_IP` (e.g. `192.168.1.100`)
   - In [`livekit/livekit.yaml`](livekit/livekit.yaml): set `node_ip: "YOUR_LAN_IP"`

### Step 3: Start All Services
Run a single command to build and launch all containers:
```bash
docker compose up -d
```

### Step 4: Verify Containers are Running
```bash
docker ps
```
You should see 4 containers running healthy:
- `livekit-server`
- `livekit-agent`
- `livekit-sip`
- `livekit-redis`

To check agent logs and ensure it connected successfully:
```bash
docker logs -f livekit-agent
```
You should see: `registered worker ... url: ws://livekit-server:7880`.

---

## 🎙️ Testing the Voice Agent

### Option A: Via Web Browser (Easiest — LiveKit Meet)

You can test speaking with the agent directly from your browser with your microphone and speakers.

1. **Generate a Connection Token**:
   Run the helper script (requires `pip install livekit-api` or run directly in Python):
   ```bash
   python generate_token.py test-room my-name
   ```
   *Alternatively, generate inside the agent container:*
   ```bash
   docker exec livekit-agent python -c "from livekit.api import AccessToken, VideoGrants; grant = VideoGrants(room_join=True, room='test-room', can_publish=True, can_subscribe=True); print(AccessToken('devkey', 'secretkeyphrase123456789012345632523532').with_identity('tester').with_grants(grant).to_jwt())"
   ```

2. **Connect to LiveKit Meet**:
   - Open [https://meet.livekit.io/?tab=custom](https://meet.livekit.io/?tab=custom) in Chrome or Edge.
   - Fill in:
     - **LiveKit Server URL**: `ws://localhost:7880` (or `ws://<HOST_LAN_IP>:7880`)
     - **Token**: *(Paste the token from Step 1)*
   - Click **Connect**.
3. **Talk to the Agent**:
   - As soon as you join, the AI voice agent automatically joins the room, greets you, and responds to your voice in real time!

---

### Option B: Via SIP Softphone (Linphone, MicroSIP, Zoiper)

If you wish to test incoming phone calls:

1. **Register Inbound Trunk & Dispatch Rule** (one-time setup):
   ```bash
   # Create Inbound Trunk
   docker run --rm -v ${PWD}:/workspace -w /workspace --network livekit-ai-system_default \
     livekit/livekit-cli:latest sip inbound create inbound-trunk.json \
     --url http://livekit-server:7880 --api-key devkey --api-secret secretkeyphrase123456789012345632523532

   # Create Dispatch Rule (directs calls to 'test-room')
   docker run --rm -v ${PWD}:/workspace -w /workspace --network livekit-ai-system_default \
     livekit/livekit-cli:latest sip dispatch create dispatch-rule.json \
     --url http://livekit-server:7880 --api-key devkey --api-secret secretkeyphrase123456789012345632523532
   ```

2. **Dial from Softphone**:
   - Open Linphone or your SIP dialer on the same network.
   - Dial: `sip:100@<HOST_LAN_IP>` (e.g. `sip:100@192.168.18.5`).
   - The SIP bridge will accept the call, route audio into `test-room`, and the AI assistant will converse with the caller.

---

## 📝 Updating the Knowledge Base (KB)

The agent instructions, persona, language, and knowledge base are defined in [`agent/agent.py`](agent/agent.py) inside the `INSTRUCTIONS` variable.

Because [`agent/agent.py`](agent/agent.py) is mounted directly as a volume into the container:

1. Open [`agent/agent.py`](agent/agent.py) and update the `INSTRUCTIONS` text with your company facts, policies, or language instructions.
2. Restart the agent container to immediately apply changes:
   ```bash
   docker compose restart livekit-agent
   ```
*(No lengthy Docker build needed — updates take effect in ~1 second!)*

---

## 🛠️ Helpful Management Commands

| Action | Command |
| :--- | :--- |
| **View real-time agent logs** | `docker logs -f livekit-agent` |
| **View SIP service logs** | `docker logs -f livekit-sip` |
| **Restart the entire stack** | `docker compose restart` |
| **Stop all services** | `docker compose down` |
| **Full rebuild & restart** | `docker compose up -d --build` |

---

## 🔍 Troubleshooting

- **No sound from the agent?**
  - Verify your `GEMINI_API_KEY` is active and has access to Gemini Realtime / Live API.
  - Check `docker logs --tail 50 livekit-agent` for any API rejection or authentication warnings.
- **Connection refused on LiveKit Meet?**
  - Make sure the server URL uses `ws://` (WebSocket) and port `7880`.
  - If connecting from another PC/phone on the LAN, use `ws://<HOST_LAN_IP>:7880` instead of `localhost`.
- **if something happen remove:**
   ```bash
   volumes:
       -./agent/agent.py:/app/agent.py
   ```
    from: docker-compose.yaml
