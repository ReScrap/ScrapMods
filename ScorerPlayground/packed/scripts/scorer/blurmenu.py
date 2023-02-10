import Scrap,SInput,SNet,SWeap,SScorer,SVec

logger = None

try:
    logger = __import__("Logger").Logger("BlurMenu")
except Exception:
    pass

def log(msg):
    if logger is not None:
        logger.info(msg)
    else:
        Scrap.Print("[STRNG][BlurMenu] " + str(msg) + "\n")

log("Starting module")


MotionBlurOffVar      = 0
MotionBlurTime        = 0
MotionBlurEndTime     = 0
MotionBlurFactorBegin = 0
MotionBlurFactorEnd   = 0


Menu = None

class Slider:
    def __init__(
            self,
            id,
            name,
            x,
            y,
            min = 0,
            max = 1,
            value = 0,
            step = 0.1,
            onChange = None,
            onSub = None,
            onAdd = None,
            itemNum = None,
        ):
        self.id       = id
        self.name     = name
        self.x        = x
        self.y        = y
        self.min      = min
        self.max      = max
        self.value    = value
        self.step     = step
        self.onChange = onChange
        self.onSub    = onSub
        self.onAdd    = onAdd
        self.itemNum  = itemNum

    def Create(self):
        import Menu

        Menu.SliderMenu(self.id, self.name, self.x, self.y)

        SScorer.Set(self.id, self.name, "MaxValue",  self.max  )
        SScorer.Set(self.id, self.name, "MinValue",  self.min  )
        SScorer.Set(self.id, self.name, "ValueStep", self.step  )
        SScorer.Set(self.id, self.name, "Value",     self.value)

        if self.onChange:
            SScorer.Set(self.id, self.name, "OnChange", self.onChange)

        if self.onSub:
            name = self.name + "_Sub"
            SScorer.Add(self.id, name, "Text"                   )
            SScorer.Set(self.id, name, "Text",        ""        )
            SScorer.Set(self.id, name, "W",           0         )
            SScorer.Set(self.id, name, "H",           0         )
            SScorer.Set(self.id, name, "OnGainFocus", self.onAdd)

        if self.onAdd:
            name = self.name + "_Add"
            SScorer.Add(self.id, name, "Text"                   )
            SScorer.Set(self.id, name, "Text",        ""        )
            SScorer.Set(self.id, name, "W",           0         )
            SScorer.Set(self.id, name, "H",           0         )
            SScorer.Set(self.id, name, "OnGainFocus", self.onAdd)

        if self.itemNum:
            itemStr = "Item" + str(self.itemNum)

            Menu.LinkLR(self.id, self.name, itemStr  )
            Menu.LinkLR(self.id, itemStr,   self.name)

        if self.itemNum and self.onSub:
            Menu.LinkLR(self.id, "DummySliderSub", itemStr)

        if self.itemNum and self.onAdd:
            Menu.LinkLR(self.id, itemStr, "DummySliderAdd")


def BlurMenu(id, control):
    import Menu
    log("Creating trip menu")

    Menu.StartNewMenu(id)
    Menu.VerticalMenu(id, Scrap.GetLangStr("Menu_Options_MyMenu"),(
            [Scrap.GetLangStr("BlurMenu_OffVar")      + ":", "Menu.DummyFunc"] ,
            [Scrap.GetLangStr("BlurMenu_Time")        + ":", "Menu.DummyFunc"] ,
            [Scrap.GetLangStr("BlurMenu_EndTime")     + ":", "Menu.DummyFunc"] ,
            [Scrap.GetLangStr("BlurMenu_FactorBegin") + ":", "Menu.DummyFunc"] ,
            [Scrap.GetLangStr("BlurMenu_FactorEnd")   + ":", "Menu.DummyFunc"] ,
            [Scrap.GetLangStr("Menu_Back"),"Menu.OptionsMenu"]),
        "Menu.OptionsMenu", XStart = 310, VerticalStep = 36, YStart = Menu.OptionMenuYStart, Font = "ScrapMedium")

    X = 330

    sliders = ["OffVar", "Time", "EndTime", "FactorBegin", "FactorEnd"]
    for i in range(len(sliders)):
        sliderName = sliders[i]
        onChange   = "BlurMenu.SetBlurVar"
        onAdd      = "BlurMenu.AddBlurVar"
        onSub      = "BlurMenu.SubBlurVar"

        Y = SScorer.Get(0, "Item" + str(i + 1), "Y") + 5

        slider = Slider(id, sliderName, X, Y, 0.1, 1, 0.01, 0, onChange, onSub, onAdd, i)
        slider.Create()

    Menu.DrawBackOptionMenu(id)


def SetBlurVar(id, control):
    Scrap.Set("MotionBlur" + control, SScorer.Get(id, control, 'Value'))

def AddBlurVar(id, control, prevcontrol):
    name = control[:-4]
    value      = SScorer.Get(id, name, 'Value')
    value_step = SScorer.Get(id, name, 'ValueStep')
    result     = value + value_step

    SScorer.Set(id, name, "Value", result)
    SScorer.SetDefault(id, prevcontrol)

def SubBlurVar(id, control, prevcontrol):
    name = control[:-4]
    value      = SScorer.Get(id, name, 'Value')
    value_step = SScorer.Get(id, name, 'ValueStep')
    result     = value - value_step

    SScorer.Set(id, name, "Value", result)
    SScorer.SetDefault(id, prevcontrol)
