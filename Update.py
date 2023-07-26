from customtkinter import CTkFrame, CTkLabel, CTkButton
from requests import get
import webbrowser
import base64

def VersionCheck(Current: dict, Web: str):
    # Raw data from the web
    Web = {"Major": Web[0], "Minor": Web[2], "Patch": Web[4]}
    
    # Compare the data
    if int(Web["Major"]) > Current["Major"]:
        return True
    elif int(Web["Minor"]) > Current["Minor"]:
        return True
    elif int(Web["Patch"]) > Current["Patch"]:
        return True
    else:
        return False


def UpdateCheck(CTkMaster, Version: str):
    # Variables
    Owner = "GhostTortilla"
    Repository = "CroppingTool"
    File = "VERSION.txt"
    
    # Construct the URL
    URL = f"https://api.github.com/repos/{Owner}/{Repository}/contents/{File}"
    # Get the data
    Response = get(URL)
    # Decode the data
    Data = Response.json()
    
    # Decode the data
    Latest = base64.b64decode(Data["content"]).decode("utf-8")
    
    # Shrink it down to the digits only by removing all non-digits and adding a dot between each newline
    Preview = "".join([x for x in Latest if x.isdigit() or x == "\n"]).replace("\n", ".")
    
    # Remove the last dot
    Preview = Preview[:-1]
    
    # Download URL
    DownloadURL = f"https://github.com/GhostTortilla/CroppingTool/releases/latest"
    if VersionCheck(Version, Preview):
        # Frame to surround the notification and place the notification on top of the window
        VersionFrame = CTkFrame(CTkMaster, width=300, height=75)
        VersionFrame.place(relx = 0.01, rely = 0.01, anchor = "nw")
        VersionFrame.lift()
        VersionFrame.after(10000, VersionFrame.destroy)
        
        # Label to notify the user that a new version is available
        VersionLabel = CTkLabel(CTkMaster, text = f"Version {Latest} is available.", font=("ComicSansMS", 20), bg_color="transparent")
        VersionLabel.place(relx = 0.03, rely = 0.01, anchor = "nw")
        VersionLabel.lift()
        VersionLabel.after(10000, VersionLabel.destroy)
        
        # Button to direct the user to the latest version
        VersionButton = CTkButton(CTkMaster, text = "Download", font=("ComicSansMS", 15), command = lambda: webbrowser.open(DownloadURL))
        VersionButton.place(relx = 0.05, rely = 0.05, anchor = "nw")
        VersionButton.lift()
        VersionButton.after(10000, VersionButton.destroy)
    
    else:
        # Label to notify that the user is on the latest version
        VersionLabel = CTkLabel(CTkMaster, text = f"Running the Latest Version", font=("ComicSansMS", 20), bg_color="black")
        VersionLabel.place(relx = 0.01, rely = 0.01, anchor = "nw")
        VersionLabel.lift()
        VersionLabel.after(5000, VersionLabel.destroy)