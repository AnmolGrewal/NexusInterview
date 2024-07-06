import requests
from datetime import datetime, timedelta
import pytz
import time
import os
import threading
from pydub import AudioSegment
from pydub.playback import play
from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Global flag to control sound playback
stop_sound = threading.Event()

def get_appointment_info(url, target_date):
    response = requests.get(url, headers={'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1'})
    response.raise_for_status()
    data = response.json()
    suitable_appointments = []
    for appointment in data:
        start_time = datetime.fromisoformat(appointment['startTimestamp'])
        if start_time < target_date:
            suitable_appointments.append(start_time)
    return suitable_appointments

def format_message(appointment_time):
    pacific_tz = pytz.timezone('US/Pacific')
    current_time = datetime.now(pacific_tz)
    formatted_date = appointment_time.strftime("%m/%d/%Y (%A)")
    formatted_time = appointment_time.strftime("%I:%M %p")
    current_time_str = current_time.strftime("%I:%M %p")
    return f"NEXUS appointment available on {formatted_date} at {formatted_time}.\nInfo is current as of {current_time_str}, Pacific Time."

def play_continuous_sound():
    sound = AudioSegment.from_file("/System/Library/Sounds/Glass.aiff", format="aiff")
    while not stop_sound.is_set():
        play(sound)
        time.sleep(0.1)  # Small delay to prevent high CPU usage

def on_press(key):
    stop_sound.set()
    return False  # Stop listener

def show_notification(message):
    os.system(f"""
    osascript -e 'display notification "{message}" with title "NEXUS Appointment"'
    """)

def send_email(subject, body):
    sender_email = "your_email@gmail.com"  # Replace with your Gmail address
    app_password = "your_app_password"  # Replace with your app password
    receiver_email = "mehrnagrani@gmail.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def main():
    # Update this ID Here Based on What you want. 5020 is Blaine
    url = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=3&locationId=5020&minimum=1"
    target_date = datetime.now() + timedelta(days=90)  # Change this to your desired target date
    
    while True:
        try:
            appointment_times = get_appointment_info(url, target_date)
            if appointment_times:
                for appointment_time in appointment_times:
                    message = format_message(appointment_time)
                    print(message)
                    show_notification(message)
                    
                    # Send email
                    email_subject = "NEXUS Appointment Available"
                    send_email(email_subject, message)

                    # Reset the stop flag
                    stop_sound.clear()
                    # Start playing sound in a separate thread
                    sound_thread = threading.Thread(target=play_continuous_sound)
                    sound_thread.start()
                    # Start listening for key press
                    with keyboard.Listener(on_press=on_press) as listener:
                        listener.join()
                    # Wait for sound thread to finish
                    sound_thread.join()
                    print("Sound stopped. Continuing to check for appointments...")
            else:
                current_time = datetime.now().strftime("%I:%M %p")
                print(f"{current_time}: No suitable appointments found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        time.sleep(71)  # Wait for 71 seconds before checking again

if __name__ == "__main__":
    main()