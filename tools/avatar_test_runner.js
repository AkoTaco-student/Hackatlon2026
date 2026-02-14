const http = require("http");

const healthUrl = "http://localhost:5000/health";
const testUrl = "http://localhost:5000/avatar-test.html";

function checkHealth() {
  return new Promise((resolve) => {
    const req = http.get(healthUrl, (res) => {
      resolve(res.statusCode === 200);
      res.resume();
    });
    req.on("error", () => resolve(false));
  });
}

async function run() {
  const ok = await checkHealth();
  if (!ok) {
    console.error("Server not running.");
    console.error("Start it with: python interface/app.py");
    process.exit(1);
  }

  console.log("Avatar test page is ready.");
  console.log(`Open: ${testUrl}`);
  console.log("You should see PASS when the avatar starts speaking.");
}

run();
