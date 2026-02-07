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
    return msvcrt.getch().decode('utf-8')

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

def Input(Text: str, FilterList: dict[str, bool] = {}, FilterType: str | None = None, RetryUntilValid: bool = True):
        
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