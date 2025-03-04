// require("dotenv").config();
const express = require("express");
const nodemailer = require("nodemailer");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
app.use(cors());
app.use(bodyParser.json());

const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: { user: "add admin email here", pass: 'add app password' },
});

app.post("/send-otp", async (req, res) => {
    const { email } = req.body;
    const otp = Math.floor(100000 + Math.random() * 900000).toString();

    await transporter.sendMail({ from: "add admin email here", to: email, subject: "Your OTP", text: `Your OTP is: ${otp}` });

    res.status(200).json({ otp, message: "OTP sent" });
});

app.listen(5000, () => console.log("Node.js server running on port 5000"));
