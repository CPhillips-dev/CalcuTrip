CalcuTrip - MPG & Fuel Cost Calculator Official Help
Version: 1.09

Author: Charles Phillips

Welcome to CalcuTrip! This is a simple and user-friendly desktop application designed to help you easily calculate your vehicle's average Miles Per Gallon (MPG) and total fuel costs for a trip. Keep track of your spending and fuel efficiency by saving the results to a text file.

Testing Markdown TOC

1. [Example](#example)
2. [Example2](#example2)
3. [Third Example](#third-example)

## Example [](#){name=example}

## [Third Example](#){name=third-example}

a
sdfasdfasd
asdfa
sdfasdfasdf

## Example2 [](#){name=example2}

📋 Table of Contents
Features

Download & Installation

How to Use the App

For Developers

Contributing

✨ Features
Calculate Average MPG: Automatically computes your vehicle's fuel efficiency.

Calculate Total Fuel Cost: Determines the total amount spent on gas for a trip.

User-Friendly Interface: A simple and intuitive graphical interface.

Data Logging: Saves trip data (mileage, MPG, fuel cost) to a .txt file for your records.

Append Trip Data: Adds new trip information to the same file, creating a running log.

View Results: Directly open the results file in your default text editor from within the app.

Built-in Help Guide: Includes a "Help" button that opens a PDF user guide.

📥 Download & Installation
Getting CalcuTrip set up is quick and easy. Just follow these steps:

Go to the Releases Page: Click here to go to the latest releases for this project.

Download the Installer: Look for the most recent version and download the CalcuTrip-Installer.exe file.

Run the Installer: Find the downloaded file on your computer and double-click it to run.

Follow the Prompts: The installation wizard will guide you through the simple setup process. Once it's finished, CalcuTrip will be installed on your computer and ready to use!

📖 How to Use the App
Once the application is installed and running, follow these simple steps:

Enter Vehicle Info: In the Vehicle info field, type the year, make, and model of your car (e.g., "2023 Honda Civic").

Enter Trip Mileage: Input the total miles driven for the trip in the Mileage field.

Enter Gas Price: Input the price per gallon of gas in the Gas price $ field.

Enter Gallons Used: Input the total number of gallons of fuel consumed during the trip.

Calculate: Click the Calculate button. The results will appear on the right-hand panel.

Save the File: A "Save As" dialog will pop up. Choose a location and name for your results file. The application will suggest a name based on your vehicle info.

Choose an Existing File (Optional): Click the Choose File button to select an existing log file to add new trip data to.

View Your Data: After saving, the View file button will become active. Click it to open the .txt log file and see all your recorded trips.

Get Help: If you need assistance, click the Help button to open the user guide PDF.

Exit: Click the Exit button to close the application.

👨‍💻 For Developers
<details>
<summary>Click here for instructions on running from source, project structure, and building.</summary>

Project Structure
CalcuTrip/
├── assets/
│   ├── imgs/
│   └── pdf/
├── main.py
└── README.md

Prerequisites
To run this project from the source code, you will need Python 3 installed on your system. The application uses the built-in tkinter library, so no external package installations are required.

Running from Source
Clone the repository:

git clone https://github.com/your-username/CalcuTrip.git

Navigate to the project directory:

cd CalcuTrip

Run the application:

python main.py


# Average MPG & Total Fuel Cost Calculator v1.09

This software denotes a fully working Tkinter GUI program that allows users to calculate the total average MPG and fuel cost for a trip.

To use this program one must enter the demographics of a car such as year, make, and model. Next, the user needs to enter valid trip details into the form. Afterward, the user can write the data to a file or view the program output results in the output window. Note. A user must enter a value greater than zero or the program will throw an error message saying: "Zero is not a valid input."

To install this software, simply download the latest installer zip found under the 'Releases' section on this GitHub repo.
Note: you must read and agree to the latest [Terms of Service](https://github.com/CPhillips-dev/average-mpg-calculator?tab=Apache-2.0-1-ov-file) and license agreements upon installing.
