# CalcuTrip
Version: 1.10
Last revision date: 08/20/2025 @ 8:17 PM EST

Author: Charles Phillips  

**CalcuTrip** is a simple, user-friendly desktop tool that helps you answer those questions instantly.  
It calculates your **average miles per gallon (MPG)** and **total fuel cost** for each trip, then saves your results to a running log so you can track fuel performance over time.  

This app is designed for:  
- Everyday drivers tracking their fuel costs  
- Students & professionals learning about vehicle efficiency  
- Anyone who wants a no-fuss MPG calculator with history logging  

---

## 📋 Table of Contents
- [Installation](#installation)
  - [Option 1: Windows Installer (Recommended)](#option-1-windows-installer-recommended)
  - [Option 2: Portable .exe (Zip Download)](#option-2-portable-exe-zip-download)
  - [Option 3: Run from Source (Python Required)](#option-3-run-from-source-python-required)

- [App Layout](#-app-layout)
- [How to Calculate a Trip (Step-by-Step)](#-how-to-calculate-a-trip-step-by-step)
- [Keeping a Trip Log](#-keeping-a-trip-log)
- [Viewing Your History](#-viewing-your-history)
- [Troubleshooting](#-troubleshooting)
- [For Developers](#-for-developers)

---

## ✨ Features
- 🖥️ **Simple GUI** (Tkinter-based, one-click run).  
- 🚙 **Trip MPG Calculation** (enter miles + fuel, get instant results).  
- 📄 **Dynamic Help Button** (always points to the project’s latest README on GitHub).  
- 📦 **Easy Distribution**: provided as both a Windows installer `.exe` and a portable (install-free) standalone `.exe`.  

---

## 🔧 Installation

### Option 1: Windows Installer (Recommended)
1. Go to the [Releases](../../releases) page.  
2. Download the latest `` installer.  
3. Run the installer and follow the setup wizard.  
4. Launch **CalcuTrip** from your Start Menu.

---

### Option 2: Portable .exe (Zip Download)
1. Download the `.zip` file from [Releases](../../releases).  
2. Extract the zip.
3. Navigate to the `src` folder.
4. Double-click `CalcuTrip.exe` to run (no install required).  

---

### Option 3: Run from Source (Python Required)
1. Clone the repo:
   ```bash
   git clone https://github.com/CPhillips-dev/CalcuTrip.git
   cd CalcuTrip

## 🗺️ App Layout
Here’s what you’ll see when CalcuTrip starts:

**Input Fields (left):**
- **Vehicle Info** → e.g. *“2022 Vio Leem”*  
- **Trip Mileage** → distance traveled (miles)  
- **Gas Price ($/gal)** → what you paid per gallon  
- **Gallons Used** → fuel consumed  

**Buttons (bottom):**
- **Calculate** → runs the MPG & cost calculation  
- **Choose File** → select a log file to save trips into  
- **View File** → open your saved trip log in Notepad  
- **Exit** → close the app safely  

**Results Panel (right):**
- Displays your **calculated MPG** and **fuel cost** after clicking **Calculate**  

---

## 🚀 How to Calculate a Trip (Step-by-Step)

### Step 1 — Enter Trip Details
Fill in all four input fields:
- (Optional) Vehicle info
- Trip miles driven
- Gas price per gallon
- Gallons of gas used


### Step 2 — Calculate
Click **Calculate**.  
→ Your **MPG** and **Total Fuel Cost** instantly appear in the results panel.  

### Step 3 — Save Your Results
A “Save As” window appears.  
- Suggested filename: e.g. `2022_Vio_Leem_fuel_data.txt`  
- Choose a folder and click **Save**  

### Step 4 — Build a Running Log
- Each time you save to the same file, new trip data is added.  
- Over time, this creates a **fuel history log** for your vehicle.  

---

## 📒 Keeping a Trip Log
- Each trip is stored in plain-text `.txt` files.  
- Easy to open, share, or import into Excel.  
- Files are lightweight and human-readable.  

---

## 📂 Viewing Your History
- Once you’ve saved at least one trip, the **View File** button becomes enabled.  
- Click it to instantly open your log in **Notepad** (or your system’s default text editor).  
- You’ll see a chronological history of trips with MPG and cost data.  

---

## ❓ Troubleshooting
**Q: “Missing input field entries” error?**  
→ Make sure all four fields are filled before pressing **Calculate**.  

**Q: “Invalid entry!” error?**  
→ Only numbers are valid in Mileage, Gas Price, and Gallons Used. Values must be greater than zero.  

**Q: App freezes after “View File”?**  
→ Close the text file before re-opening with the button.  

---

## 👨‍💻 For Developers
CalcuTrip is open source and built with **Python + Tkinter**.  
The `Help` button dynamically links to this README, ensuring the latest usage instructions are always available.  

Project structure:  

CalcuTrip/

- ├── src/
- │ └── main.py
- ├── assets/
- │ ├── imgs/
- │ └── license/
- └── README.md
