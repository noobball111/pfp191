import tkinter as tk

# Band-aid and hacky solution to Thonny not liking real-time inputs
# Next time lets just learn how to use tkinter and make the UI instead so we dont have to rely on console differences between VSCode and Thonny
def get_ghost_key():
    root = tk.Tk()
    root.attributes('-alpha', 0)
    root.attributes('-topmost', True)
    root.geometry("1920x1080")

    key_pressed = [None]

    def key_handler(event):
        key_pressed[0] = event.keysym
        root.destroy()

    root.bind('<Key>', key_handler)
    
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

def Include(value: str, FilterList):
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
    if RawInput.lower() == "/r" or RawInput.lower() == "/return":
        return "/r", True

    if FilterType == "Include":
        success = Include(RawInput, FilterList) 
    elif FilterType == "Exclude":
        success = Exclude(RawInput, FilterList)
    else:
        success = True

    while (RetryUntilValid and not success):
        print("Invalid input, please re-enter!")
        RawInput = input(Text)
        if RawInput.lower() == "/r" or RawInput.lower() == "/return":
            return "/r", True

        if FilterType == "Include":
            success = Include(RawInput, FilterList) 
        elif FilterType == "Exclude":
            success = Exclude(RawInput, FilterList)

    if RetryUntilValid: return RawInput, success
    return RawInput, success