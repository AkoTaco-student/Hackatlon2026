import StreamingAvatar, {
  AvatarQuality,
  StreamingEvents,
  TaskType,
} from "https://esm.sh/@heygen/streaming-avatar";

export class AvatarStream {
  constructor(videoEl, statusEl) {
    this.videoEl = videoEl;
    this.statusEl = statusEl;
    this.avatar = null;
    this.sessionReady = false;
    this.pendingText = "";
    this.flushTimer = null;
    this.reconnectAttempts = 0;
    this.readyResolvers = [];
    this.onStartTalking = null;
    this.onStopTalking = null;
  }

  setTalkingCallbacks({ onStart, onStop }) {
    this.onStartTalking = onStart;
    this.onStopTalking = onStop;
  }

  setStatus(text) {
    if (this.statusEl) {
      this.statusEl.textContent = text;
    }
  }

  async init() {
    const config = await this.fetchConfig();
    if (config.provider === "none") {
      this.setStatus("Missing HEYGEN_API_KEY");
      return;
    }
    if (config.provider !== "heygen") {
      this.setStatus("D-ID fallback not configured");
      return;
    }
    await this.start(config.heygen);
  }

  async fetchConfig() {
    const resp = await fetch("/api/avatar/config");
    if (!resp.ok) {
      throw new Error("Failed to load avatar config");
    }
    return await resp.json();
  }

  async start(heygenConfig = {}) {
    if (this.avatar) {
      return;
    }

    this.setStatus("Starting avatar...");
    const tokenResp = await fetch("/api/heygen/token", { method: "POST" });
    if (!tokenResp.ok) {
      const data = await tokenResp.json().catch(() => ({}));
      throw new Error(data.error || "Failed to get HeyGen token");
    }
    const { token } = await tokenResp.json();

    this.avatar = new StreamingAvatar({ token });

    this.avatar.on(StreamingEvents.STREAM_READY, (event) => {
      const mediaStream = event.detail;
      this.videoEl.srcObject = mediaStream;
      this.videoEl.play().catch(() => {});
      this.sessionReady = true;
      this.setStatus("Avatar live");
      this.reconnectAttempts = 0;
      this.readyResolvers.forEach((resolve) => resolve());
      this.readyResolvers = [];
      if (this.pendingText) {
        this.flush();
      }
    });

    this.avatar.on(StreamingEvents.STREAM_DISCONNECTED, () => {
      this.sessionReady = false;
      this.setStatus("Avatar disconnected - reconnecting...");
      this.scheduleReconnect(heygenConfig);
    });

    this.avatar.on(StreamingEvents.AVATAR_START_TALKING, () => {
      if (typeof this.onStartTalking === "function") {
        this.onStartTalking();
      }
    });

    this.avatar.on(StreamingEvents.AVATAR_STOP_TALKING, () => {
      if (typeof this.onStopTalking === "function") {
        this.onStopTalking();
      }
    });

    await this.avatar.createStartAvatar({
      avatarName: heygenConfig.avatar_id || "default",
      quality: AvatarQuality.High,
      voice: heygenConfig.voice_id
        ? {
            voiceId: heygenConfig.voice_id,
          }
        : undefined,
    });
  }

  scheduleReconnect(heygenConfig) {
    if (this.reconnectAttempts > 3) {
      this.setStatus("Reconnect failed - restart avatar");
      return;
    }
    const delay = 1000 * Math.pow(2, this.reconnectAttempts);
    this.reconnectAttempts += 1;
    setTimeout(() => {
      this.stop();
      this.start(heygenConfig).catch((err) => {
        this.setStatus(`Reconnect failed: ${err.message}`);
      });
    }, delay);
  }

  waitUntilReady(timeoutMs = 30000) {
    if (this.sessionReady) {
      return Promise.resolve();
    }
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        reject(new Error("Avatar not ready"));
      }, timeoutMs);
      this.readyResolvers.push(() => {
        clearTimeout(timer);
        resolve();
      });
    });
  }

  speak(text) {
    if (!text) {
      return;
    }
    this.pendingText += text;
    this.flushIfNeeded();
  }

  flushIfNeeded() {
    const shouldFlush =
      this.pendingText.length > 80 ||
      /[.!?]\\s$/.test(this.pendingText) ||
      /[.!?]\\s$/.test(this.pendingText.trim());

    if (shouldFlush) {
      this.flush();
      return;
    }

    if (this.flushTimer) {
      return;
    }
    this.flushTimer = setTimeout(() => {
      this.flush();
    }, 250);
  }

  async flush() {
    if (this.flushTimer) {
      clearTimeout(this.flushTimer);
      this.flushTimer = null;
    }
    const text = this.pendingText.trim();
    if (!text) {
      this.pendingText = "";
      return;
    }
    if (!this.avatar || !this.sessionReady) {
      this.setStatus("Avatar not ready yet");
      return;
    }
    this.pendingText = "";
    try {
      await this.avatar.speak({
        text,
        task_type: TaskType.REPEAT,
      });
    } catch (err) {
      this.setStatus(`Speak failed: ${err.message}`);
    }
  }

  async stop() {
    if (!this.avatar) {
      return;
    }
    try {
      await this.avatar.stopAvatar();
    } catch (err) {
      this.setStatus(`Stop failed: ${err.message}`);
    }
    this.avatar = null;
    this.sessionReady = false;
  }
}
