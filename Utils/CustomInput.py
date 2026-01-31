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
    if value.isdigit() and FilterList["Int"]:
        return False
    if IsFloat(value) and FilterList["Float"]:
        return False
    
    return True

class CustomInput:
    def Input(Text, FilterList = {}, FilterType = None):
        
        """
        Filter List dict:
        +Int
        +Float
        """
        
        RawInput = input(Text)
        if FilterType == "Include":
            return RawInput, Include(RawInput, FilterList)
        elif FilterType == "Exclude":
            return RawInput, Exclude(RawInput, FilterList)
        else:
            return RawInput, "Str"
        