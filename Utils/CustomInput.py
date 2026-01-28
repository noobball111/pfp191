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
    def Input(Text, FilterList, FilterType):
        
        """
        Filter List dict:
        +Int
        +Float
        """
        
        if not FilterList:
            FilterList = {"Int": True, "Float": True}
        
        RawInput = input(Text)
        if not FilterType or FilterType == "Include":
            return Include(RawInput, FilterList)
        else:
            return Exclude(RawInput, FilterList)
        