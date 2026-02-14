import { AvatarStream } from "./avatarStream.js";

const avatarVideo = document.getElementById("avatarVideo");
const avatarStatus = document.getElementById("avatarStatus");
const testStatus = document.getElementById("testStatus");

const avatarStream = new AvatarStream(avatarVideo, avatarStatus);

let pass = false;

avatarStream.setTalkingCallbacks({
  onStart: () => {
    pass = true;
    testStatus.textContent = "PASS: Avatar started talking.";
  },
  onStop: () => {
    if (!pass) return;
    testStatus.textContent = "PASS: Avatar finished speaking.";
  },
});

async function runTest() {
  try {
    await avatarStream.init();
    await avatarStream.waitUntilReady(30000);
    testStatus.textContent = "Sending test phrase...";
    avatarStream.speak(
      "Dette er en test av sanntidsavataren. Kan du høre meg?"
    );
    setTimeout(() => {
      if (!pass) {
        testStatus.textContent =
          "FAIL: Avatar did not start speaking within 25 seconds.";
      }
    }, 25000);
  } catch (err) {
    testStatus.textContent = `FAIL: ${err.message}`;
  }
}

runTest();
