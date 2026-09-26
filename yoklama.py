import customtkinter as ctk
import json
import atexit
from pathlib import Path
import sys

# Title Configuration
TITLE_TXT = "Yoklama Tablosu" # Title Text
TITLE_FAMILY = "JetBrainsMono NF ExtraBold Italic" # Title Text Font
TITLE_COLOR = "#FFFFFF" # Title Text Color
TITLE_SIZE = 30 # Title Text Size
TITLE_WEIGHT = "bold" # Title Text Weight

# Member Name Configuration
MEMBER_FAMILY = None # Member Text Font
MEMBER_COLOR = None # Member Text Color
MEMBER_SIZE = None # Member Text Size
MEMBER_WEIGHT = "normal" # Member Text Weight

# Button Configuration
BTN_PT = 20 # "Button Text Size"
BTN_WEIGHT = "bold" # "Button Text Weight"
BTN_FAMILY = None # Button Text Font
BTN_PADX = 5 # Horizontal Padding on the buttons
BTN_PADY = 5 # Vertical Padding on the buttons
YOK_FG = "#000000" # "Yok" Background Color
YOK_TXT = "#787878" # "Yok" Text Color
VAR_FG = "#FFFFFF" # "Var" Backgorund Color
VAR_TXT = "#787878" # "Var" Text Color
CLEAR_PADY = (0,40) # Vertical Padding on the "Sıfırla" Button

#General Stuff Configuration
BG_COLOR = "#011638" # "General Background Color"
MF_PADX = 20 # Horizontal Padding on the table
MF_PADY = 200 # Vertical Padding on the table


# Alternative Dark Mode Color Scheme
YOK_FG = "#990822"
YOK_TXT = "#f74a69"
VAR_FG = "#0aa629"
VAR_TXT = "#36e058"
BG_COLOR = None





# Handler for BG_COLOR
if BG_COLOR is None:
    BG_COLOR = "#242424"

FULLSCREEN = True
FULLSCREEN_BUGFIX = True

def fullscreen_handler(event=None):
    global FULLSCREEN
    FULLSCREEN = not FULLSCREEN
    if not FULLSCREEN_BUGFIX:
        root.attributes("-fullscreen",FULLSCREEN)
        root.update_idletasks()
    else:
        if not FULLSCREEN:
            root.overrideredirect(False)
            if sys.platform.startswith("win"):
                root.wm_state("zoomed")
            else:
                try:
                    root.attributes("-zoomed",True)
                except Exception:
                    root.geometry("1000x600+100+100")
            root.focus_force()
        else:
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            root.geometry(f"{width}x{height}+0+0")
            root.overrideredirect(True)
    

def handle_button(btn: ctk.CTkButton):
    if btn.cget("text") == "VAR":
        btn.configure(text="YOK",fg_color=YOK_FG,text_color=YOK_TXT,font=ctk.CTkFont(family=BTN_FAMILY,size=BTN_PT,weight=BTN_WEIGHT))
    elif btn.cget("text") == "YOK":
        btn.configure(text="VAR",fg_color=VAR_FG,text_color=VAR_TXT,font=ctk.CTkFont(family=BTN_FAMILY,size=BTN_PT,weight=BTN_WEIGHT))

def reset_all(member_guis):
    for member in member_guis:
        for i in range(1,9):
            member[i].configure(text="YOK",fg_color=YOK_FG,text_color=YOK_TXT,font=ctk.CTkFont(family=BTN_FAMILY,size=BTN_PT,weight=BTN_WEIGHT))

def take_save(member_guis,members):
    config = {}
    member_stats = [[""] * 9 for _ in range(len(members))]
    for member in range(len(member_guis)):
        for ders in range(1,9):
            member_stats[member][ders] = member_guis[member][ders].cget("text")
    if member_stats == DEFAULT_MEMBER_STATS:
        member_stats = None
    with open("config.json",encoding="utf-8",mode="w") as f:
        config["members"] = members
        config["member_stats"] = member_stats
        json.dump(config,f,indent=4)

def load_save(member_stats,members,member_guis):
    if member_stats == None:
        return
    if len(member_stats) <= len(member_guis):
        count = len(member_stats)
    else:
        count = len(member_guis)
    for member in range(count):
        for ders in range(1,9):
            if member_stats[member][ders] == "YOK":
                member_guis[member][ders].configure(text="YOK",fg_color=YOK_FG,text_color=YOK_TXT,font=ctk.CTkFont(family=BTN_FAMILY,size=BTN_PT,weight=BTN_WEIGHT))
            elif member_stats[member][ders] == "VAR":
                member_guis[member][ders].configure(text="VAR",fg_color=VAR_FG,text_color=VAR_TXT,font=ctk.CTkFont(family=BTN_FAMILY,size=BTN_PT,weight=BTN_WEIGHT))

def reload(member_guis):
    raise NotImplementedError # This will when implemented reload all the texts to update the font etc. preferences

def main() -> None:
    if not Path("config.json").is_file():
        raise Exception("config.json yok")
    with open("config.json",encoding="utf-8") as f:
        config:dict = json.load(f)
    members: list = config["members"]
    member_stats: list = config.get("member_stats",None) # pyright: ignore[reportAssignmentType]
    global root
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    root.title("Yoklama Tablosu")
    root.grid_columnconfigure(0,weight=1)
    root.grid_rowconfigure(1,weight=1)
    root.configure(fg_color=BG_COLOR)
    member_guis: list[list[ctk.CTkButton | ctk.CTkLabel | None]] = [[None] * 9 for _ in range(len(members))]
    main_frame = ctk.CTkFrame(root,fg_color=BG_COLOR)
    main_frame.grid(row=1,column=0,sticky="nsew",padx=MF_PADX,pady=MF_PADY)
    title = ctk.CTkLabel(root,text=TITLE_TXT,text_color=TITLE_COLOR,font=ctk.CTkFont(family=TITLE_FAMILY,size=TITLE_SIZE,weight=TITLE_WEIGHT))
    global DEFAULT_MEMBER_STATS
    title.grid(row=0,pady=20)
    DEFAULT_MEMBER_STATS = [[""]+ (["YOK"] * 8) for _ in range(len(members))] 
    for col in range(9):
        main_frame.grid_columnconfigure(col, weight=1)
    for row in range(len(members)):
        main_frame.grid_rowconfigure(row, weight=1)
    for i in range(len(members)):
        member: str = members[i]
        member_guis[i][0] = ctk.CTkLabel(main_frame,text=member,text_color=MEMBER_COLOR,font=ctk.CTkFont(family=MEMBER_FAMILY,size=MEMBER_SIZE,weight=MEMBER_WEIGHT))
        name: ctk.CTkLabel | ctk.CTkButton | None = member_guis[i][0]
        assert isinstance(name,ctk.CTkLabel)
        name.grid(row=i,column=0)
        for ders in range(1,9):
            btn = ctk.CTkButton(main_frame,text="YOK",fg_color=YOK_FG,text_color=YOK_TXT,font=ctk.CTkFont(family=BTN_FAMILY,size=BTN_PT,weight=BTN_WEIGHT))
            assert isinstance(btn,ctk.CTkButton)
            btn.configure(command=lambda bt=btn:handle_button(bt))
            btn.grid(row=i,column=ders,sticky="nsew",padx=BTN_PADX,pady=BTN_PADY)
            member_guis[i][ders] = btn
    clear_all_btn = ctk.CTkButton(root,text="SIFIRLA",fg_color=YOK_FG,text_color=YOK_TXT,command= lambda mg = member_guis: reset_all(mg),font=ctk.CTkFont(family=BTN_FAMILY,size=BTN_PT,weight=BTN_WEIGHT))
    clear_all_btn.grid(row=2,column=0,pady=CLEAR_PADY)
    atexit.register(lambda mg = member_guis, m = members: take_save(mg,m))
    load_save(member_stats,members,member_guis)
    global FULLSCREEN,FULLSCREEN_BUGFIX
    # root.after(0,lambda: root.attributes("-fullscreen",FULLSCREEN))
    if not FULLSCREEN_BUGFIX:
        root.update_idletasks()
        root.after(50, lambda: root.attributes("-fullscreen", True))
    else:
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.geometry(f"{width}x{height}+0+0")
        root.overrideredirect(True)
    root.bind("<F11>",fullscreen_handler)
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print(f"An error occured: {e}")
        traceback.print_exc()
        input()