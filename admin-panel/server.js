const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const chokidar = require("chokidar");

const app = express();
app.use(cors());

const DB_PATH = path.join(__dirname, "db.json");

let clients = [];

function sendEventsToAll(newUsers) {
  clients.forEach((client) =>
    client.response.write(`data: ${JSON.stringify(newUsers)}\n\n`)
  );
}

app.get("/events", (req, res) => {
  const headers = {
    "Content-Type": "text/event-stream",
    Connection: "keep-alive",
    "Cache-Control": "no-cache",
  };
  res.writeHead(200, headers);

  const data = `data: ${JSON.stringify(
    JSON.parse(fs.readFileSync(DB_PATH)).users
  )}\n\n`;
  res.write(data);
  const clientId = Date.now();
  const newClient = {
    id: clientId,
    response: res,
  };
  clients.push(newClient);

  req.on("close", () => {
    console.log(`${clientId} Connection closed`);
    clients = clients.filter((client) => client.id !== clientId);
  });
});



app.listen(3001, () => {
  console.log("SSE server running on port 3001");
});
