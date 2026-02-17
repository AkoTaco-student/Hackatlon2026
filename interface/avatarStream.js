import {
  LiveAvatarSession,
  SessionEvent,
  AgentEventsEnum,
} from "https://esm.sh/@heygen/liveavatar-web-sdk@0.0.10?bundle";

export class AvatarStream {
  constructor(videoEl, statusEl) {
    this.videoEl = videoEl;
    this.statusEl = statusEl;
    this.session = null;
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
      this.setStatus("Missing LIVEAVATAR_API_KEY");
      return;
    }
    if (config.provider !== "liveavatar") {
      this.setStatus("LiveAvatar not configured");
      return;
    }
    await this.start(config.liveavatar);
  }

  async fetchConfig() {
    const resp = await fetch("/api/avatar/config");
    if (!resp.ok) {
      throw new Error("Failed to load avatar config");
    }
    return await resp.json();
  }

  async start(liveavatarConfig = {}) {
    if (this.session) {
      return;
    }

    this.setStatus("Starting avatar...");
    const tokenResp = await fetch("/api/liveavatar/token", { method: "POST" });
    if (!tokenResp.ok) {
      const data = await tokenResp.json().catch(() => ({}));
      throw new Error(data.error || "Failed to get LiveAvatar token");
    }
    const { session_token: sessionToken } = await tokenResp.json();
    if (!sessionToken) {
      throw new Error("LiveAvatar session token missing");
    }

    this.session = new LiveAvatarSession(sessionToken, {
      apiUrl: liveavatarConfig.api_url || undefined,
      voiceChat: false,
    });

    this.session.on(SessionEvent.SESSION_STREAM_READY, () => {
      this.session.attach(this.videoEl);
      this.videoEl.muted = false;
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

    this.session.on(SessionEvent.SESSION_STATE_CHANGED, (state) => {
      this.setStatus(`Session: ${state}`);
    });

    this.session.on(SessionEvent.SESSION_DISCONNECTED, () => {
      this.sessionReady = false;
      this.setStatus("Avatar disconnected - reconnecting...");
      this.scheduleReconnect(liveavatarConfig);
    });

    this.session.on(AgentEventsEnum.AVATAR_SPEAK_STARTED, () => {
      if (typeof this.onStartTalking === "function") {
        this.onStartTalking();
      }
    });

    this.session.on(AgentEventsEnum.AVATAR_SPEAK_ENDED, () => {
      if (typeof this.onStopTalking === "function") {
        this.onStopTalking();
      }
    });

    try {
      await this.session.start();
    } catch (err) {
      this.setStatus(`Start failed: ${err.message}`);
      throw err;
    }
  }

  scheduleReconnect(liveavatarConfig) {
    if (this.reconnectAttempts > 3) {
      this.setStatus("Reconnect failed - restart avatar");
      return;
    }
    const delay = 1000 * Math.pow(2, this.reconnectAttempts);
    this.reconnectAttempts += 1;
    setTimeout(() => {
      this.stop();
      this.start(liveavatarConfig).catch((err) => {
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
    if (!this.session || !this.sessionReady) {
      this.setStatus("Avatar not ready yet");
      return;
    }
    this.pendingText = "";
    try {
      await this.session.repeat(text);
    } catch (err) {
      this.setStatus(`Speak failed: ${err.message}`);
    }
  }

  async stop() {
    if (!this.session) {
      return;
    }
    try {
      await this.session.stop();
    } catch (err) {
      this.setStatus(`Stop failed: ${err.message}`);
    }
    this.session = null;
    this.sessionReady = false;
  }
}
