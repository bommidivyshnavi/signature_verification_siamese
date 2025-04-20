//server.js
const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const dotenv = require("dotenv");
const connectDB = require("./config/db");
const authRoutes = require("./routes/auth");
const { networkInterfaces } = require("os");

dotenv.config();
const app = express();
const PORT = process.env.PORT || 5000;

// Function to get MAC address
function getMacAddress() {
  const nets = networkInterfaces();
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      // Skip internal (i.e., 127.0.0.1) and non-MAC addresses
      if (!net.internal && net.mac !== "00:00:00:00:00:00") {
        return net.mac;
      }
    }
  }
  return null;
}

// Allowed MAC address
const ALLOWED_MAC = process.env.ALLOWED_MAC;

const macAddress = getMacAddress();
if (macAddress.replace(/-/g, ":").toLowerCase() !== ALLOWED_MAC.replace(/-/g, ":").toLowerCase()) {
  console.error("Unauthorized machine. Shutting down.");
  process.exit(1);
}

// Connect to MongoDB
connectDB();

app.use(cors());
app.use(bodyParser.json());
app.use(express.static("public"));
app.use("/api", authRoutes);

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
