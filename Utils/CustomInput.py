import msvcrt

# Local functions

def IsFloat(value):
    try:
        float(value)
        return True
    except:
        return False

def Include(value, FilterList):
    if value.isdigit() and FilterList["Int"]:
        return True
    if IsFloat(value) and FilterList["Float"]:
        return True

def Exclude(value, FilterList):
    if IsFloat(value) and FilterList["Float"]:
        return False
    if value.isdigit() and FilterList["Int"]:
        return False
    
    return True

def AwaitNumInputs():
    key = 'a'
    while not key.isdigit():
        key = msvcrt.getch().decode('utf-8')

    return int(key)

def AwaitNumInputsBelow(n):
    key = n
    while key >= n:
        key = AwaitNumInputs()
        print("Key captured: ", key)

    return key

def Input(Text, FilterList = {}, FilterType = None, RetryUntilValid = True):
        
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

    return RawInput, success
        

        https://prod.liveshare.vsengsaas.visualstudio.com/join?80B355B7E5A3AACD9CEC22CF364445409DF0