# Import tkinter library
# Program name:       Average MPG and Total Fuel Cost calculator
# Author:             Charles Phillips
# Version:            version 1.0
# Last revision date: 12/12/2022
# The objective of this program is to prompt a user to enter the demographics of a car such as year, make and model,
# and then generate the calculated average MPG of a car along with the total amount of money spent on fuel.
# Finally, it records the results to a file.

import os
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter.filedialog import asksaveasfilename

'-----------------"Function for creating tkinter windows"--------------'
# Title of program
title = 'Average MPG and Total Fuel Cost Calculator'
mainScreen = Tk()  # Creates a tkinter window
mainScreen.iconphoto(True, PhotoImage(file='icon.png'))  # True allows my custom app icon to show up on each new window
mainScreen.title(title + ' - Main Screen')
mainScreen.geometry("600x440")  # Sets the geometry of the tkinter frame
mainScreen.configure(bg='#7F7F7F')  # Sets the window background to dark grey


# Main function for creating widgets, placing widgets, and initializing key variables for use in the program
class UIWindow:
    def __init__(self, window):  # This function initializes the program window.
        self.avgMpg = 0
        self.carInfo = ''
        self.file_Path = ''
        self.prev_file_Path = ''  # Used to store the previous file path that was successfully writen to
        self.fuelCost = 0
        self.gasPrice = 0
        self.gasUsed = 0
        self.tripMileage = 0
        self.tripNumber = 0
        self.total_fields = 4
        self.valid_fields = 0
        self.headerImg = PhotoImage(file='header.png', master=window)  # Creates a header background for the screen
        self.bg_lbl = Label(window, image=self.headerImg)
        self.bg_lbl.place(x=-2, y=-2)
        # Creates the UI images
        self.panelImg = PhotoImage(file='result_panel.png', master=window)
        self.result_panel = Label(window, image=self.panelImg)
        self.result_panel.place(x=350, y=125)
        self.bg_header_text = Label(window, text='Average MPG and Total Fuel Cost Calculator', bg="#929292", fg="white",
                                    font="Calibri, 18")
        self.bg_header_text.place(x=100, y=35)

        # Create labels, inputs and place it on the window using the tkinter grid manager
        self.carInfoLbl = Label(window, text="Car year, make and model:", bg="#7F7F7F", fg="white", font="Calibri, 12")
        self.carInfoLbl.place(x=5, y=125)
        self.carInfoInput = Entry(window, bd=3, width=20)  # This creates an entry field for the car demographics
        self.carInfoInput.place(x=200, y=125)  # This is the coordinate to place the input box
        self.gasPriceLbl = Label(window, text='Price of gas per gallon: $', bg="#7F7F7F", fg="white",
                                 font="Calibri, 12")
        self.gasPriceLbl.place(x=15, y=225)
        self.gasPriceInput = Entry(window, bd=3)
        self.gasPriceInput.place(x=200, y=225)
        self.gasUsedLbl = Label(window, text='Gallons of gas used:', bg="#7F7F7F", fg="white", font="Calibri, 12")
        self.gasUsedLbl.place(x=50, y=275)
        self.gasUsedInput = Entry(window, bd=3)
        self.gasUsedInput.place(x=200, y=275)
        self.tripMileageLbl = Label(window, text='Trip mileage:', bg="#7F7F7F", fg="white", font="Calibri, 12")
        self.tripMileageLbl.place(x=100, y=175)
        self.tripMileageInput = Entry(window, bd=3)  # bd=3 creates a 3d border outline around the input box
        self.tripMileageInput.place(x=200, y=175)
        # Header for program result output
        self.resultHeader = Label(window, text='Program results:', bg="#8F8F8F", fg="white",
                                  font="Calibri, 12", )
        self.resultHeader.place(x=375, y=150)

        # The results of the program are printed out using these labels
        self.avgMpgLbl = Label(window, text=f'Average MPG: ', bg="#8F8F8F", fg="white", font="Calibri, 12", )
        # Holder for describing the received output results
        self.avgMpgLbl.place(x=375, y=200)
        self.avgMpg_result = Label(window, bg="#8F8F8F", fg="white", font="Calibri, 12")
        self.avgMpg_result.place(x=480, y=200)
        self.fuelCostLbl = Label(text=f'Total fuel cost: $ ', bg="#8F8F8F", fg="white", font="Calibri, 12")
        self.fuelCostLbl.place(x=375, y=250)
        self.fuelCost_result = Label(window, bg="#8F8F8F", fg="white", font="Calibri, 12")
        self.fuelCost_result.place(x=490, y=250)
        # Label for displaying current file path
        self.currentFilePathLbl = Label(window, text='Currently saving to:', bg="#7F7F7F", fg="white",
                                        font="Calibri, 10")
        self.currentFilePathLbl.place(x=7, y=405)
        self.currentFilePath = Label(window, text=self.file_Path, bg="#7F7F7F", fg="white", font="Calibri, 10")
        self.currentFilePath.place(x=125, y=405)
        # Button for calculating trip data and writing a file
        self.calculateBtn = Button(window, bg="#ADADAD", height=2, width=15, fg="white", relief='groove',
                                   text='Calculate trip data', command=lambda: self.check_fields(self.gather_data),
                                   state=NORMAL)
        self.calculateBtn.place(x=10, y=350)
        # Button for creating a new file to save calculated data to.
        # self.portal passes my intended command through a validation process before allowing the input into my program
        self.chooseFileBtn = Button(window, bg="#ADADAD", height=2, width=10, fg="white", relief='groove',
                                    text='Choose file', command=lambda: self.check_fields(self.choose_file),
                                    state=NORMAL)
        self.chooseFileBtn.place(x=150, y=350)
        # Button for viewing the contents of the currently opened file.
        self.viewFileBtn = Button(window, bg="#ADADAD", height=2, width=10, fg="white", relief='groove',
                                  text='View file', command=self.view_file, state=DISABLED)
        self.viewFileBtn.place(x=250, y=350)
        # Button for prompting the user if they wish to quit the app
        self.mainExitBtn = Button(window, text="Exit", bg="#ADADAD", height=2, width=10, fg="white",
                                  relief='groove', command=self.quit_app_prompt)
        self.mainExitBtn.place(x=450, y=350)

    # ########################################### Functions used for input validation

    # Function for checking if all the input fields are both filled and contain valid
    # entries before passing the input variables into the program.
    def check_fields(self, command):
        if not self.empty_fields() and self.validated_fields():
            command()

    # Function for verifying that all the input fields are filled before allowing the user to create a file
    def empty_fields(self):
        if len(self.carInfoInput.get()) == 0 or len(self.tripMileageInput.get()) == 0 or len(
                self.gasPriceInput.get()) == 0 or len(self.gasUsedInput.get()) == 0:
            messagebox.showerror('Missing input field entries!', 'All entry fields need to be filled in to create file.')
            return True
        else:
            return False

    # Function for validating entered car names
    def validate_str(self, str_in):
        if str_in.isalnum() != 0:
            messagebox.showerror('Invalid car name!', 'Please enter a valid, car year, make and model.')
        else:
            str_out = str_in
            self.valid_fields += 1
            return str_out

    # Function for checking numerical entry fields
    def validate_num(self, var_in, field):
        try:
            if float(var_in) > 0:
                var_out = float(var_in)
                self.valid_fields += 1
                return var_out
        except ValueError:
            messagebox.showerror('Invalid entry!', f"The {field} entry field contains the string input: {var_in}.")
        else:
            messagebox.showerror('Invalid entry!', f"{var_in} entered in the {field} field was not greater than zero.")

    # Checks each input field for validity before returning true
    def validated_fields(self):
        self.carInfo = self.validate_str(self.carInfoInput.get())  # Checks the current value from the input field
        self.gasPrice = self.validate_num(self.gasPriceInput.get(), 'Gas price')
        self.gasUsed = self.validate_num(self.gasUsedInput.get(), 'Gas used')
        self.tripMileage = self.validate_num(self.tripMileageInput.get(), 'Trip mileage')
        if self.valid_fields == self.total_fields:
            self.valid_fields = 0
            return True
        else:
            self.valid_fields = 0
            return False

    # This function is used to calculate the total average mpg and the amount of money spent in gas.
    def gather_data(self):
        round(self.gasPrice, 2)
        round(self.gasUsed, 2)
        round(self.tripMileage, 2)
        # Mathematical formula for calculating the average MPG
        avgMpg = int(round(self.tripMileage / self.gasUsed, 1))
        self.avgMpg = round(avgMpg, 2)

        # Calculation to determine the total amount of gas money spent on a trip.
        fuelCost = int(round(self.tripMileage / self.avgMpg, 1)) * self.gasPrice
        self.fuelCost = round(fuelCost, 2)
        self.avgMpg_result.configure(text=self.avgMpg)  # Displays the total average MPG in program result window
        self.fuelCost_result.configure(text=self.fuelCost)  # Displays the total cost of fuel in program result window
        if self.file_Path != '':  # If a file is not currently opened, it asks the user to create a new file
            self.write_to_file_prompt()
        else:
            self.create_file_prompt()

    # Function for opening a save file window which allows the user to choose which file the program writes new data to
    def choose_file(self):
        self.file_Path = asksaveasfilename(initialfile=f'{self.carInfo} fuel economy data.txt', defaultextension=".txt",
                                           filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        self.calculateBtn.config(state=NORMAL)
        if not self.file_Path:  # If the user fails to enter a filename, this prevents the program from accepting a
            # null filename to write contents to.
            self.file_Path = self.prev_file_Path
            pass
        else:
            self.tripNumber = 1
            self.currentFilePath.configure(text=self.file_Path)  # Displays the current file path at the bottom of
            # the screen
            self.write_to_file_prompt()  # Asks the user if they want to write trip data to the current file or not
            self.viewFileBtn.config(state=NORMAL)  # Shows the view file button after writing new trip data to a file

    # ############################# User prompt message boxes #################################

    # Function to ask the user if they want to create a new file
    def create_file_prompt(self):
        response = messagebox.askquestion('Save data?', 'Save data to a file?')
        if response == 'yes':
            self.choose_file()  # Calls the function for choosing a new file to write trip data to
        elif response == 'no':
            pass
        else:
            messagebox.showwarning('error', 'Something went wrong!')

    # Function to ask the user if they want to add the calculated results to the open file or not
    def write_to_file_prompt(self):
        response = messagebox.askquestion('Write Data?', 'Write trip data to current file?')
        if response == 'yes':
            self.write_data()  # Calls the function for writing new trip data to current file
        elif response == 'no':
            pass
        else:
            messagebox.showwarning('error', 'Something went wrong!')

    # Function to ask the user if they want to quit the app or not
    def quit_app_prompt(self):
        response = messagebox.askquestion('Quit App?', 'Are you sure you want to quit?')
        if response == 'yes':
            self.quit_app()  # Calls the function for quitting the app
        elif response == 'no':
            pass
        else:
            messagebox.showwarning('error', 'Something went wrong!')

    '-----------------------------"File management functions"------------------------------'

    ########################################################################################

    # Function for writing trip data to the current file
    def write_data(self):
        print(self.file_Path)
        self.prev_file_Path = self.file_Path
        with open(self.file_Path, 'a') as fileContent:
            fileContent.write(
                str(f"On trip {self.tripNumber}, your {self.carInfo} averaged {self.avgMpg} MPG on a trip of"
                    f"{self.tripMileage} miles. ") + '\n')
            fileContent.write(str(f"Your total cost of fuel spent was: ${self.fuelCost}") + '\n')
            fileContent.close()  # Closes the open file
        # Enables new UI buttons once a file has been created
        self.tripNumber += 1
        self.clear_fields()  # This clears the input and output fields for use in the next iteration

    # Function for viewing the currently opened file's trip data
    def view_file(self):
        print(self.file_Path)
        os.system('"%s"' % self.file_Path)
        return

    '"Cleanup functions for clearing input entry fields, resetting program results and quitting the app"'

    ################################################################################################

    # Function for clearing input entry fields after writing data to a file
    def clear_fields(self):
        self.carInfoInput.delete(0, END)  # Clears input fields
        self.tripMileageInput.delete(0, END)
        self.gasPriceInput.delete(0, END)
        self.gasUsedInput.delete(0, END)

    # Function for quitting the app
    def quit_app(self):
        exit()


'------------------'"Tkinter window size configuration"'------------------------'
#################################################################################

# Makes tkinter windows Non-Resizable
mainScreen.resizable(False, False)
window_width = 600  # Default window size
window_height = 440  # Default window height

# Grabs the current default screen, height and width for use in centering.
screen_width = mainScreen.winfo_screenwidth()
screen_height = mainScreen.winfo_screenheight()

# Sets the position of the window to the center of the screen
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
mainScreen.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Sets the max and min size for each of the windows
mainWindow = UIWindow(mainScreen)  # Creates an instance for the main tkinter window
mainScreen.mainloop()  # Loops the mainScreen tkinter window
