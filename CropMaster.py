# -- Preloading -- #
import sys
import os

# Icon Path
Icon = os.path.join(sys._MEIPASS, 'Assets', 'Icon.ico') if getattr(sys, 'frozen', False) else os.path.join('Assets', 'Icon.ico')

# Check if the script is running in a bundled application
if getattr(sys, 'frozen', False):
    # If it is, add the bundled customtkinter directory to sys.path
    sys.path.append(os.path.join(sys._MEIPASS, 'customtkinter'))
    sys.path.append(os.path.join(sys._MEIPASS, 'CTkMessagebox'))
    sys.path.append(os.path.join(sys._MEIPASS, 'CTkToolTip'))


# -- Main Program -- #
from PIL import Image as IMG, ImageTk
from CTkMessagebox import CTkMessagebox
from CTkToolTip import CTkToolTip
from Update import UpdateCheck
from customtkinter import *
import math

class App(CTk):

    def __init__(self):
        CTk.__init__(self)
        CTk._set_appearance_mode(self, "dark")
        self.WindowWidth = 1920
        self.WindowHeight = 1080
        CTk.title(self, "Cropping Tool 0.2.0")
        CTk.iconbitmap(self, default=Icon)
        
        # Get screen width and height
        self.ScreenWidth = self.winfo_screenwidth()
        self.ScreenHeight = self.winfo_screenheight()
        
        # Calculate the position to center the window
        SpawnX = int((self.ScreenWidth / 2) - (self.WindowWidth / 2))
        SpawnY = int((self.ScreenHeight / 2) - (self.WindowHeight / 2))

        # Set the geometry with the start coordinates
        CTk.geometry(self, f'{self.WindowWidth}x{self.WindowHeight}+{SpawnX}+{SpawnY}')
        
        # Translate above to be proportionate to new window size
        self.CanvasMaxHeight = 751
        self.canvas = CTkCanvas(self, width=self.WindowWidth, height=self.CanvasMaxHeight, highlightthickness=0, bg="black")
        self.canvas.place(relx=0.0, rely=0.0, anchor = "nw")
        self.ImageOnCanvas = None
        
        # Global Widget Variables
        self.WidgetFont = "ComicSansMS"
        
        # Load the Resources and create the layout
        self.LoadResources()
        self.Layout()
        
        # Red Square Information
        self.SquareObject = None

        # InformationData
        self.InformationDictionary = {
            "Files Found": 0,
            "Zoom Level": 1.0,
            "Width": 0,
            "Height": 0,
            "Aspect Ratio": "0 : 0",
        }
        
        # Increment Button Dictionary
        self.ButtonStatus = {
            self.UpButton: "normal",
            self.DownButton: "normal",
            self.PlusOneButton: "normal",
            self.PlusFiveButton: "normal",
            self.PlusTenButton: "normal",
            self.MinusOneButton: "disabled",
            self.MinusFiveButton: "disabled",
            self.MinusTenButton: "disabled",
        }

        # Version Control
        VERSION = {"Major": 0, "Minor": 2, "Patch": 0}
        UpdateCheck(self, VERSION)
    
    def LoadResources(self):
        AssetBaseDirectory = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        
        ### Arrow Images ###
        self.UpArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "UpArrow.png")), None, (25, 30))
        self.DownArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "DownArrow.png")), None, (25, 30))
        self.LeftArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "LeftArrow.png")), None, (25, 30))
        self.RightArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "RightArrow.png")), None, (25, 30))
        
        ### Grey Arrow Images ###
        self.GreyUpArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "GreyUpArrow.png")), None, (25, 30))
        self.GreyDownArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "GreyDownArrow.png")), None, (25, 30))
        self.GreyLeftArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "GreyLeftArrow.png")), None, (25, 30))
        self.GreyRightArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "GreyRightArrow.png")), None, (25, 30))
    
    def Layout(self):
        ### Switches ###
        # Overwrite existing files Switch
        self.OverwriteExistingFiles = CTkSwitch(self, text="Overwrite Files", font=(self.WidgetFont, 25), switch_height=25, switch_width=50)
        self.OverwriteExistingFiles.place(relx=0.266, rely=0.83, anchor="center")
        self.CreateToolTip(self.OverwriteExistingFiles, "Overwrite Existing Files\nIf enabled, will replace existing files in the Output Directory.")

        # Keep Red Square Size Switch
        self.KeepRedSquareSizeSwitch = CTkSwitch(self, text="Keep Crop Size", font=(self.WidgetFont, 25), switch_height=25, switch_width=50)
        self.KeepRedSquareSizeSwitch.place(relx=0.268, rely=0.88, anchor="center")
        self.CreateToolTip(self.KeepRedSquareSizeSwitch,"Keep Selection Size\nIf enabled, will preserve the size of the selected area.")
                
        # Resize Directory Switch
        self.ResizeDirectory = CTkSwitch(self, text="Resize Directory", font=(self.WidgetFont, 25), switch_height=25, switch_width=50)
        self.ResizeDirectory.place(relx=0.27, rely=0.93, anchor="center")
        self.CreateToolTip(self.ResizeDirectory, "Resize Directory Toggle\nIf enabled, resizes all images in the selected directory.")
        
        # Lock Aspect Ratio Switch
        self.LockAspectRatio = CTkSwitch(self, text="Lock Aspect Ratio", font=(self.WidgetFont, 25), switch_height=25, switch_width=50)
        self.LockAspectRatio.place(relx=0.275, rely=0.98, anchor="center")
        self.CreateToolTip(self.LockAspectRatio, "Aspect Ratio Lock\nWill disable the Height slider and adjust the Height based on the Width.")
        
        ### Buttons ###
        # Select Directory Button
        SelectDirectoryButton = CTkButton(self, text="Select Directory", font=(self.WidgetFont, 20), command=self.LoadDirectory, width=35, height=30)
        SelectDirectoryButton.place(relx=0.045, rely=0.7175, anchor="center")
        
        # Open Output Dir Button
        self.OpenOutputDirButton = CTkButton(self, text="Open Output", font=(self.WidgetFont, 20), command=self.OpenOutputDirectory, width=35, height=30, state="disabled", fg_color="grey")
        self.OpenOutputDirButton.place(relx=0.038, rely=0.7575, anchor="center")
        
        # Crop Button
        self.CropButton = CTkButton(self, text="Crop", font=(self.WidgetFont, 30), command=self.CropAndSaveImageMain, state="disabled", fg_color="grey")
        self.CropButton.place(relx=0.45, rely=0.975, anchor="center")
        
        # Resize Button
        self.ResizeButton = CTkButton(self, text="Resize", font=(self.WidgetFont, 30), command=self.ResizeImageWindow, state="disabled", fg_color="grey")
        self.ResizeButton.place(relx=0.55, rely=0.975, anchor="center")
        
        # Next Image Button
        self.NextImageButton = CTkButton(self, text=">>>", font=(self.WidgetFont, 25), command=self.NextImage, state="disabled", fg_color="grey")
        self.NextImageButton.place(relx=0.55, rely=0.725, anchor="center")
        
        # Previous Image Button
        self.PreviousImageButton = CTkButton(self, text="<<<", font=(self.WidgetFont, 25), command=self.PreviousImage, state="disabled", fg_color="grey")
        self.PreviousImageButton.place(relx=0.45, rely=0.725, anchor="center")

        # Reset Square Button
        self.ResetSquareButton = CTkButton(self, text="Reset Square", font=(self.WidgetFont, 20), command=self.ResetSquare, state="disabled", fg_color="grey", hover_color="red")
        self.ResetSquareButton.place(relx=0.125, rely=0.7175, anchor="center")
        self.CreateToolTip(self.ResetSquareButton, "Reset Square\nResets the Red Square to the original size of the image.")
        
        # Exit Button
        self.ExitButton = CTkButton(self, text="Exit", font=(self.WidgetFont, 20), command=self.destroy, hover_color="red")
        self.ExitButton.place(relx=0.0425, rely=0.976, anchor="center")
        
        # Show Info Button
        self.ShowInfoButton = CTkButton(self, text="Show Info", font=(self.WidgetFont, 20), command=self.ShowInformation, hover_color="#3B88C3")
        self.ShowInfoButton.place(relx=0.0425, rely=0.925, anchor="center")
        
        ### Original Dimension Info ###
        LabelGap = 30
        InputGap = 65
        # Original Dimension Info Frame
        self.OriginalDimensionInfoFrame = CTkFrame(self, width=275, height=310)
        self.OriginalDimensionInfoFrame.place(relx=0.825, y=765)
        self.OriginalDimensionInfoFrame.configure(border_color="black", border_width=5)
        self.OriginalDimensionInfoFrame.lower()
        
        # Original Dimension Info Label
        self.OriginalDimensionLabel = CTkLabel(self.OriginalDimensionInfoFrame, text="Original Dimensions", font=(self.WidgetFont, 25), text_color="black")
        self.OriginalDimensionLabel.place(relx=0.5, y=20, anchor="center")
        self.OriginalDimensionLabel.lift()
        self.CreateToolTip(self.OriginalDimensionLabel, "Original Dimensions\nThe dimensions of the image before the crop.")
        
        # Original Dimension Info Width Label
        self.OriginalDimensionoWidthLabel = CTkLabel(self.OriginalDimensionInfoFrame, text="Width", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.OriginalDimensionoWidthLabel.place(relx=0.25, y=20 + LabelGap, anchor="center")
        self.OriginalDimensionoWidthLabel.lift()
        
        # Original Dimension Info Height Label
        self.OriginalDimensionHeightLabel = CTkLabel(self.OriginalDimensionInfoFrame, text="Height", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.OriginalDimensionHeightLabel.place(relx=0.75, y=20 + LabelGap, anchor="center")
        self.OriginalDimensionHeightLabel.lift()
        
        # Original Dimension Info Width Value Label
        self.OriginalDimensionWidthVar = StringVar(value="0")
        self.OriginalDimensionWidthValueLabel = CTkEntry(self.OriginalDimensionInfoFrame, placeholder_text="0", font=(self.WidgetFont, 17), text_color="white", width=80, height=20, textvariable=self.OriginalDimensionWidthVar, state="disabled")
        self.OriginalDimensionWidthValueLabel.place(relx=0.25, y=20 + InputGap, anchor="center")
        self.OriginalDimensionWidthValueLabel.configure(justify="center")
        self.OriginalDimensionWidthValueLabel.lift()
        
        # Original Dimension Info Height Value Label
        self.OriginalDimensionHeightVar = StringVar(value="0")
        self.OriginalDimensionHeightValueLabel = CTkEntry(self.OriginalDimensionInfoFrame, placeholder_text="0", font=(self.WidgetFont, 17), text_color="white", width=80, height=20, textvariable=self.OriginalDimensionHeightVar, state="disabled")
        self.OriginalDimensionHeightValueLabel.place(relx=0.75, y=20 + InputGap, anchor="center")
        self.OriginalDimensionHeightValueLabel.configure(justify="center")
        self.OriginalDimensionHeightValueLabel.lift()
        
        # Original Dimension Info New Dimensions Label
        self.NewDimensionsLabel = CTkLabel(self.OriginalDimensionInfoFrame, text="New Dimensions", font=(self.WidgetFont, 25), text_color="black")
        self.NewDimensionsLabel.place(relx=0.5, y=120, anchor="center")
        self.NewDimensionsLabel.lift()
        self.CreateToolTip(self.NewDimensionsLabel, "New Dimensions\nThe dimensions of the image after the crop.")
        
        # Original Dimension Info New Dimensions Width Label
        self.NewDimensionsWidthLabel = CTkLabel(self.OriginalDimensionInfoFrame, text="Width", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.NewDimensionsWidthLabel.place(relx=0.25, y=120 + LabelGap, anchor="center")
        self.NewDimensionsWidthLabel.lift()
        
        # Original Dimension Info New Dimensions Height Label
        self.NewDimensionsHeightLabel = CTkLabel(self.OriginalDimensionInfoFrame, text="Height", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.NewDimensionsHeightLabel.place(relx=0.75, y=120 + LabelGap, anchor="center")
        self.NewDimensionsHeightLabel.lift()
        
        # Original Dimension Info New Dimensions Width Value Label
        self.NewDimensionsWidthVar = StringVar(value="0")
        self.NewDimensionsWidthValueLabel = CTkEntry(self.OriginalDimensionInfoFrame, placeholder_text="0", font=(self.WidgetFont, 17), text_color="white", width=80, height=20, textvariable=self.NewDimensionsWidthVar, state="disabled")
        self.NewDimensionsWidthValueLabel.place(relx=0.25, y=120 + InputGap, anchor="center")
        self.NewDimensionsWidthValueLabel.configure(justify="center")
        self.NewDimensionsWidthValueLabel.lift()
        
        # Original Dimension Info New Dimensions Height Value Label
        self.NewDimensionsHeightVar = StringVar(value="0")
        self.NewDimensionsHeightValueLabel = CTkEntry(self.OriginalDimensionInfoFrame, placeholder_text="0", font=(self.WidgetFont, 17), text_color="white", width=80, height=20, textvariable=self.NewDimensionsHeightVar, state="disabled")
        self.NewDimensionsHeightValueLabel.place(relx=0.75, y=120 + InputGap, anchor="center")
        self.NewDimensionsHeightValueLabel.configure(justify="center")
        self.NewDimensionsHeightValueLabel.lift()
        
        # Aspect Ratio Label
        self.AspectRatioLabel = CTkLabel(self.OriginalDimensionInfoFrame, text="Aspect Ratio", font=(self.WidgetFont, 25), text_color="black")
        self.AspectRatioLabel.place(relx=0.5, y=220, anchor="center")
        self.AspectRatioLabel.lift()
        self.CreateToolTip(self.AspectRatioLabel, "Aspect Ratio\nThe aspect ratio of the image.")
        
        # Aspect Ratio Original Label
        self.AspectRatioOriginalLabel = CTkLabel(self.OriginalDimensionInfoFrame, text="Image", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.AspectRatioOriginalLabel.place(relx=0.25, y=220 + LabelGap, anchor="center")
        self.AspectRatioOriginalLabel.lift()
        
        # Aspect Ratio New Label
        self.AspectRatioNewLabel = CTkLabel(self.OriginalDimensionInfoFrame, text="Crop", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.AspectRatioNewLabel.place(relx=0.75, y=220 + LabelGap, anchor="center")
        self.AspectRatioNewLabel.lift()
        
        # Aspect Ratio Original Value Label
        self.AspectRatioOriginalVar = StringVar(value="0 : 0")
        self.AspectRatioOriginalValueLabel = CTkEntry(self.OriginalDimensionInfoFrame, placeholder_text="0", font=(self.WidgetFont, 17, "bold"), text_color="white", width=100, height=20, textvariable=self.AspectRatioOriginalVar, state="disabled")
        self.AspectRatioOriginalValueLabel.place(relx=0.25, y=220 + InputGap, anchor="center")
        self.AspectRatioOriginalValueLabel.configure(justify="center")
        self.AspectRatioOriginalValueLabel.lift()
        
        # Aspect Ratio New Value Label
        self.AspectRatioNewVar = StringVar(value="0 : 0")
        self.AspectRatioNewValueLabel = CTkEntry(self.OriginalDimensionInfoFrame, placeholder_text="0", font=(self.WidgetFont, 17, "bold"), text_color="white", width=100, height=20, textvariable=self.AspectRatioNewVar, state="disabled")
        self.AspectRatioNewValueLabel.place(relx=0.75, y=220 + InputGap, anchor="center")
        self.AspectRatioNewValueLabel.configure(justify="center")
        self.AspectRatioNewValueLabel.lift()
        
        ### Red Square Controls ###
        # Red Square Frame
        self.RedSquareFrame = CTkFrame(self, width=350, height=310)
        self.RedSquareFrame.place(relx=0.625, y=765)
        self.RedSquareFrame.configure(border_color="black", border_width=5)
        self.RedSquareFrame.lower()
        
        # Red Square Frame Dimensions Label
        self.SquareDimensionsLabel = CTkLabel(self.RedSquareFrame, text="Square Dimensions", font=(self.WidgetFont, 25), text_color="black")
        self.SquareDimensionsLabel.place(relx=0.5, y=20, anchor="center")
        self.SquareDimensionsLabel.lift()
        self.CreateToolTip(self.SquareDimensionsLabel, "Square Dimensions\nThe dimensions of the Red Crop Square.")

        # Red Square Frame Width Input Label
        self.HeightInputLabel = CTkLabel(self.RedSquareFrame, text="Height", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.HeightInputLabel.place(relx=0.25, y=20 + LabelGap, anchor="center")
        self.HeightInputLabel.lift()
        
        # Red Square Frame Height Input Label
        self.RedSquareWidthInputLabel = CTkLabel(self.RedSquareFrame, text="Width", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.RedSquareWidthInputLabel.place(relx=0.75, y=20 + LabelGap, anchor="center")
        self.RedSquareWidthInputLabel.lift()

        # Red Square Width Input
        self.RedSquareImageHeightVar = StringVar(value="0")
        self.RedSquareHeightInput = CTkEntry(self.RedSquareFrame, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white", placeholder_text="0", textvariable=self.RedSquareImageHeightVar)
        self.RedSquareHeightInput.place(relx=0.25, y=20 + InputGap, anchor="center")
        self.RedSquareHeightInput.configure(justify="center")
        self.RedSquareHeightInput.lift()
        
        # Red Square Height Input
        self.RedSquareImageWidthVar = StringVar(value="0")
        self.RedSquareWidthInput = CTkEntry(self.RedSquareFrame, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white", placeholder_text="0", textvariable=self.RedSquareImageWidthVar)
        self.RedSquareWidthInput.place(relx=0.75, y=20 + InputGap, anchor="center")
        self.RedSquareWidthInput.configure(justify="center")
        self.RedSquareWidthInput.lift()
        
        # Update Red Square Button
        self.UpdateSquareButton = CTkButton(self.RedSquareFrame, text="Update", font=(self.WidgetFont, 20), command=self.UpdateRedSquare, hover_color="#3B88C3", state="disabled", fg_color="grey")
        self.UpdateSquareButton.place(relx=0.25, y=130, anchor="center")
        
        # Center Red Square Button
        self.CenterSquareButton = CTkButton(self.RedSquareFrame, text="Center", font=(self.WidgetFont, 20), command=self.CenterRedSquare, hover_color="#3B88C3", state="disabled", fg_color="grey")
        self.CenterSquareButton.place(relx=0.75, y=130, anchor="center")
        
        # Add Traces to the Red Square Input Fields
        self.RedSquareImageHeightVar.trace_add("write", lambda *args: self.UpdateRedSquareInput(WH="Height"))
        self.RedSquareImageWidthVar.trace_add("write", lambda *args: self.UpdateRedSquareInput(WH="Width"))
        
        # Red Square Custom Aspect Ratio Label
        self.CustomAspectRatioLabel = CTkLabel(self.RedSquareFrame, text="Custom Aspect Ratio", font=(self.WidgetFont, 25), text_color="black")
        self.CustomAspectRatioLabel.place(relx=0.5, y=170, anchor="center")
        self.CustomAspectRatioLabel.lift()
        
        # Custom Aspect Ratio X Entry
        self.CustomAspectRatioXVar = StringVar(value="Height")
        self.CustomAspectRatioXInput = CTkEntry(self.RedSquareFrame, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="grey", placeholder_text="Height", textvariable=self.CustomAspectRatioXVar, state="disabled")
        self.CustomAspectRatioXInput.place(relx=0.25, y=205, anchor="center")
        self.CustomAspectRatioXInput.configure(justify="center", border_color="red", border_width=2)
        self.CustomAspectRatioXInput.lift()
        
        # Custom Aspect Ratio Y Entry
        self.CustomAspectRatioYVar = StringVar(value="Width")
        self.CustomAspectRatioYInput = CTkEntry(self.RedSquareFrame, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="grey", placeholder_text="Width", textvariable=self.CustomAspectRatioYVar, state="disabled")
        self.CustomAspectRatioYInput.place(relx=0.75, y=205, anchor="center")
        self.CustomAspectRatioYInput.configure(justify="center", border_color="red", border_width=2)
        
        # Switch to use Custom Aspect Ratio
        self.CustomAspectRatioSwitch = CTkSwitch(self.RedSquareFrame, text="Use Custom Aspect Ratio", font=(self.WidgetFont, 20), switch_height=20, switch_width=40, command=self.EnableCustomAspectRatio)
        self.CustomAspectRatioSwitch.place(relx=0.5, y=240, anchor="center")
        self.CreateToolTip(self.CustomAspectRatioSwitch, "Use Custom Aspect Ratio\nIf enabled, will use the custom aspect ratio.")
        
        # Lock Width and Height Switch
        self.LockWidthHeightSwitchSide = BooleanVar(value=False)
        self.LockWidthHeightSwitch = CTkSwitch(self.RedSquareFrame, text="", switch_height=20, switch_width=50, command=self.LockCustomAspectRatio, progress_color="red", fg_color="grey", font=(self.WidgetFont, 20), state="disabled", variable=self.LockWidthHeightSwitchSide)
        self.LockWidthHeightSwitch.place(relx=0.575, y=280, anchor="center")
        self.CreateToolTip(self.LockWidthHeightSwitch, "Lock Width\nIf enabled, will lock the width of the Red Square.")
        
        # Lock Height Label
        self.LockWidthLabel = CTkLabel(self.RedSquareFrame, text="Lock Height", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.LockWidthLabel.place(relx=0.25, y=250 + LabelGap, anchor="center")
        self.LockWidthLabel.lift()
        
        # Lock Width Label
        self.LockHeightLabel = CTkLabel(self.RedSquareFrame, text="Lock Width", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.LockHeightLabel.place(relx=0.75, y=250 + LabelGap, anchor="center")
        self.LockHeightLabel.lift()
        
        ### ARROW CONFIG ###
        # Arrow Button Locations and Controls
        SideButtonSpacing = 1.8
        DownButtonSpacing = 2.3
        ButtonHeight = 30 / 1080
        ButtonWidth = 25 / 1920
        StartX = 0.5
        StartY = 0.775
        
        # Up Button
        self.UpButton = CTkButton(self, command=lambda: self.PressButton("Up"), image=self.UpArrowImage, fg_color="#3B88C3", width=30, height=30, hover_color="#3B88C3", text="", border_width=0, border_spacing=0)
        self.UpButton.place(relx=StartX, rely=StartY, anchor="center")
        # Down Button
        self.DownButton = CTkButton(self, command=lambda: self.PressButton("Down"), image=self.DownArrowImage, fg_color="#3B88C3", width=30, height=30, hover_color="#3B88C3", text="", border_width=0, border_spacing=0)
        self.DownButton.place(relx=StartX, rely=StartY + DownButtonSpacing * ButtonHeight + 0.01, anchor="center")
        # Left Button
        self.LeftButton = CTkButton(self, command=lambda: self.PressButton("Left"), image=self.LeftArrowImage, fg_color="#3B88C3", width=30, height=30, hover_color="#3B88C3", text="", border_width=0, border_spacing=0)
        self.LeftButton.place(relx=StartX - SideButtonSpacing * ButtonWidth, rely=StartY + ButtonHeight + 0.01, anchor="center")
        # Right Button
        self.RightButton = CTkButton(self, command=lambda: self.PressButton("Right"), image=self.RightArrowImage, fg_color="#3B88C3", width=30, height=30, hover_color="#3B88C3", text="", border_width=0, border_spacing=0)
        self.RightButton.place(relx=StartX + SideButtonSpacing * ButtonWidth, rely=StartY + ButtonHeight + 0.01, anchor="center")
        
        ### Arrow Fidelity Buttons ###
        # Adjustment Input Field
        self.AdjustmentInput = CTkLabel(self, height=30, width=75, font=(self.WidgetFont, 20), text_color="white", justify="center", text="1", bg_color="#3B88C3")
        self.AdjustmentInput.place(relx=0.5, rely=0.915, anchor="center")
        self.CreateToolTip(self.AdjustmentInput, "Adjustment Input\nThe amount to move the Red Square by.", FontSize=20)

        # +1 Button
        self.PlusOneButton = CTkButton(self, text="+1", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("+", 1), width=50, hover_color="#3B88C3", corner_radius=10)
        self.PlusOneButton.place(relx=0.535, rely=0.915, anchor="center")
        # +5 Button
        self.PlusFiveButton = CTkButton(self, text="+5", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("+", 5), width=50, hover_color="#3B88C3", corner_radius=10)
        self.PlusFiveButton.place(relx=0.562, rely=0.915, anchor="center")
        # +10 Button
        self.PlusTenButton = CTkButton(self, text="+10", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("+", 10), width=50, hover_color="#3B88C3", corner_radius=10)
        self.PlusTenButton.place(relx=0.5904, rely=0.915, anchor="center")
        # -1 Button
        self.MinusOneButton = CTkButton(self, text="-1", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("-", 1), width=50, hover_color="#3B88C3", corner_radius=10, state="disabled", fg_color="grey")
        self.MinusOneButton.place(relx=0.465, rely=0.915, anchor="center")
        # -5 Button
        self.MinusFiveButton = CTkButton(self, text="-5", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("-", 5), width=50, hover_color="#3B88C3", corner_radius=10, state="disabled", fg_color="grey")
        self.MinusFiveButton.place(relx=0.438, rely=0.915, anchor="center")
        # -10 Button
        self.MinusTenButton = CTkButton(self, text="-10", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("-", 10), width=50, hover_color="#3B88C3", corner_radius=10, state="disabled", fg_color="grey")
        self.MinusTenButton.place(relx=0.4105, rely=0.915, anchor="center")

    def CreateToolTip(self, Widget, Text: str, FontSize: int = 20):
        # Create a tooltip from the given text and widget
        CTkToolTip(widget=Widget, message=Text, font=(self.WidgetFont, FontSize), delay=0.1, border_color="red", border_width=2, bg_color="black", alpha=1.0)
    
    def EnableDisableIncrement(self, CurrentValue: int):
        Buttons = {
            "up": {"button": self.UpButton, "condition": CurrentValue < self.CanvasMaxHeight},
            "down": {"button": self.DownButton, "condition": CurrentValue < self.CanvasMaxHeight},
            "plus_one": {"button": self.PlusOneButton, "condition": CurrentValue < self.WindowWidth},
            "plus_five": {"button": self.PlusFiveButton, "condition": CurrentValue < self.WindowWidth - 4},
            "plus_ten": {"button": self.PlusTenButton, "condition": CurrentValue < self.WindowWidth - 9},
            "minus_one": {"button": self.MinusOneButton, "condition": CurrentValue > 1},
            "minus_five": {"button": self.MinusFiveButton, "condition": CurrentValue > 5},
            "minus_ten": {"button": self.MinusTenButton, "condition": CurrentValue > 10},
        }
        
        for ButtonData in Buttons.values():
            Button = ButtonData["button"]
            Enable = ButtonData["condition"]
            State = self.ButtonStatus[Button]
            if Enable and State == "disabled":
                self.EnableInteract(Button)
                self.ButtonStatus[Button] = "normal"
            elif not Enable and State == "normal":
                self.DisableInteract(Button)
                self.ButtonStatus[Button] = "disabled"
    
    def UpdateAdjustmentLabel(self, Type: str, Value: int):
        # Grab the current value of the Adjustment Label
        CurrentValue = int(self.AdjustmentInput.cget("text"))

        # If the Type is to Increment the value
        if Type == "+":
            CurrentValue += Value
            if CurrentValue > self.WindowWidth:
                CTkMessagebox(title="Info", message="Can't be greater than the Width of the window.", icon="info")
                return
            else:
                self.AdjustmentInput.configure(text=CurrentValue)
                self.EnableDisableIncrement(CurrentValue)
        
        # If the Type is to Decrement the value
        elif Type == "-":
            CurrentValue -= Value
            if CurrentValue < 1:
                CTkMessagebox(title="Info", message="Can't be less than 1.", icon="info")
                return
            else:
                self.AdjustmentInput.configure(text=CurrentValue)
                self.EnableDisableIncrement(CurrentValue)
        # If the Type is invalid
        else:
            return
    
    def DisableInteract(self, button: CTkButton | CTkSwitch):
        if button == self.UpButton:
            button.configure(image=None)
            button.configure(image=self.GreyUpArrowImage, state="disabled", fg_color="grey", border_color="red", border_width=2)
        elif button == self.DownButton:
            button.configure(image=None)
            button.configure(image=self.GreyDownArrowImage, state="disabled", fg_color="grey", border_color="red", border_width=2)
        elif isinstance(button, CTkButton):
            button.configure(state="disabled", fg_color="grey")
        elif isinstance(button, CTkSwitch):
            button.configure(state="disabled", button_color="grey")
            
    def EnableInteract(self, button: CTkButton | CTkSwitch):
        if button == self.UpButton:
            button.configure(image=None)
            button.configure(image=self.UpArrowImage, state="normal", fg_color="#3B88C3", border_width=0)
        elif button == self.DownButton:
            button.configure(image=None)
            button.configure(image=self.DownArrowImage, state="normal", fg_color="#3B88C3", border_width=0)
        elif isinstance(button, CTkButton):
            button.configure(state="normal", fg_color="#1F6AA5")
        elif isinstance(button, CTkSwitch):
            button.configure(state="normal", button_color="#1F6AA5")
    
    def FadingInformationTextBox(self, Message: str, Duration: int = 5000):
        # Create a Label with the given message and destroy it after 5 seconds
        FadingLabel = CTkLabel(self, text=Message, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white")
        FadingLabel.place(relx=0.01, rely=0.01, anchor="nw")
        FadingLabel.lift()
        FadingLabel.after(Duration, FadingLabel.destroy)
        
        # Canvas for later, if Buttons are required.
        #FadingFrame = CTkFrame(self, width=300, height=75)
        #FadingFrame.place(relx=0.01, rely=0.01, anchor="nw")
        #FadingFrame.lift()
        #FadingFrame.after(5000, FadingFrame.destroy)
    
    def OpenOutputDirectory(self):
        # Open the Folder
        try:
            os.startfile(self.dir_path + "\\Output")
        except:
            # If it fails, open the current working directory
            os.startfile(os.getcwd())
    
    def ShowInformation(self):
        # Information Canvas Popup
        InformationPopOut = CTkToplevel(self, width=500, height=500, fg_color="black")
        InformationPopOut.title("Information")
        InformationPopOut.geometry(f"500x500+{int(self.ScreenWidth / 2 - 250)}+{int(self.ScreenHeight / 2 - 250)}")
        InformationPopOut.resizable(False, False)
        InformationPopOut.lift()
        InformationPopOut.attributes("-topmost", True)
        
        # Exit Button
        InformationExitButton = CTkButton(InformationPopOut, text="Exit", font=(self.WidgetFont, 20), command=InformationPopOut.destroy, hover_color="red")
        InformationExitButton.place(relx=0.5, rely=0.95, anchor="center")
        
        # Iterate over the data inside the InformationDictionary
        for Index, (Key, Value) in enumerate(self.InformationDictionary.items()):
            # Create the Key Label
            KeyLabel = CTkLabel(InformationPopOut, text=Key, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white")
            KeyLabel.place(relx=0.05, rely=0.05 + Index * 0.05, anchor="nw")
            KeyLabel.lift()
            
            # Create the Value Label
            ValueLabel = CTkLabel(InformationPopOut, text=Value, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white")
            ValueLabel.place(relx=0.4, rely=0.05 + Index * 0.05, anchor="nw")
            ValueLabel.lift()

    def UpdateRedSquareInput(self, WH: str):
        # Get the Max Width and Height
        MaxWidth = self.ResizedWidth
        MaxHeight = self.ResizedHeight

        # Ignore, when the Values are empty or 0
        if self.RedSquareImageHeightVar.get() in ["", 0, "0"] or self.RedSquareImageWidthVar.get() in ["", 0, "0"]:
            return

        # Get the current values of the Width and Height
        CurrentHeight = int(self.RedSquareImageHeightVar.get())
        CurrentWidth = int(self.RedSquareImageWidthVar.get())
        
        if WH == "Width":
            # If the Width is greater than the Max Width
            if CurrentWidth > MaxWidth:
                # Set the Width to the Max Width
                self.RedSquareImageWidthVar.set(MaxWidth)
                # If the Height is greater than the Max Height
                if CurrentHeight > MaxHeight:
                    # Set the Height to the Max Height
                    self.RedSquareImageHeightVar.set(MaxHeight)
            # If the Height is greater than the Max Height
            elif CurrentHeight > MaxHeight:
                # Set the Height to the Max Height
                self.RedSquareImageHeightVar.set(MaxHeight)
                # If the Width is greater than the Max Width
                if CurrentWidth > MaxWidth:
                    # Set the Width to the Max Width
                    self.RedSquareImageWidthVar.set(MaxWidth)
        elif WH == "Height":
            # If the Height is greater than the Max Height
            if CurrentHeight > MaxHeight:
                # Set the Height to the Max Height
                self.RedSquareImageHeightVar.set(MaxHeight)
                # If the Width is greater than the Max Width
                if CurrentWidth > MaxWidth:
                    # Set the Width to the Max Width
                    self.RedSquareImageWidthVar.set(MaxWidth)
            # If the Width is greater than the Max Width
            elif CurrentWidth > MaxWidth:
                # Set the Width to the Max Width
                self.RedSquareImageWidthVar.set(MaxWidth)
                # If the Height is greater than the Max Height
                if CurrentHeight > MaxHeight:
                    # Set the Height to the Max Height
                    self.RedSquareImageHeightVar.set(MaxHeight)
        else:
            return
    
    def EnableCustomAspectRatio(self):
        if self.CustomAspectRatioSwitch.get() == 0:
            # Disable the Input fields for the Custom Aspect Ratio
            self.CustomAspectRatioXInput.configure(state="disabled", border_color="red", text_color="grey")
            self.CustomAspectRatioYInput.configure(state="disabled", border_color="red", text_color="grey")
            # Set the Variables to Width and Height again as a reset
            self.CustomAspectRatioXVar.set("Height")
            self.CustomAspectRatioYVar.set("Width")
            # Disable the LockWidthHeightSwitch
            self.LockWidthHeightSwitch.configure(state="disabled", button_color="grey", fg_color="grey")
            # For sanity enable and set both the Width and Height Input Fields tro default
            self.RedSquareHeightInput.configure(state="normal", border_color="#565B5E", text_color="white")
            self.RedSquareWidthInput.configure(state="normal", border_color="#565B5E", text_color="white")
            # Switch the LockWidthHeightSwitch to the Left
            self.LockWidthHeightSwitchSide.set(False)
        else:
            # Enable the Input fields for the Custom Aspect Ratio
            self.CustomAspectRatioXInput.configure(state="normal", border_color="#565B5E", text_color="white")
            self.CustomAspectRatioYInput.configure(state="normal", border_color="#565B5E", text_color="white")
            # Set the variables to blank strings
            self.CustomAspectRatioXVar.set("")
            self.CustomAspectRatioYVar.set("")
            # Enable the LockWidthHeightSwitch
            self.LockWidthHeightSwitch.configure(state="normal", fg_color="red")
            # Disable the Height Input Field
            self.RedSquareHeightInput.configure(state="disabled", border_color="red", text_color="grey")
            # Switch the LockWidthHeightSwitch to the Left
            self.LockWidthHeightSwitchSide.set(False)
    
    def LockCustomAspectRatio(self):
        # Check if the Custom Aspect Ratio has been enable first
        if self.CustomAspectRatioSwitch.get() == 0:
            return
        # Disable the height input field if the switch is toggled on
        if self.LockWidthHeightSwitch.get() == 1:
            self.RedSquareHeightInput.configure(state="normal", border_color="#565B5E", text_color="white")
            self.RedSquareWidthInput.configure(state="disabled", border_color="red", text_color="grey")
        else:
            self.RedSquareHeightInput.configure(state="disabled", border_color="red", text_color="grey")
            self.RedSquareWidthInput.configure(state="normal", border_color="#565B5E", text_color="white")
            
    
    def UpdateRedSquare(self):
        # Get the New Width and Height
        NewWidth = int(self.RedSquareImageWidthVar.get())
        NewHeight = int(self.RedSquareImageHeightVar.get())

        # if the Aspect Ratio Switch is toggled on
        if self.LockAspectRatio.get() == 1:
            # Keep the aspect ratio and update the Width and Height to preserve the aspect ratio, round up to the nearest whole number
            if NewWidth > NewHeight:
                NewHeight = math.ceil(NewWidth / self.AspectRatio)
            elif NewHeight > NewWidth:
                NewWidth = math.ceil(NewHeight * self.AspectRatio)
            else:
                pass
        
        # If the Custom aspect ratio switch is toggled on
        if self.CustomAspectRatioSwitch.get() == 1:
            # Grab the Custom Aspect Ratio Values
            CustomAspectWidth, CustomAspectHeight = int(self.CustomAspectRatioXVar.get()), int(self.CustomAspectRatioYVar.get())
            AspectRatioValue = CustomAspectWidth / CustomAspectHeight
            if NewWidth / NewHeight > AspectRatioValue:
                NewHeight = math.ceil(NewWidth / AspectRatioValue)
                # Check if the value goes out of bounds of the original image and scale down both values if they do
                if NewHeight > self.ResizedHeight:
                    NewHeight = self.ResizedHeight
                    NewWidth = math.ceil(NewHeight * AspectRatioValue)
                    NewHeight = math.ceil(NewWidth / AspectRatioValue)
            elif NewWidth / NewHeight < AspectRatioValue:
                NewWidth = math.ceil(NewHeight * AspectRatioValue)
                # Check if the value goes out of bounds of the original image and scale down both values if they do
                if NewWidth > self.ResizedWidth:
                    NewWidth = self.ResizedWidth
                    NewHeight = math.ceil(NewWidth / AspectRatioValue)
                    NewWidth = math.ceil(NewHeight * AspectRatioValue)
            else:
                pass
        
        # Update the SquareObject
        self.SquareObject.Update(Width=NewWidth, Height=NewHeight)
        
        # Simplified Width and Height Calculation for the Variables
        self.CommonDivisor = math.gcd(NewWidth, NewHeight)
        self.SimpleWidth = int(NewWidth / self.CommonDivisor)
        self.SimpleHeight = int(NewHeight / self.CommonDivisor)
        self.AspectRatioNewVar.set(f"{self.SimpleWidth} : {self.SimpleHeight}")
        
        # Update the New Dimensions Width and Height Labels
        self.NewDimensionsWidthVar.set(int(NewWidth / self.Zoom))
        self.NewDimensionsHeightVar.set(int(NewHeight / self.Zoom))
        
        # Update the Adjustment Input Field
        self.RedSquareImageHeightVar.set(int(NewHeight))
        self.RedSquareImageWidthVar.set(int(NewWidth))
        
    def CenterRedSquare(self):
        # Get the width and height of the image
        ImageWidth = self.canvas.winfo_width()
        ImageHeight = self.canvas.winfo_height()

        # Get the width and height of the square
        SquareWidth = self.SquareObject.Width
        SquareHeight = self.SquareObject.Height
        
        # Get the X and Y of the square
        SquareX = self.SquareObject.X
        SquareY = self.SquareObject.Y

        # Get the center of the image
        ImageCenterX = ImageWidth / 2
        ImageCenterY = ImageHeight / 2

        # Get the center of the square
        SquareCenterX = SquareX + SquareWidth / 2
        SquareCenterY = SquareY + SquareHeight / 2

        # Get the difference between the center of the image and the center of the square
        DifferenceX = ImageCenterX - SquareCenterX
        DifferenceY = ImageCenterY - SquareCenterY
        
        # If the Difference is less than one, set it to 0. To Avoid rounding errors
        if DifferenceX < 1:
            DifferenceX = 0
        if DifferenceY < 1:
            DifferenceY = 0

        # Move the square by the difference
        self.SquareObject.Update(X=SquareX + DifferenceX, Y=SquareY + DifferenceY)

    def LoadDirectory(self):
        # Select a directory and load all the images in it
        self.dir_path = filedialog.askdirectory(initialdir="./", title="Select a Directory")
        if not self.dir_path:
            # No directory was selected, return and do nothing
            return

        # Get all the image files in the directory
        self.ImageFiles = [f for f in os.listdir(self.dir_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if not self.ImageFiles:
            CTkMessagebox(title="Error", message="No images found in the selected directory.", icon="warning", option_1="Ok")
            return

        # Update Information Dictionary with the number of files
        self.InformationDictionary["Files Found"] = len(self.ImageFiles)
        
        # Display the number of images found
        self.FadingInformationTextBox(Message=f"Found {len(self.ImageFiles)} images from the selected directory.", Duration=3000)
        
        # Enable the Next Image Button and the Resize + Crop Buttons
        self.EnableInteract(self.NextImageButton)
        self.EnableInteract(self.ResizeButton)
        self.EnableInteract(self.ResetSquareButton)
        self.EnableInteract(self.CropButton)
        self.EnableInteract(self.CenterSquareButton)
        self.EnableInteract(self.UpdateSquareButton)

        # Load the first image
        self.ImageIndex = 0
        self.LoadImage(self.ImageIndex)

    def CropAndSaveImageMain(self):
        # Format the savepath to only show the last 2 folders and name. Replace rest with a ..
        SavePath = self.dir_path
        SavePath = SavePath.replace("\\", "/")
        SavePath = SavePath.split("/")
        SavePath = SavePath[-2:]
        SavePath = "/".join(SavePath)
        SavePath = f"..{SavePath}"
        
        # If Directory flag is toggled, crop all images inside the folder to the given size
        if self.ResizeDirectory.get() == True:
            ResizedImageCounter = 0
            for imageName in self.ImageFiles:
                Data = self.CropAndSaveImage(imageName)
                ResizedImageCounter += 1
                if Data == False:
                    return
            self.FadingInformationTextBox(Message=f"Saved {ResizedImageCounter} Images\nTo {SavePath}", Duration=5000)
            # Enable the Select Output Directory
            self.EnableInteract(self.OpenOutputDirButton)
        else:
            Data = self.CropAndSaveImage(self.ImageFiles[self.ImageIndex])
            if Data == True:
                self.FadingInformationTextBox(Message=f"Saved {self.ImageFiles[self.ImageIndex]}\nTo {SavePath}", Duration=5000)
                self.EnableInteract(self.OpenOutputDirButton)
            else:
                pass

    def CropAndSaveImage(self, imageName):
        # Get the Squares X, Y, Width and Height
        SquareX = self.SquareObject.X
        SquareY = self.SquareObject.Y
        SquareWidth = self.SquareObject.Width
        SquareHeight = self.SquareObject.Height
        
        # Calculate the area of the Red Square which will get cut out, and all nunmbers are rounded to the nearest whole number
        CropArea = (round(SquareX - self.ImageX, None), round(SquareY - self.ImageY, None), round(SquareX + SquareWidth - self.ImageX, None), round(SquareY + SquareHeight - self.ImageY, None))

        # Converted Crop Area = Crop Area Divided by the Zoom Level rounded to the nearest full integer
        FullCrop = (round(CropArea[0] / self.Zoom), round(CropArea[1] / self.Zoom), round(CropArea[2] / self.Zoom), round(CropArea[3] / self.Zoom))
        
        # Open the Original Image for converting
        self.OriginalCropImage = IMG.open(f"{self.dir_path}/{imageName}")
        
        # Grab that Area from the scaled image and downscale the cropped bit to the original size
        CroppedImage = self.OriginalCropImage.crop(FullCrop).resize((self.ImageWidth, self.ImageHeight), IMG.Resampling.LANCZOS)
        
        # Create OutPut Directory if it doesn't exist
        if not os.path.exists(f"{self.dir_path}/Output"):
            os.mkdir(f"{self.dir_path}/Output")

        ## Save the cropped image to the Output directory
        OriginalImageName, OriginalImageExtension = os.path.splitext(imageName)
        CroppedImageName = f"{OriginalImageName}{OriginalImageExtension}"
        SavePath = os.path.join(f"{self.dir_path}/Output", CroppedImageName)
        if self.OverwriteExistingFiles.get() == True:
            CroppedImage.save(SavePath)
            return True
        if not os.path.exists(f"{self.dir_path}/Output/{CroppedImageName}"):
            CroppedImage.save(SavePath)
            return True
        else:
            CTkMessagebox(title="Error", message=f"File {CroppedImageName} already exists in the Output directory.", icon="warning", option_1="Ok")
            return False
    
    def NextImage(self):
        if self.ImageIndex >= len(self.ImageFiles) - 2:
            self.DisableInteract(self.NextImageButton)

        if self.ImageIndex < len(self.ImageFiles) - 1:
            self.ImageIndex += 1
            self.canvas.delete("all")
            self.LoadImage(self.ImageIndex)
            self.EnableInteract(self.PreviousImageButton)
        else:
            self.DisableInteract(self.NextImageButton)

    def PreviousImage(self):
        if self.ImageIndex <= 1:
            self.DisableInteract(self.PreviousImageButton)
            
        if self.ImageIndex > 0:
            self.ImageIndex -= 1
            self.canvas.delete("all")
            self.LoadImage(self.ImageIndex)
            self.EnableInteract(self.NextImageButton)
        else:
            self.DisableInteract(self.PreviousImageButton)
    
    def ResetSquare(self):
        # Grab values for the Width, Height and Position of the Image
        Width = self.ImageWidth * self.Zoom
        Height = self.ImageHeight * self.Zoom
        X, Y = self.ImageX, self.ImageY
        
        # Update the SquareObject
        self.SquareObject.Update(X=X, Y=Y, Width=Width, Height=Height)
        
        # Update the Red Square Input Fields
        self.RedSquareImageWidthVar.set(int(Width))
        self.RedSquareImageHeightVar.set(int(Height))

    def PressButton(self, Direction: str):
        # Check if there is an iamge present
        if self.ImageOnCanvas is None:
            CTkMessagebox(title="Error", message="Please select an image first.", icon="warning", option_1="Ok")
            return

        # Get the Adjustment Value        
        AdjustmentValue = int(self.AdjustmentInput.cget("text"))
        
        # TL;DR
        # Check if the Adjustment Value is greater than the distance between the square and the edge of the image
        # If it is, move the square to the edge of the image and display a message
        # If it isn't, move the square by the Adjustment Value
        if Direction == "Up":
            if AdjustmentValue > self.SquareObject.Y - self.ImageY or AdjustmentValue < 0:
                self.SquareObject.Update(Y=self.ImageY)
                self.FadingInformationTextBox(Message="Reached the Max value\nOnly moved the square to the edge.", Duration=2500)
            else:
                self.SquareObject.Update(Y=self.SquareObject.Y - AdjustmentValue)
        elif Direction == "Down":
            if AdjustmentValue > self.ImageY + self.ResizedHeight - self.SquareObject.Y - self.SquareObject.Height or AdjustmentValue < 0:
                self.SquareObject.Update(Y=self.ImageY + (self.ResizedHeight - self.SquareObject.Height))
                self.FadingInformationTextBox(Message="Reached the Max value\nOnly moved the square to the edge.", Duration=2500)
            else:
                self.SquareObject.Update(Y=self.SquareObject.Y + AdjustmentValue)
        elif Direction == "Left":
            if AdjustmentValue > self.SquareObject.X - self.ImageX or AdjustmentValue < 0:
                self.SquareObject.Update(X=self.ImageX)
                self.FadingInformationTextBox(Message="Reached the Max value\nOnly moved the square to the edge.", Duration=2500)
            else:
                self.SquareObject.Update(X=self.SquareObject.X - AdjustmentValue)
        elif Direction == "Right":
            if AdjustmentValue > self.ImageX + self.ResizedWidth - self.SquareObject.X - self.SquareObject.Width or AdjustmentValue < 0:
                self.SquareObject.Update(X=self.ImageX + (self.ResizedWidth - self.SquareObject.Width))
                self.FadingInformationTextBox(Message="Reached the Max value\nOnly moved the square to the edge.", Duration=2500)
            else:
                self.SquareObject.Update(X=self.SquareObject.X + AdjustmentValue)
        
    def LoadImage(self, ImageNr: int):
        # Load the image
        self.PreviewImage = IMG.open(f"{self.dir_path}/{self.ImageFiles[ImageNr]}")
        
        # Get the size of the image
        self.ImageWidth, self.ImageHeight = self.PreviewImage.size
        
        # Calculate the Aspect Ratio
        self.AspectRatio = self.ImageWidth / self.ImageHeight
        
        # Simplified Width and Height Calculation for the Original Aspect Ratio with HUman Readable format
        self.CommonDivisor = math.gcd(self.ImageWidth, self.ImageHeight)
        self.SimpleWidth = int(self.ImageWidth / self.CommonDivisor)
        self.SimpleHeight = int(self.ImageHeight / self.CommonDivisor)
        self.AspectRatioOriginalVar.set(f"{self.SimpleWidth} : {self.SimpleHeight}")

        # Update the Dimension Labels
        self.OriginalDimensionWidthVar.set(self.ImageWidth)
        self.OriginalDimensionHeightVar.set(self.ImageHeight)

        # Resize the image to fit the canvas
        CanvasWidth, CanvasHeight = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        # Substract 1 to prevent the Red Square from being cut off
        if self.AspectRatio > (CanvasWidth / CanvasHeight):
            self.ResizedWidth = CanvasWidth - 1
            self.ResizedHeight = int(CanvasWidth / self.AspectRatio) - 1
        else:
            self.ResizedHeight = CanvasHeight - 1
            self.ResizedWidth = int(CanvasHeight * self.AspectRatio) - 1

        # Resize the image
        self.PreviewImage = self.PreviewImage.resize((self.ResizedWidth, self.ResizedHeight), resample=IMG.Resampling.LANCZOS)
        
        # Create the PhotoImage
        self.PhotoImage = ImageTk.PhotoImage(self.PreviewImage)

        # Center the image on the canvas
        self.ImageX = (CanvasWidth - self.ResizedWidth) // 2
        self.ImageY = (CanvasHeight - self.ResizedHeight) // 2
        
        # Create the Image on the Canvas
        self.ImageOnCanvas = self.canvas.create_image(self.ImageX, self.ImageY, image=self.PhotoImage, anchor="nw")
        
        # Calculate the Zoom Levels
        self.ZoomWidth = self.ResizedWidth / self.ImageWidth
        self.ZoomHeight = self.ResizedWidth / self.ImageHeight
        self.Zoom = (self.ZoomWidth + self.ZoomHeight) / 2
        
        # Update the Information Dictionary
        self.InformationDictionary["Width"] = self.ImageWidth
        self.InformationDictionary["Height"] = self.ImageHeight
        self.InformationDictionary["Zoom Level"] = round(self.Zoom, 2)
        
        # Create the Square
        if self.KeepRedSquareSizeSwitch.get() and self.SquareObject is not None:
            # Use the stored properties
            StartX, StartY, StoredWidth, StoredHeight = self.SquareObject.SquareProperties

            # Create the Square Object and update the Red Square Input Fields
            self.SquareObject = Square(self.canvas, StartX, StartY, StoredWidth, StoredHeight, "red")
            self.RedSquareImageWidthVar.set(StoredWidth)
            self.RedSquareImageHeightVar.set(StoredHeight)
            self.SquareObject.Update(KeepSize=True)
        else:
            # Create the Square Object and update the Red Square Input Fields
            self.SquareObject = Square(self.canvas, self.ImageX, self.ImageY, self.ResizedWidth, self.ResizedHeight, "red")
            self.RedSquareImageWidthVar.set(self.ResizedWidth)
            self.RedSquareImageHeightVar.set(self.ResizedHeight)
            self.SquareObject.Update()
        
        # Store the Original Size of the image to reset the Square's size to the original size
        self.OriginalSize = (self.ImageX, self.ImageY, self.ImageX + self.ResizedWidth, self.ImageY + self.ResizedWidth)

        # Update the New Dimensions Labels
        self.NewDimensionsWidthVar.set(round(self.SquareObject.Width / self.Zoom))
        self.NewDimensionsHeightVar.set(round(self.SquareObject.Height / self.Zoom))

    ### Resize Image Window ###
    def ResizeImageWindow(self):
        # Center the window on the screen
        self.ResizeWindow = CTkToplevel(self, width=400, height=300, fg_color="black")
        self.ResizeWindow.title("Resize Image")
        self.ResizeWindow.geometry(f"400x300+{int(self.ScreenWidth / 2 - 250)}+{int(self.ScreenHeight / 2 - 250)}")
        self.ResizeWindow.resizable(False, False)
        self.ResizeWindow.attributes("-topmost", True)
        
        # Value Label
        self.ResizeValueLabel = CTkLabel(self.ResizeWindow, text="Value", font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white")
        self.ResizeValueLabel.place(relx=0.5, rely=0.05, anchor="nw")
        
        # Lock Label
        self.ResizeLockLabel = CTkLabel(self.ResizeWindow, text="Lock", font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white")
        self.ResizeLockLabel.place(relx=0.775, rely=0.05, anchor="nw")
        
        # Width Label
        WidthLabel = CTkLabel(self.ResizeWindow, text="Width", font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white")
        WidthLabel.place(relx=0.05, rely=0.175, anchor="nw")
        WidthLabel.lift()
        
        # Width Input
        self.ResizeImageWidthVar = StringVar(value=self.ImageWidth)
        self.WidthInput = CTkEntry(self.ResizeWindow, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white", placeholder_text=self.ImageWidth, textvariable=self.ResizeImageWidthVar)
        self.WidthInput.place(relx=0.4, rely=0.175, anchor="nw")
        self.WidthInput.lift()
        
        # Width Lock
        self.ResizeWidthLock = CTkSwitch(self.ResizeWindow, text="", font=(self.WidgetFont, 10), bg_color="black", fg_color="black", text_color="white", command=self.ResizeBoxIsTriggered, progress_color="black", border_color="grey", border_width=2, button_hover_color="#D5D9DE")
        self.ResizeWidthLock.place(relx=0.8, rely=0.175, anchor="nw")
        
        # Height Label
        HeightLabel = CTkLabel(self.ResizeWindow, text="Height", font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white")
        HeightLabel.place(relx=0.05, rely=0.275, anchor="nw")
        HeightLabel.lift()
        
        # Height Lock
        self.ResizeHeightLock = CTkSwitch(self.ResizeWindow, text="", font=(self.WidgetFont, 10), bg_color="black", fg_color="black", text_color="white", command=self.ResizeBoxIsTriggered, progress_color="black", border_color="grey", border_width=2, button_hover_color="#D5D9DE")
        self.ResizeHeightLock.place(relx=0.8, rely=0.275, anchor="nw")
        
        # Height Input
        self.ResizeImageHeightVar = StringVar(value=self.ImageHeight)
        self.HeightInput = CTkEntry(self.ResizeWindow, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white", placeholder_text=self.ImageHeight, textvariable=self.ResizeImageHeightVar)
        self.HeightInput.place(relx=0.4, rely=0.275, anchor="nw")
        self.HeightInput.lift()
        
        # Resize entire Directory Switch
        self.ResizeEntireDirectory = CTkSwitch(self.ResizeWindow, text="Resize Directory", font=(self.WidgetFont, 20), switch_height=25, switch_width=50)
        self.ResizeEntireDirectory.place(relx=0.1, rely=0.5, anchor="nw")
        
        # Keep Aspect Ratio Switch
        self.ResizeKeepAspectRatio = CTkSwitch(self.ResizeWindow, text="Keep Aspect Ratio", font=(self.WidgetFont, 20), switch_height=25, switch_width=50)
        self.ResizeKeepAspectRatio.place(relx=0.1, rely=0.65, anchor="nw")
        
        # Resize Button
        ResizeButton = CTkButton(self.ResizeWindow, text="Resize", font=(self.WidgetFont, 20), command=self.ResizeImage, hover_color="#3B88C3")
        ResizeButton.place(relx=0.1, rely=0.85, anchor="nw")
        ResizeButton.lift()
        
        # Cancel Button
        CancelButton = CTkButton(self.ResizeWindow, text="Cancel", font=(self.WidgetFont, 20), command=self.ResizeWindow.destroy, hover_color="red")
        CancelButton.place(relx=0.55, rely=0.85, anchor="nw")
        CancelButton.lift()
        
        # Trace the Width and Height Inputs
        self.ResizeImageWidthVar.trace_add("write", lambda *args: self.ResizeUpdate("Width"))
        self.ResizeImageHeightVar.trace_add("write", lambda *args: self.ResizeUpdate("Height"))
    
    def ResizeBoxIsTriggered(self):
        if self.ResizeWidthLock.get():
            self.ResizeHeightLock.configure(state="disabled", button_color="red")
            self.ResizeWidthLock.configure(state="normal", button_color="#377D08")
        elif self.ResizeHeightLock.get():
            self.ResizeWidthLock.configure(state="disabled", button_color="red")
            self.ResizeHeightLock.configure(state="normal", button_color="#377D08")
        else:
            self.ResizeHeightLock.configure(state="normal", button_color="#D5D9DE")
            self.ResizeWidthLock.configure(state="normal", button_color="#D5D9DE")
    
    def ResizeUpdate(self, WH: str):
        MaxSize = 9999
    
        if WH == "Height":
            if self.ResizeImageHeightVar.get() == "" or self.ResizeImageHeightVar.get() == "0":
                return
            if self.ResizeHeightLock.get():
                NewSize = int(self.ResizeImageHeightVar.get()) * (self.ImageWidth / self.ImageHeight)
                if NewSize >= MaxSize:
                    self.ResizeImageWidthVar.set(int(MaxSize))
                    self.ResizeImageHeightVar.set(int(MaxSize))
                    return
                else:
                    self.ResizeImageWidthVar.set(int(NewSize))
                    return
            if self.ResizeKeepAspectRatio.get() and self.ResizeImageWidthVar.get() != 0:
                NewSize = int(self.ResizeImageWidthVar.get()) / (self.ImageWidth / self.ImageHeight)
                if NewSize >= MaxSize:
                    self.ResizeImageHeightVar.set(int(MaxSize))
                    self.ResizeImageWidthVar.set(int(MaxSize))
                    return
                else:
                    self.ResizeImageHeightVar.set(int(NewSize))
                    return
            else:
                return
        elif WH == "Width":
            if self.ResizeImageWidthVar.get() == "" or self.ResizeImageWidthVar.get() == "0":
                return
            if self.ResizeWidthLock.get():
                NewSize = int(self.ResizeImageWidthVar.get()) / (self.ImageWidth / self.ImageHeight)
                if NewSize >= MaxSize:
                    self.ResizeImageHeightVar.set(int(MaxSize))
                    self.ResizeImageWidthVar.set(int(MaxSize))
                    return
                else:
                    self.ResizeImageHeightVar.set(int(NewSize))
                    return
            if self.ResizeKeepAspectRatio.get() and self.ResizeImageHeightVar.get() != 0:
                NewSize = int(self.ResizeImageHeightVar.get()) * (self.ImageWidth / self.ImageHeight)
                if NewSize >= MaxSize:
                    self.ResizeImageWidthVar.set(int(MaxSize))
                    self.ResizeImageHeightVar.set(int(MaxSize))
                    return
                else:
                    self.ResizeImageWidthVar.set(int(NewSize))
                    return
        else:
            return

    def ResizeImage(self):
        # Check if both Height and Width are filled in
        NewWidth = int(self.ResizeImageWidthVar.get())
        NewHeight = int(self.ResizeImageHeightVar.get())

        # Check if the variables are 0 or empty
        if not NewWidth or not NewHeight or NewWidth == 0 or NewHeight == 0:
            CTkMessagebox(title="Error", message="Please fill in both Width and Height.", icon="warning", option_1="Ok")
            return

        # If both are filled and not zero, proceed with resizing
        self.ResizeImg = IMG.open(f"{self.dir_path}/{self.ImageFiles[self.ImageIndex]}")
        # Resize the image
        self.ResizeImg = self.ResizeImg.resize((NewWidth, NewHeight), IMG.LANCZOS)
        # Create OutPut Directory if it doesn't exist
        if not os.path.exists(f"{self.dir_path}/Output"):
            os.mkdir(f"{self.dir_path}/Output")
        # Save the Image
        self.ResizeImg.save(f"{self.dir_path}/Output/ResizedImage.png")
        # Check if the Resize Entire Directory Switch is on
        if self.ResizeEntireDirectory.get():
            # Resize all images in the directory
            for Image in os.listdir(self.dir_path):
                # Check if the file is a valid image
                if Image.endswith(".png") or Image.endswith(".jpg") or Image.endswith(".jpeg") or Image.endswith(".gif"):
                    # Open the image
                    self.ResizeImg = IMG.open(f"{self.dir_path}/{Image}")
                    # Resize the image
                    self.ResizeImg = self.ResizeImg.resize((NewWidth, NewHeight), IMG.LANCZOS)
                    # Save the image
                    self.ResizeImg.save(f"{self.dir_path}/Output/{Image}")
                else:
                    continue
            # Display a CTkMessagebox with the amount of images resized
            CTkMessagebox(title="Success", message=f"Resized {len(os.listdir(self.dir_path))} images.", icon="info", option_1="Ok")
            self.EnableInteract(self.OpenOutputDirButton)
        else:
            CTkMessagebox(title="Success", message="Resized 1 image.", icon="info", option_1="Ok")
            self.EnableInteract(self.OpenOutputDirButton)

### Other Classes ###
class Square:
    def __init__(self, Canvas: CTkCanvas, X: int, Y: int, Width: int, Height: int, Color="Red"):
        self.Canvas = Canvas
        self.X = X
        self.Y = Y
        self.Width = Width
        self.Height = Height
        self.Color = Color
        self.ID = None
        self.SquareProperties = None

    def Draw(self, KeepSize=False):
        if self.ID != None:
            self.Canvas.delete(self.ID)
        self.ID = self.Canvas.create_rectangle(self.X, self.Y, self.X + self.Width, self.Y + self.Height, outline=self.Color)
        if not KeepSize:
            self.SquareProperties = (self.X, self.Y, self.Width, self.Height)
        else:
            pass

    def Update(self, X=None, Y=None, Width=None, Height=None, KeepSize=False):
        # For better readability create a dict and go over the attrivutes.
        Attributes = {"X": X, "Y": Y, "Width": Width, "Height": Height}
        for Attribute, Value in Attributes.items():
            if Value != None:
                setattr(self, Attribute, Value)
        # Update the Square Properties
        self.SquareProperties = (self.X, self.Y, self.Width, self.Height)
        # ReDraw the Square
        self.Draw(KeepSize)

if __name__ == "__main__":
    App().mainloop()
