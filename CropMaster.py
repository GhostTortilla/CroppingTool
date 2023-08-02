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
        """
        Description
        -----------
        Init Function for the Main Application
        """
        
        CTk.__init__(self)
        CTk._set_appearance_mode(self, "dark")
        self.WindowWidth = 1920
        self.WindowHeight = 1080
        self.Version = "0.2.0" # <- Version Control (Might need to get moved to a more accesible and easier to maintain place)
        CTk.title(self, f"Cropping Tool{self.Version}")
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
        self.MainLayout()
        
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
        VERSION = {"Major": int(self.Version[0]), "Minor": int(self.Version[2]), "Patch": int(self.Version[4])}
        UpdateCheck(self, VERSION)
    
    def LoadResources(self):
        """
        Description
        -----------
        Function to Load all the assets and create the images
        """
        
        # Get the Asset Base Directory
        AssetBaseDirectory = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        
        # Load and create the Normal Arrow Images
        self.UpArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "UpArrow.png")), None, (25, 30))
        self.DownArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "DownArrow.png")), None, (25, 30))
        self.LeftArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "LeftArrow.png")), None, (25, 30))
        self.RightArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "RightArrow.png")), None, (25, 30))
        
        # Load and create the Grey Arrow Images
        self.GreyUpArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "GreyUpArrow.png")), None, (25, 30))
        self.GreyDownArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "GreyDownArrow.png")), None, (25, 30))
        self.GreyLeftArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "GreyLeftArrow.png")), None, (25, 30))
        self.GreyRightArrowImage = CTkImage(IMG.open(os.path.join(AssetBaseDirectory, "Assets", "GreyRightArrow.png")), None, (25, 30))
    
    def MainLayout(self):
        """
        Description
        -----------
        Main Layout Function, All Layout related functions are bundled here.\n
        To execute as one in the startup process
        """
        
        # Switch Placement
        self.SwitchLayout()
        
        # Button Placement
        self.ButtonLayout()
        
        # Info Frame Placement
        self.InfoFrameLayout()
        
        # Red Square Placement
        self.RedSquareLayout()
        
        # Arrow Placement
        self.PositionArrowLayout()
    
    def SwitchLayout(self):
        """
        Description
        -----------
        Function for adding switches to the Layout
        """
        
        # Overwrite existing files Switch
        # - When Toggled, will overwrite all existing files in the output directory
        self.OverwriteExistingFiles = CTkSwitch(self, text="Overwrite Files", font=(self.WidgetFont, 25), switch_height=25, switch_width=50)
        self.OverwriteExistingFiles.place(relx=0.266, rely=0.83, anchor="center")
        self.CreateToolTip(self.OverwriteExistingFiles, "Overwrite Existing Files\nIf enabled, will replace existing files in the Output Directory.")

        # Keep Red Square Size Switch
        # - When Toggled, will keep the size of the red square when moving to the next image
        self.KeepRedSquareSizeSwitch = CTkSwitch(self, text="Keep Crop Size", font=(self.WidgetFont, 25), switch_height=25, switch_width=50)
        self.KeepRedSquareSizeSwitch.place(relx=0.268, rely=0.88, anchor="center")
        self.CreateToolTip(self.KeepRedSquareSizeSwitch,"Keep Selection Size\nIf enabled, will preserve the size of the selected area.")
                
        # Resize Directory Switch
        # - When Toggled, will resize all images in the selected directory (Only applicable when using the Resize Button)
        self.ResizeDirectory = CTkSwitch(self, text="Resize Directory", font=(self.WidgetFont, 25), switch_height=25, switch_width=50)
        self.ResizeDirectory.place(relx=0.27, rely=0.93, anchor="center")
        self.CreateToolTip(self.ResizeDirectory, "Resize Directory Toggle\nIf enabled, resizes all images in the selected directory.")
        
        # Lock Aspect Ratio Switch
        # - When Toggled, will lock the aspect ratio of the image
        self.LockAspectRatio = CTkSwitch(self, text="Lock Aspect Ratio", font=(self.WidgetFont, 25), switch_height=25, switch_width=50)
        self.LockAspectRatio.place(relx=0.275, rely=0.98, anchor="center")
        self.CreateToolTip(self.LockAspectRatio, "Aspect Ratio Lock\nAuto Adjusts opposite dimension (W/H) when enabled.")

    def ButtonLayout(self):
        """
        Description
        -----------
        Function for adding buttons to the Layout
        """

        # Select Directory Button
        # - Opens a file dialog to select a directory, Needs to be used in order to unlock the rest of the buttons etc.
        SelectDirectoryButton = CTkButton(self, text="Select Directory", font=(self.WidgetFont, 20), command=self.LoadDirectory, width=35, height=30)
        SelectDirectoryButton.place(relx=0.045, rely=0.7175, anchor="center")
        
        # Open Output Dir Button
        # - Opens the output directory in the file explorer if it exists, else opens the Current Working Directory CWD.
        self.OpenOutputDirButton = CTkButton(self, text="Open Output", font=(self.WidgetFont, 20), command=self.OpenOutputDirectory, width=35, height=30, state="disabled", fg_color="grey")
        self.OpenOutputDirButton.place(relx=0.038, rely=0.7575, anchor="center")
        
        # Crop Button
        # - Crops the image and saves it to the output directory if it exists, else creates it.
        self.CropButton = CTkButton(self, text="Crop", font=(self.WidgetFont, 30), command=self.CropAndSaveImageMain, state="disabled", fg_color="grey")
        self.CropButton.place(relx=0.45, rely=0.975, anchor="center")
        
        # Next Image Button
        # - Goes to the next image
        self.NextImageButton = CTkButton(self, text=">>>", font=(self.WidgetFont, 25), command=self.NextImage, state="disabled", fg_color="grey")
        self.NextImageButton.place(relx=0.55, rely=0.725, anchor="center")
        
        # Previous Image Button
        # - Goes back to the previous image
        self.PreviousImageButton = CTkButton(self, text="<<<", font=(self.WidgetFont, 25), command=self.PreviousImage, state="disabled", fg_color="grey")
        self.PreviousImageButton.place(relx=0.45, rely=0.725, anchor="center")

        # Reset Square Button
        # - Resets the red square to the original size of the image
        self.ResetSquareButton = CTkButton(self, text="Reset Square", font=(self.WidgetFont, 20), command=self.ResetSquare, state="disabled", fg_color="grey", hover_color="red")
        self.ResetSquareButton.place(relx=0.125, rely=0.7175, anchor="center")
        self.CreateToolTip(self.ResetSquareButton, "Reset Square\nResets the Red Square to the original size of the image.")
        
        # Show Info Button
        # - Opens the Information Window
        self.ShowInfoButton = CTkButton(self, text="Show Info", font=(self.WidgetFont, 20), command=self.ShowInformation, hover_color="#3B88C3")
        self.ShowInfoButton.place(relx=0.0425, rely=0.925, anchor="center")
        
        # Resize Button
        # - Opens the Resize Window
        self.ResizeButton = CTkButton(self, text="Resize", font=(self.WidgetFont, 30), command=self.ResizeImageWindow, state="disabled", fg_color="grey")
        self.ResizeButton.place(relx=0.55, rely=0.975, anchor="center")
        
        # Exit Button
        # - Exits the program
        self.ExitButton = CTkButton(self, text="Exit", font=(self.WidgetFont, 20), command=self.destroy, hover_color="red")
        self.ExitButton.place(relx=0.0425, rely=0.976, anchor="center")

    def InfoFrameLayout(self):
        """
        Description
        -----------
        Function for adding the Info Dimension Frame to the Layout\n
        
        Comment Information\n
        - \# Short Info
        - \# - Detail Info
        - \# + Extra Info
        
        """

        # Base Variables for Positioning
        LabelGap = 30
        InputGap = 65
        
        # Base Frame
        # - Frame for the Original Dimension Information to put all the widgets on / inside
        # + IF abbreviation for InfoFrame will get used in the rest of the code
        self.InfoFrame = CTkFrame(self, width=275, height=310)
        self.InfoFrame.place(relx=0.825, y=765)
        self.InfoFrame.configure(border_color="black", border_width=5)
        self.InfoFrame.lower()
        
        # Info Label
        # - Label for the Original Dimension Information
        self.IF_OriginalDimension_InfoLabel = CTkLabel(self.InfoFrame, text="Original Dimensions", font=(self.WidgetFont, 25), text_color="black")
        self.IF_OriginalDimension_InfoLabel.place(relx=0.5, y=20, anchor="center")
        self.IF_OriginalDimension_InfoLabel.lift()
        # - Tooltip for the Original Dimension Information
        self.CreateToolTip(self.IF_OriginalDimension_InfoLabel, "Original Dimensions\nThe dimensions of the image before the crop.")
        
        # Original Dimensions Width Label
        # - Label for the Original Dimension Width
        self.IF_OriginalDimension_WidthLabel = CTkLabel(self.InfoFrame, text="Width", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.IF_OriginalDimension_WidthLabel.place(relx=0.25, y=20 + LabelGap, anchor="center")
        self.IF_OriginalDimension_WidthLabel.lift()
        
        # Original Dimensions Height Label
        # - Label for the Original Dimension Height
        self.IF_OriginalDimension_HeightLabel = CTkLabel(self.InfoFrame, text="Height", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.IF_OriginalDimension_HeightLabel.place(relx=0.75, y=20 + LabelGap, anchor="center")
        self.IF_OriginalDimension_HeightLabel.lift()
        
        # Original Dimension Width Value Label
        # - Label for the Original Dimension Width Value
        # + Disabled by default, Enabled when a directory has been selected
        self.IF_OriginalDimension_WidthVar = StringVar(value="0")
        self.IF_OriginalDimension_WidthValueLabel = CTkEntry(self.InfoFrame, placeholder_text="0", font=(self.WidgetFont, 17), text_color="white", width=80, height=20, textvariable=self.IF_OriginalDimension_WidthVar, state="disabled")
        self.IF_OriginalDimension_WidthValueLabel.place(relx=0.25, y=20 + InputGap, anchor="center")
        self.IF_OriginalDimension_WidthValueLabel.configure(justify="center")
        self.IF_OriginalDimension_WidthValueLabel.lift()
        
        # Original Dimension Height Value Label
        # - Label for the Original Dimension Height Value
        # + Disabled by default, Enabled when a directory has been selected
        self.IF_OriginalDimension_HeightVar = StringVar(value="0")
        self.IF_OriginalDimension_HeightValueLabel = CTkEntry(self.InfoFrame, placeholder_text="0", font=(self.WidgetFont, 17), text_color="white", width=80, height=20, textvariable=self.IF_OriginalDimension_HeightVar, state="disabled")
        self.IF_OriginalDimension_HeightValueLabel.place(relx=0.75, y=20 + InputGap, anchor="center")
        self.IF_OriginalDimension_HeightValueLabel.configure(justify="center")
        self.IF_OriginalDimension_HeightValueLabel.lift()
        
        # New Dimensions
        # - Label for the New Dimension Information
        self.IF_NewDimension_InfoLabel = CTkLabel(self.InfoFrame, text="New Dimensions", font=(self.WidgetFont, 25), text_color="black")
        self.IF_NewDimension_InfoLabel.place(relx=0.5, y=120, anchor="center")
        self.IF_NewDimension_InfoLabel.lift()
        self.CreateToolTip(self.IF_NewDimension_InfoLabel, "New Dimensions\nThe dimensions of the image after the crop. (Full Size)")
        
        # New Dimensions Width Label
        # - Label for the New Dimension Width
        self.IF_NewDimension_WidthLabel = CTkLabel(self.InfoFrame, text="Width", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.IF_NewDimension_WidthLabel.place(relx=0.25, y=120 + LabelGap, anchor="center")
        self.IF_NewDimension_WidthLabel.lift()
        
        # New Dimensions Height Label
        # - Label for the New Dimension Height
        self.IF_NewDimension_HeightLabel = CTkLabel(self.InfoFrame, text="Height", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.IF_NewDimension_HeightLabel.place(relx=0.75, y=120 + LabelGap, anchor="center")
        self.IF_NewDimension_HeightLabel.lift()
        
        # New Dimension Width Value Label
        # - Label for the New Dimension Width Value
        # + Disabled by default, Enabled when a directory has been selected
        self.IF_NewDimension_WidthVar = StringVar(value="0")
        self.IF_NewDimension_WidthValueLabel = CTkEntry(self.InfoFrame, placeholder_text="0", font=(self.WidgetFont, 17), text_color="white", width=80, height=20, textvariable=self.IF_NewDimension_WidthVar, state="disabled")
        self.IF_NewDimension_WidthValueLabel.place(relx=0.25, y=120 + InputGap, anchor="center")
        self.IF_NewDimension_WidthValueLabel.configure(justify="center")
        self.IF_NewDimension_WidthValueLabel.lift()
        
        # New Dimension Height Value Label
        # - Label for the New Dimension Height Value
        # + Disabled by default, Enabled when a directory has been selected
        self.IF_NewDimension_HeightVar = StringVar(value="0")
        self.IF_NewDimension_HeightValueLabel = CTkEntry(self.InfoFrame, placeholder_text="0", font=(self.WidgetFont, 17), text_color="white", width=80, height=20, textvariable=self.IF_NewDimension_HeightVar, state="disabled")
        self.IF_NewDimension_HeightValueLabel.place(relx=0.75, y=120 + InputGap, anchor="center")
        self.IF_NewDimension_HeightValueLabel.configure(justify="center")
        self.IF_NewDimension_HeightValueLabel.lift()
        
        # Aspect Ratio Label
        # - Label for the Aspect Ratio Information
        self.IF_AspectRatioLabel = CTkLabel(self.InfoFrame, text="Aspect Ratio", font=(self.WidgetFont, 25), text_color="black")
        self.IF_AspectRatioLabel.place(relx=0.5, y=220, anchor="center")
        self.IF_AspectRatioLabel.lift()
        self.CreateToolTip(self.IF_AspectRatioLabel, "Aspect Ratio\nThe aspect ratio of the image.")
        
        # Aspect Ratio Original Label
        # - Label for the Aspect Ratio Original
        self.IF_Original_AspectRatioLabel = CTkLabel(self.InfoFrame, text="Image", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.IF_Original_AspectRatioLabel.place(relx=0.25, y=220 + LabelGap, anchor="center")
        self.IF_Original_AspectRatioLabel.lift()
        
        # Aspect Ratio New Label
        # - Label for the Aspect Ratio New
        self.IF_New_AspectRatioLabel = CTkLabel(self.InfoFrame, text="Crop", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.IF_New_AspectRatioLabel.place(relx=0.75, y=220 + LabelGap, anchor="center")
        self.IF_New_AspectRatioLabel.lift()
        
        # Aspect Ratio Original Value Label
        # - Label for the Aspect Ratio Original Value
        # + Disabled by default, Enabled when a directory has been selected
        self.IF_Original_AspectRatioVar = StringVar(value="0 : 0")
        self.IF_Original_AspectRatioValueLabel = CTkEntry(self.InfoFrame, placeholder_text="0", font=(self.WidgetFont, 17, "bold"), text_color="white", width=100, height=20, textvariable=self.IF_Original_AspectRatioVar, state="disabled")
        self.IF_Original_AspectRatioValueLabel.place(relx=0.25, y=220 + InputGap, anchor="center")
        self.IF_Original_AspectRatioValueLabel.configure(justify="center")
        self.IF_Original_AspectRatioValueLabel.lift()
        
        # Aspect Ratio New Value Label
        # - Label for the Aspect Ratio New Value
        # + Disabled by default, Enabled when a directory has been selected
        self.IF_New_AspectRatioVar = StringVar(value="0 : 0")
        self.IF_New_AspectRatioValueLabel = CTkEntry(self.InfoFrame, placeholder_text="0", font=(self.WidgetFont, 17, "bold"), text_color="white", width=100, height=20, textvariable=self.IF_New_AspectRatioVar, state="disabled")
        self.IF_New_AspectRatioValueLabel.place(relx=0.75, y=220 + InputGap, anchor="center")
        self.IF_New_AspectRatioValueLabel.configure(justify="center")
        self.IF_New_AspectRatioValueLabel.lift()

    def RedSquareLayout(self):
        """
        Description
        -----------
        Function for adding the Red Square Frame to the Layout\n
        
        Comment Information\n
        - \# Short Info
        - \# - Detail Info
        - \# + Extra Info
        
        """
        
        # Base Variables for Positioning
        LabelGap = 30
        InputGap = 65
        
        # Red Square Frame
        # - Frame for the Red Square Information to put all the widgets on / inside
        # + RS abbreviation for RedSquareFrame will get used in the rest of the code
        self.RedSquareFrame = CTkFrame(self, width=350, height=310)
        self.RedSquareFrame.place(relx=0.625, y=765)
        self.RedSquareFrame.configure(border_color="black", border_width=5)
        self.RedSquareFrame.lower()
        
        # Red Square Dimensions Label
        # - Label for the Red Square Dimensions
        self.RS_DimensionsLabel = CTkLabel(self.RedSquareFrame, text="Square Dimensions", font=(self.WidgetFont, 25), text_color="black")
        self.RS_DimensionsLabel.place(relx=0.5, y=20, anchor="center")
        self.RS_DimensionsLabel.lift()
        # - Tooltip for the Red Square Dimensions
        self.CreateToolTip(self.RS_DimensionsLabel, "Square Dimensions\nThe dimensions of the Red Crop Square.")

        # Red Square Height Input Label
        # - Label for the Red Square Height Input
        self.RS_HeightInputLabel = CTkLabel(self.RedSquareFrame, text="Height", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.RS_HeightInputLabel.place(relx=0.25, y=20 + LabelGap, anchor="center")
        self.RS_HeightInputLabel.lift()
        
        # Red Square Width Input Label
        # - Label for the Red Square Width Input
        self.RS_WidthInputLabel = CTkLabel(self.RedSquareFrame, text="Width", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.RS_WidthInputLabel.place(relx=0.75, y=20 + LabelGap, anchor="center")
        self.RS_WidthInputLabel.lift()

        # Red Square Height Input
        # - Input for the Red Square Height
        # + Enabled by Default, Is controlled by the Custom Aspect Ratio Switch
        self.RS_ImageHeightVar = StringVar(value="0")
        self.RS_HeightInput = CTkEntry(self.RedSquareFrame, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white", placeholder_text="0", textvariable=self.RS_ImageHeightVar)
        self.RS_HeightInput.place(relx=0.25, y=20 + InputGap, anchor="center")
        self.RS_HeightInput.configure(justify="center")
        self.RS_HeightInput.lift()
        
        # Red Square Height Input
        # - Input for the Red Square Width
        # + Enabled by Default, Is controlled by the Custom Aspect Ratio Switch
        self.RS_ImageWidthVar = StringVar(value="0")
        self.RS_WidthInput = CTkEntry(self.RedSquareFrame, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="white", placeholder_text="0", textvariable=self.RS_ImageWidthVar)
        self.RS_WidthInput.place(relx=0.75, y=20 + InputGap, anchor="center")
        self.RS_WidthInput.configure(justify="center")
        self.RS_WidthInput.lift()
        
        # Update Red Square Button
        # - Button for updating the Red Square size
        self.RS_UpdateSquareButton = CTkButton(self.RedSquareFrame, text="Update", font=(self.WidgetFont, 20), command=self.UpdateRedSquare, hover_color="#3B88C3", state="disabled", fg_color="grey")
        self.RS_UpdateSquareButton.place(relx=0.25, y=130, anchor="center")
        
        # Center Red Square Button
        # - Button for centering the Red Square on the image
        self.RS_CenterSquareButton = CTkButton(self.RedSquareFrame, text="Center", font=(self.WidgetFont, 20), command=self.CenterRedSquare, hover_color="#3B88C3", state="disabled", fg_color="grey")
        self.RS_CenterSquareButton.place(relx=0.75, y=130, anchor="center")
        
        # Traces to follow the Width and Height Inputs for automatic updates when locks are placed
        self.RS_ImageHeightVar.trace_add("write", lambda *args: self.UpdateRedSquareInput(WH="Height"))
        self.RS_ImageWidthVar.trace_add("write", lambda *args: self.UpdateRedSquareInput(WH="Width"))
        
        # Custom Aspect Ratio Label
        # - Label for the Custom Aspect Ratio
        self.RS_CustomAspectRatioLabel = CTkLabel(self.RedSquareFrame, text="Custom Aspect Ratio", font=(self.WidgetFont, 25), text_color="black")
        self.RS_CustomAspectRatioLabel.place(relx=0.5, y=170, anchor="center")
        self.RS_CustomAspectRatioLabel.lift()
        
        # Custom Aspect Ratio Height Value Entry
        # - Entry for the Custom Aspect Ratio Height Value
        # + Disabled by Default, Is controlled by the Custom Aspect Ratio Switch
        self.RS_CustomAspectRatioXVar = StringVar(value="Height")
        self.RS_CustomAspectRatioXInput = CTkEntry(self.RedSquareFrame, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="grey", placeholder_text="Height", textvariable=self.RS_CustomAspectRatioXVar, state="disabled")
        self.RS_CustomAspectRatioXInput.place(relx=0.25, y=205, anchor="center")
        self.RS_CustomAspectRatioXInput.configure(justify="center", border_color="red", border_width=2)
        self.RS_CustomAspectRatioXInput.lift()
        
        # Custom Aspect Ratio Width Value Entry
        # - Entry for the Custom Aspect Ratio Width Value
        # + Disabled by Default, Is controlled by the Custom Aspect Ratio Switch
        self.RS_CustomAspectRatioYVar = StringVar(value="Width")
        self.RS_CustomAspectRatioYInput = CTkEntry(self.RedSquareFrame, font=(self.WidgetFont, 20), bg_color="black", fg_color="black", text_color="grey", placeholder_text="Width", textvariable=self.RS_CustomAspectRatioYVar, state="disabled")
        self.RS_CustomAspectRatioYInput.place(relx=0.75, y=205, anchor="center")
        self.RS_CustomAspectRatioYInput.configure(justify="center", border_color="red", border_width=2)
        
        # Custom Aspect Ratio Switch
        # - Switch for enabling the Custom Aspect Ratio
        # + Enables the Custom Aspect Ratio Inputs
        self.CustomAspectRatioSwitch = CTkSwitch(self.RedSquareFrame, text="Use Custom Aspect Ratio", font=(self.WidgetFont, 20), switch_height=20, switch_width=40, command=self.EnableCustomAspectRatio)
        self.CustomAspectRatioSwitch.place(relx=0.5, y=240, anchor="center")
        self.CreateToolTip(self.CustomAspectRatioSwitch, "Use Custom Aspect Ratio\nIf enabled, will use the custom aspect ratio.")
        
        # Lock Width Height Switch
        # - Switch for locking the Width and Height of the Red Square
        # + Toggles between which value is locked, this is decided on which side the switch is on
        self.LockWidthHeightSwitchSide = BooleanVar(value=False)
        self.LockWidthHeightSwitch = CTkSwitch(self.RedSquareFrame, text="", switch_height=20, switch_width=50, command=self.LockCustomAspectRatio, progress_color="red", fg_color="grey", font=(self.WidgetFont, 20), state="disabled", variable=self.LockWidthHeightSwitchSide)
        self.LockWidthHeightSwitch.place(relx=0.575, y=280, anchor="center")
        self.CreateToolTip(self.LockWidthHeightSwitch, "Lock Width\nIf enabled, will lock the width of the Red Square.")
        
        # Lock Width Label
        # - Label for the Lock Width
        self.LockWidthLabel = CTkLabel(self.RedSquareFrame, text="Lock Height", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.LockWidthLabel.place(relx=0.25, y=250 + LabelGap, anchor="center")
        self.LockWidthLabel.lift()
        
        # Lock Width Label
        # - Label for the Lock Height
        self.LockHeightLabel = CTkLabel(self.RedSquareFrame, text="Lock Width", font=(self.WidgetFont, 20), text_color="lightgrey")
        self.LockHeightLabel.place(relx=0.75, y=250 + LabelGap, anchor="center")
        self.LockHeightLabel.lift()
        
    def PositionArrowLayout(self):
        """
        Description
        -----------
        Function for adding the Red Square Frame to the Layout\n
        
        Comment Information\n
        - \# Short Info
        - \# - Detail Info
        - \# + Extra Info
        
        """
        
        # Base Variables for Positioning
        # - Spacing between the buttons and starting positions
        SideButtonSpacing = 1.8
        DownButtonSpacing = 2.3
        ButtonHeight = 30 / 1080
        ButtonWidth = 25 / 1920
        StartX = 0.5
        StartY = 0.775
        
        # Up Button
        # - Button for moving the Red Square Up
        self.UpButton = CTkButton(self, command=lambda: self.PressButton("Up"), image=self.UpArrowImage, fg_color="#3B88C3", width=30, height=30, hover_color="#3B88C3", text="", border_width=0, border_spacing=0)
        self.UpButton.place(relx=StartX, rely=StartY, anchor="center")
        
        # Down Button
        # - Button for moving the Red Square Down
        self.DownButton = CTkButton(self, command=lambda: self.PressButton("Down"), image=self.DownArrowImage, fg_color="#3B88C3", width=30, height=30, hover_color="#3B88C3", text="", border_width=0, border_spacing=0)
        self.DownButton.place(relx=StartX, rely=StartY + DownButtonSpacing * ButtonHeight + 0.01, anchor="center")
        
        # Left Button
        # - Button for moving the Red Square Left
        self.LeftButton = CTkButton(self, command=lambda: self.PressButton("Left"), image=self.LeftArrowImage, fg_color="#3B88C3", width=30, height=30, hover_color="#3B88C3", text="", border_width=0, border_spacing=0)
        self.LeftButton.place(relx=StartX - SideButtonSpacing * ButtonWidth, rely=StartY + ButtonHeight + 0.01, anchor="center")
        
        # Right Button
        # - Button for moving the Red Square Right
        self.RightButton = CTkButton(self, command=lambda: self.PressButton("Right"), image=self.RightArrowImage, fg_color="#3B88C3", width=30, height=30, hover_color="#3B88C3", text="", border_width=0, border_spacing=0)
        self.RightButton.place(relx=StartX + SideButtonSpacing * ButtonWidth, rely=StartY + ButtonHeight + 0.01, anchor="center")
        
        # Adjustment Amount Entry
        # - Entry for the Adjustment Amount
        # + Controls the amount thq Direction Buttons should move the Red Square
        self.AdjustmentInput = CTkLabel(self, height=30, width=75, font=(self.WidgetFont, 20), text_color="white", justify="center", text="1", bg_color="#3B88C3")
        self.AdjustmentInput.place(relx=0.5, rely=0.915, anchor="center")
        self.CreateToolTip(self.AdjustmentInput, "Adjustment Input\nThe amount to move the Red Square by.", FontSize=20)

        # Increment +1 Button
        # - Button for incrementing the Adjustment Input by 1
        self.PlusOneButton = CTkButton(self, text="+1", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("+", 1), width=50, hover_color="#3B88C3", corner_radius=10)
        self.PlusOneButton.place(relx=0.535, rely=0.915, anchor="center")
        
        # Increment +5 Button
        # - Button for incrementing the Adjustment Input by 5
        self.PlusFiveButton = CTkButton(self, text="+5", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("+", 5), width=50, hover_color="#3B88C3", corner_radius=10)
        self.PlusFiveButton.place(relx=0.562, rely=0.915, anchor="center")
        
        # Increment +10 Button
        # - Button for incrementing the Adjustment Input by 10
        self.PlusTenButton = CTkButton(self, text="+10", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("+", 10), width=50, hover_color="#3B88C3", corner_radius=10)
        self.PlusTenButton.place(relx=0.5904, rely=0.915, anchor="center")
        
        # Decrement -1 Button
        # - Button for decrementing the Adjustment Input by 1
        self.MinusOneButton = CTkButton(self, text="-1", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("-", 1), width=50, hover_color="#3B88C3", corner_radius=10, state="disabled", fg_color="grey")
        self.MinusOneButton.place(relx=0.465, rely=0.915, anchor="center")
        
        # Decrement -5 Button
        # - Button for decrementing the Adjustment Input by 5
        self.MinusFiveButton = CTkButton(self, text="-5", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("-", 5), width=50, hover_color="#3B88C3", corner_radius=10, state="disabled", fg_color="grey")
        self.MinusFiveButton.place(relx=0.438, rely=0.915, anchor="center")
        
        # Decrement -10 Button
        # - Button for decrementing the Adjustment Input by 10
        self.MinusTenButton = CTkButton(self, text="-10", font=(self.WidgetFont, 20), command=lambda: self.UpdateAdjustmentLabel("-", 10), width=50, hover_color="#3B88C3", corner_radius=10, state="disabled", fg_color="grey")
        self.MinusTenButton.place(relx=0.4105, rely=0.915, anchor="center")

    def CreateToolTip(self, Widget, Text: str, FontSize: int = 20):
        """
        Description
        -----------
        Returns a tooltip for a given widget with the given text.\n

        Parameters
        ----------
        Widget: :class:`CTkWidget`
            The widget to add the tooltip to.
        
        Text: :class:`str`
            The text to display in the tooltip.
        
        FontSize: :class:`int`
            The font size of the tooltip text. Default is 20.

        Returns
        -------
        Type: :class:`None`
        """
        
        # Create the tooltip
        CTkToolTip(widget=Widget, message=Text, font=(self.WidgetFont, FontSize), delay=0.1, border_color="red", border_width=2, bg_color="black", alpha=1.0)
    
    def EnableDisableIncrement(self, CurrentValue: int):
        """
        Description
        -----------
        Enables or Disables the Increment Buttons based on the Current Value.\n

        Parameters
        ----------
        CurrentValue: :class:`int`
            The current value of the Adjustment Input.

        Returns
        -------
        Type: :class:`None`
        """
        
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
        """
        Description
        -----------
        Updates the Adjustment Label based on the Type and Value.\n

        Parameters
        ----------
        Type: :class:`str`
            The type of update to do. Can be either "+" or "-". (Add or Subtract)
        
        Value: :class:`int`
            The value to add or subtract from the Adjustment Label.

        Returns
        -------
        Type: :class:`None`
        """
        
        # Get the Current Value of the Adjustment Label
        CurrentValue = int(self.AdjustmentInput.cget("text"))

        # If the Type is to Increment the value
        if Type == "+":
            CurrentValue += Value
            if CurrentValue > self.WindowWidth:
                # Display a Messagebox if the value is greater than the Width of the window
                CTkMessagebox(title="Info", message="Can't be greater than the Width of the window.", icon="info")
                return
            else:
                # Update the Adjustment Label
                self.AdjustmentInput.configure(text=CurrentValue)
                # Enable or Disable the Increment Buttons
                self.EnableDisableIncrement(CurrentValue)
        
        # If the Type is to Decrement the value
        elif Type == "-":
            CurrentValue -= Value
            if CurrentValue < 1:
                # Display a Messagebox if the value is less than 1
                CTkMessagebox(title="Info", message="Can't be less than 1.", icon="info")
                return
            else:
                # Update the Adjustment Label
                self.AdjustmentInput.configure(text=CurrentValue)
                # Enable or Disable the Increment Buttons
                self.EnableDisableIncrement(CurrentValue)

        # If the Type is not "+" or "-" just return
        else:
            return
    
    def DisableInteract(self, Widget: CTkButton | CTkSwitch):
        """
        Description
        -----------
        Disables the given Button or Switch\n

        Parameters
        ----------
        Type: :class:`CTkButton` | :class:`CTkSwitch`
            The widget to disable.
        
        Returns
        -------
        Type: :class:`None`
        """

        # Need to look into
        if Widget == self.UpButton:
            Widget.configure(image=None)
            Widget.configure(image=self.GreyUpArrowImage, state="disabled", fg_color="grey", border_color="red", border_width=2)
        elif Widget == self.DownButton:
            Widget.configure(image=None)
            Widget.configure(image=self.GreyDownArrowImage, state="disabled", fg_color="grey", border_color="red", border_width=2)
        elif isinstance(Widget, CTkButton):
            Widget.configure(state="disabled", fg_color="grey")
        elif isinstance(Widget, CTkSwitch):
            Widget.configure(state="disabled", button_color="grey")
            
    def EnableInteract(self, button: CTkButton | CTkSwitch):
        """
        Description
        -----------
        Enables the given Button or Switch\n

        Parameters
        ----------
        Type: :class:`CTkButton` | :class:`CTkSwitch`
            The widget to Enable.
        
        Returns
        -------
        Type: :class:`None`
        """
        
        # Need to look into
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
        """
        Description
        -----------
        Small Fading text in the Top Left Corner of the Window.\n
        Possibility to add Buttons to the Fading Frame for later.\n

        Parameters
        ----------
        Message: :class:`str`
            The message to display in the Fading Label.
        
        Duration: :class:`int`
            The duration in milliseconds to display the Fading Label. Default is 5000.
        
        Returns
        -------
        Type: :class:`None`
        """
        
        # Create a Label with the given message and destroy it after 5 seconds (5000 Milliseconds)
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
        """
        Description
        -----------
        Opens the Output Directory.\n
        Needs rework, is a little "Too Simple atm.".
        """
        
        # Open the Folder
        try:
            os.startfile(self.dir_path + "\\Output")
        except:
            # If it fails, open the current working directory
            os.startfile(os.getcwd())
    
    def ShowInformation(self):
        """
        Description
        -----------
        Shows a Popup with Information about the differant values of the Program.\n
        More Information will get added here later~
        """
        
        # Create the Popup Window
        # - The Popup Window is a Toplevel Widget, and will be placed in the center and on top of the main window
        InformationPopOut = CTkToplevel(self, width=500, height=500, fg_color="black")
        InformationPopOut.title("Information")
        InformationPopOut.geometry(f"500x500+{int(self.ScreenWidth / 2 - 250)}+{int(self.ScreenHeight / 2 - 250)}")
        InformationPopOut.resizable(False, False)
        InformationPopOut.lift()
        InformationPopOut.attributes("-topmost", True)
        
        # Information Exit Button
        # - Button for closing the Information Popup
        InformationExitButton = CTkButton(InformationPopOut, text="Exit", font=(self.WidgetFont, 20), command=InformationPopOut.destroy, hover_color="red")
        InformationExitButton.place(relx=0.5, rely=0.95, anchor="center")
        
        # Information Title Labels and Values
        # - Iterates over the Information Dict and places the Keys and Values in the Popup
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
        """
        Description
        -----------
        Updates the Red Square Input based on the Width or Height.\n

        Parameters
        ----------
        WH: :class:`str`
            The Width or Height to update the Red Square Input for.
        
        Returns
        -------
        Type: :class:`None`
        """

        # Get the Max Width and Height
        MaxWidth = self.ResizedWidth
        MaxHeight = self.ResizedHeight

        # Ignore, when the Values are empty or 0
        if self.RS_ImageHeightVar.get() in ["", 0, "0"] or self.RS_ImageWidthVar.get() in ["", 0, "0"]:
            return

        # Get the current values of the Width and Height
        CurrentHeight = int(self.RS_ImageHeightVar.get())
        CurrentWidth = int(self.RS_ImageWidthVar.get())
        
        if WH == "Width":
            # If the Width is greater than the Max Width
            if CurrentWidth > MaxWidth:
                # Set the Width to the Max Width
                self.RS_ImageWidthVar.set(MaxWidth)
                # If the Height is greater than the Max Height
                if CurrentHeight > MaxHeight:
                    # Set the Height to the Max Height
                    self.RS_ImageHeightVar.set(MaxHeight)
            # If the Height is greater than the Max Height
            elif CurrentHeight > MaxHeight:
                # Set the Height to the Max Height
                self.RS_ImageHeightVar.set(MaxHeight)
                # If the Width is greater than the Max Width
                if CurrentWidth > MaxWidth:
                    # Set the Width to the Max Width
                    self.RS_ImageWidthVar.set(MaxWidth)
        elif WH == "Height":
            # If the Height is greater than the Max Height
            if CurrentHeight > MaxHeight:
                # Set the Height to the Max Height
                self.RS_ImageHeightVar.set(MaxHeight)
                # If the Width is greater than the Max Width
                if CurrentWidth > MaxWidth:
                    # Set the Width to the Max Width
                    self.RS_ImageWidthVar.set(MaxWidth)
            # If the Width is greater than the Max Width
            elif CurrentWidth > MaxWidth:
                # Set the Width to the Max Width
                self.RS_ImageWidthVar.set(MaxWidth)
                # If the Height is greater than the Max Height
                if CurrentHeight > MaxHeight:
                    # Set the Height to the Max Height
                    self.RS_ImageHeightVar.set(MaxHeight)
        else:
            return
    
    def EnableCustomAspectRatio(self):
        """
        Description
        -----------
        Enables or Disables the Custom Aspect Ratio Inputs.\n
        Manages the different widgets surrounding this. (Enabling / Disabling Buttons etc.)
        """
        
        if self.CustomAspectRatioSwitch.get() == 0:
            # Disable the Input fields for the Custom Aspect Ratio
            self.RS_CustomAspectRatioXInput.configure(state="disabled", border_color="red", text_color="grey")
            self.RS_CustomAspectRatioYInput.configure(state="disabled", border_color="red", text_color="grey")
            # Set the Variables to Width and Height again as a reset
            self.RS_CustomAspectRatioXVar.set("Height")
            self.RS_CustomAspectRatioYVar.set("Width")
            # Disable the LockWidthHeightSwitch
            self.LockWidthHeightSwitch.configure(state="disabled", button_color="grey", fg_color="grey")
            # For sanity enable and set both the Width and Height Input Fields tro default
            self.RS_HeightInput.configure(state="normal", border_color="#565B5E", text_color="white")
            self.RS_WidthInput.configure(state="normal", border_color="#565B5E", text_color="white")
            # Switch the LockWidthHeightSwitch to the Left
            self.LockWidthHeightSwitchSide.set(False)
        else:
            # Enable the Input fields for the Custom Aspect Ratio
            self.RS_CustomAspectRatioXInput.configure(state="normal", border_color="#565B5E", text_color="white")
            self.RS_CustomAspectRatioYInput.configure(state="normal", border_color="#565B5E", text_color="white")
            # Set the variables to blank strings
            self.RS_CustomAspectRatioXVar.set("")
            self.RS_CustomAspectRatioYVar.set("")
            # Enable the LockWidthHeightSwitch
            self.LockWidthHeightSwitch.configure(state="normal", fg_color="red")
            # Disable the Height Input Field
            self.RS_HeightInput.configure(state="disabled", border_color="red", text_color="grey")
            # Switch the LockWidthHeightSwitch to the Left
            self.LockWidthHeightSwitchSide.set(False)
    
    def LockCustomAspectRatio(self):
        """
        Description
        -----------
        Locks the Height Input of the Red Square if the Aspect Ratio Switch has been toggled.\n
        """
        
        # Check if the Custom Aspect Ratio has been enable first
        if self.CustomAspectRatioSwitch.get() == 0:
            return
        # Disable the height input field if the switch is toggled on
        if self.LockWidthHeightSwitch.get() == 1:
            self.RS_HeightInput.configure(state="normal", border_color="#565B5E", text_color="white")
            self.RS_WidthInput.configure(state="disabled", border_color="red", text_color="grey")
        else:
            self.RS_HeightInput.configure(state="disabled", border_color="red", text_color="grey")
            self.RS_WidthInput.configure(state="normal", border_color="#565B5E", text_color="white")
            
    def UpdateRedSquare(self):
        """
        Description
        -----------
        Brains behind the Red Square, needs some reworking to work with the new Custom Aspect Ratio Stuff.
        """
        
        # Get the New Width and Height
        NewWidth = int(self.RS_ImageWidthVar.get())
        NewHeight = int(self.RS_ImageHeightVar.get())

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
            CustomAspectWidth, CustomAspectHeight = int(self.RS_CustomAspectRatioXVar.get()), int(self.RS_CustomAspectRatioYVar.get())
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
        self.IF_New_AspectRatioVar.set(f"{self.SimpleWidth} : {self.SimpleHeight}")
        
        # Update the New Dimensions Width and Height Labels
        self.IF_NewDimension_WidthVar.set(int(NewWidth / self.Zoom))
        self.IF_NewDimension_HeightVar.set(int(NewHeight / self.Zoom))
        
        # Update the Adjustment Input Field
        self.RS_ImageHeightVar.set(int(NewHeight))
        self.RS_ImageWidthVar.set(int(NewWidth))
        
    def CenterRedSquare(self):
        """
        Description
        -----------
        Function to Center the Red Square on the Image.\n
        Not working a 100% Needs some more tweaks
        """
        
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
        """
        Description
        -----------
        Will Load all the images from the selected directory.\n
        makes all Images accessible from the ImageFiles list for other functions to use.
        """
        
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
        self.EnableInteract(self.RS_CenterSquareButton)
        self.EnableInteract(self.RS_UpdateSquareButton)

        # Load the first image
        self.ImageIndex = 0
        self.LoadImage(self.ImageIndex)

    def CropAndSaveImageMain(self):
        """
        Description
        -----------
        Main Function for Cropping and Saving Images.\n
        Will either crop all images in the directory or just the current image.
        """
        
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

    def CropAndSaveImage(self, ImageName: str):
        """
        Description
        -----------
        Crops and Saves the given image.\n
        Crops and Saves the image to the Output directory, Controlled by the "CropAndSaveImage" Function.
        
        Parameters
        ----------
        ImageName: :class:`str`
            The name of the image to crop and save.
        
        Returns
        -------
        Type: :class:`bool`
            Returns True if the image was saved successfully, False if it wasn't.
        """

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
        self.OriginalCropImage = IMG.open(f"{self.dir_path}/{ImageName}")
        
        # Grab that Area from the scaled image and downscale the cropped bit to the original size
        CroppedImage = self.OriginalCropImage.crop(FullCrop).resize((self.ImageWidth, self.ImageHeight), IMG.Resampling.LANCZOS)
        
        # Create OutPut Directory if it doesn't exist
        if not os.path.exists(f"{self.dir_path}/Output"):
            os.mkdir(f"{self.dir_path}/Output")

        ## Save the cropped image to the Output directory
        OriginalImageName, OriginalImageExtension = os.path.splitext(ImageName)
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
        """
        Description
        -----------
        Loads the next image in the ImageFiles list and displays it.
        """

        # Disable the Next Image Button if the last image is reached
        if self.ImageIndex >= len(self.ImageFiles) - 2:
            self.DisableInteract(self.NextImageButton)

        # Remove the Image from the Canvas and load the new image
        if self.ImageIndex < len(self.ImageFiles) - 1:
            self.ImageIndex += 1
            self.canvas.delete("all")
            self.LoadImage(self.ImageIndex)
            self.EnableInteract(self.PreviousImageButton)
        else:
            self.DisableInteract(self.NextImageButton)

    def PreviousImage(self):
        """
        Description
        -----------
        Loads the next image in the ImageFiles list and displays it.
        """
        
        # Disable the Previous Image Button if the first image is reached
        if self.ImageIndex <= 1:
            self.DisableInteract(self.PreviousImageButton)
        
        # Remove the Image from the Canvas and load the new image
        if self.ImageIndex > 0:
            self.ImageIndex -= 1
            self.canvas.delete("all")
            self.LoadImage(self.ImageIndex)
            self.EnableInteract(self.NextImageButton)
        else:
            self.DisableInteract(self.PreviousImageButton)
    
    def ResetSquare(self):
        """
        Description
        -----------
        Resets the Red Square to the original Size and Position.
        """

        # Grab values for the Width, Height and Position of the Image
        Width = self.ImageWidth * self.Zoom
        Height = self.ImageHeight * self.Zoom
        X, Y = self.ImageX, self.ImageY
        
        # Update the SquareObject
        self.SquareObject.Update(X=X, Y=Y, Width=Width, Height=Height)
        
        # Update the Red Square Input Fields
        self.RS_ImageWidthVar.set(int(Width))
        self.RS_ImageHeightVar.set(int(Height))

    def PressButton(self, Direction: str):
        """
        Description
        -----------
        Function used by the four move buttons to move the Red Square around.
        
        Parameters
        ----------
        Direction: :class:`str`
            The direction to move the square in. Can be either "Up", "Down", "Left" or "Right".
        
        Returns
        -------
        Type: :class:`None`
        """
        
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
        """
        Description
        -----------
        Loads the given image from the ImageFiles list and displays it on the canvas.\n
        Adjusts different values to dispålay the correct data about the image.
        
        Parameters
        ----------
        ImageNr: :class:`int`
            The index of the image to load from the ImageFiles list.
        
        Returns
        -------
        Type: :class:`None`
        """

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
        self.IF_Original_AspectRatioVar.set(f"{self.SimpleWidth} : {self.SimpleHeight}")

        # Update the Dimension Labels
        self.IF_OriginalDimension_WidthVar.set(self.ImageWidth)
        self.IF_OriginalDimension_HeightVar.set(self.ImageHeight)

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
            self.RS_ImageWidthVar.set(StoredWidth)
            self.RS_ImageHeightVar.set(StoredHeight)
            self.SquareObject.Update(KeepSize=True)
        else:
            # Create the Square Object and update the Red Square Input Fields
            self.SquareObject = Square(self.canvas, self.ImageX, self.ImageY, self.ResizedWidth, self.ResizedHeight, "red")
            self.RS_ImageWidthVar.set(self.ResizedWidth)
            self.RS_ImageHeightVar.set(self.ResizedHeight)
            self.SquareObject.Update()
        
        # Store the Original Size of the image to reset the Square's size to the original size
        self.OriginalSize = (self.ImageX, self.ImageY, self.ImageX + self.ResizedWidth, self.ImageY + self.ResizedWidth)

        # Update the New Dimensions Labels
        self.IF_NewDimension_WidthVar.set(round(self.SquareObject.Width / self.Zoom))
        self.IF_NewDimension_HeightVar.set(round(self.SquareObject.Height / self.Zoom))

    def ResizeImageWindow(self):
        """
        Description
        -----------
        Seperate Window to Resize an Image to a new size.\n
        Will resize the image to the given size and save it to the Output directory.
        """
        
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
        """
        Description
        -----------
        Child Function for the ResizeImageWindow.\n
        Will check if the Width or Height Lock is toggled on and disable the other one, else reset both.
        """
        
        # If the Width Lock is toggled on, disable the Height Lock
        if self.ResizeWidthLock.get():
            self.ResizeHeightLock.configure(state="disabled", button_color="red")
            self.ResizeWidthLock.configure(state="normal", button_color="#377D08")
        # If the Height Lock is toggled on, disable the Width Lock
        elif self.ResizeHeightLock.get():
            self.ResizeWidthLock.configure(state="disabled", button_color="red")
            self.ResizeHeightLock.configure(state="normal", button_color="#377D08")
        # If neither are toggled on, enable both
        else:
            self.ResizeHeightLock.configure(state="normal", button_color="#D5D9DE")
            self.ResizeWidthLock.configure(state="normal", button_color="#D5D9DE")
    
    def ResizeUpdate(self, WH: str):
        """
        Description
        -----------
        Function which is triggered on the entry boxes in the ResizeImageWindow.\n
        Will change the opposite value to keep the aspect ratio and prevent it from going out of bounds. (9999)
        
        Parameters
        ----------
        WH: :class:`str`
            The Width or Height to update. Can be either "Width" or "Height".
        
        Returns
        -------
        Type: :class:`None`
        """
        
        # Max Size of the Width and Height (Can easily be bigger, but shouldn't be needed)
        MaxSize = 9999
    
        # Section for Updating the Width when the Height is changed
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

        # Section for Updating the Height when the Width is changed
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
        
        # If neither Width or Height are given in the argument, return
        else:
            return

    def ResizeImage(self):
        """
        Description
        -----------
        Function to Resize an Image to a new size.
        """

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
            # Display a CTkMessagebox with only 1 image resized
            CTkMessagebox(title="Success", message="Resized 1 image.", icon="info", option_1="Ok")
            self.EnableInteract(self.OpenOutputDirButton)

### Other Classes ###
class Square:
    """
    Description
    -----------
    The Square Class is used to create a square on the canvas.\n
    This Square is able to get manipulated around on the screen and is indicative on the area which will get cropped.\n
    As Such it needs to get updated when the image is resized or moved, hence this class.
    """
    
    def __init__(self, Canvas: CTkCanvas, X: int, Y: int, Width: int, Height: int, Color="Red"):
        """
        Description
        -----------
        The Constructor for the Square Class.
        """
        
        self.Canvas = Canvas
        self.X = X
        self.Y = Y
        self.Width = Width
        self.Height = Height
        self.Color = Color
        self.ID = None
        self.SquareProperties = None

    def Draw(self, KeepSize=False):
        """
        Description
        -----------
        Draw Function for the Square Class.
        
        Parameters
        ----------
        KeepSize: :class:`bool`
            If True, the Square will keep the same size as before, else it will update the SquareProperties.
        
        Returns
        -------
        Type: :class:`None`
        """
        
        if self.ID != None:
            self.Canvas.delete(self.ID)
        self.ID = self.Canvas.create_rectangle(self.X, self.Y, self.X + self.Width, self.Y + self.Height, outline=self.Color)
        if not KeepSize:
            self.SquareProperties = (self.X, self.Y, self.Width, self.Height)
        else:
            pass

    def Update(self, X=None, Y=None, Width=None, Height=None, KeepSize=False):
        """
        Description
        -----------
        Update Function for the Square Class. Initiates a redraw of the square with the updated values.
        
        Parameters
        ----------
        X: :class:`int`
            The new X position of the square. Defaults to None.
        Y: :class:`int`
            The new Y position of the square. Defaults to None.
        Width: :class:`int`
            The new Width of the square. Defaults to None.
        Height: :class:`int`
            The new Height of the square. Defaults to None.
        KeepSize: :class:`bool`
            If True, the Square will keep the same size as before, else it will update the SquareProperties.
        
        Returns
        -------
        Type: :class:`None`
        """

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
