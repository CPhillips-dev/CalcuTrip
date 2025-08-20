# Program name:       CalcuTrip
# Author:             Charles Phillips
# Version:            version 1.09
# Last revision date: 08/14/2025

# The objective of this program is to prompt a user to enter the demographics of a vehicle such as year, make, and model,
# and then generate the calculated average MPG of a vehicle along with the total amount of money spent on fuel.
# Finally, it records the results to a file.

import subprocess
import sys
import os
import json
import configparser
import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter.filedialog import asksaveasfilename

# -------------------- Helpers --------------------------------
def resource_path(relative_path: str) -> str:
    """
    Return absolute path to resource, works in developer mode, PyInstaller --onedir and --onefile.
    - For --onefile PyInstaller sets sys._MEIPASS to the temporary folder.
    - For --onedir PyInstaller sets sys.frozen and the exe is next to the data; use sys.executable directory.
    - Otherwise use the source file directory (this script lives in src/).
    """
    if getattr(sys, 'frozen', False):
        # running in a bundle
        base = getattr(sys, '_MEIPASS', None)
        if not base:
            # --onedir case: use directory containing the exe
            base = os.path.dirname(sys.executable)
    else:
        # running in normal python environment; assume assets are relative to project root
        # this file is expected in src/, assets in project_root/assets/
        this_file = os.path.abspath(__file__)
        src_dir = os.path.dirname(this_file)
        base = os.path.dirname(src_dir)  # project root
    return os.path.normpath(os.path.join(base, relative_path))

# -----------------"Image path setup and error checking"--------------
image_paths = {
    "icon": 'assets/imgs/icon.png',
    "header": 'assets/imgs/header.png',
    "result_panel": 'assets/imgs/result_panel.png'
}

def get_image_path(image_key: str) -> str:
    rel = image_paths.get(image_key)
    if not rel:
        raise KeyError(f"No image key '{image_key}' configured")
    return resource_path(rel)

# -----------------"Creating tkinter windows"--------------
mainScreen = Tk()

# Try to set icon and ignore failures gracefully
try:
    icon_path = get_image_path("icon")
    mainScreen.iconphoto(True, PhotoImage(file=icon_path))
except Exception:
    # If icon missing, continue silently
    pass

mainScreen.title('CalcuTrip - Main Screen')
mainScreen.geometry("600x440")
mainScreen.configure(bg="#565656")

class UIWindow:
    def __init__(self, window):
        self.window = window  # store root window reference here

        # program state
        self.avgMpg = 0.0
        self.vehicleInfo = ''
        self.file_Path = ''
        self.fuelCost = 0.0
        self.gasPrice = 0.0
        self.gasUsed = 0.0
        self.tripMileage = 0.0
        self.tripNumber = 1
        self.total_fields = 4
        self.valid_fields = 0

        # tkinter vars for dynamic labels
        self.vehicleInfoVar = StringVar()
        self.avgMpgVar = StringVar()
        self.fuelCostVar = StringVar()
        self.currentFilePathVar = StringVar(value="Current File Path: Not selected")

        # Header image (if available)
        try:
            header_img_path = get_image_path("header")
            self.headerImg = PhotoImage(file=header_img_path)
            self.bg_lbl = Label(window, image=self.headerImg, bg="#BDBDBD")
            self.bg_lbl.place(x=-2, y=-2)
        except Exception:
            # fallback: plain background header text only
            self.bg_lbl = None

        # Title label
        self.bg_header_text = Label(window, text='CalcuTrip - Average MPG & Fuel Cost Calculator', bg="#929292", fg="white",
                                    font="Calibri, 16")
        self.bg_header_text.place(x=95, y=35)

        # Result panel image (right side)
        try:
            result_panel_path = get_image_path("result_panel")
            self.panelImg = PhotoImage(file=result_panel_path)
            self.result_panel = Label(window, image=self.panelImg)
            self.result_panel.place(x=325, y=125)
        except Exception:
            self.result_panel = None

        # Labels dictionary for left input and right results
        self.labels = {
            "vehicleInfoLbl": Label(window, text='Vehicle info ', bg="#565656", fg="white", font="Calibri, 12"),
            "gasPriceLbl": Label(window, text='Gas price $ ', bg="#565656", fg="white", font="Calibri, 12"),
            "gasUsedLbl": Label(window, text='Gallons used ', bg="#565656", fg="white", font="Calibri, 12"),
            "tripMileageLbl": Label(window, text=f'Mileage (Trip {self.tripNumber})', bg="#565656", fg="white", font="Calibri, 12"),
            "vehicleHeaderLbl": Label(window, textvariable=self.vehicleInfoVar, bg="#8F8F8F", fg="white", font="Calibri, 12"),
            "avgMpgLbl": Label(window, textvariable=self.avgMpgVar, bg="#8F8F8F", fg="white", font="Calibri, 12"),
            "fuelCostLbl": Label(window, textvariable=self.fuelCostVar, bg="#8F8F8F", fg="white", font="Calibri, 12"),
            "currentFilePathLbl": Label(window, textvariable=self.currentFilePathVar, bg="#565656", fg="white", font="Calibri, 10")
        }

        # Entry widgets
        self.vehicleInfoInput = Entry(window, bd=3, width=15)
        self.vehicleInfoInput.place(x=175, y=125)
        self.tripMileageInput = Entry(window, bd=3, width=15)
        self.tripMileageInput.place(x=175, y=175)
        self.gasPriceInput = Entry(window, bd=3, width=15)
        self.gasPriceInput.place(x=175, y=225)
        self.gasUsedInput = Entry(window, bd=3, width=15)
        self.gasUsedInput.place(x=175, y=275)

        # place labels (match original layout)
        self.labels["vehicleInfoLbl"].place(x=50, y=125)
        self.labels["gasPriceLbl"].place(x=50, y=225)
        self.labels["gasUsedLbl"].place(x=50, y=275)
        self.labels["tripMileageLbl"].place(x=50, y=175)
        self.labels["vehicleHeaderLbl"].place(x=350, y=150)
        self.labels["avgMpgLbl"].place(x=350, y=200)
        self.labels["fuelCostLbl"].place(x=350, y=250)
        self.labels["currentFilePathLbl"].place(x=48, y=375)

        # Buttons
        self.calculateBtn = Button(window, bg="#ADADAD", height=1, width=10, fg="white", relief='groove',
                                   text='Calculate', command=lambda: self.check_fields(self.gather_data), state=NORMAL)
        self.calculateBtn.place(x=50, y=325)

        self.chooseFileBtn = Button(window, bg="#ADADAD", height=1, width=10, fg="white", relief='groove',
                                    text='Choose File', command=self.choose_file)
        self.chooseFileBtn.place(x=155, y=325)

        self.viewFileBtn = Button(window, bg="#ADADAD", height=1, width=10, fg="white", relief='groove',
                                  text='View file', command=self.view_file, state=DISABLED)
        self.viewFileBtn.place(x=255, y=325)

        self.helpBtn = Button(window, text="Help", bg="#ADADAD", height=1, width=10, fg="white", relief='groove',
                              command=self.open_help)
        self.helpBtn.place(x=355, y=325)

        self.mainExitBtn = Button(window, text="Exit", bg="#ADADAD", height=1, width=10, fg="white", relief='groove',
                                  command=self.quit_app_prompt)
        self.mainExitBtn.place(x=460, y=325)

    # ------------- Validation / field checking ------------------
    def check_fields(self, command):
        if not self.empty_fields() and self.validated_fields():
            command()
        # after performing operation clear inputs
        # (you already clear inside write_data as well; calling here keeps behavior consistent)
        self.clear_fields()

    def empty_fields(self) -> bool:
        if len(self.vehicleInfoInput.get().strip()) == 0 or len(self.tripMileageInput.get().strip()) == 0 or len(
                self.gasPriceInput.get().strip()) == 0 or len(self.gasUsedInput.get().strip()) == 0:
            messagebox.showerror('Missing input field entries!', 'All entry fields need to be filled in to create file.')
            return True
        return False

    def validate_str(self, str_in: str) -> str:
        s = str_in.strip()
        if not s:
            messagebox.showerror('Invalid vehicle name!', 'Please enter a valid vehicle year, make and model.')
            return None
        # sanitize for filenames: replace spaces/hyphens with underscore
        sanitized = s.replace(' ', '_').replace('-', '_')
        self.valid_fields += 1
        return sanitized

    def validate_num(self, var_in: str, field: str):
        try:
            val = float(var_in)
        except ValueError:
            messagebox.showerror('Invalid entry!', f"The {field} entry field contains the string input: {var_in}.")
            return None
        if val <= 0:
            messagebox.showerror('Invalid entry!', f"{var_in} entered in the {field} field was not greater than zero.")
            return None
        self.valid_fields += 1
        return val

    def validated_fields(self) -> bool:
        # reset counters before validating
        self.valid_fields = 0
        self.vehicleInfo = self.validate_str(self.vehicleInfoInput.get())
        self.gasPrice = self.validate_num(self.gasPriceInput.get(), field='Gas price')
        self.gasUsed = self.validate_num(self.gasUsedInput.get(), field='Gas used')
        self.tripMileage = self.validate_num(self.tripMileageInput.get(), field='Trip mileage')

        if self.valid_fields == self.total_fields:
            self.valid_fields = 0
            return True
        else:
            self.valid_fields = 0
            return False

    # ------------- Calculation and results ---------------------
    def gather_data(self):
        # Avoid division by zero (validated already ensures gasUsed > 0)
        try:
            avgMpg = self.tripMileage / self.gasUsed
        except Exception as e:
            messagebox.showerror("Error", f"Could not calculate MPG: {e}")
            return

        self.avgMpg = round(avgMpg, 2)

        # fuelCost = (tripMileage / avgMpg) * gasPrice  => which simplifies to gasUsed * gasPrice
        # using tripMileage/avgMpg is redundant; use gasUsed * gasPrice (less error-prone)
        self.fuelCost = round(self.gasUsed * self.gasPrice, 2)

        # update UI labels (textvariable)
        self.vehicleInfoVar.set(f'Vehicle: {self.vehicleInfo}')
        self.avgMpgVar.set(f'Average MPG: {self.avgMpg}')
        self.fuelCostVar.set(f'Total fuel cost: ${self.fuelCost}')

        # ask for file path and write
        self.file_Path = self.get_vehicle_file_path()
        if self.file_Path:
            self.write_data()

    # ---------------- File handling ----------------------------
    def get_vehicle_file_path(self) -> str:
        """
        Suggest a filename and prompt the user where to save (keeps Ask Save As behavior).
        """
        suggested_name = f"{self.vehicleInfo}_fuel_data.txt" if self.vehicleInfo else "fuel_data.txt"
        file_path = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=suggested_name,
            title="Save As"
        )
        if file_path:
            self.currentFilePathVar.set(f"Current File Path: {file_path}")
        return file_path

    def write_data(self):
        # append rows in a simple tabular-like text format
        try:
            first_row = not os.path.exists(self.file_Path) or os.path.getsize(self.file_Path) == 0
            with open(self.file_Path, 'a', encoding='utf-8') as fileContent:
                if first_row:
                    fileContent.write(f"{'Trip Number':<12}| {'Trip Mileage':<15}| {'Average MPG':<15}| {'Fuel Cost':<15}\n")
                    fileContent.write("-" * 65 + '\n')
                fileContent.write(f"{self.tripNumber:<12}| {self.tripMileage:<15}| {self.avgMpg:<15}| ${self.fuelCost:<14.2f}\n")
                fileContent.write("-" * 65 + '\n')
        except Exception as e:
            messagebox.showerror("File Error", f"Could not write to file:\n{e}")
            return

        self.tripNumber += 1
        self.viewFileBtn.config(state=NORMAL)
        # keep the results visible but clear inputs
        self.clear_fields()

    def choose_file(self):
        """
        Let user choose an existing file to write to (keeps original behavior).
        """
        file_name = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Choose file to save results",
            initialfile=f"{self.vehicleInfo}_fuel_data.txt" if self.vehicleInfo else "fuel_data.txt"
        )
        if file_name:
            self.file_Path = file_name
            self.currentFilePathVar.set(f"File path: {self.file_Path}")
            # If file exists and has content, set tripNumber to next row count (optional)
            try:
                if os.path.exists(self.file_Path):
                    # crude way to find next trip number: count lines that look like data rows
                    with open(self.file_Path, 'r', encoding='utf-8') as f:
                        lines = [ln for ln in f if ln.strip()]
                    # If header exists, estimate trips by counting separator lines
                    self.tripNumber = max(1, sum(1 for ln in lines if ln.strip() and not ln.startswith('-')) )
            except Exception:
                self.tripNumber = 1

    def view_file(self):
        """Open the current results file in Notepad (Windows) without blocking the GUI."""
        if not getattr(self, 'file_Path', None):
            messagebox.showwarning("No file selected", "There is no file to open. Please choose a file or create one first.")
            return
        try:
            # Use Popen so Notepad opens independently — GUI won't freeze.
            subprocess.Popen(['notepad.exe', self.file_Path], shell=False)
        except FileNotFoundError:
            # Notepad not found (very unlikely on Windows) — fallback to os.startfile
            try:
                os.startfile(self.file_Path)
            except Exception as e:
                messagebox.showerror("Error opening file", f"Could not open file:\n{e}")
        except Exception as e:
            messagebox.showerror("Error opening file", f"Could not open file:\n{e}")

    # ------------- Utility UI functions ------------------------
    def clear_fields(self):
        self.vehicleInfoInput.delete(0, END)
        self.tripMileageInput.delete(0, END)
        self.gasPriceInput.delete(0, END)
        self.gasUsedInput.delete(0, END)

    def quit_app_prompt(self):
        response = messagebox.askquestion('Quit App?', 'Are you sure you want to quit?')
        if response == 'yes':
            self.quit_app()

    def quit_app(self):
        self.window.destroy()

    def get_readme_url(self):
        ghUserName, ghRepoName = self.get_repo_metadata()
        return f"https://github.com/{ghUserName}/{ghRepoName}/blob/main/README.md"

    def get_repo_metadata(self):
        # 1. Try .git/config if available
        git_config = os.path.join(os.getcwd(), ".git", "config")
        if os.path.exists(git_config):
            parser = configparser.ConfigParser()
            parser.read(git_config)
            try:
                url = parser.get("remote \"origin\"", "url")
                # handle git@github.com:user/repo.git OR https://github.com/user/repo.git
                if url.startswith("git@"):
                    url = url.replace("git@", "https://").replace(":", "/")
                if url.endswith(".git"):
                    url = url[:-4]
                parts = url.split("/")
                return parts[-2], parts[-1]
            except Exception:
                pass

        # 2. Try repo_metadata.json if it exists
        repo_json = os.path.join(os.getcwd(), "_internal/repo/repo_metadata.json")
        if os.path.exists(repo_json):
            with open(repo_json, "r") as f:
                try:
                    data = json.load(f)
                    return data["ghUserName"], data["ghRepoName"]
                except Exception:
                    pass

        # 3. Fallback (safe default)
        return "CPhillips-dev", "CalcuTrip"

    # ------------- Help  -----------------------------
    def open_help(self):
        webbrowser.open(self.get_readme_url())

# ------------------ Tkinter window size configuration ------------------------
# Keep window fixed size (as before)
mainScreen.resizable(False, False)
window_width = 600
window_height = 440

# center on screen
screen_width = mainScreen.winfo_screenwidth()
screen_height = mainScreen.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
mainScreen.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# create UI and start
mainWindow = UIWindow(mainScreen)
mainScreen.mainloop()