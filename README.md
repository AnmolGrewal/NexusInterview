# NEXUS Appointment Checker

This script checks for available NEXUS appointments and notifies you when a suitable appointment is found.

## Features

- Regularly checks for NEXUS appointments within a specified timeframe
- Plays an audio alert when an appointment is found
- Sends desktop notifications
- Emails notifications to a specified address
- Provides timestamps for each check

## Prerequisites

- Python 3.6+
- pip (Python package installer)

## Installation

1. Clone this repository or download the script.

2. Install the required Python packages:

3. Ensure you have a Gmail account with 2-factor authentication enabled.

4. Generate an App Password for your Gmail account:
- Go to your Google Account settings
- Navigate to the "Security" section
- Find "2-Step Verification" and ensure it's turned on
- Below that, find "App passwords" and click on it
- Select "Mail" as the app and "Other" as the device (name it "Python script" or similar)
- Use the generated 16-character password in the script

## Configuration

1. Open the script in a text editor.

2. Replace `"your_email@gmail.com"` with your Gmail address.

3. Replace `"your_app_password"` with the App Password you generated.

4. Adjust the `target_date` in the `main()` function if you want to change the appointment search window.

5. Modify the `url` in the `main()` function if you need to check a different NEXUS enrollment center.

## Usage

Run the script from the command line:

python nexus_appointment_checker.py

The script will continuously check for appointments, printing timestamps for each check. When an appointment is found:

- An audio alert will play
- A desktop notification will appear
- An email will be sent to the specified address

Press any key to stop the audio alert and continue checking.

## Note

This script is designed for personal use. Be respectful of the NEXUS appointment system and avoid making excessive requests.

## Troubleshooting

If you encounter issues with email sending:
- Double-check your Gmail address and App Password
- Ensure 2-factor authentication is enabled on your Gmail account
- Check your Gmail account for any security alerts or login attempt notifications

For other issues, check the console output for error messages.

## License

This project is open source and available under the [MIT License](LICENSE).