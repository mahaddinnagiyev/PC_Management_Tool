# My Computer Utility App

This app is a simple, easy-to-use desktop utility that provides various functions for managing your computer. It is built using Python with several useful libraries and packages. The app includes features for adjusting your system's brightness and volume, checking the weather, displaying a clock, managing a calendar, taking screenshots, and opening commonly used applications like File Explorer, Google, and GitHub.

## Features

- **System Info**: Get information about your computer.
- **Adjust Brightness**: Control screen brightness with ease.
- **Adjust Volume**: Control system volume using a user-friendly interface.
- **Weather App**: View current weather and forecasts.
- **Clock App**: Displays the current time.
- **Calendar App**: A simple calendar for keeping track of dates.
- **Screenshot App**: Take screenshots of your screen.
- **Open File Explorer**: Quickly open your file explorer.
- **Open Google**: Open Google in your default web browser.
- **Open GitHub**: Directly open GitHub in your web browser.

## Packages Used

This app relies on several Python packages:

- `tkinter`: For creating the GUI interface.
- `screen_brightness_control`: For controlling the screen brightness.
- `pycaw`: For controlling system audio volume.
- `requests`: For fetching weather data.
- `tkcalendar`: For displaying and interacting with the calendar.
- `PIL` (Pillow): For handling image files and taking screenshots.
- `pyautogui`: For taking screenshots.
- `psutil`: For getting system information.
- `webbrowser`: For opening URLs (Google and GitHub).
- `subprocess`: For running system commands like opening File Explorer.

## System Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- `pycaw` (install via `pip install pycaw`)
- `screen_brightness_control` (install via `pip install screen-brightness-control`)
- `Pillow` (install via `pip install pillow`)
- `tkcalendar` (install via `pip install tkcalendar`)
- `psutil` (install via `pip install psutil`)
- `requests` (install via `pip install requests`)
- `pyautogui` (install via `pip install pyautogui`)

## Installation

To run the app, follow these steps:

1. Clone or download the repository.
2. Ensure you have Python 3.x installed on your machine.
3. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt

4. Run the app using the following command:
   ```bash
   python app.py
   ```

If you'd like to download the app as an `.exe` file, use the following link:

<a href="https://drive.google.com/drive/folders/1M2OWxoBiiwyKsOrPzkypAMcijrxr2MI2?usp=drive_link" target="_blank">Download Link</a>

After downloading, navigate to the `/dist/` folder and run `app.exe` by executing:
```bash
./dist/app.exe
```

after download enter and click /dist/app.exe

## How to Use

Once you run the app, you can access the following functionalities:

1. Brightness Control: Adjust the screen brightness.
2. Volume Control: Increase or decrease system volume.
3. Weather App: View the current weather by entering your location.
4. Clock App: Displays the current time and updates in real-time.
5. Calendar App: Interact with the calendar and select dates.
6. Screenshot App: Capture and save screenshots of your screen.
7. Open File Explorer: Opens the file explorer on your system.
8. Open Google: Opens Google in your default web browser.
9. Open GitHub: Opens GitHub in your default web browser.

## License
This project is open-source and available under the MIT License.
