import Scrap,SInput,SNet,SWeap,SScorer,SVec

logger = None

try:
    logger = __import__("Logger").Logger("MyMenu")
except Exception:
    pass

def log(*args):
    if logger is not None:
        logger.info(args)
    else:
        args = list(args)

        for i in range(len(args)):
            args[i] = str(args[i])
            if args[i] == None:
                args[i] = ""

        args = ["[MyMenu]"] + args
        msg = string.join(args, " ")
        Scrap.Print(msg + "\n")

log("Starting module")

# ResetToDefault()


def SetState(var, val):
    # log('SetState("' + var + '", ' + str(val) + ')')
    Scrap.SetSaveVar(var, str(val))
    Scrap.SaveConfig()


def GetState(var, val = None):
    # log('GetState("' + var + '")')
    result = Scrap.GetSaveVar(var)

    if result is None:
        return val
    else:
        return result


MOTD = ""

Menu = None

def MyMenu(id, control):
    ResetToDefault()

    import Menu
    log("Creating cusom menu")

    Menu.StartNewMenu(id)

    Menu.VerticalMenu(id, Scrap.GetLangStr("Menu_Options_MyMenu"),(
            [Scrap.GetLangStr("My_Menu_Test_Bool")    + ":", "MyMenu.TestBool"    ],
            [Scrap.GetLangStr("My_Menu_Test_Counter") + ":", "MyMenu.TestCounter" ],
            [Scrap.GetLangStr("My_Menu_Test_Slider")  + ":", "Menu.DummyFunc"       ],
            [Scrap.GetLangStr("BlurMenu_Menu"),"BlurMenu.BlurMenu"],
            [Scrap.GetLangStr("Menu_Back"),"Menu.OptionsMenu"]),
        "Menu.OptionsMenu", XStart = 310, VerticalStep = 36, YStart = Menu.OptionMenuYStart, Font = "ScrapMedium")

    controlName = "TestBool"
    caption = ""

    if GetState('test_bool') == '0':
        caption = "False"
    else:
        caption = "True"

    SScorer.Add(id,controlName,"Text")
    SScorer.Set(id,controlName,"Font", "ScrapMedium")
    SScorer.Set(id,controlName,"Text", caption)
    SScorer.Set(id,controlName,"CentralText", 1)
    SScorer.Set(id,controlName,"Align", "Left")
    SScorer.Set(id,controlName,"Red",SScorer.Get(0,"Item1","Red"))
    SScorer.Set(id,controlName,"Green",SScorer.Get(0,"Item1","Green"))
    SScorer.Set(id,controlName,"Blue",SScorer.Get(0,"Item1","Blue"))
    SScorer.Set(id,controlName,"X",330)
    SScorer.Set(id,controlName,"Y",SScorer.Get(0,"Item1","Y"))
    SScorer.Set(id,controlName,"Effect", "Shadow")
    SScorer.Set(id,controlName,"OnAccept", "MyMenu.TestBool")

    controlName = "TestCounter"
    SScorer.Add(id,controlName,"Text")
    SScorer.Set(id,controlName,"Font", "ScrapMedium")
    SScorer.Set(id,controlName,"Text", str(GetState('test_counter', 0)))
    SScorer.Set(id,controlName,"CentralText", 1)
    SScorer.Set(id,controlName,"Align", "Left")
    SScorer.Set(id,controlName,"Red",SScorer.Get(0,"Item1","Red"))
    SScorer.Set(id,controlName,"Green",SScorer.Get(0,"Item1","Green"))
    SScorer.Set(id,controlName,"Blue",SScorer.Get(0,"Item1","Blue"))
    SScorer.Set(id,controlName,"X",330)
    SScorer.Set(id,controlName,"Y",SScorer.Get(0,"Item2","Y"))
    SScorer.Set(id,controlName,"Effect", "Shadow")
    SScorer.Set(id,controlName,"OnAccept", "MyMenu.TestCounter")

    X = 330

    Y = SScorer.Get(0, "Item3", "Y") + 5
    controlName = "TestSlider"
    Menu.SliderMenu(id, controlName, X, Y)
    SScorer.Set(id,controlName,"MaxValue", 1 )
    SScorer.Set(id,controlName,"ValueStep", 0.1 )
    SScorer.Set(id,controlName,"Value", float(GetState('test_slider', 0)) )
    SScorer.Set(id,controlName,"OnChange","MyMenu.TestSlider_Change")


    controlName = "DummySliderSub"
    SScorer.Add(id,controlName,"Text")
    SScorer.Set(id,controlName,"Text","")
    SScorer.Set(id,controlName,"W",0)
    SScorer.Set(id,controlName,"H",0)
    SScorer.Set(id,controlName,"OnGainFocus","MyMenu.TestSlider_Sub")

    controlName = "DummySliderAdd"
    SScorer.Add(id,controlName,"Text")
    SScorer.Set(id,controlName,"Text","")
    SScorer.Set(id,controlName,"W",0)
    SScorer.Set(id,controlName,"H",0)
    SScorer.Set(id,controlName,"OnGainFocus","MyMenu.TestSlider_Add")

    Menu.LinkLR(id, "TestSlider",     "Item3")
    Menu.LinkLR(id, "Item3",          "TestSlider")
    Menu.LinkLR(id, "DummySliderSub", "Item3")
    Menu.LinkLR(id, "Item3",          "DummySliderAdd")

    Menu.DrawBackOptionMenu(id)

def ResetToDefault():
    state_vars = ['test_bool', 'test_counter', 'test_slider']

    for var in state_vars:
        if Scrap.GetSaveVar(var) is None:
            Scrap.CreateSaveVar(var, '0')

    # Scrap.CreateSaveVar('test_bool',    '1')
    # Scrap.CreateSaveVar('test_counter', '0')
    # Scrap.CreateSaveVar('test_slider',  '0')

    log("State inited")


def TestBool(id, control):
    if GetState('test_bool') == '1':
        SetState('test_bool', 0)
        SScorer.Set(id, "TestBool", "Text", "False")
    else:
        SetState('test_bool', 1)
        SScorer.Set(id, "TestBool", "Text", "True")


def TestCounter(id, control):
    SetState('test_counter', int(GetState('test_counter', 0)) + 1)
    SScorer.Set(id, "TestCounter", "Text", str(GetState('test_counter', 0)))


def TestSlider_Change(id, control):
    SetState('test_slider', SScorer.Get(id, 'TestSlider', 'Value'))

def TestSlider_Sub(id, control, prevcontrol):
    log(id, control, prevcontrol)
    value      = SScorer.Get(id, 'TestSlider', 'Value')
    value_step = SScorer.Get(id, 'TestSlider', 'ValueStep')
    result     = value - value_step

    SetState('test_slider', result)
    SScorer.Set(id, 'TestSlider', "Value", result)
    SScorer.SetDefault(id,prevcontrol)

def TestSlider_Add(id, control, prevcontrol):
    log(id, control, prevcontrol)
    value      = SScorer.Get(id, 'TestSlider', 'Value')
    value_step = SScorer.Get(id, 'TestSlider', 'ValueStep')
    result     = value + value_step

    SetState('test_slider', result)
    SScorer.Set(id, 'TestSlider', "Value", result)
    SScorer.SetDefault(id, prevcontrol)


log('End of file')
