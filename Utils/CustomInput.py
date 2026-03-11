import tkinter as tk

def get_ghost_key():
    root = tk.Tk()
    
    # 1. Make the window transparent (0.0 is invisible, 1.0 is solid)
    root.attributes('-alpha', 0.0)
    
    # 2. Keep it on top of Thonny so it maintains focus
    root.attributes('-topmost', True)
    
    # 3. Position it over the mouse or center (optional)
    root.geometry("100x100+500+500")

    key_pressed = [None]

    def key_handler(event):
        key_pressed[0] = event.keysym
        root.destroy()

    root.bind('<Key>', key_handler)
    
    # Focus the window so the user doesn't have to click it
    root.focus_force()
    
    root.mainloop()
    return key_pressed[0]

import msvcrt
# from typing import Any

# Local functions

def IsFloat(value: str):
    try:
        float(value)
        return True
    except:
        return False

def Include(value: str, FilterList: dict[str, bool]):
    if value.isdigit() and FilterList["Int"]:
        return True
    if IsFloat(value) and FilterList["Float"]:
        return True

def Exclude(value: str, FilterList: dict[str, bool]):
    if IsFloat(value) and FilterList["Float"]:
        return False
    if value.isdigit() and FilterList["Int"]:
        return False
    
    return True

def AwaitInput():
    # return msvcrt.getch().decode('utf-8')
    return get_ghost_key()  

def AwaitNumInputs() -> int:
    key = 'a'
    while not key.isdigit():
        key = AwaitInput()

    return int(key)

def AwaitNumInputsBelow(n: int) -> int:
    key: int = n
    while key >= n:
        key = AwaitNumInputs()
        # print("Key captured: ", key)

    return key

def Input(Text: str, FilterList: dict[str, bool] = {}, FilterType: str | None = None, RetryUntilValid: bool = True) -> str | tuple[str, bool | None]:
        
    """
    Filter List dict:
    +Int
    +Float
    """
    
    success = False
    
    RawInput = input(Text)
    if FilterType == "Include":
        success = Include(RawInput, FilterList) 
    elif FilterType == "Exclude":
        success = Exclude(RawInput, FilterList)
    else:
        success = True

    while (RetryUntilValid and not success):
        print("Invalid input, please re-enter!")
        RawInput = input(Text)
        if FilterType == "Include":
            success = Include(RawInput, FilterList) 
        elif FilterType == "Exclude":
            success = Exclude(RawInput, FilterList)

    if RetryUntilValid: return RawInput
    return RawInput, success