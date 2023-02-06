import Scrap,SInput,SNet,SWeap,SScorer,SVec


def log(msg):
	Scrap.Print("[STRNG][PCMenu] " + msg + "\n")


log("Starting module")

MOTD = ""

Menu = None
MyMenuLib = __import__("modsmenu")
MyMenu = MyMenuLib.MyMenu

log("Mods menu imported")

def AbortWaitRedefine(id):
	global ControlMenuId
	SScorer.SetCursor(ControlMenuId,"Cursor")
	SInput.AbortListenToDefine()
	Scrap.Set("EscapeEvent","Menu.Init")
	SInput.SetActionSet("Menu")
	SScorer.SetCursor(ControlMenuId,"Cursor")
	RefreshControlMenu()


def KetRedefineFunc():
	AbortWaitRedefine(id)


def ClearKeyEntry(id,control):
	import string

	nset = string.split(control,".")
	SInput.ClearDefinedList(id,nset[0],nset[1],1)
	RefreshControlMenu()


def WaitForKeyPress(id,control):
	import string

	SScorer.Set(id,"1"+control,"Red",255)
	SScorer.Set(id,"1"+control,"Green",241)
	SScorer.Set(id,"1"+control,"Blue",174)
	SScorer.Set(id,    control,"Red",255)
	SScorer.Set(id,    control,"Green",241)
	SScorer.Set(id,    control,"Blue",174)
	SScorer.SetCursor(id,"")
	SScorer.Set(id,"Cursor","Visible",0)

	nset = string.split(control,".")

	SInput.ListenToDefine(id,nset[0],nset[1],"PCMenu.KetRedefineFunc");
	Scrap.Set("EscapeEvent","PCMenu.AbortWaitRedefine")
	SInput.SetActionSet("Inactive")

def RefreshControlMenu():
	import string
	global ControlMenuArray
	global ControlMenuId

	for v in ControlMenuArray:
		iname = "1"+v[2]
		nset = string.split(v[2],".")

		try:
			thelist = string.split(SInput.GetDefinedList(ControlMenuId,nset[0],nset[1],1),", ")
		except:
			pass

		listsize = len(thelist)
		definedlist = ""
		for lel in thelist:
			nv = string.split(lel,":")
			if  (nv[0]=="Mouse"):
				definedlist = definedlist+" \2"+nv[1]
			elif(nv[0]=="Kb"):
				definedlist = definedlist+" \3"+nv[1]
			elif(nv[0]=="Joy1"):
				definedlist = definedlist+" \4"+nv[1]
			elif(nv[0]=="Joy2"):
				definedlist = definedlist+" \5"+nv[1]
			elif(nv[0]=="Joy3"):
				definedlist = definedlist+" \6"+nv[1]
			elif(nv[0]=="Joy4"):
				definedlist = definedlist+" \7"+nv[1]



		SScorer.Set(ControlMenuId,iname,"Text",definedlist)
		if listsize>=4:
			SScorer.Set(ControlMenuId,v[2],"OnAccept","Menu.DummyFunc")

			SScorer.Set(ControlMenuId,iname,"Red",128)
			SScorer.Set(ControlMenuId,iname,"Green", 128)
			SScorer.Set(ControlMenuId,iname,"Blue",  128)

			SScorer.Set(ControlMenuId,v[2],"Red",128)
			SScorer.Set(ControlMenuId,v[2],"Green", 128)
			SScorer.Set(ControlMenuId,v[2],"Blue",  128)
		else:
			SScorer.Set(ControlMenuId,v[2],"OnAccept","PCMenu.WaitForKeyPress")

			SScorer.Set(ControlMenuId,v[2],"Red",183)
			SScorer.Set(ControlMenuId,v[2],"Green", 220)
			SScorer.Set(ControlMenuId,v[2],"Blue",  255)

			SScorer.Set(ControlMenuId,iname,"Red",183)
			SScorer.Set(ControlMenuId,iname,"Green",220)
			SScorer.Set(ControlMenuId,iname,"Blue",255)


def CreateControlMenu(id,title,menu,backfunc,AcTab):
	import string
	global ControlMenuArray
	ControlMenuArray = menu
	global ControlMenuId
	ControlMenuId = id

	Menu.StartNewMenu(id)

	XSeparator = 295
	XSeparatorSize = 5

	Menu.VerticalMenu(id,title,menu,backfunc,XSeparator-XSeparatorSize,Font="Horatio",VerticalStep = 21,MinYStart=-88)

	# Hint de borrado de tecla
	SScorer.Add(ControlMenuId, "Hint", "Hint")
	SScorer.Set(ControlMenuId, "Hint", "Font", "Horatio")
	SScorer.Set(ControlMenuId, "Hint", "Effect", "Shadow")
	SScorer.Set(ControlMenuId, "Hint", "Align", "Center")
	SScorer.Set(ControlMenuId, "Hint", "X", 320)
	SScorer.Set(ControlMenuId, "Hint", "Y", 384)
	SScorer.Set(ControlMenuId, "Hint", "Red", 255)
	SScorer.Set(ControlMenuId, "Hint", "Green", 241)
	SScorer.Set(ControlMenuId, "Hint", "Blue", 174)
	SScorer.Set(ControlMenuId, "Hint", "Visible", 1)

	for v in menu:
		iname = "1"+v[2]

		SScorer.Add(ControlMenuId,iname,"Text")
		SScorer.Set(ControlMenuId,iname,"X",XSeparator+XSeparatorSize)
		SScorer.Set(ControlMenuId,iname,"Y",SScorer.Get(ControlMenuId,v[2],"Y")+10)
		SScorer.Set(ControlMenuId,iname,"Font","Terminal8")
		SScorer.Set(ControlMenuId,iname,"Align","Left")
		SScorer.Set(ControlMenuId,v[2],"OnDelete","PCMenu.ClearKeyEntry")

	RefreshControlMenu()


	# El botón de Back
	iname = "Back"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","ScrapBig")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Back"))
	SScorer.Set(id,iname,"X",320)
	SScorer.Set(id,iname,"Y",Menu.BackButtonYStart)
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"OnAccept","PCMenu.ControlsMenu")
	SScorer.Set(id,iname,"Red",   183)
	SScorer.Set(id,iname,"Green", 220)
	SScorer.Set(id,iname,"Blue",  255)
	SScorer.Set(id,iname,"Effect", "Shadow");

	Menu.AddTabs(id,(
	                ["Ship",     	"PCMenu.RacerMoveControlsMenu", Scrap.GetLangStr("Menu_Controls_Ship")],
	                ["Attack",   	"PCMenu.RacerAttackControlsMenu", Scrap.GetLangStr("Menu_Controls_Attack")],
	                ["Character",	"PCMenu.WalkCharControlsMenu", Scrap.GetLangStr("Menu_Controls_Character")],
	                ["Action",   	"PCMenu.UseCharControlsMenu", Scrap.GetLangStr("Menu_Controls_Action")]
	            ),AcTab)

	# Linkamos la primera opción del menu con el tab activo
	SScorer.Set(id,AcTab,"Up","Back")
	SScorer.Set(id,AcTab,"Down",menu[0][2])
	SScorer.Set(id,menu[0][2],"Up",AcTab)
	SScorer.Set(id,"Back","Down",AcTab)

	# Linkamos la última opción del menu con el botón Back
	Menu.LinkUD(id, Menu.VerticalMenuLastControl, iname)

	Menu.DrawCircuitMenu(id)



def RacerMoveControlsMenu(id,control=""):
	mnu =	[
	                [Scrap.GetLangStr("Menu_Controls_Ship_Forward"),"",    		"Racer.Forward"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_Backwards"),"",  		"Racer.Backward"],
	                #[Scrap.GetLangStr("Menu_Controls_Ship_Accelerate"),"", 	"Racer.TrustUp"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_Boost"),"",      		"Racer.Boost"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_StrafeUp"),"",		"Racer.StrafeUp"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_StrafeDown"),"", 		"Racer.StrafeDown"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_StrafeLeft"),"", 		"Racer.StrafeLeft"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_StrafeRight"),"",		"Racer.StrafeRight"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_BlockStrafe"),"",		"Racer.BockStrafe"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_RotateUp"),"",   		"Racer.Up"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_RotateDown"),"", 		"Racer.Down"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_RotateLeft"),"", 		"Racer.Left"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_RotateRight"),"",		"Racer.Right"],
	                [Scrap.GetLangStr("Menu_Controls_Ship_SwitchView"),"",		"Racer.SwitchView"]

		]
	CreateControlMenu(id, None,mnu,
	                "PCMenu.ControlsMenu","Ship")


def RacerAttackControlsMenu(id,control=""):
	mnu =	(
	                [Scrap.GetLangStr("Menu_Controls_Attack_Fire"),"",           	"Racer.Fire"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_Countermeasure"),"", 	"Racer.CM"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_NextWeapon"),"",    	"Racer.NextWeapon"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_PreviousWeapon"),"",	"Racer.PrevWeapon"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_Laser"),"",          	"Racer.Laser"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_Vulcan"),"",         	"Racer.Vulcan"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_Devastator"),"",     	"Racer.Devastator"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_Tesla"),"",          	"Racer.Tesla"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_ATPC"),"",       	"Racer.ATPC"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_Swarm"),"",          	"Racer.Swarm"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_Inferno"),"",          	"Racer.Inferno"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_LockEnemyShip"),"",	"Racer.TargetNext"],
	                [Scrap.GetLangStr("Menu_Controls_Attack_LockShip"),"",		"Racer.TargetReticle"]
		)
	CreateControlMenu(id, None,mnu,
	                "PCMenu.ControlsMenu","Attack")


def WalkCharControlsMenu(id,control=""):
	mnu = (
	                [Scrap.GetLangStr("Menu_Controls_Character_Forward"),"",     	"Walk.Forward"],
	                [Scrap.GetLangStr("Menu_Controls_Character_Backwards"),"",    	"Walk.Backward"],
	                [Scrap.GetLangStr("Menu_Controls_Character_StrafeLeft"),"",   	"Walk.StrafeLeft"],
	                [Scrap.GetLangStr("Menu_Controls_Character_StrafeRight"),"",   	"Walk.StrafeRight"],
	                [Scrap.GetLangStr("Menu_Controls_Character_TurnLeft"),"",      	"Walk.TurnLeft"],
	                [Scrap.GetLangStr("Menu_Controls_Character_TurnRight"),"",     	"Walk.TurnRight"],
	                [Scrap.GetLangStr("Menu_Controls_Character_TurnUp"),"",        	"Walk.TurnUp"],
	                [Scrap.GetLangStr("Menu_Controls_Character_TurnDown"),"",      	"Walk.TurnDown"],
	                [Scrap.GetLangStr("Menu_Controls_Character_RunWalk"),"",       	"Walk.SwitchRunWalk"],
	                [Scrap.GetLangStr("Menu_Controls_Character_BlockStrafe"),"",   	"Walk.BlockStrafe"]
	      )
	CreateControlMenu(id, None,mnu,
	                "PCMenu.ControlsMenu","Character")


def UseCharControlsMenu(id,control=""):
	mnu = (
	                [Scrap.GetLangStr("Menu_Controls_Action_Action"),"",  		"Walk.Use"],
	                [Scrap.GetLangStr("Menu_Controls_Action_SpecialAction"),"",   	"Walk.Action"],
	                [Scrap.GetLangStr("Menu_Controls_Action_Overwrite"),"",       	"Walk.Possession"],
	                [Scrap.GetLangStr("Menu_Controls_Action_NextOption"),"",      	"Walk.NextAction"],
	                [Scrap.GetLangStr("Menu_Controls_Action_PreviousOption"),"",  	"Walk.PrevAction"],
	                [Scrap.GetLangStr("Menu_Controls_Action_PadLeft"),"",         	"Walk.StrafeTurnLeft"],
	                [Scrap.GetLangStr("Menu_Controls_Action_PadRight"),"",        	"Walk.StrafeTurnRight"],
	                [Scrap.GetLangStr("Menu_Controls_Action_PadBlockStrafe"),"",  	"Walk.CameraCenter"],
	                [Scrap.GetLangStr("Menu_Controls_Action_Chat"),"",            	"Racer.Chat"],
	                [Scrap.GetLangStr("Menu_Controls_Action_ShowScorer"),""    , 	"Racer.Scorer"]
	      )
	CreateControlMenu(id, None,mnu,
	                "PCMenu.ControlsMenu","Action")


def ResetEverything(id,control):

	SInput.ResetToDefault()
	MyMenu.ResetToDefault()

	Scrap.Set("InvertMouse",0)
	Scrap.Set("MouseSensitivityH",1)
	Scrap.Set("MouseSensitivityV",1)

	Scrap.Set( "XBInvertCharYPad",     Scrap.Def("XBInvertCharYPad"   ) )
	Scrap.Set( "XBCDigitalAsAnalog",   Scrap.Def("XBCDigitalAsAnalog" ) )
	Scrap.Set( "XBCameraAutoPad",      Scrap.Def("XBCameraAutoPad"    ) )
	Scrap.Set( "XBInvertLRChar",       Scrap.Def("XBInvertLRChar"     ) )
	Scrap.Set( "XBInvertVehicleYPad",  Scrap.Def("XBInvertVehicleYPad") )
	Scrap.Set( "XBVDigitalAsAnalog",   Scrap.Def("XBVDigitalAsAnalog" ) )
	Scrap.Set( "XBVehicleAsFPS",       Scrap.Def("XBVehicleAsFPS"     ) )
	Scrap.Set( "XBInvertLRVehicle",    Scrap.Def("XBInvertLRVehicle"  ) )

	ControlsMenu(id,control)


def ResetToDefault(id,control):
	Menu.YesNoMenu(id,Scrap.GetLangStr("Menu_Controls_ResetToDefaultQuestion"),"PCMenu.ResetEverything","PCMenu.ControlsMenu")



def OptionYesNo(id, control):

	if Scrap.Get(control)==1:
		Scrap.Set(control,0)
		SScorer.Set(id,control,"Text",Scrap.GetLangStr("Menu_Question_No"))
	else:
		Scrap.Set(control,1)
		SScorer.Set(id,control,"Text",Scrap.GetLangStr("Menu_Question_Yes"))



def AlwaysRun(id,control):
	cadeno = "Always Run  "

	if Scrap.Get("AlwaysRun"):
		Scrap.Set("AlwaysRun",0)
		SScorer.Set(id,control,"Text",cadeno+Scrap.GetLangStr("Menu_Question_No"))
	else:
		Scrap.Set("AlwaysRun",1)
		SScorer.Set(id,control,"Text",cadeno+Scrap.GetLangStr("Menu_Question_Yes"))

def ControlsMenu(id,control):

	Menu.StartNewMenu(id)

	Menu.VerticalMenu(id,Scrap.GetLangStr("Menu_Options_Controls"),(
	                [Scrap.GetLangStr("Menu_Controls_Mouse"),"PCMenu.MouseControlsMenu"],
	                [Scrap.GetLangStr("Menu_Controls_Redefine"),"PCMenu.RacerMoveControlsMenu"],
	                [Scrap.GetLangStr("XBox_Menu_Controller_Configuration"),"PCMenu.ControllerConfig"],
	                [Scrap.GetLangStr("Menu_Controls_ResetToDefault"),"PCMenu.ResetToDefault"],
	                [Scrap.GetLangStr("Menu_Back"),"Menu.OptionsMenu"]),
	                "Menu.OptionsMenu", YStart = Menu.OptionMenuYStart)
	Menu.DrawBackOptionMenu(id)

##########################################################################################################
currentActionSet = ""

options = {}

optionsChar = { "Item1" : ("XBCameraAutoPad",     "ConfigurationTypeChar"),
		"Item2" : ("XBInvertCharYPad",    "InvertYChar"),
		"Item3" : ("XBCDigitalAsAnalog",  "DigitalCrossChar"),
		"Item4" : ("XBInvertLRChar",      "InvertTriggersChar")
	      }

optionsShip = { "Item1" : ("XBVehicleAsFPS",      "ConfigurationTypeShip"),
		"Item2" : ("XBInvertVehicleYPad", "InvertYShip"),
		"Item3" : ("XBVDigitalAsAnalog",  "DigitalCrossShip"),
		"Item4" : ("XBInvertLRVehicle",   "InvertTriggersShip")
	      }

baseYPos = 280

buttons = { "Y"      : ("Left",  388, baseYPos - 60),
	    "X"      : ("Left",  388, baseYPos - 40),
	    "B"      : ("Left",  388, baseYPos - 20),
	    "A"      : ("Left",  388, baseYPos),
	    "BLACK"  : ("Left",  388, baseYPos + 20),
	    "WHITE"  : ("Left",  388, baseYPos + 40),
	    "BACK"   : ("Right", 252, baseYPos + 4),
	    "START"  : ("Right", 252, baseYPos + 28),
	    "L"      : ("Right", 280, baseYPos - 105),
	    "R"      : ("Left",  360, baseYPos - 105),
	  }

buttonsSymbols = { "Y"     : "\x17",
		   "X"     : "\x16",
		   "B"     : "\x15",
		   "A"     : "\x14",
		   "BLACK" : "\x1D",
		   "WHITE" : "\x1C",
		   "BACK"  : "\x1B",
		   "START" : "\x1A",
		   "R"     : "\x19",
		   "L"     : "\x18",
		 }

def ControllerConfig(id, control):

	import Menu
	global options, currentActionSet

	currentActionSet = Menu.LastMode
	if (currentActionSet == "Walk"):
		options = optionsChar
		FillControllerMenu(id, control, "Char")
	else:
		currentActionSet = "Racer"
		options = optionsShip
		FillControllerMenu(id, control, "Ship")

def ControllerConfigCharMenu(id, control):

	global options, currentActionSet

	currentActionSet = "Walk"
	options = optionsChar
	FillControllerMenu(id, control, "Char")


def ControllerConfigShipMenu(id, control):

	global options, currentActionSet

	currentActionSet = "Racer"
	options = optionsShip
	FillControllerMenu(id, control, "Ship")

def FillControllerMenu(id, control, actualTab):

	Menu.StartNewMenu(id)

	if (actualTab == "Ship"):
		cad = Scrap.GetLangStr("XBox_Menu_Controller_Configuration_Option")
	else:
		cad = Scrap.GetLangStr("XBox_Menu_Controller_CameraType")

	# Añado las opciones
	Menu.VerticalMenu(id, None, (
	                [cad                                                            + ":", "PCMenu.SwitchOption"],
	                [Scrap.GetLangStr("XBox_Menu_Controller_InvertY_Option")        + ":", "PCMenu.SwitchOption"],
	                [Scrap.GetLangStr("XBox_Menu_Controller_DigitalCross_Option")   + ":", "PCMenu.SwitchOption"],
	                [Scrap.GetLangStr("XBox_Menu_Controller_InvertTriggers_Option") + ":", "PCMenu.SwitchOption"],
	                [Scrap.GetLangStr("Menu_Back"), "PCMenu.ControlsMenu"]),
	                "PCMenu.ControlsMenu", YStart = 90, MinYStart = 90, Font = "Horatio", VerticalStep = 20)

	i = 1
	optionsKeys = options.keys()
	optionsKeys.sort()
	for key in optionsKeys:
		PlaceMenuOption(id, i, options[key][1])
		SetOptionValue(id, options[key][1])
		i = i + 1

	SScorer.SetDefault(id, "Item1")

	# Muestro el dibujo del mando con las acciones asociadas a cada botón
	if (actualTab == "Char"):
		ShowPadConfig(id, "Walk")
	else:
		ShowPadConfig(id, "Racer")

	# Pongo los tabs
	Menu.AddTabs(id, (
	                ["Char", "PCMenu.ControllerConfigCharMenu", Scrap.GetLangStr("XBox_Menu_Controller_Character_Tab")],
	                ["Ship", "PCMenu.ControllerConfigShipMenu", Scrap.GetLangStr("XBox_Menu_Controller_Ship_Tab")],
	            ), actualTab, ParamTabSize = 37, Hint = 0, CenterTextInTabs = 1)

	if (actualTab == "Char"):
		Menu.LinkUD(id, "Char", "Item1")
		Menu.LinkUD(id, "Item4", "Char")
	else:
		Menu.LinkUD(id, "Ship", "Item1")
		Menu.LinkUD(id, "Item4", "Ship")

	Menu.DrawCircuitMenu(id)

def SwitchOption(id, control):

	global SaveOptions

	SaveOptions = 1

	gvar, optionType = options[control]
	if (Scrap.Get(gvar) == 0):
		Scrap.Set(gvar, 1)
	else:
		Scrap.Set(gvar, 0)

	SInput.ResetToDefault()
	SetOptionValue(id, optionType)
	ShowPadConfig(id, currentActionSet)

def PlaceMenuOption(id, n, controlName):

	XMiddle = 330

	itemName = "Item" + `n`
	X = XMiddle - SScorer.Get(id, itemName, "W") - 5
	Y = SScorer.Get(id, itemName, "Y")

	SScorer.Set(id, itemName, "X", X)

	SScorer.Add(id, controlName, "Text")
	SScorer.Set(id, controlName, "Font", "Horatio")
	SScorer.Set(id, controlName, "X", XMiddle)
	SScorer.Set(id, controlName, "Y", Y)
	SScorer.Set(id, controlName, "Visible", 1)
	SScorer.Set(id, controlName, "Red",   183)
	SScorer.Set(id, controlName, "Green", 220)
	SScorer.Set(id, controlName, "Blue",  255)

def SetOptionValue(id, control):

	########
	# Char #
	########

	if   (control == "ConfigurationTypeChar"):

		if (Scrap.Get("XBCameraAutoPad") == 1):
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("XBox_Menu_Controller_CameraType_Option1"))
		else:
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("XBox_Menu_Controller_CameraType_Option2"))

	elif (control == "InvertYChar"):

		if (Scrap.Get("XBInvertCharYPad") == 1):
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("Menu_Question_Yes"))
		else:
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("Menu_Question_No"))

	elif (control == "DigitalCrossChar"):

		if (Scrap.Get("XBCDigitalAsAnalog") == 1):
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("XBox_Menu_Controller_DigitalCross_Char_Option1"))
		else:
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("XBox_Menu_Controller_DigitalCross_Char_Option2"))

	elif (control == "InvertTriggersChar"):

		if (Scrap.Get("XBInvertLRChar") == 1):
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("Menu_Question_Yes"))
		else:
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("Menu_Question_No"))

	########
	# Ship #
	########

	elif (control == "ConfigurationTypeShip"):

		if (Scrap.Get("XBVehicleAsFPS") == 0):
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("XBox_Menu_Controller_Configuration1"))
		else:
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("XBox_Menu_Controller_Configuration2"))

	elif (control == "InvertYShip"):

		if (Scrap.Get("XBInvertVehicleYPad") == 1):
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("Menu_Question_Yes"))
		else:
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("Menu_Question_No"))

	elif (control == "DigitalCrossShip"):

		if (Scrap.Get("XBVDigitalAsAnalog") == 1):
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("XBox_Menu_Controller_DigitalCross_Ship_Option2"))
		else:
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("XBox_Menu_Controller_DigitalCross_Ship_Option1"))

	elif (control == "InvertTriggersShip"):

		if (Scrap.Get("XBInvertLRVehicle") == 1):
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("Menu_Question_Yes"))
		else:
			SScorer.Set(id, control, "Text", Scrap.GetLangStr("Menu_Question_No"))

def DrawLine(id, name, posX = 64, posY = 64, sizeX = 512, sizeY = 352, alpha = 92, red = 0, green = 0, blue = 32):

	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Sprite")
	SScorer.Set(id, name, "X",      posX)
	SScorer.Set(id, name, "Y",      posY)
	SScorer.Set(id, name, "ScaleX", sizeX)
	SScorer.Set(id, name, "ScaleY", sizeY)
	SScorer.Set(id, name, "Unit", 1)
	SScorer.Set(id, name, "Alpha", alpha)
	SScorer.Set(id, name, "Red",   red)
	SScorer.Set(id, name, "Green", green)
	SScorer.Set(id, name, "Blue",  blue)
	SScorer.Set(id, name, "Visible", 1)

def UpdatePadText(id, ActionSet):

	# Texto de los botones
	buttonsSymbolsKeys = buttonsSymbols.keys()
	for b in buttons.keys():

		blank = " "
		if (b in buttonsSymbolsKeys):
			cad = buttonsSymbols[b]
			desc = SInput.GetEntry("Pad1", b, ActionSet)[1]
			desc = Scrap.GetLangStr("XBox_Menu_Controller_" + desc)
		else:
			cad = ""
			blank = ""

		if (b in ["Y", "X", "B", "A", "BLACK", "WHITE", "R"]):
			finalText = cad + blank + desc
			if (desc == ""):
				SScorer.Set(id, b, "Text", cad + blank + Scrap.GetLangStr("XBox_Menu_Controller_NoAction"))
			else:
				SScorer.Set(id, b, "Text", finalText)
		else:
			finalText = desc + " " + cad
			SScorer.Set(id, b, "Text", finalText)

	# Texto de los sticks analógicos y de la cruceta digital
	# Primero oculto todos los controles (luego los voy activando según se necesiten)
	for c in ["DCrossLR", "DCrossUD", "LeftThumbstickLR", "LeftThumbstickUD", "RightThumbstickLR", "RightThumbstickUD"]:
		SScorer.Set(id, c, "Visible", 0)

	for c in ["TextDCrossLR", "TextDCrossUD", "TextLeftThumbstickLR", "TextLeftThumbstickUD", "TextRightThumbstickLR", "TextRightThumbstickUD"]:
		SScorer.Set(id, c, "Visible", 0)


	if (ActionSet == "Walk"):

		name = "TextLeftThumbstickLR"
		SScorer.Set(id, name, "Text", Scrap.GetLangStr("XBox_Menu_Controller_LeftThumbstick_Char_Option"))
		SScorer.Set(id, name, "X", 250)
		SScorer.Set(id, name, "Visible", 1)

		name = "TextRightThumbstickLR"
		SScorer.Set(id, name, "Text", Scrap.GetLangStr("XBox_Menu_Controller_RightThumbstick_Char_Option"))
		SScorer.Set(id, name, "X", 345)
		SScorer.Set(id, name, "Visible", 1)

		if (Scrap.Get("XBCDigitalAsAnalog") == 0):

			name = "TextDCrossLR"
			SScorer.Set(id, name, "Text", Scrap.GetLangStr("XBox_Menu_Controller_DigitalCross_Char_Option2"))
			SScorer.Set(id, name, "X", 295)
			SScorer.Set(id, name, "Visible", 1)

	else:

		if (Scrap.Get("XBVDigitalAsAnalog") == 0):

			name = "DCrossLR"
			SScorer.Set(id, name, "Visible", 1)

			name = "TextDCrossLR"
			SScorer.Set(id, name, "Text", Scrap.GetLangStr("XBox_Menu_Controller_DigitalCross_Ship_LR"))
			SScorer.Set(id, name, "Visible", 1)

			name = "DCrossUD"
			SScorer.Set(id, name, "Visible", 1)

			name = "TextDCrossUD"
			SScorer.Set(id, name, "Text", Scrap.GetLangStr("XBox_Menu_Controller_DigitalCross_Ship_UD"))
			SScorer.Set(id, name, "Visible", 1)

		if (Scrap.Get("XBVehicleAsFPS") == 0):

			name = "RightThumbstickLR"
			SScorer.Set(id, name, "Visible", 1)

			name = "TextRightThumbstickLR"
			SScorer.Set(id, name, "Text", Scrap.GetLangStr("XBox_Menu_Controller_RightThumbstick_Ship_Option1_LR"))
			SScorer.Set(id, name, "Visible", 1)

			name = "RightThumbstickUD"
			SScorer.Set(id, name, "Visible", 1)

			name = "TextRightThumbstickUD"
			SScorer.Set(id, name, "Text", Scrap.GetLangStr("XBox_Menu_Controller_RightThumbstick_Ship_Option1_UD"))
			SScorer.Set(id, name, "Visible", 1)

			name = "TextLeftThumbstickLR"
			SScorer.Set(id, name, "Text", Scrap.GetLangStr("XBox_Menu_Controller_LeftThumbstick_Ship_Option1"))
			SScorer.Set(id, name, "X", 250)
			SScorer.Set(id, name, "Visible", 1)

		else:

			name = "LeftThumbstickLR"
			SScorer.Set(id, name, "Visible", 1)

			name = "TextLeftThumbstickLR"
			SScorer.Set(id, name, "Text", Scrap.GetLangStr("XBox_Menu_Controller_LeftThumbstick_Ship_Option2_LR"))
			SScorer.Set(id, name, "Visible", 1)

			name = "LeftThumbstickUD"
			SScorer.Set(id, name, "Visible", 1)

			name = "TextLeftThumbstickUD"
			SScorer.Set(id, name, "Text", Scrap.GetLangStr("XBox_Menu_Controller_LeftThumbstick_Ship_Option2_UD"))
			SScorer.Set(id, name, "Visible", 1)

			name = "TextRightThumbstickLR"
			SScorer.Set(id, name, "Text", Scrap.GetLangStr("XBox_Menu_Controller_RightThumbstick_Ship_Option2"))
			SScorer.Set(id, name, "X", 345)
			SScorer.Set(id, name, "Visible", 1)

def ShowPadConfig(id, ActionSet, YOffset = 0):

	# Controles de texto de los botones
	for b in buttons.keys():

		props = buttons[b]
		if (SScorer.Get(id, b, "Visible") == None):
			SScorer.Add(id, b, "Text")
		SScorer.Set(id, b, "Font", "Horatio")
		SScorer.Set(id, b, "Align", props[0])
		SScorer.Set(id, b, "X", props[1])
		SScorer.Set(id, b, "Y", props[2] + YOffset)
		SScorer.Set(id, b, "Visible", 1)

	# Controles de texto de los sticks analógicos y la cruceta digital
	name = "TextRightThumbstickLR"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Text")
	SScorer.Set(id, name, "Font", "Horatio")
	SScorer.Set(id, name, "Align", "Left")
	SScorer.Set(id, name, "X", 375)
	SScorer.Set(id, name, "Y", 378 + YOffset)

	name = "TextRightThumbstickUD"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Text")
	SScorer.Set(id, name, "Font", "Horatio")
	SScorer.Set(id, name, "Align", "Left")
	SScorer.Set(id, name, "X", 375)
	SScorer.Set(id, name, "Y", 350 + YOffset)

	name = "TextLeftThumbstickLR"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Text")
	SScorer.Set(id, name, "Font", "Horatio")
	SScorer.Set(id, name, "Align", "Right")
	SScorer.Set(id, name, "X", 215)
	SScorer.Set(id, name, "Y", 245 + YOffset)

	name = "TextLeftThumbstickUD"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Text")
	SScorer.Set(id, name, "Font", "Horatio")
	SScorer.Set(id, name, "Align", "Right")
	SScorer.Set(id, name, "X", 215)
	SScorer.Set(id, name, "Y", 215 + YOffset)

	name = "TextDCrossLR"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Text")
	SScorer.Set(id, name, "Font", "Horatio")
	SScorer.Set(id, name, "Align", "Right")
	SScorer.Set(id, name, "X", 265)
	SScorer.Set(id, name, "Y", 378 + YOffset)

	name = "TextDCrossUD"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Text")
	SScorer.Set(id, name, "Font", "Horatio")
	SScorer.Set(id, name, "Align", "Right")
	SScorer.Set(id, name, "X", 265)
	SScorer.Set(id, name, "Y", 350 + YOffset)

	# Dibujo las lineas (para los textos que lo necesiten)
	DrawLine(id, "RStickLine",  338, baseYPos + 1 + YOffset,  1, 100, 255, 40, 228, 240)
	DrawLine(id, "LStickLine",  254, baseYPos - 21 + YOffset, 28, 1, 255, 40, 228, 240)
	DrawLine(id, "LTrigger",    273, baseYPos - 83 + YOffset, 1, 44, 255, 40, 228, 240)
	DrawLine(id, "RTrigger",    367, baseYPos - 83 + YOffset, 1, 44, 255, 40, 228, 240)
	DrawLine(id, "DCrossLine",  300, baseYPos + 1 + YOffset,  1, 100, 255, 40, 228, 240)
	DrawLine(id, "DCrossLine1", 250, baseYPos + 1 + YOffset,  50, 1, 255, 40, 228, 240)
	DrawLine(id, "DCrossLine2", 250, baseYPos + 1 - 15 + YOffset,  1, 15, 255, 40, 228, 240)

	if ((ActionSet == "Racer" and Scrap.Get("XBVDigitalAsAnalog") == 1) or (ActionSet == "Walk" and Scrap.Get("XBCDigitalAsAnalog") == 1)):
		SScorer.Set(id, "DCrossLine",  "Visible", 0)
	else:
		SScorer.Set(id, "DCrossLine1", "Visible", 0)
		SScorer.Set(id, "DCrossLine2", "Visible", 0)


	# Pongo los dibujos del mando
	name = "Pad"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Sprite")
	SScorer.Set(id, name, "Discardable", 1)
	SScorer.Set(id, name, "HighRes", 1)
	SScorer.Set(id, name, "IsMultiSprite", 1)
	SScorer.Set(id, name, "File", "2D/Menu/PadS.alpha.tga")
	SScorer.Set(id, name, "Highlight", 0)
	SScorer.Set(id, name, "SpriteIndex", 1)
	SScorer.Set(id, name, "PivotX", 0.5)
	SScorer.Set(id, name, "PivotY", 0.5)
	SScorer.Set(id, name, "X", 320)
	SScorer.Set(id, name, "Y", baseYPos + YOffset)

	name = "DCrossLR"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Sprite")
	SScorer.Set(id, name, "Discardable", 1)
	SScorer.Set(id, name, "HighRes", 1)
	SScorer.Set(id, name, "IsMultiSprite", 1)
	SScorer.Set(id, name, "File", "2D/Menu/PadS.alpha.tga")
	SScorer.Set(id, name, "Highlight", 0)
	SScorer.Set(id, name, "SpriteIndex", 2)
	SScorer.Set(id, name, "X", 270)
	SScorer.Set(id, name, "Y", 378 + YOffset)

	name = "DCrossUD"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Sprite")
	SScorer.Set(id, name, "Discardable", 1)
	SScorer.Set(id, name, "HighRes", 1)
	SScorer.Set(id, name, "IsMultiSprite", 1)
	SScorer.Set(id, name, "File", "2D/Menu/PadS.alpha.tga")
	SScorer.Set(id, name, "Highlight", 0)
	SScorer.Set(id, name, "SpriteIndex", 3)
	SScorer.Set(id, name, "X", 270)
	SScorer.Set(id, name, "Y", 350 + YOffset)

	name = "LeftThumbstickLR"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Sprite")
	SScorer.Set(id, name, "Discardable", 1)
	SScorer.Set(id, name, "HighRes", 1)
	SScorer.Set(id, name, "IsMultiSprite", 1)
	SScorer.Set(id, name, "File", "2D/Menu/PadS.alpha.tga")
	SScorer.Set(id, name, "Highlight", 0)
	SScorer.Set(id, name, "SpriteIndex", 4)
	SScorer.Set(id, name, "X", 220)
	SScorer.Set(id, name, "Y", 245 + YOffset)

	name = "LeftThumbstickUD"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Sprite")
	SScorer.Set(id, name, "Discardable", 1)
	SScorer.Set(id, name, "HighRes", 1)
	SScorer.Set(id, name, "IsMultiSprite", 1)
	SScorer.Set(id, name, "File", "2D/Menu/PadS.alpha.tga")
	SScorer.Set(id, name, "Highlight", 0)
	SScorer.Set(id, name, "SpriteIndex", 5)
	SScorer.Set(id, name, "X", 220)
	SScorer.Set(id, name, "Y", 215 + YOffset)

	name = "RightThumbstickLR"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Sprite")
	SScorer.Set(id, name, "Discardable", 1)
	SScorer.Set(id, name, "HighRes", 1)
	SScorer.Set(id, name, "IsMultiSprite", 1)
	SScorer.Set(id, name, "File", "2D/Menu/PadS.alpha.tga")
	SScorer.Set(id, name, "Highlight", 0)
	SScorer.Set(id, name, "SpriteIndex", 4)
	SScorer.Set(id, name, "X", 340)
	SScorer.Set(id, name, "Y", 378 + YOffset)

	name = "RightThumbstickUD"
	if (SScorer.Get(id, name, "Visible") == None):
		SScorer.Add(id, name, "Sprite")
	SScorer.Set(id, name, "Discardable", 1)
	SScorer.Set(id, name, "HighRes", 1)
	SScorer.Set(id, name, "IsMultiSprite", 1)
	SScorer.Set(id, name, "File", "2D/Menu/PadS.alpha.tga")
	SScorer.Set(id, name, "Highlight", 0)
	SScorer.Set(id, name, "SpriteIndex", 5)
	SScorer.Set(id, name, "X", 340)
	SScorer.Set(id, name, "Y", 350 + YOffset)

	# Pongo los textos de las acciones asociadas a cada botón y a cada stick
	UpdatePadText(id, ActionSet)

##########################################################################################################

def MouseControlsMenu(id,control):

	Menu.StartNewMenu(id)

	Acceleration  = Scrap.GetLangStr("Menu_Controls_Mouse_Acceleration" )
	Smooth        = Scrap.GetLangStr("Menu_Controls_Mouse_Smooth"       )
	Camera_Smooth = Scrap.GetLangStr("Menu_Controls_Mouse_Camera_Smooth")

	if Acceleration  == "":
		Acceleration  = "Acceleration"
	if Smooth        == "":
		Smooth        = "Smooth"
	if Camera_Smooth  == "":
		Camera_Smooth = "Camera Smooth"

	Menu.VerticalMenu(id,Scrap.GetLangStr("Menu_Controls_Mouse"),(
	                [Scrap.GetLangStr("Menu_Controls_Mouse_Invert")+":","PCMenu.InvertMouse"],
	                [Scrap.GetLangStr("Menu_Controls_Mouse_SensitivityH")+":","Menu.DummyFunc"],
	                [Scrap.GetLangStr("Menu_Controls_Mouse_SensitivityV")+":","Menu.DummyFunc"],
	                [Scrap.GetLangStr("Menu_Back"),"PCMenu.ControlsMenu"]),
	                "PCMenu.ControlsMenu", XStart = 310, VerticalStep = 36, YStart = Menu.OptionMenuYStart, Font = "ScrapMedium")

	controlName = "InvertMouse"
	SScorer.Add(id,controlName,"Text")
	SScorer.Set(id,controlName,"Font", "ScrapMedium")
	SScorer.Set(id,controlName,"Text", "WWW")
	SScorer.Set(id,controlName,"CentralText", 1)
	SScorer.Set(id,controlName,"Align", "Left")
	SScorer.Set(id,controlName,"Red",SScorer.Get(0,"Item1","Red"))
	SScorer.Set(id,controlName,"Green",SScorer.Get(0,"Item1","Green"))
	SScorer.Set(id,controlName,"Blue",SScorer.Get(0,"Item1","Blue"))
	SScorer.Set(id,controlName,"X",330)
	SScorer.Set(id,controlName,"Y",SScorer.Get(0,"Item1","Y"))
	SScorer.Set(id,controlName,"Effect", "Shadow")
	SScorer.Set(id,controlName,"OnAccept", "PCMenu.OptionYesNo")

	OptionYesNo(id,"InvertMouse")
	OptionYesNo(id,"InvertMouse")




	X = 330

	Y = SScorer.Get(0,"Item2","Y")
	controlName = "SensitivitySliderX"
	Menu.SliderMenu(id, controlName, X, Y)
	SScorer.Set(id,controlName,"Value", MouseSensitivityFormula(sens=Scrap.Get("MouseSensitivityH")) )
	SScorer.Set(id,controlName,"OnChange","PCMenu.MouseSensitivityChange")

	Y = SScorer.Get(0,"Item3","Y")
	controlName = "SensitivitySliderY"
	Menu.SliderMenu(id, controlName, X, Y)
	SScorer.Set(id,controlName,"Value", MouseSensitivityFormula(sens=Scrap.Get("MouseSensitivityV")) )
	SScorer.Set(id,controlName,"OnChange","PCMenu.MouseSensitivityChange")


	# enlazamos los controles de sensibilidad con unos dummies
	controlName = "DummySliderSub"
	SScorer.Add(id,controlName,"Text")
	SScorer.Set(id,controlName,"Text","")
	SScorer.Set(id,controlName,"W",0)
	SScorer.Set(id,controlName,"H",0)
	SScorer.Set(id,controlName,"OnGainFocus","PCMenu.MouseSensitivitySliderFocus_Sub")

	controlName = "DummySliderAdd"
	SScorer.Add(id,controlName,"Text")
	SScorer.Set(id,controlName,"Text","")
	SScorer.Set(id,controlName,"W",0)
	SScorer.Set(id,controlName,"H",0)
	SScorer.Set(id,controlName,"OnGainFocus","PCMenu.MouseSensitivitySliderFocus_Add")

	# X
	Menu.LinkLR(id,"SensitivitySliderX","Item2")
	Menu.LinkLR(id,"Item2","SensitivitySliderX")
	Menu.LinkLR(id,"DummySliderSub","Item2")
	Menu.LinkLR(id,"Item2","DummySliderAdd")

	# Y
	Menu.LinkLR(id,"SensitivitySliderY","Item3")
	Menu.LinkLR(id,"Item3","SensitivitySliderY")
	Menu.LinkLR(id,"DummySliderSub","Item3")
	Menu.LinkLR(id,"Item3","DummySliderAdd")



	# Back Tab

	SScorer.Set(id,"TitleBarL","Visible",0)
	SScorer.Set(id,"TitleBarM","Visible",0)
	SScorer.Set(id,"TitleBarR","Visible",0)

	SizeX = 36.5 * Menu.TabQuadSize
	SizeY = 21 * Menu.TabQuadSize
	TabX = 320 - SizeX/2
	TabY = SScorer.Get(id,"TitleBarM","Y")

	iname = "VideoOptionsTab"
	SScorer.Add(id,iname,"Tab")
	Menu.SetTabDefaults(id,iname)
	SScorer.Set(id,iname,"X", TabX)
	SScorer.Set(id,iname,"Y", TabY)
	SScorer.Set(id,iname,"SizeX", SizeX)
	SScorer.Set(id,iname,"SizeY", SizeY)
	SScorer.Set(id,iname,"TabInit",0)
	SScorer.Set(id,iname,"TabEnd", 0)
	SScorer.Set(id,iname,"TabMax", 0)
	SScorer.Set(id,iname,"SizeTabQuad", 0)
	SScorer.Set(id,iname,"Type", 2)	#TAB_MISSION
	SScorer.Set(id,iname,"Alpha", 150)
	SScorer.Set(id,iname,"Red",    60)
	SScorer.Set(id,iname,"Green", 150)
	SScorer.Set(id,iname,"Blue",  200)


	Menu.DrawBackOptionMenu(id)


def InvertMouse(id,control):
	OptionYesNo(id, "InvertMouse")


def MouseSensitivitySliderFocus_Sub(id,control,prevcontrol):

	slidercontrol = ""
	if prevcontrol == "Item2" :	# X
		slidercontrol = "SensitivitySliderX"
	elif prevcontrol == "Item3" :	# Y
		slidercontrol = "SensitivitySliderY"

	value = SScorer.Get(id,slidercontrol,"Value")
	valuestep = SScorer.Get(id,slidercontrol,"ValueStep")

	SScorer.Set(id,slidercontrol,"Value", value - valuestep)
	MouseSensitivityChange(id,control)

	SScorer.SetDefault(id,prevcontrol)


def MouseSensitivitySliderFocus_Add(id,control,prevcontrol):

	slidercontrol = ""
	if prevcontrol == "Item2" :	# X
		slidercontrol = "SensitivitySliderX"
	elif prevcontrol == "Item3" :	# Y
		slidercontrol = "SensitivitySliderY"

	value = SScorer.Get(id,slidercontrol,"Value")
	valuestep = SScorer.Get(id,slidercontrol,"ValueStep")

	SScorer.Set(id,slidercontrol,"Value", value + valuestep)
	MouseSensitivityChange(id,control)

	SScorer.SetDefault(id,prevcontrol)


def MouseSensitivityFormula(value=-1,sens=-1):
	if (value>=0):
		sens = 1.0
		if (value<=5) :
			sens = 0.2 + (value/6.25)
		else:
			sens = 1+(value-5)*1.6
		return sens

	if (sens>=0):
		value = 1.0
		if (sens<=1) :
			value = (sens-0.2)*6.25
		else:
			value = 5+((sens-1)/1.6)
		return value


def MouseSensitivityChange(id, control):

	Scrap.Set("MouseSensitivityH", MouseSensitivityFormula( value=SScorer.Get(id,"SensitivitySliderX","Value") ) )
	Scrap.Set("MouseSensitivityV", MouseSensitivityFormula( value=SScorer.Get(id,"SensitivitySliderY","Value") ) )

	#print "MouseSensitivityH: ", Scrap.Get("MouseSensitivityH")
	#print "MouseSensitivityV: ", Scrap.Get("MouseSensitivityV")




MultiplayerMenu = ["Net",""]

#######################     Browsing    #######################
# i = 0;import PCMenu;PCMenu.ServersInfo.append('192.168.1.121', 'Unnamed Server', 1, 11, 256, 27960)
# i = i+1;import PCMenu;PCMenu.ServersInfo.append('192.168.1.121', `i`, 1, 11, 256, 27960)
BrowsingActualDomain = "Internet"
BrowserSlots = 13
BrowserSort = "Ping"
BrowserSortOrder = 0


SIBF_DEDICATED   =  1
SIBF_FORCE_SHIP  =  2
SIBF_PASSWORD    =  4


def OnNetBrowse(address,flags,ServerName,NumPlayers,MaxPlayers,GameVersion,LocalSelectedPort,GameType,Ping,MapName):
	global ServersInfo, BrowserSort, BrowserSortOrder

	if flags & SIBF_DEDICATED:
		ServerName = "\x9 "+ServerName
	else:
		ServerName = "  "+ServerName

	if flags & SIBF_PASSWORD:
		ServerName = "\x8 "+ServerName
	else:
		ServerName = "  "+ServerName

	infoblock = (Ping,address,ServerName,NumPlayers,MaxPlayers,GameVersion,LocalSelectedPort,GameType,MapName,flags)

	if BrowserSort == "Name" :
		ServersInfo.append([ServerName,infoblock])
	elif BrowserSort == "Type" :
		ServersInfo.append([GameType,infoblock])
	elif BrowserSort == "Players" :
		ServersInfo.append([`NumPlayers`+"/"+`MaxPlayers`,infoblock])
	elif BrowserSort == "Map" :
		ServersInfo.append([MapName,infoblock])
	else :
		ServersInfo.append([Ping,infoblock])

	ServersInfo.sort()
	if BrowserSortOrder == 1:
		ServersInfo.reverse()

	UpdateBrowseMenu(0)


def BrowserSortExecute():
	global ServersInfo, BrowserSort, BrowserSortOrder

	for t in ServersInfo :
		if BrowserSort == "Name" :
			t[0] = t[1][2]
		elif BrowserSort == "Type" :
			t[0] = t[1][7]
		elif BrowserSort == "Players" :
			t[0] = - t[1][3] #`t[1][3]` + "/" + `t[1][4]`
		elif BrowserSort == "Map" :
			t[0] = t[1][8]
		else :
			t[0] = t[1][0]

	ServersInfo.sort()
	if BrowserSortOrder == 1:
		ServersInfo.reverse()



def BrowseLocalMenu(id,control):
	global ServersInfo,ServerIndex
	import string

	Scrap.Set("DefaultServerPort",Scrap.Def("DefaultServerPort")) # resetearlo porque si
	ServerIndex = 0
	ServersInfo = []
	SNet.InitBrowser()
	Scrap.Set("OnNetBrowseCallback","PCMenu.OnNetBrowse")
	SNet.SendMasterString("ver="+string.split(Scrap.Ver()," ")[0])
	Scrap.Set("MasterCommandFunc","PCMenu.MasterCommand")

def MasterCommand(cadeno):
	if cadeno[0:4] == "msg=":
		import Menu
		global MOTD
		MOTD = cadeno[4:]
		SScorer.Set(0, "MOTD", "Text", cadeno[4:])


def BrowseINetMenu(id,control):
	global ServersInfo,ServerIndex

	ServerIndex = 0
	ServersInfo = []

	SNet.InitBrowser(0,Scrap.Get("MasterServerAddress"))
	if InetMasterBrowse(8):
		Scrap.Set("OnNetBrowseCallback","PCMenu.OnNetBrowse")
	else:
		SNet.DoneBrowser()
		#Menu.VerticalMenu(id,"ERROR : Master not specified.",(
		#				[(Scrap.GetLangStr("Menu_Back"),"PCMenu.JoinMenu"),
		#				 (" ","")]),
		#				"PCMenu.AbortJoin",YStart = Menu.SubMenuYStart)


def InetMasterBrowse(i):
	while i:
		i = i-1
		if SNet.SendMasterString("Brw="+`i*32`+","+`(i+1)*32-1`)==0:
			return 0
	return 1


def BrowserMenuBack(id,control):
	SScorer.SetOnNext(id, "")
	SScorer.SetOnPrev(id, "")
	SNet.DoneBrowser()

	MainMenu(id,control)


def RefreshBrowseMenu(id,control):
	global ServersInfo,ServerIndex, BrowsingActualDomain

	SNet.DoneBrowser()

	if BrowsingActualDomain == "Internet" :
		SNet.PingInetSvrs()
		ServerIndex = 0
		ServersInfo = []

		BrowseINetMenu(id,control)

	elif BrowsingActualDomain == "Local" :

		BrowseLocalMenu(id,control)

	UpdateBrowseMenu(id)


def RefreshBrowseMenuButton(id,control):
	SNet.DoneBrowser()
	RefreshBrowseMenu(id,control)



def BrowseLocalMenuPrevious(id,control):
	global ServersInfo,ServerIndex

	if len(ServersInfo)>ServerIndex+BrowserSlots:
		ServerIndex =	ServerIndex+1
		UpdateBrowseMenu(id)

def BrowseLocalMenuNext(id,control):
	global ServersInfo,ServerIndex

	if 0 < ServerIndex:
		ServerIndex =	ServerIndex-1
		UpdateBrowseMenu(id)

def BrowseLocalMenuPgUp(id,control):
	global ServersInfo,ServerIndex

	leninfo = len(ServersInfo)
	if leninfo<=BrowserSlots:
		ServerIndex = 0
	elif leninfo>ServerIndex+(BrowserSlots*2):
		ServerIndex =	ServerIndex+BrowserSlots
	else:
		ServerIndex =	leninfo-BrowserSlots

	UpdateBrowseMenu(id)

def BrowseLocalMenuPgDown(id,control):
	global ServersInfo,ServerIndex

	if BrowserSlots-1 < ServerIndex:
		ServerIndex =	ServerIndex-BrowserSlots
	else:
		ServerIndex =	0

	UpdateBrowseMenu(id)

def BrowseLocalJoin(id,control):
	global ServersInfo,ServerIndex

	i = int(control[11:])-1+ServerIndex
	if i<len(ServersInfo):
		si = ServersInfo[i][1]

		Scrap.Set("DefaultServerAddress",si[1])

		pyfil = "scripts/net/n"+si[7]+".py"
		if not Scrap.FileExist(pyfil) and not Scrap.FileExist(pyfil+"c"):
			MOTD = si[7]+" modification not supported."
			SScorer.Set(0, "MOTD", "Text", MOTD)
			return


		pyfil = "Levels/"+si[8]+"/Scripts/Map.py"
		if not Scrap.FileExist(pyfil) and not Scrap.FileExist(pyfil+"c"):
			MOTD = si[8]+" map not found."
			SScorer.Set(0, "MOTD", "Text", MOTD)
			return

		Scrap.Set("DefaultServerPort",si[6])

		SNet.DoneBrowser()
		TryJoin(id,control)


def UnicodeParse(text, maxlen):
	#return text[:maxlen]

	le = len(text)
	ntext = min( le, maxlen )

	if ntext<=0 :
		return ""

	j=0
	while j<ntext and j<le:
		if text[j]=="\x1" :
			j = j+4
			ntext = ntext+4
		j=j+1
	if j>le :
		ntext = le
	else :
		ntext = j

	return text[:ntext]



def CreateBrowseMenu(id):

	menulist = ([])

	for i in range(BrowserSlots) :
		menulist.append( ["-",        "PCMenu.BrowseLocalJoin", "BrowserSlot"+`i+1`] )

	Menu.VerticalMenu(id,"",menulist,
	               "PCMenu.BrowserMenuBack",88,VerticalStep = 16,Font="Terminal8Fixed",YStart=129+24)

	# El botón de Refresh
	iname = "Refresh"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_MultiPlayer_Refresh"))
	SScorer.Set(id,iname,"X",320)
	SScorer.Set(id,iname,"Y",384)
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"OnAccept","PCMenu.RefreshBrowseMenuButton")
	SScorer.Set(id,iname,"Red",   183)
	SScorer.Set(id,iname,"Green", 220)
	SScorer.Set(id,iname,"Blue",  255)
	SScorer.Set(id,iname,"Effect", "Shadow");


	# Browse Columns Lines
	Alpha = 64

	iname = "BrowserColumnLine_H"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",78)
	SScorer.Set(id,iname,"Y",139)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",468)
	SScorer.Set(id,iname,"ScaleY",1)
	SScorer.Set(id,iname,"Alpha",Alpha)


	# Browse Columns
	y = 128

	Red = 183
	Green = 220
	Blue = 255

	ScaleY = 240
	Y = 120


	LastX = 76
	X = 252

	iname = "BrowserColumn_Name"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Terminal8Fixed")
	SScorer.Set(id,iname,"Text",UnicodeParse(Scrap.GetLangStr("Menu_MultiPlayer_ServerName"),28))
	SScorer.Set(id,iname,"X",LastX+(X-LastX)/2)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"Red",   Red)
	SScorer.Set(id,iname,"Green", Green)
	SScorer.Set(id,iname,"Blue",  Blue)
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"W", 0)
	SScorer.Set(id,iname,"H", 0)

	iname = "BrowserColumnLine_Name"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",X)
	SScorer.Set(id,iname,"Y",Y)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",1)
	SScorer.Set(id,iname,"ScaleY",ScaleY)
	SScorer.Set(id,iname,"Alpha",Alpha)

	iname = "BrowserColumnBack_Name"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",LastX+2)
	SScorer.Set(id,iname,"Y",Y)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",X-LastX-3)
	SScorer.Set(id,iname,"ScaleY",18)
	SScorer.Set(id,iname,"Alpha",Alpha)
	SScorer.Set(id,iname,"OnAccept","PCMenu.BrowserColumnBack_Click")
	SScorer.Set(id,iname,"W",X-LastX-3)
	SScorer.Set(id,iname,"H",18)



	LastX = X
	X = 342

	iname = "BrowserColumn_Type"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Terminal8Fixed")
	SScorer.Set(id,iname,"Text",UnicodeParse(Scrap.GetLangStr("Menu_MultiPlayer_ServerType"),15))
	SScorer.Set(id,iname,"X",LastX+(X-LastX)/2)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"Red",   Red)
	SScorer.Set(id,iname,"Green", Green)
	SScorer.Set(id,iname,"Blue",  Blue)
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"W", 0)
	SScorer.Set(id,iname,"H", 0)

	iname = "BrowserColumnLine_Type"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",X)
	SScorer.Set(id,iname,"Y",Y)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",1)
	SScorer.Set(id,iname,"ScaleY",ScaleY)
	SScorer.Set(id,iname,"Alpha",Alpha)

	iname = "BrowserColumnBack_Type"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",LastX+2)
	SScorer.Set(id,iname,"Y",Y)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",X-LastX-3)
	SScorer.Set(id,iname,"ScaleY",18)
	SScorer.Set(id,iname,"Alpha",Alpha)
	SScorer.Set(id,iname,"OnAccept","PCMenu.BrowserColumnBack_Click")
	SScorer.Set(id,iname,"W",X-LastX-3)
	SScorer.Set(id,iname,"H",18)



	LastX = X
	X = 390

	iname = "BrowserColumn_Players"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Terminal8Fixed")
	SScorer.Set(id,iname,"Text",UnicodeParse(Scrap.GetLangStr("Menu_MultiPlayer_PlayersNumber"),7))
	SScorer.Set(id,iname,"X",LastX+(X-LastX)/2)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"Red",   Red)
	SScorer.Set(id,iname,"Green", Green)
	SScorer.Set(id,iname,"Blue",  Blue)
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"W", 0)
	SScorer.Set(id,iname,"H", 0)

	iname = "BrowserColumnLine_Players"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",X)
	SScorer.Set(id,iname,"Y",Y)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",1)
	SScorer.Set(id,iname,"ScaleY",ScaleY)
	SScorer.Set(id,iname,"Alpha",Alpha)

	iname = "BrowserColumnBack_Players"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",LastX+2)
	SScorer.Set(id,iname,"Y",Y)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",X-LastX-3)
	SScorer.Set(id,iname,"ScaleY",18)
	SScorer.Set(id,iname,"Alpha",Alpha)
	SScorer.Set(id,iname,"OnAccept","PCMenu.BrowserColumnBack_Click")
	SScorer.Set(id,iname,"W",X-LastX-3)
	SScorer.Set(id,iname,"H",18)



	LastX = X
	X = 510

	iname = "BrowserColumn_Map"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Terminal8Fixed")
	SScorer.Set(id,iname,"Text",UnicodeParse(Scrap.GetLangStr("Menu_MultiPlayer_Map"),19))
	SScorer.Set(id,iname,"X",LastX+(X-LastX)/2)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"Red",   Red)
	SScorer.Set(id,iname,"Green", Green)
	SScorer.Set(id,iname,"Blue",  Blue)
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"W", 0)
	SScorer.Set(id,iname,"H", 0)

	iname = "BrowserColumnLine_Map"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",X)
	SScorer.Set(id,iname,"Y",Y)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",1)
	SScorer.Set(id,iname,"ScaleY",ScaleY)
	SScorer.Set(id,iname,"Alpha",Alpha)

	iname = "BrowserColumnBack_Map"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",LastX+2)
	SScorer.Set(id,iname,"Y",Y)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",X-LastX-3)
	SScorer.Set(id,iname,"ScaleY",18)
	SScorer.Set(id,iname,"Alpha",Alpha)
	SScorer.Set(id,iname,"OnAccept","PCMenu.BrowserColumnBack_Click")
	SScorer.Set(id,iname,"W",X-LastX-3)
	SScorer.Set(id,iname,"H",18)



	LastX = X
	X = 546

	iname = "BrowserColumn_Ping"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Terminal8Fixed")
	SScorer.Set(id,iname,"Text",UnicodeParse(Scrap.GetLangStr("Menu_MultiPlayer_Ping"),6))
	SScorer.Set(id,iname,"X",LastX+(X-LastX)/2)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"Red",   Red)
	SScorer.Set(id,iname,"Green", Green)
	SScorer.Set(id,iname,"Blue",  Blue)
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"W", 0)
	SScorer.Set(id,iname,"H", 0)

	iname = "BrowserColumnLine_Ping"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",X)
	SScorer.Set(id,iname,"Y",Y)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",1)
	SScorer.Set(id,iname,"ScaleY",ScaleY)
	SScorer.Set(id,iname,"Alpha",Alpha)

	iname = "BrowserColumnBack_Ping"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",LastX+2)
	SScorer.Set(id,iname,"Y",Y)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",X-LastX-3)
	SScorer.Set(id,iname,"ScaleY",18)
	SScorer.Set(id,iname,"Alpha",Alpha)
	SScorer.Set(id,iname,"OnAccept","PCMenu.BrowserColumnBack_Click")
	SScorer.Set(id,iname,"W",X-LastX-3)
	SScorer.Set(id,iname,"H",18)



	# Botones
	X = 547
	Y = 120
	name = "BrowserUp"
	SScorer.Add(id, name, "Button")
	SScorer.Set(id, name, "IsMultiSprite", 1)
	SScorer.Set(id, name, "HighRes", 1)
	SScorer.Set(id, name, "File", "2D/Menu/GenericButtons.alpha.tga")
	SScorer.Set(id, name, "SpriteIndex", 3)
	SScorer.Set(id, name, "FocusSpriteIndex", 4)
	SScorer.Set(id, name, "Highlight", 1)
	SScorer.Set(id, name, "X", X)
	SScorer.Set(id, name, "Y", Y)
	SScorer.Set(id, name, "W", 20)
	SScorer.Set(id, name, "H", 20)
	SScorer.Set(id, name, "FocusPivotX",  -2)
	SScorer.Set(id, name, "FocusPivotY",  -2)
	SScorer.Set(id, name, "Complex", 0)
	SScorer.Set(id, name, "Visible", 1)
	SScorer.Set(id, name, "Rotate", 1)
	SScorer.Set(id, name, "OnAccept", "PCMenu.BrowseLocalMenuNext")
	SScorer.Set(id, name, "MultiPress", 1)

	Y = 344
	name = "BrowserDown"
	SScorer.Add(id, name, "Button")
	SScorer.Set(id, name, "IsMultiSprite", 1)
	SScorer.Set(id, name, "HighRes", 1)
	SScorer.Set(id, name, "File", "2D/Menu/GenericButtons.alpha.tga")
	SScorer.Set(id, name, "SpriteIndex", 3)
	SScorer.Set(id, name, "FocusSpriteIndex", 4)
	SScorer.Set(id, name, "Highlight", 1)
	SScorer.Set(id, name, "X", X)
	SScorer.Set(id, name, "Y", Y)
	SScorer.Set(id, name, "W", 20)
	SScorer.Set(id, name, "H", 20)
	SScorer.Set(id, name, "FocusPivotX",  -2)
	SScorer.Set(id, name, "FocusPivotY",  -2)
	SScorer.Set(id, name, "Complex", 0)
	SScorer.Set(id, name, "Visible", 1)
	SScorer.Set(id, name, "Rotate", 1)
	SScorer.Set(id, name, "Mirror", 1)
	SScorer.Set(id, name, "OnAccept", "PCMenu.BrowseLocalMenuPrevious")
	SScorer.Set(id, name, "MultiPress", 1)

	Menu.LinkUD(id, "BrowserUp","BrowserDown")

	Menu.LinkLR(id, "BrowserSlot1","BrowserUp")
	Menu.LinkLR(id, "BrowserSlot1","BrowserDown")

	X = 549
	YMin = 136
	YSize = 208

	iname = "BrowserSlider"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",X+1)
	SScorer.Set(id,iname,"Y",YMin)
	SScorer.Set(id,iname,"W",0)
	SScorer.Set(id,iname,"H",0)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",11)
	SScorer.Set(id,iname,"ScaleY",YSize)
	SScorer.Set(id,iname,"Alpha",92)
	SScorer.Set(id,iname,"Red",192)
	SScorer.Set(id,iname,"Green",192)
	SScorer.Set(id,iname,"Blue",255)

	iname = "BrowserSliderArea"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",X)
	SScorer.Set(id,iname,"Y",YMin)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",13)
	SScorer.Set(id,iname,"ScaleY",YSize)
	SScorer.Set(id,iname,"W",20)
	SScorer.Set(id,iname,"H",YSize)
	SScorer.Set(id,iname,"FocusPivotX",-3)
	SScorer.Set(id,iname,"FocusPivotY",0)
	SScorer.Set(id,iname,"Alpha",24)
	SScorer.Set(id,iname,"OnGainFocus", "PCMenu.BrowserSliderGainFocus")
	SScorer.Set(id,iname,"OnLooseFocus", "PCMenu.BrowserSliderLooseFocus")


	name = "BrowseTab"
	SScorer.Add(id,name,"Tab")
	Menu.SetTabDefaults(id,name)
	SScorer.Set(id,name,"X", 72 )
	SScorer.Set(id,name,"Y", 114 )
	SScorer.Set(id,name,"SizeX", 496)
	SScorer.Set(id,name,"SizeY", 252)
	SScorer.Set(id,name,"Type", 4)
	SScorer.Set(id,name,"Alpha",  92)
	SScorer.Set(id,name,"Red",   32)
	SScorer.Set(id,name,"Green", 255)
	SScorer.Set(id,name,"Blue",  255)


	#SScorer.SetOnNext(id, "PCMenu.BrowseLocalMenuPgUp")
	#SScorer.SetOnPrev(id, "PCMenu.BrowseLocalMenuPgDown")


def BrowserColumnBack_Click(id,control):
	global BrowserSort, BrowserSortOrder

	iname = "BrowserColumnBack_" + BrowserSort
	SScorer.Set(id,iname,"Red",   255)
	SScorer.Set(id,iname,"Green", 255)
	SScorer.Set(id,iname,"Blue",  255)
	SScorer.Set(id,iname,"Alpha", 64)

	NewBrowserSort = control[18:]
	if BrowserSort == NewBrowserSort :
		if BrowserSortOrder == 0:
			BrowserSortOrder = 1
		else :
			BrowserSortOrder = 0
	else :
		BrowserSortOrder = 0

	BrowserSort = NewBrowserSort

	iname = "BrowserColumnBack_" + NewBrowserSort
	SScorer.Set(id,iname,"Red",   255)
	SScorer.Set(id,iname,"Green", 255)
	SScorer.Set(id,iname,"Blue",  192)
	SScorer.Set(id,iname,"Alpha", 128)

	BrowserSortExecute()

	UpdateBrowseMenu(id)



def BrowserSliderGainFocus(id,prevcontrol,control):
	iname = "BrowserSliderArea"
	SScorer.Set(id,iname,"OnRender","PCMenu.BrowserSliderOnRender")

def BrowserSliderLooseFocus(id,prevcontrol,control):
	iname = "BrowserSliderArea"
	SScorer.Set(id,iname,"OnRender","")

def BrowserSliderOnRender(id,control):
	global ServersInfo,ServerIndex
	nserv = len(ServersInfo)

	if not SScorer.GetMenuAccept(id):
		return

	if nserv<=BrowserSlots:
		return

	YMin = 136
	YSize = 208

	ycursor = SScorer.Get(id,"Cursor","Y")

	yp = ycursor - YMin - 5

	if yp < 0 :
		yp = 0

	if yp > YSize-10 :
		yp = YSize-10
	phase = (yp/(YSize-10))

	aServerIndex = ServerIndex
	ServerIndex = int(float((nserv-BrowserSlots)+1) * phase)
	if ServerIndex>=nserv-BrowserSlots :
		ServerIndex = nserv-BrowserSlots

	if aServerIndex != ServerIndex:
		UpdateBrowseMenu(id)


def UpdateBrowseSlider(id):
	global ServersInfo,ServerIndex
	nserv = len(ServersInfo)

	YMin = 136
	YSize = 208

	if nserv <= BrowserSlots :
		iname = "BrowserSlider"
		SScorer.Set(id,iname,"Y",YMin)
		SScorer.Set(id,iname,"ScaleY",YSize)
	else :
		YStep = YSize / float((nserv - BrowserSlots)+1)
		YStepSize = YStep

		if YStepSize < 10 :
			YStepSize = 10
			YCor = YStepSize - YStep
			YStep = (YSize-YCor) / float((nserv - BrowserSlots)+1)

		iname = "BrowserSlider"
		SScorer.Set(id,iname,"Y",YMin + ServerIndex*YStep)
		SScorer.Set(id,iname,"ScaleY",YStepSize)


def UpdateBrowseMenu(id):
	global ServersInfo,ServerIndex
	nserv = len(ServersInfo)

	icount = 0
	for i in range(BrowserSlots):
		SvrName = ""

		if nserv > i+ServerIndex:
			SvrInf = ServersInfo[i+ServerIndex][1]
			SvrName = BrowseFormatServerLine(SvrInf)

		name = "BrowserSlot" + `i+1`
		SScorer.Set(id,name,"Text",SvrName)
		SScorer.Set(id,name,"W",460)

		SScorer.Set(id,name,"Up","BrowserSlot" + `i`)
		SScorer.Set(id,name,"Down","BrowserSlot" + `i+2`)
		SScorer.Set(id,name,"Right","BrowserUp")

		if SvrName :
			icount = icount + 1
			SScorer.Set(id,name,"Visible",1)
		else :
			SScorer.Set(id,name,"Visible",0)

	if icount <=0 :

		name = "Refresh"
		if BrowsingActualDomain == "Internet" :
			Menu.LinkUD(id,"JoinInternet",name)
		elif BrowsingActualDomain == "Local" :
			Menu.LinkUD(id,"JoinLocal",name)

	else :

		name = "BrowserSlot1"

		if BrowsingActualDomain == "Internet" :
			Menu.LinkUD(id,"JoinInternet",name)
		elif BrowsingActualDomain == "Local" :
			Menu.LinkUD(id,"JoinLocal",name)

		name = "BrowserSlot" + `icount`
		Menu.LinkUD(id,name,"Refresh")

	UpdateBrowseSlider(id)


def BrowseFormatServerLine(SvrInf):
	import string

	name = string.ljust(SvrInf[2], 28)[:28]

	#text = Scrap.GetLangStr("Net_Type_"+SvrInf[7])
	#if not text :
	text = SvrInf[7]

	if SvrInf[9] & SIBF_FORCE_SHIP:
		text = "\xB "+text
	else:
		text = "\xA "+text

	mod = string.ljust(text, 14)[:14]

	ping = string.rjust(`SvrInf[0]`, 4)[:4]

	players = string.rjust("("+`SvrInf[3]`+ "/"+`SvrInf[4]`+")",7)[:7]

	#text = Scrap.GetLangStr("Station_"+SvrInf[8])
	#if not text :
	text = SvrInf[8]
	mapname = string.ljust(text,19)[:19]

	SvrLine	= name + " " + mod + " " + players + " " + mapname + " " + ping

	return SvrLine


#####################################################################


def MultiPlayerMenu(id, control):
	"Menu multiplayer"

	import Init
	global MultiplayerMenu

	Menu.StartNewMenu(id)

	if (Init.inMainMenu or Init.isShipEdit):

		NetJoinGameMenu(id, control)

	else:
		Opts =		[
				[Scrap.GetLangStr("Menu_ReturnToGame"),"Menu.BackToGame"],
				MultiplayerMenu,
				[Scrap.GetLangStr("Menu_Multiplayer_ShipMenu"),"ShipEdit.EnterEditShipMenu"],
				[Scrap.GetLangStr("Menu_Options"),"Menu.OptionsMenu"],
				[Scrap.GetLangStr("Menu_AbortGame"),"PCMenu.AbortMultiplayerGame"]
				]

		if SNet.IsServer():
			Opts.insert(2,[Scrap.GetLangStr("Net_Menu_Restart_Svr"),"PCMenu.MenuRestartServer"])

		# Vengo desde una partida en curso
		Menu.VerticalMenu(id,"Multiplayer",Opts,"Menu.BackToGame", YStart = Menu.OptionMenuYStart)

		if MultiplayerMenu[1]=="":
			Menu.DisableMenuItem(id, 2, 5)
		Menu.fromMultiPlayer = 1
		Menu.DrawBackOptionMenu(id)



def MenuRestartServer(id,control):
	import Init
	if Scrap.GetTime() > 15:
		SNet.ServerChangeLevel(Init.Path)


def MenuInitServer(id,control):
	import Net

	ServerMapList = eval(Scrap.Get("ServerMapList"))
	if len(ServerMapList)<=0 :
		ServerMapList = Net.ModesMap[Scrap.Get("ServerType")]
		Scrap.Set("ServerMapList", `ServerMapList`)
		UpdateMapList(id)

	mapname = ServerMapList[0]
	SNet.InitServer("Levels/"+mapname,Scrap.Get("DefaultMaxPlayersOnServer"),0)


def MenuJoinGame(id,control):
	import string
	SNet.CloseClient()
	cadeno = string.splitfields(SScorer.Get(id,"Item1","Text"),":")
	Scrap.Set("DefaultServerAddress",cadeno[0])
	if len(cadeno)>1:
		Scrap.Set("DefaultServerPort",int(cadeno[1]))
	else:
		Scrap.Set("DefaultServerPort",Scrap.Def("DefaultServerPort"))

	TryJoin(id,control)

def TryJoin	(id,control):
	andres = Scrap.Get("DefaultServerAddress")
	oporto = Scrap.Get("DefaultServerPort")
	SNet.InitClient(andres,oporto)
	Menu.StartNewMenu(id)

	joinaddress = andres+":"+`oporto`
	Menu.VerticalMenu(id, Scrap.GetLangStr("Net_Menu_Connecting")%joinaddress ,(
					[(Scrap.GetLangStr("Menu_Multiplayer_JoinGame_Abort"),"PCMenu.AbortJoin"),
					 (" ","")]),
					"PCMenu.AbortJoin",YStart = Menu.SubMenuYStart)

	Menu.DrawBackSubMenu(id)
	ShowConectionStatus()


def JoinPassword(id,control):
	Scrap.Set("ClientPassword",SScorer.Get(id,"Item1","Text",))
	TryJoin(id,control)

def AskPassword	(id,control):

	Password  = Scrap.GetLangStr("Menu_Multiplayer_Advanced_Password" )
	if Password  == "":
		Password  = "Password"

	Menu.StartNewMenu(id)

	Menu.VerticalMenu(id,Password,(
	                (Scrap.Get("ClientPassword"),"!EditText"),
	                (Scrap.GetLangStr("Menu_Multiplayer_JoinGame"),"PCMenu.JoinPassword"),
	                (Scrap.GetLangStr("Menu_Multiplayer_JoinGame_Abort"),"PCMenu.AbortJoin")),
	                "PCMenu.AbortJoin",Font="Horatio",VerticalStep=45,YStart=Menu.SubMenuYStart)

	SScorer.Set(id,"Item1","Font","Horatio")
	SScorer.Set(id,"Item1","MaxInput",20)
	SScorer.Set(id,"Item1","X",320-240)

	SScorer.Set(id,"Item2","Y",SScorer.Get(id,"Item1","Y")+35)
	SScorer.Set(id,"Item2","X",320-100)

	SScorer.Set(id,"Item3","Y",SScorer.Get(id,"Item1","Y")+35)
	SScorer.Set(id,"Item3","X",320+140)

	Menu.LinkLR(id,"Item2","Item3")
	Menu.LinkLR(id,"Item3","Item2")

	Menu.DrawBackSubMenu(id)


def	ShowConectionStatus():
	import Menu

	LastTitle = SScorer.Get(0,"Title","Text")

	ccs = Scrap.Get("ClientConectionStatus")
	if ccs == "server_is_not_responding":
		SScorer.Set(0,"Title","Text", Scrap.GetLangStr("Net_Menu_ServerDown") )
	elif ccs == "need_password":
		SNet.CloseClient()
		AskPassword(0,"")
		return
	elif ccs == "server_is_full":
		SScorer.Set(0,"Title","Text", Scrap.GetLangStr("Net_Menu_ServerFull") )
		SNet.CloseClient()
		Scrap.AddScheduledFunc(Scrap.GetTime(),Scrap.DeleteScheduledFuncs,("ConectionStatus",),"DeleteConectionStatus")

		SScorer.Set(0,"Item1","Text",Scrap.GetLangStr("Menu_Multiplayer_JoinGame_Retry"))
		SScorer.Set(0,"Item1","X",320)
		y = SScorer.Get(0,"Item1","Y")
		SScorer.Set(0,"Item1","CentralText",1)
		SScorer.Set(0,"Item1","OnAccept","PCMenu.TryJoin")
		SScorer.Set(0,"Item1","Y",y)

		SScorer.Set(0,"Item2","Text",Scrap.GetLangStr("Menu_Multiplayer_JoinGame_Abort"))
		SScorer.Set(0,"Item2","X",320)
		y = SScorer.Get(0,"Item2","Y")
		SScorer.Set(0,"Item2","CentralText",1)
		SScorer.Set(0,"Item2","OnAccept","PCMenu.AbortJoin")
		SScorer.Set(0,"Item2","Y",y)

	YBar = SScorer.Get(0,"TitleBarM", "Y")
	Title = SScorer.Get(0,"Title","Text")

	if LastTitle != Title :
		Menu.DrawMenuTitleBar(0, YBar, Title)

	Scrap.AddScheduledFunc(Scrap.GetTime()+0.25,ShowConectionStatus,(),"ConectionStatus")


def AbortJoin(id,control):
	Scrap.DeleteScheduledFuncs("ConectionStatus")
	SNet.CloseClient()
	NetJoinGameMenu(id,control)

def SpecifyIPMenu(id,control):

	Menu.VerticalMenu(id,"",(
	                [Scrap.Get("DefaultServerAddress"),"!EditText"],
	                [Scrap.GetLangStr("Menu_Multiplayer_JoinGame"),"PCMenu.MenuJoinGame"]),
	                "",Font="Horatio",VerticalStep=45,YStart=140)

	SScorer.Set(id,"Item1","Font","Horatio")
	SScorer.Set(id,"Item1","MaxInput",21)
	SScorer.Set(id,"Item1","X",320-164)

	SScorer.Set(id,"Item2","Y",SScorer.Get(id,"Item1","Y")+35)


def AbortMultiplayerGame(id, control):
	"Aborta una partida multiplayer"

	Menu.YesNoMenu(id,Scrap.GetLangStr("Menu_AbortGame_Question"),"Menu.AuxAbortGame","PCMenu.MultiPlayerMenu")



############
# Net Menu #
############

MapSlots = 9
MapIndex = 0

def NetDefaultContentMenu(id, control, AcTab = "Create"):
	import Init,Scorer

	# El botón de Back
	iname = "Back"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","ScrapBig")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Back"))
	SScorer.Set(id,iname,"X",320)
	SScorer.Set(id,iname,"Y",Menu.BackButtonYStart)
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"OnAccept","Menu.MainMenu")
	SScorer.Set(id,iname,"Red",   183)
	SScorer.Set(id,iname,"Green", 220)
	SScorer.Set(id,iname,"Blue",  255)
	SScorer.Set(id,iname,"Effect", "Shadow");

	# El botón de Garaje
	iname = "Garaje"
	text = Scrap.GetLangStr("Menu_Multiplayer_ShipMenu")
	textWidth, textHeight = SScorer.GetTextArea("ScrapMedium", text)
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","ScrapMedium")
	SScorer.Set(id,iname,"Text",text)
	SScorer.Set(id,iname,"X",504)
	SScorer.Set(id,iname,"Y",47)
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"OnAccept","ShipEdit.EnterEditShipMenu")
	SScorer.Set(id,iname,"Red",   183)
	SScorer.Set(id,iname,"Green", 220)
	SScorer.Set(id,iname,"Blue",  255)
	SScorer.Set(id,iname,"Effect", "Shadow")

	name = "GarajeButtonTab"
	SScorer.Add(id,name,"Tab")
	Menu.SetTabDefaults(id,name)
	SScorer.Set(id,name,"X", 432 )
	SScorer.Set(id,name,"Y", 32 )
	SScorer.Set(id,name,"SizeX", 150)
	SScorer.Set(id,name,"SizeY", 36)
	SScorer.Set(id,name,"TabInit",0)
	SScorer.Set(id,name,"TabEnd", 0)
	SScorer.Set(id,name,"TabMax", 0)
	SScorer.Set(id,name,"SizeTabQuad", 0)
	SScorer.Set(id,name,"Type", 0)
	SScorer.Set(id,name,"Alpha",  128)
	SScorer.Set(id,name,"Red",   255)
	SScorer.Set(id,name,"Green", 241)
	SScorer.Set(id,name,"Blue",  174)


	SScorer.SetDefault(id,"Back")

	Menu.AddTabs(id,(
	                ["Create",     	"PCMenu.NetCreateGameMenu", Scrap.GetLangStr("Menu_Multiplayer_CreateGame")],
	                ["Join",   	"PCMenu.NetJoinGameMenu", Scrap.GetLangStr("Menu_Multiplayer_JoinGame")]
	                #["Garaje",   	"ShipEdit.EnterEditShipMenu", Scrap.GetLangStr("Menu_Multiplayer_ShipMenu")]
	            ),AcTab, ParamTabSize = 26, Hint = 0)

	Menu.LinkLR(id,"Join","Garaje")
	Menu.LinkLR(id,"Garaje","Create")

	SScorer.SetDefault(id,AcTab)

	# Message Of The Day
	txt = MOTD
	objName = "MOTD"
	SScorer.Add(id, objName, "Text")
	SScorer.Set(id, objName, "Text", txt)
	SScorer.Set(id, objName, "X", Scorer.MarginH + 5)
	SScorer.Set(id, objName, "Y", 480 - Scorer.MarginV - 20)
	SScorer.Set(id, objName, "Font", "HoratioSmall")
	SScorer.Set(id, objName, "Effect", "Shadow")
	SScorer.Set(id, objName, "Align", "Left")
	SScorer.Set(id, objName, "Red",   183)
	SScorer.Set(id, objName, "Green", 220)
	SScorer.Set(id, objName, "Blue",  255)
	SScorer.Set(id, objName, "Alpha", 255)
	SScorer.Set(id, objName, "Visible", 1)

	Menu.DrawCircuitMenu(id)



def NetCreateGameMenu(id, control):
	import Net, Menu

	global MapIndex
	MapIndex = 0

	SNet.DoneBrowser()

	ServerType = Scrap.Get("ServerType")
	bServerTypeOK = 0
	for t in Net.Modes:
		if t == ServerType:
			bServerTypeOK = 1
	if not bServerTypeOK :
		Scrap.Set("ServerType", Net.Modes[0])


	ColorTitle = 143, 180, 215
	ColorOption = 183, 220, 255

	Menu.StartNewMenu(id)


	x = 74
	y = 80

	stepy = 36


	# Server Name
	title = Scrap.GetLangStr("Menu_MultiPlayer_ServerName") + ":"

	iname = "ServerNameTitle"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",title)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")

	textWidth, textHeight = SScorer.GetTextArea("Horatio", title)

	Scrap.Get("ServerName")
	iname = "ServerName"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.Get("ServerName"))
	SScorer.Set(id,iname,"X",x+textWidth+10)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"OnAccept", "!EditText")
	SScorer.Set(id,iname,"MaxInput", 18)
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnGainFocus", "PCMenu.ServerNameGainFocus")
	SScorer.Set(id,iname,"OnLooseFocus", "PCMenu.ServerNameLooseFocus")
	SScorer.Set(id,iname,"OnRender", "")


	y = y + stepy

	# Server Type
	title = Scrap.GetLangStr("Menu_MultiPlayer_ServerType") + ":"

	iname = "ServerTypeTitle"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",title)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")

	textWidth, textHeight = SScorer.GetTextArea("Horatio", title)

	text = Scrap.GetLangStr("Net_Type_TeamFlag")
	iname = "ServerType"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",text)
	SScorer.Set(id,iname,"X",x+textWidth+10+140)
	SScorer.Set(id,iname,"Y",y+12)
	SScorer.Set(id,iname,"Align","Center")
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")

	iname = "ServerType"
	Menu.PreviousNextMenuSimple(0, iname, x+textWidth+10,y+12,280)
	SScorer.Set(id, iname+"Prev", "OnAccept", "PCMenu.ServerTypePrev")
	SScorer.Set(id, iname+"Next", "OnAccept", "PCMenu.ServerTypeNext")


	iname = "ServerTypeInfoDummy"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"X",x+textWidth+42)
	SScorer.Set(id,iname,"Y",y-2)
	SScorer.Set(id,iname,"W",216)
	SScorer.Set(id,iname,"H",28)
	SScorer.Set(id,iname,"OnAccept", "PCMenu.ServerTypeInfo")


	iname = "ServerTypeInfo"
	SScorer.Add(id,iname, "Text")
	SScorer.Set(id,iname, "Font","ScrapMedium")
	SScorer.Set(id,iname, "Text","i")
	SScorer.Set(id,iname, "X", x+textWidth+310+6)
	SScorer.Set(id,iname, "Y", y-1)
	SScorer.Set(id,iname, "W", 25)
	SScorer.Set(id,iname, "H", 25)
	SScorer.Set(id,iname, "Center", 1)
	SScorer.Set(id,iname, "Visible", 1)
	SScorer.Set(id,iname, "Effect", "Outline")
	SScorer.Set(id,iname, "FocusPivotX", -10)
	SScorer.Set(id,iname, "FocusPivotY", 1)
	SScorer.Set(id,iname, "Red",   165)
	SScorer.Set(id,iname, "Green", 192)
	SScorer.Set(id,iname, "Blue",  255)
	SScorer.Set(id,iname, "OnAccept", "PCMenu.ServerTypeInfo")

	iname = "ServerTypeInfoBack"
	SScorer.Add(id,iname, "Sprite")
	SScorer.Set(id,iname, "IsMultiSprite", 1)
	SScorer.Set(id,iname, "HighRes", 1)
	SScorer.Set(id,iname, "File", "2D/ShipEditor/Buttons.alpha.tga")
	SScorer.Set(id,iname, "SpriteIndex", 1)
	SScorer.Set(id,iname, "X", x+textWidth+310-9)
	SScorer.Set(id,iname, "Y", y-8+4)



	y = y + stepy


	# Players Number
	title = Scrap.GetLangStr("Menu_MultiPlayer_PlayersNumber") + ":"

	iname = "PlayersNumberTitle"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",title)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")

	textWidth, textHeight = SScorer.GetTextArea("Horatio", title)

	x = x + textWidth+10

	text = `Scrap.Get("DefaultMaxPlayersOnServer")+1`
	iname = "PlayersNumber"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"IsNumeric", 1)
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",text)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"OnAccept", "!EditText")
	SScorer.Set(id,iname,"MaxInput", 2)
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnGainFocus", "PCMenu.PlayersNumberGainFocus")
	SScorer.Set(id,iname,"OnLooseFocus", "PCMenu.PlayersNumberLooseFocus")
	SScorer.Set(id,iname,"OnRender", "")

	textWidth, textHeight = SScorer.GetTextArea("Horatio", text)

	x = x + textWidth + 40


	# FragLimit
	title = "-" + ":"

	iname = "FragLimitTitle"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",title)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")

	textWidth, textHeight = SScorer.GetTextArea("Horatio", title)

	x = x + textWidth+10

	text = `Scrap.Get("FragLimit")`
	iname = "FragLimit"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"IsNumeric", 1)
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",text)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"OnAccept", "!EditText")
	SScorer.Set(id,iname,"MaxInput", 2)
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnGainFocus", "PCMenu.FragLimitGainFocus")
	SScorer.Set(id,iname,"OnLooseFocus", "PCMenu.FragLimitLooseFocus")
	SScorer.Set(id,iname,"OnRender", "")


	# MapList

	x = 72
	y = 192

	for i in range(MapSlots):

		iname = "MapSlotBack" + `i+1`
		SScorer.Add(id,iname,"Sprite")
		SScorer.Set(id,iname,"Unit",1)
		SScorer.Set(id,iname,"X",x + 8)
		SScorer.Set(id,iname,"Y",y + 7 + i*17)
		SScorer.Set(id,iname,"ScaleX",  230)
		SScorer.Set(id,iname,"ScaleY",  16)
		SScorer.Set(id,iname,"Red",   255)
		SScorer.Set(id,iname,"Green", 255)
		SScorer.Set(id,iname,"Blue",  222)
		SScorer.Set(id,iname,"Alpha", 32)
		SScorer.Set(id,iname,"Visible", 0)

		iname = "MapSlot" + `i+1`
		SScorer.Add(id,iname,"Text")
		SScorer.Set(id,iname,"Font","HoratioSmall")
		SScorer.Set(id,iname,"Text","XXXXX")
		SScorer.Set(id,iname,"X",x + 8)
		SScorer.Set(id,iname,"Y",y + 5 + i*17)
		SScorer.Set(id,iname,"Red",   183)
		SScorer.Set(id,iname,"Green", 220)
		SScorer.Set(id,iname,"Blue",  255)
		SScorer.Set(id,iname,"W",  230)
		SScorer.Set(id,iname,"H",  22)
		SScorer.Set(id,iname,"Up",  "MapSlot" + `i+0`)
		SScorer.Set(id,iname,"Down",  "MapSlot" + `i+2`)
		SScorer.Set(id,iname,"Right",  "MapUp")


	# Botones UpDown/Slider
	X = x + 244
	Y = 198
	name = "MapUp"
	SScorer.Add(id, name, "Button")
	SScorer.Set(id, name, "IsMultiSprite", 1)
	SScorer.Set(id, name, "HighRes", 1)
	SScorer.Set(id, name, "File", "2D/Menu/GenericButtons.alpha.tga")
	SScorer.Set(id, name, "SpriteIndex", 3)
	SScorer.Set(id, name, "FocusSpriteIndex", 4)
	SScorer.Set(id, name, "Highlight", 1)
	SScorer.Set(id, name, "X", X)
	SScorer.Set(id, name, "Y", Y)
	SScorer.Set(id, name, "W", 20)
	SScorer.Set(id, name, "H", 20)
	SScorer.Set(id, name, "FocusPivotX",  -2)
	SScorer.Set(id, name, "FocusPivotY",  -2)
	SScorer.Set(id, name, "Complex", 0)
	SScorer.Set(id, name, "Visible", 1)
	SScorer.Set(id, name, "Rotate", 1)
	SScorer.Set(id, name, "OnAccept", "PCMenu.MapDown")
	SScorer.Set(id, name, "MultiPress", 1)

	Y = 338
	name = "MapDown"
	SScorer.Add(id, name, "Button")
	SScorer.Set(id, name, "IsMultiSprite", 1)
	SScorer.Set(id, name, "HighRes", 1)
	SScorer.Set(id, name, "File", "2D/Menu/GenericButtons.alpha.tga")
	SScorer.Set(id, name, "SpriteIndex", 3)
	SScorer.Set(id, name, "FocusSpriteIndex", 4)
	SScorer.Set(id, name, "Highlight", 1)
	SScorer.Set(id, name, "X", X)
	SScorer.Set(id, name, "Y", Y)
	SScorer.Set(id, name, "W", 20)
	SScorer.Set(id, name, "H", 20)
	SScorer.Set(id, name, "FocusPivotX",  -2)
	SScorer.Set(id, name, "FocusPivotY",  -2)
	SScorer.Set(id, name, "Complex", 0)
	SScorer.Set(id, name, "Visible", 1)
	SScorer.Set(id, name, "Rotate", 1)
	SScorer.Set(id, name, "Mirror", 1)
	SScorer.Set(id, name, "OnAccept", "PCMenu.MapUp")
	SScorer.Set(id, name, "MultiPress", 1)

	Menu.LinkLR(id,"MapSlot1","MapDown")
	Menu.LinkLR(id,"MapSlot1","MapUp")

	Menu.LinkUD(id,"FragLimit","MapUp")
	Menu.LinkUD(id,"MapUp","MapDown")
	Menu.LinkUD(id,"MapDown","CreateButton")

	X = x + 246
	YMin = 214
	YSize = 124

	iname = "MapSlider"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",X+1)
	SScorer.Set(id,iname,"Y",YMin)
	SScorer.Set(id,iname,"W",0)
	SScorer.Set(id,iname,"H",0)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",11)
	SScorer.Set(id,iname,"ScaleY",YSize)
	SScorer.Set(id,iname,"Alpha",92)
	SScorer.Set(id,iname,"Red",192)
	SScorer.Set(id,iname,"Green",192)
	SScorer.Set(id,iname,"Blue",255)

	iname = "MapSliderArea"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",X)
	SScorer.Set(id,iname,"Y",YMin)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",13)
	SScorer.Set(id,iname,"ScaleY",YSize)
	SScorer.Set(id,iname,"W",20)
	SScorer.Set(id,iname,"H",YSize)
	SScorer.Set(id,iname,"FocusPivotX",-3)
	SScorer.Set(id,iname,"FocusPivotY",0)
	SScorer.Set(id,iname,"Alpha",24)
	SScorer.Set(id,iname,"OnGainFocus", "PCMenu.MapSliderGainFocus")
	SScorer.Set(id,iname,"OnLooseFocus", "PCMenu.MapSliderLooseFocus")


	iname = "MapColumn_Line"
	SScorer.Add(id,iname,"Sprite")
	SScorer.Set(id,iname,"X",X - 4)
	SScorer.Set(id,iname,"Y",y + 8)
	SScorer.Set(id,iname,"Unit",1)
	SScorer.Set(id,iname,"ScaleX",1)
	SScorer.Set(id,iname,"ScaleY",152)
	SScorer.Set(id,iname,"Alpha",64)


	name = "MapListTab"
	SScorer.Add(id,name,"Tab")
	Menu.SetTabDefaults(id,name)
	SScorer.Set(id,name,"X", x )
	SScorer.Set(id,name,"Y", y )
	SScorer.Set(id,name,"SizeX", 266)
	SScorer.Set(id,name,"SizeY", 168)
	SScorer.Set(id,name,"Type", 4)
	SScorer.Set(id,name,"Alpha",  32)
	SScorer.Set(id,name,"Red",   32)
	SScorer.Set(id,name,"Green", 255)
	SScorer.Set(id,name,"Blue",  255)


	# Map Preview
	x = 344

	name = "MapPreviewTab"
	SScorer.Add(id,name,"Tab")
	Menu.SetTabDefaults(id,name)
	SScorer.Set(id,name,"X", x )
	SScorer.Set(id,name,"Y", y )
	SScorer.Set(id,name,"SizeX", 224)
	SScorer.Set(id,name,"SizeY", 168)
	SScorer.Set(id,name,"Type", 4)
	SScorer.Set(id,name,"Alpha",  1)
	SScorer.Set(id,name,"Red",   32)
	SScorer.Set(id,name,"Green", 255)
	SScorer.Set(id,name,"Blue",  255)

	for j in Net.NetMaps:
		name = "MapPreviewSlot_" + j
		SScorer.Add(id,name,"Sprite")
		SScorer.Set(id,name,"X", x )
		SScorer.Set(id,name,"Y", y )
		SScorer.Set(id,name,"File", "Levels/"+j+"/2D/MapPreview.alpha.tga" )
		SScorer.Set(id,name,"Visible", 0 )
		SScorer.Set(id,name,"Alpha", 0 )


	# El botón de Crear partida
	iname = "CreateButton"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Multiplayer_CreateGame"))
	SScorer.Set(id,iname,"X",320)
	SScorer.Set(id,iname,"Y",384)
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"OnAccept","PCMenu.MenuInitServer")
	SScorer.Set(id,iname,"Red",   183)
	SScorer.Set(id,iname,"Green", 220)
	SScorer.Set(id,iname,"Blue",  255)
	SScorer.Set(id,iname,"Effect", "Shadow")

	Advanced  = Scrap.GetLangStr("Menu_Multiplayer_Advanced" )
	if Advanced  == "":
		Advanced  = "Advanced"

	# El botón de avanzado
	iname = "AdvancedButton"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Advanced)
	SScorer.Set(id,iname,"Y",384)
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",100)
	SScorer.Set(id,iname,"OnAccept","PCMenu.AdvancedServer")
	SScorer.Set(id,iname,"Red",   183)
	SScorer.Set(id,iname,"Green", 220)
	SScorer.Set(id,iname,"Blue",  255)
	SScorer.Set(id,iname,"Effect", "Shadow")


	# Actualize el tipo de servidor actual (ojo , esto fuerza la actualización de los mapas tambien)
	UpdateServerType(id)


	NetDefaultContentMenu(id, control, "Create")

	Menu.LinkUD(id,"Create","ServerName")

	Menu.LinkLR(id,"ServerTypeNext","ServerTypeInfo")
	Menu.LinkUD(id,"ServerName","ServerTypeInfo")
	Menu.LinkUD(id,"ServerTypeInfo","FragLimit")

	Menu.LinkUD(id,"ServerName","ServerTypeNext")
	Menu.LinkUD(id,"ServerName","ServerTypePrev")

	Menu.LinkLR(id,"ServerTypePrev","ServerTypeNext")
	Menu.LinkUD(id,"ServerTypePrev","PlayersNumber")

	Menu.LinkUD(id,"ServerTypeNext","FragLimit")

	Menu.LinkLR(id,"PlayersNumber","FragLimit")

	Menu.LinkUD(id,"FragLimit","MapSlot1")
	Menu.LinkUD(id,"PlayersNumber","MapSlot1")

	Menu.LinkUD(id,"CreateButton","Back")
	Menu.LinkUD(id,"Back","Create")

	Menu.LinkLR(id,"AdvancedButton","CreateButton")
	Menu.LinkLR(id,"CreateButton","AdvancedButton")

	SScorer.SetOnNext(id, "PCMenu.NetJoinGameMenu")
	SScorer.SetOnPrev(id, "PCMenu.NetJoinGameMenu")

	SScorer.SetOnCancel(id, "Menu.MainMenu")

	SScorer.SetDefault(id,"Create")


def AdvancedServer(id,control):

	Menu.StartNewMenu(id)

	Password  = Scrap.GetLangStr("Menu_Multiplayer_Advanced_Password" )
	if Password  == "":
		Password  = "Password"

	Force  = Scrap.GetLangStr("Menu_Multiplayer_Advanced_Force" )
	if Force  == "":
		Force  = "Force server vehicle"

	Advanced_Options  = Scrap.GetLangStr("Menu_Multiplayer_Advanced_Options" )
	if Advanced_Options  == "":
		Advanced_Options  = "Advanced Options"

	Dedicated  = Scrap.GetLangStr("Menu_Multiplayer_Advanced_Dedicated" )
	if Dedicated  == "":
		Dedicated  = "Run Dedicated Server"


	if Scrap.Get("UseServerPassword"):
		pasuse = "\x2 "+Password+":"
	else:
		pasuse = "\x3 "+Password

	if Scrap.Get("ForceServerVehicle"):
		fsvd = "\x2 "+Force
	else:
		fsvd = "\x3 "+Force


	Menu.VerticalMenu(id,Advanced_Options,(
	                (pasuse,"PCMenu.SwitchUsePass"),
	                (Scrap.Get("ServerPassword"),"!EditText"),
	                (fsvd,"PCMenu.SwitchForceVehicle"),
	                (GetDataRateText(),"PCMenu.SetDataRate"),
#	                (Dedicated,"PCMenu.RunDedicatedServer"),
	                (Scrap.GetLangStr("Menu_Back"),"PCMenu.BackToCreateServer")),
	                "PCMenu.BackToCreateServer",Font="Horatio",VerticalStep=45,YStart=Menu.SubMenuYStart)

	SScorer.Set(id,"Item1","X",100)

	SScorer.Set(id,"Item2","Font","Horatio")
	SScorer.Set(id,"Item2","MaxInput",20)
	SScorer.Set(id,"Item2","X",320-100)
	SScorer.Set(id,"Item2","Y",SScorer.Get(id,"Item1","Y"))

	Menu.LinkUD(id,"Item1","Item3")
	if Scrap.Get("UseServerPassword"):
		Menu.LinkLR(id,"Item1","Item2")
		Menu.LinkLR(id,"Item2","Item1")
	else:
		SScorer.Set(id,"Item2","Visible",0)

	Menu.LinkUD(id,"Join","JoinInternet")


	SScorer.Set(id,"Item3","Y",SScorer.Get(id,"Item1","Y")+32)
	SScorer.Set(id,"Item3","X",100)

	SScorer.Set(id,"Item4","Y",SScorer.Get(id,"Item3","Y")+35)
	SScorer.Set(id,"Item4","X",100)

	SScorer.Set(id,"Item5","Y",SScorer.Get(id,"Item4","Y")+35)

	Menu.DrawBackSubMenu(id)

def BackToCreateServer(id, control):
	Scrap.Set("ServerPassword",SScorer.Get(id,"Item2","Text"))
	NetCreateGameMenu(id,control)

def SwitchForceVehicle(id, control):
	Force  = Scrap.GetLangStr("Menu_Multiplayer_Advanced_Force" )
	if Force  == "":
		Force  = "Force server vehicle"

	if Scrap.Get("ForceServerVehicle"):
		SScorer.Set(id,"Item3","Text","\x3 "+Force)
		Scrap.Set("ForceServerVehicle",0)
	else:
		SScorer.Set(id,"Item3","Text","\x2 "+Force)
		Scrap.Set("ForceServerVehicle",1)

def SwitchUsePass(id, control):
	Password  = Scrap.GetLangStr("Menu_Multiplayer_Advanced_Password" )
	if Password  == "":
		Password  = "Password"

	if Scrap.Get("UseServerPassword"):
		Scrap.Set("UseServerPassword",0)
		SScorer.Set(id,"Item1","Text","\x3 "+Password)
		SScorer.Set(id,"Item2","Visible",0)
		SScorer.Set(id,"Item1", "Right", "")
		SScorer.Set(id,"Item1", "Left",  "")
	else:
		Scrap.Set("UseServerPassword",1)
		SScorer.Set(id,"Item1","Text","\x2 "+Password+":")
		Menu.LinkLR(id,"Item1","Item2")
		Menu.LinkLR(id,"Item2","Item1")
		SScorer.Set(id,"Item2","Visible",1)

def RunDedicatedServer(id, control):
	import Net

	#### Check the map list...
	ServerMapList = eval(Scrap.Get("ServerMapList"))
	if len(ServerMapList)<=0 :
		ServerMapList = Net.ModesMap[Scrap.Get("ServerType")]
		Scrap.Set("ServerMapList", `ServerMapList`)

	#### Init the sever...
	Scrap.Set("ServerPassword",SScorer.Get(id,"Item2","Text"))
	Scrap.SaveConfig()
	Scrap.Set("ReRunAtExitParams",'-console -dedicated -imap:"Levels/'+ServerMapList[0]+'"')
	Scrap.Exit()

def SetDataRate(id, control):

	if   Scrap.Get("ServerDataRateLimit")==    2560:
		Scrap.Set("ServerDataRateLimit",5120)
	elif Scrap.Get("ServerDataRateLimit")==    5120:
		Scrap.Set("ServerDataRateLimit",10240)
	elif Scrap.Get("ServerDataRateLimit")==   10240:
		Scrap.Set("ServerDataRateLimit",15360)
	elif Scrap.Get("ServerDataRateLimit")==   15360:
		Scrap.Set("ServerDataRateLimit",20480)
	elif Scrap.Get("ServerDataRateLimit")==   20480:
		Scrap.Set("ServerDataRateLimit",30720)
	elif Scrap.Get("ServerDataRateLimit")==   30720:
		Scrap.Set("ServerDataRateLimit",40960)
	elif Scrap.Get("ServerDataRateLimit")==   40960:
		Scrap.Set("ServerDataRateLimit",409600000)
	else:
		Scrap.Set("ServerDataRateLimit", 2560)

	SScorer.Set(id,"Item4","Text",GetDataRateText())

def GetDataRateText():
	DataRate  = Scrap.GetLangStr("Menu_Multiplayer_Advanced_DataRate" )
	if DataRate  == "":
		DataRate  = "Connection type"

	if Scrap.Get("ServerDataRateLimit")>40960:
		return DataRate+" : LAN"
	else:
		return DataRate+" : "+`Scrap.Get("ServerDataRateLimit")/80`+" kbps"


def ServerTypePrev(id, control):
	import Net
	global MapIndex

	ServerType = Scrap.Get("ServerType")
	NewServerType = Net.Modes[0]
	size = len(Net.Modes)

	i = 0
	for t in Net.Modes:
		if t == ServerType:
			if i==0:
				NewServerType = Net.Modes[size-1]
			else:
				NewServerType = Net.Modes[i-1]
		i = i + 1

	Scrap.Set("ServerType",NewServerType)

	MapIndex = 0
	UpdateServerType(id)


def ServerTypeNext(id, control):
	import Net
	global MapIndex

	ServerType = Scrap.Get("ServerType")
	NewServerType = Net.Modes[0]
	size = len(Net.Modes)

	i = 0
	for t in Net.Modes:
		if t == ServerType:
			if i==size-1:
				NewServerType = Net.Modes[0]
			else:
				NewServerType = Net.Modes[i+1]
		i = i + 1

	Scrap.Set("ServerType",NewServerType)

	MapIndex = 0
	UpdateServerType(id)



def UpdateServerType(id):
	import Net

	ServerType = Scrap.Get("ServerType")
	tysvr = Scrap.GetLangStr("Net_Type_"+ServerType)
	if not tysvr:
		tysvr = ServerType
	SScorer.Set(id,"ServerType","Text",tysvr)


	tysvr = Scrap.GetLangStr("Menu_MultiPlayer_"+ServerType+"_Limit")
	if not tysvr:
		tysvr = "Limit"

	title = tysvr + ":"

	textWidth, textHeight = SScorer.GetTextArea("Horatio", title)

	SScorer.Set(id,"FragLimitTitle","Text",title)
	SScorer.Set(id,"FragLimit", "X", SScorer.Get(id,"FragLimitTitle","X") + textWidth + 10)

	Net.PurgeServerMapList()

	UpdateMapList(id)


def ServerTypeInfo(id,control):
	import Menu

	ServerType = Scrap.Get("ServerType")
	name = Scrap.GetLangStr("Net_Type_"+ServerType)
	help = Scrap.GetLangStr("Net_Help_"+ServerType)
	if not help:
		name = ServerType
		help = "Unofficial modification!"

	Menu.ShowTextBox(id, help, "PCMenu.NetCreateGameMenu", "PCMenu.NetCreateGameMenu" )

	y = SScorer.Get(id,"MissionDesc","Y")
	SScorer.Set(id,"MissionDesc","Y", y+45)

	iname = "ServerTypeInfo"
	SScorer.Add(id,iname, "Text", 1)
	SScorer.Set(id,iname, "Font","ScrapMedium")
	SScorer.Set(id,iname, "Text",name)
	SScorer.Set(id,iname, "X", 320)
	SScorer.Set(id,iname, "Y", y+22)
	SScorer.Set(id,iname, "Align", "Center")
	SScorer.Set(id,iname, "Visible", 1)
	SScorer.Set(id,iname, "Effect", "Outline")
	SScorer.Set(id,iname, "Red",   160)
	SScorer.Set(id,iname, "Green", 180)
	SScorer.Set(id,iname, "Blue",  255)


def MapUp(id,control):
	import Net
	global MapIndex

	ServerType = Scrap.Get("ServerType")
	MapList = Net.ModesMap[ServerType]

	if len(MapList) > MapIndex+MapSlots:
		MapIndex = MapIndex+1
		UpdateMapList(id)

def MapDown(id,control):
	global MapIndex

	if 0 < MapIndex:
		MapIndex = MapIndex-1
		UpdateMapList(id)


def MapSliderGainFocus(id,prevcontrol,control):
	iname = "MapSliderArea"
	SScorer.Set(id,iname,"OnRender","PCMenu.MapSliderOnRender")

def MapSliderLooseFocus(id,prevcontrol,control):
	iname = "MapSliderArea"
	SScorer.Set(id,iname,"OnRender","")

def MapSliderOnRender(id,control):
	import Net
	global MapIndex

	ServerType = Scrap.Get("ServerType")
	MapList = Net.ModesMap[ServerType]

	nmaps = len(MapList)

	if not SScorer.GetMenuAccept(id):
		return

	if nmaps<=MapSlots:
		return

	YMin = 214
	YSize = 124

	ycursor = SScorer.Get(id,"Cursor","Y")

	yp = ycursor - YMin - 5

	if yp < 0 :
		yp = 0

	if yp > YSize-10 :
		yp = YSize-10
	phase = (yp/(YSize-10))

	aMapIndex = MapIndex
	MapIndex = int(float((nmaps-MapSlots)+1) * phase)
	if MapIndex>=nmaps-MapSlots :
		MapIndex = nmaps-MapSlots

	if aMapIndex != MapIndex:
		UpdateMapList(id)


def UpdateMapSlider(id):
	import Net

	ServerType = Scrap.Get("ServerType")
	MapList = Net.ModesMap[ServerType]

	nmaps = len(MapList)

	YMin = 214
	YSize = 124

	if nmaps <= MapSlots :
		iname = "MapSlider"
		SScorer.Set(id,iname,"Y",YMin)
		SScorer.Set(id,iname,"ScaleY",YSize)
	else :
		YStep = YSize / float((nmaps - MapSlots)+1)
		YStepSize = YStep

		if YStepSize < 10 :
			YStepSize = 10
			YCor = YStepSize - YStep
			YStep = (YSize-YCor) / float((nmaps - MapSlots)+1)

		iname = "MapSlider"
		SScorer.Set(id,iname,"Y",YMin + MapIndex*YStep)
		SScorer.Set(id,iname,"ScaleY",YStepSize)



def UpdateMapList(id):
	import Net
	global MapIndex

	ServerType = Scrap.Get("ServerType")
	ServerMapList = eval(Scrap.Get("ServerMapList"))

	for i in range(MapSlots):
		iname = "MapSlot"+`i+1`
		SScorer.Set(id,iname,"Hint","")
		SScorer.Set(id,iname,"Text","")
		SScorer.Set(id,iname,"OnAccept", "")
		SScorer.Set(id,iname,"OnGainFocus", "")
		SScorer.Set(id,iname,"OnLooseFocus", "")

		iname = "MapSlotBack"+`i+1`
		SScorer.Set(id,iname,"Visible", 0)

	i = 0
	slot = 0
	for t in Net.ModesMap[ServerType]:

		if i>=MapIndex and i-MapIndex<MapSlots:


			mapname = Scrap.GetLangStr("Station_"+t)
			iname = "MapSlot"+`slot+1`
			SScorer.Set(id,iname,"Hint",t)
			SScorer.Set(id,iname,"OnAccept", "PCMenu.MapChoose")
			SScorer.Set(id,iname,"OnGainFocus", "PCMenu.MapPreviewOn")
			SScorer.Set(id,iname,"OnLooseFocus", "PCMenu.MapPreviewOff")

			selected = 0
			for j in ServerMapList :
				if j==t :
					selected = 1

			if selected :
				SScorer.Set(id,iname,"Text","\x02 "+mapname)
				SScorer.Set(id,iname,"Red",   255)
				SScorer.Set(id,iname,"Green", 241)
				SScorer.Set(id,iname,"Blue",  174)

				tname = "MapSlotBack"+`slot+1`
				SScorer.Set(id,tname,"Visible", 1)

			else :
				SScorer.Set(id,iname,"Text","\x03 "+mapname)
				SScorer.Set(id,iname,"Red",   183)
				SScorer.Set(id,iname,"Green", 220)
				SScorer.Set(id,iname,"Blue",  255)

			SScorer.Set(id,iname,"Down",  "MapSlot" + `slot+2`)

			slot = slot + 1

			if slot<=MapSlots/2 :
				Menu.LinkLR(id,"MapSlot" + `slot`,"MapUp")
			else :
				Menu.LinkLR(id,"MapSlot" + `slot`,"MapDown")

		i = i+1

	Menu.LinkLR(id,"MapSlot1","MapUp")
	Menu.LinkLR(id,"MapSlot" + `slot`,"MapDown")

	Menu.LinkUD(id,"MapSlot" + `slot`,"CreateButton")

	UpdateMapSlider(id)


def MapChoose(id, control):
	mapname = SScorer.Get(id,control,"Hint")

	ServerMapList = eval(Scrap.Get("ServerMapList"))
	NewServerMapList = []

	selected = 0
	for j in ServerMapList :
		if j==mapname :
			selected = 1
		else :
			NewServerMapList.append(j)

	if not selected :
		NewServerMapList.append(mapname)

	Scrap.Set("ServerMapList",`NewServerMapList`)

	UpdateMapList(id)



def MapPreviewOn(id, control,prevcontrol):
	lastmapname = SScorer.Get(id,prevcontrol,"Hint")
	mapname = SScorer.Get(id,control,"Hint")

	if lastmapname:
		name = "MapPreviewSlot_"+lastmapname
		SScorer.Set(id,name,"Visible",1)
		SScorer.Set(id,name,"OnRender", "!ScorerSpriteFadeOut" )

	name = "MapPreviewSlot_"+mapname
	SScorer.Set(id,name,"Visible",1)
	SScorer.Set(id,name,"OnRender","!ScorerSpriteFadeIn")


def MapPreviewOff(id, control,prevcontrol):
	mapname = SScorer.Get(id,control,"Hint")

	if mapname :
		name = "MapPreviewSlot_"+mapname
		SScorer.Set(id,name,"Visible",1)
		SScorer.Set(id,name,"OnRender","!ScorerSpriteFadeOut")



def ServerNameGainFocus(id, control,prevcontrol):
	SScorer.Set(id, control, "OnRender", "PCMenu.ServerNameOnRender")

def ServerNameLooseFocus(id, control,prevcontrol):
	SScorer.Set(id, control, "OnRender", "")

def ServerNameOnRender(id, control):
	text = SScorer.Get(id, control, "Text")
	Scrap.Set("ServerName",text)



def PlayersNumberGainFocus(id, control,prevcontrol):
	SScorer.Set(id, control, "OnRender", "PCMenu.PlayersNumberOnRender")

def PlayersNumberLooseFocus(id, control,prevcontrol):
	SScorer.Set(id, control, "OnRender", "")

def PlayersNumberOnRender(id, control):
	text = SScorer.Get(id, control, "Text")
	if not text :
		text = "2"
		SScorer.Set(id, control, "Text", text)
	if int(text) < 2 :
		text = "2"
		SScorer.Set(id, control, "Text", text)
	if int(text) > 16 :
		text = "16"
		SScorer.Set(id, control, "Text", text)
	Scrap.Set("DefaultMaxPlayersOnServer",int(text)-1)



def FragLimitGainFocus(id, control,prevcontrol):
	SScorer.Set(id, control, "OnRender", "PCMenu.FragLimitOnRender")

def FragLimitLooseFocus(id, control,prevcontrol):
	SScorer.Set(id, control, "OnRender", "")

def FragLimitOnRender(id, control):
	text = SScorer.Get(id, control, "Text")
	if not text :
		text = "1"
		SScorer.Set(id, control, "Text", text)
	if int(text) < 1 :
		text = "1"
		SScorer.Set(id, control, "Text", text)
	if int(text) > 99 :
		text = "99"
		SScorer.Set(id, control, "Text", text)
	Scrap.Set("FragLimit",int(text))



def NetJoinGameMenu(id, control):
	global BrowserSort, BrowserSortOrder

	ActControl = SScorer.GetActual(id)

	Menu.StartNewMenu(id)

	y = 92
	xmargin = 72
	xstep = (640-(xmargin*2))/3


	name = "JoinButton_Internet"
	SScorer.Add(id,name,"Sprite")
	SScorer.Set(id,name,"Unit",1)
	SScorer.Set(id,name,"X",xmargin + (xstep*1)-(xstep) + 1)
	SScorer.Set(id,name,"Y",y-11)
	SScorer.Set(id,name,"ScaleX",xstep-2)
	SScorer.Set(id,name,"ScaleY",24)
	SScorer.Set(id,name,"W",xstep-2)
	SScorer.Set(id,name,"H",24)
	SScorer.Set(id,name,"OnAccept","PCMenu.NetJoinInternetMenu")
	SScorer.Set(id,name,"Red",  32)
	SScorer.Set(id,name,"Green",255)
	SScorer.Set(id,name,"Blue", 255)
	if BrowsingActualDomain == "Internet" :
		SScorer.Set(id,name,"Alpha",48)
	else:
		SScorer.Set(id,name,"Alpha",10)

	name = "JoinInternet"
	SScorer.Add(id,name,"Text")
	SScorer.Set(id,name,"Font","Horatio")
	SScorer.Set(id,name,"Text",Scrap.GetLangStr("Menu_Multiplayer_JoinGame_Internet"))
	SScorer.Set(id,name,"X",xmargin + (xstep*1)-(xstep/2))
	SScorer.Set(id,name,"Y",y)
	SScorer.Set(id,name,"Red",   183)
	SScorer.Set(id,name,"Green", 220)
	SScorer.Set(id,name,"Blue",  255)
	SScorer.Set(id,name,"CentralText",1)
	SScorer.Set(id,name,"OnAccept","PCMenu.NetJoinInternetMenu")
	SScorer.Set(id,name,"FocusPivotX", -((xstep/2) - (SScorer.Get(id,name,"W")/2)) )
	SScorer.Set(id,name,"W",xstep)



	name = "JoinButton_Local"
	SScorer.Add(id,name,"Sprite")
	SScorer.Set(id,name,"Unit",1)
	SScorer.Set(id,name,"X",xmargin + (xstep*2)-(xstep)+1)
	SScorer.Set(id,name,"Y",y-11)
	SScorer.Set(id,name,"ScaleX",xstep-2)
	SScorer.Set(id,name,"ScaleY",24)
	SScorer.Set(id,name,"W",xstep-2)
	SScorer.Set(id,name,"H",24)
	SScorer.Set(id,name,"OnAccept","PCMenu.NetJoinLocalMenu")
	SScorer.Set(id,name,"Red",  32)
	SScorer.Set(id,name,"Green",255)
	SScorer.Set(id,name,"Blue", 255)
	if BrowsingActualDomain == "Local" :
		SScorer.Set(id,name,"Alpha",48)
	else:
		SScorer.Set(id,name,"Alpha",10)

	name = "JoinLocal"
	SScorer.Add(id,name,"Text")
	SScorer.Set(id,name,"Font","Horatio")
	SScorer.Set(id,name,"Text", Scrap.GetLangStr("Menu_Multiplayer_JoinGame_LocalNetwork"))
	SScorer.Set(id,name,"X",xmargin + (xstep*2)-(xstep/2))
	SScorer.Set(id,name,"Y",y)
	SScorer.Set(id,name,"Red",   183)
	SScorer.Set(id,name,"Green", 220)
	SScorer.Set(id,name,"Blue",  255)
	SScorer.Set(id,name,"CentralText",1)
	SScorer.Set(id,name,"OnAccept","PCMenu.NetJoinLocalMenu")
	SScorer.Set(id,name,"FocusPivotX", -((xstep/2) - (SScorer.Get(id,name,"W")/2)) )
	SScorer.Set(id,name,"W",xstep)



	name = "JoinButton_IP"
	SScorer.Add(id,name,"Sprite")
	SScorer.Set(id,name,"Unit",1)
	SScorer.Set(id,name,"X",xmargin + (xstep*3)-(xstep)+1)
	SScorer.Set(id,name,"Y",y-11)
	SScorer.Set(id,name,"ScaleX",xstep-2)
	SScorer.Set(id,name,"ScaleY",24)
	SScorer.Set(id,name,"W",xstep-2)
	SScorer.Set(id,name,"H",24)
	SScorer.Set(id,name,"OnAccept","PCMenu.NetJoinIPMenu")
	SScorer.Set(id,name,"Red",  32)
	SScorer.Set(id,name,"Green",255)
	SScorer.Set(id,name,"Blue", 255)
	if BrowsingActualDomain == "IP" :
		SScorer.Set(id,name,"Alpha",48)
	else:
		SScorer.Set(id,name,"Alpha",10)

	name = "JoinIP"
	SScorer.Add(id,name,"Text")
	SScorer.Set(id,name,"Font","Horatio")
	SScorer.Set(id,name,"Text",Scrap.GetLangStr("Menu_Multiplayer_JoinGame_IP"))
	SScorer.Set(id,name,"X",xmargin + (xstep*3)-(xstep/2))
	SScorer.Set(id,name,"Y",y)
	SScorer.Set(id,name,"Red",   183)
	SScorer.Set(id,name,"Green", 220)
	SScorer.Set(id,name,"Blue",  255)
	SScorer.Set(id,name,"CentralText",1)
	SScorer.Set(id,name,"OnAccept","PCMenu.NetJoinIPMenu")
	SScorer.Set(id,name,"FocusPivotX", -((xstep/2) - (SScorer.Get(id,name,"W")/2)) )
	SScorer.Set(id,name,"W",xstep)



	if BrowsingActualDomain == "Internet" :
		CreateBrowseMenu(id)
		RefreshBrowseMenu(id,control)
		BrowserSortOrder = 1
		BrowserColumnBack_Click(id,"BrowserColumnBack_" + BrowserSort)
	elif BrowsingActualDomain == "Local" :
		CreateBrowseMenu(id)
		RefreshBrowseMenu(id,control)
		BrowserSortOrder = 1
		BrowserColumnBack_Click(id,"BrowserColumnBack_" + BrowserSort)
	elif BrowsingActualDomain == "IP" :
		SpecifyIPMenu(id,control)


	NetDefaultContentMenu(id, control, "Join")

	SScorer.SetOnCancel(id, "Menu.MainMenu")

	SScorer.SetOnNext(id, "PCMenu.NetCreateGameMenu")
	SScorer.SetOnPrev(id, "PCMenu.NetCreateGameMenu")

	Menu.LinkLR(id,"JoinInternet","JoinLocal")
	Menu.LinkLR(id,"JoinLocal","JoinIP")

	Menu.LinkUD(id,"Join","JoinInternet")
	Menu.LinkUD(id,"Join","JoinLocal")
	Menu.LinkUD(id,"Join","JoinIP")

	if BrowsingActualDomain == "Internet" :
		Menu.LinkUD(id,"Join","JoinInternet")
		#Menu.LinkUD(id,"JoinInternet","Refresh")
		Menu.LinkUD(id,"Refresh","Back")
	elif BrowsingActualDomain == "Local" :
		Menu.LinkUD(id,"Join","JoinLocal")
		#Menu.LinkUD(id,"JoinLocal","Refresh")
		Menu.LinkUD(id,"Refresh","Back")
	elif BrowsingActualDomain == "IP" :
		Menu.LinkUD(id,"Join","JoinIP")
		Menu.LinkUD(id,"JoinIP","Item1")
		Menu.LinkUD(id,"Item1","Item2")
		Menu.LinkUD(id,"Item2","Back")

	Menu.LinkUD(id,"Back","Join")

	if ActControl:
		SScorer.SetDefault(id,ActControl)
	else:
		SScorer.SetDefault(id,"Join")




def NetJoinInternetMenu(id, control):
	global BrowsingActualDomain

	SNet.DoneBrowser()

	BrowsingActualDomain = "Internet"
	NetJoinGameMenu(id,control)


def NetJoinLocalMenu(id, control):
	global BrowsingActualDomain

	SNet.DoneBrowser()

	BrowsingActualDomain = "Local"
	NetJoinGameMenu(id,control)


def NetJoinIPMenu(id, control):
	global BrowsingActualDomain
	BrowsingActualDomain = "IP"

	SNet.DoneBrowser()

	NetJoinGameMenu(id,control)


def OptionsMenu(id,control):

	Menu.StartNewMenu(id)

	if (Menu.fromSinglePlayer):
		Menu.VerticalMenu(id,Scrap.GetLangStr("Menu_Options"),(
	                [Scrap.GetLangStr("Menu_Skill_Level"),"Menu.SetSkillMenu"],
		 	[Scrap.GetLangStr("Menu_Options_Video"),"PCMenu.VideoMenu"],
		        [Scrap.GetLangStr("Menu_Options_Audio"),"Menu.AudioMenu"],
	                [Scrap.GetLangStr("Menu_Options_Controls"),"PCMenu.ControlsMenu"],
	                [Scrap.GetLangStr("Menu_Back"),"Menu.SinglePlayerMenu"]),
	                "Menu.SinglePlayerMenu", YStart=Menu.OptionMenuYStart)
	        Menu.DrawBackOptionMenu(id)

	elif (Menu.fromMultiPlayer):
		Menu.VerticalMenu(id,Scrap.GetLangStr("Menu_Options"),(
		 	[Scrap.GetLangStr("Menu_Options_Video"),"PCMenu.VideoMenu"],
		        [Scrap.GetLangStr("Menu_Options_Audio"),"Menu.AudioMenu"],
	                [Scrap.GetLangStr("Menu_Options_Controls"),"PCMenu.ControlsMenu"],
	                [Scrap.GetLangStr("Menu_Back"),"PCMenu.MultiPlayerMenu"]),
	                "PCMenu.MultiPlayerMenu", YStart=Menu.SubMenuYStart)
	        Menu.DrawBackSubMenu(id)

	else:
		import Init
		if (Init.isDemo):
			Menu.VerticalMenu(id,Scrap.GetLangStr("Menu_Options"),(
		                [Scrap.GetLangStr("Menu_Options_Video"),"PCMenu.VideoMenu"],
		                [Scrap.GetLangStr("Menu_Options_Audio"),"Menu.AudioMenu"],
		                [Scrap.GetLangStr("Menu_Options_Controls"),"PCMenu.ControlsMenu"],
		                [Scrap.GetLangStr("Menu_Back"),"Menu.MainMenu"]),
		                "Menu.MainMenu", YStart=Menu.OptionMenuYStart)
		else:
			Menu.VerticalMenu(id,Scrap.GetLangStr("Menu_Options"),(
		                [Scrap.GetLangStr("Menu_Options_Video"),"PCMenu.VideoMenu"],
		                [Scrap.GetLangStr("Menu_Options_Audio"),"Menu.AudioMenu"],
		                [Scrap.GetLangStr("Menu_Options_Controls"),"PCMenu.ControlsMenu"],
		                [Scrap.GetLangStr("Menu_Credits"),"Menu.CreditsMenu"],
		                [Scrap.GetLangStr("Menu_Options_MyMenu"),"MyMenu.MyMenu"],
		                [Scrap.GetLangStr("Menu_Back"),"Menu.MainMenu"]),
		                "Menu.MainMenu", YStart=Menu.OptionMenuYStart)
		Menu.DrawBackOptionMenu(id)



# Video Options
YesValue = "\2 " + Scrap.GetLangStr("Menu_Question_Yes")
NoValue = "\3 " + Scrap.GetLangStr("Menu_Question_No")


def VideoMenu(id,control):
	global VideoModes, CurrentVideoMode, SelectedVideoMode


	ColorTitle = 143, 180, 215
	ColorOption = 183, 220, 255


	FillVideoModes()
	FillTextureFilter()
	FillTextureDetail()
	FillShadowsDetail()


	Menu.StartNewMenu(id)

	Menu.VerticalMenu(id,Scrap.GetLangStr("Menu_Options_Video"),(
			["",""],
	                [Scrap.GetLangStr("Menu_Back"),"PCMenu.VideoMenuBack"]),
	                "PCMenu.VideoMenuBack", XStart = 250, YStart = Menu.OptionMenuYStart)

	ystep = 28
	x = 260
	xval = 270
	y = 172


	# Video Mode

	iname = "TitleVideoMode"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_Mode") + ":")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Right")
	SScorer.Set(id,iname,"GetExtens",1)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.ChangeVideoMode")


	iname = "VideoMode"
	Menu.PreviousNextMenuSimple(id, iname, xval, y+12, 260)
	SScorer.Set(id,iname+"Back","Alpha", 32 )

	SScorer.Set(id,iname+"Prev","OnAccept", "PCMenu.PrevVideoMode" )
	SScorer.Set(id,iname+"Prev","MultiPress", 1)

	SScorer.Set(id,iname+"Next","OnAccept", "PCMenu.NextVideoMode" )
	SScorer.Set(id,iname+"Next","MultiPress", 1)

	Menu.LinkLR(id, "TitleVideoMode", "VideoModePrev")
	Menu.LinkLR(id, "VideoModePrev", "VideoModeNext")

	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text","WWWWWWWWWWWWWWW")
	SScorer.Set(id,iname,"X",xval+130)
	SScorer.Set(id,iname,"Y",y+12)
	SScorer.Set(id,iname,"Align","Center")
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	#SScorer.Set(id,iname,"OnAccept", "PCMenu.ChangeVideoMode")




	# Texture Filter
	y = y + ystep

	iname = "TitleTextureFilter"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_TextureFilter") + ":")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Right")
	SScorer.Set(id,iname,"GetExtens",1)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.ChangeTextureFilter")

	iname = "TextureFilter"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text","WWWWWWWWWW")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",xval)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.ChangeTextureFilter")




	# Texture Detail
	y = y + ystep
	tname = "TextureDetail"

	iname = "Title" + tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_TextureDetail") + ":")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Right")
	SScorer.Set(id,iname,"GetExtens",1)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)

	iname = tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text","WWWWWWW")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",xval)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)



	# Gamma
	y = y + ystep
	tname = "Gamma"

	iname = "Title" + tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_Gamma") + ":")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Right")
	SScorer.Set(id,iname,"GetExtens",1)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)

	iname = tname
	Menu.SliderMenu(id, iname, xval, y)
	SScorer.Set(id,iname,"MinValue",  0.0 )
	SScorer.Set(id,iname,"MaxValue",  1.0 )
	SScorer.Set(id,iname,"ValueStep", 0.1 )
	SScorer.Set(id,iname,"Value", 1 )
	SScorer.Set(id,iname,"OnChange","PCMenu.Change" + tname)


	# enlazamos los controles de sensibilidad con unos dummies
	controlName = "DummySliderSub"
	SScorer.Add(id,controlName,"Text")
	SScorer.Set(id,controlName,"Text","")
	SScorer.Set(id,controlName,"W",0)
	SScorer.Set(id,controlName,"H",0)
	SScorer.Set(id,controlName,"OnGainFocus","PCMenu.GammaSliderFocus_Sub")

	controlName = "DummySliderAdd"
	SScorer.Add(id,controlName,"Text")
	SScorer.Set(id,controlName,"Text","")
	SScorer.Set(id,controlName,"W",0)
	SScorer.Set(id,controlName,"H",0)
	SScorer.Set(id,controlName,"OnGainFocus","PCMenu.GammaSliderFocus_Add")

	Menu.LinkLR(id,"Gamma","TitleGamma")
	Menu.LinkLR(id,"TitleGamma","Gamma")
	Menu.LinkLR(id,"DummySliderSub","TitleGamma")
	Menu.LinkLR(id,"TitleGamma","DummySliderAdd")




	ystep = 22

	x = 240
	xval = 250
	y = 298 - ystep



	# Shadows Detail
	y = y + ystep
	tname = "ShadowsDetail"

	iname = "Title" + tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_Shadows") + ":")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Right")
	SScorer.Set(id,iname,"GetExtens",1)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)

	iname = tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text","WWWWWW")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",xval)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)


	y = y + ystep


	# VSync
	y = y + ystep
	tname = "VSync"

	iname = "Title" + tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_VSync") + ":")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Right")
	SScorer.Set(id,iname,"GetExtens",1)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)

	iname = tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text","WWWW")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",xval)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)



	# Video Lock
	y = y + ystep
	tname = "Lock"

	iname = "Title" + tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_Lock") + ":")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Right")
	SScorer.Set(id,iname,"GetExtens",1)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)

	iname = tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text","WWWW")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",xval)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)




	x = 460
	xval = 470
	y = 298 - ystep



	# Fog
	y = y + ystep
	tname = "Fog"

	iname = "Title" + tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_Fog") + ":")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Right")
	SScorer.Set(id,iname,"GetExtens",1)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)

	iname = tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text","WWWW")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",xval)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)



	# Bloom
	y = y + ystep
	tname = "Bloom"

	iname = "Title" + tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_Bloom") + ":")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Right")
	SScorer.Set(id,iname,"GetExtens",1)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)

	iname = tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text","WWWW")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",xval)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)




	# MotionBlur
	y = y + ystep
	tname = "MotionBlur"

	iname = "Title" + tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_MotionBlur") + ":")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Right")
	SScorer.Set(id,iname,"GetExtens",1)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)

	iname = tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text","WWWW")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",xval)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)



	# Deformation
	y = y + ystep
	tname = "DuDv"

	iname = "Title" + tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_Deformation") + ":")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",x)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Right")
	SScorer.Set(id,iname,"GetExtens",1)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorTitle[0])
	SScorer.Set(id,iname,"Green", ColorTitle[1])
	SScorer.Set(id,iname,"Blue",  ColorTitle[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)

	iname = tname
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"Text","WWWW")
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"X",xval)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Align","Left")
	SScorer.Set(id,iname,"Red",   ColorOption[0])
	SScorer.Set(id,iname,"Green", ColorOption[1])
	SScorer.Set(id,iname,"Blue",  ColorOption[2])
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.Change" + tname)



	VideoGetLast(id)
	UpdateVideoOptions(id)


	y = 420

	# Defaults
	iname = "Defaults"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"X",320-150)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_SetDefaults"))
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"Red",   183)
	SScorer.Set(id,iname,"Green", 220)
	SScorer.Set(id,iname,"Blue",  255)
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.VideoDefaults")


	# Apply
	iname = "Apply"
	SScorer.Add(id,iname,"Text")
	SScorer.Set(id,iname,"Font","Horatio")
	SScorer.Set(id,iname,"X",320+150)
	SScorer.Set(id,iname,"Y",y)
	SScorer.Set(id,iname,"Text",Scrap.GetLangStr("Menu_Video_Apply"))
	SScorer.Set(id,iname,"CentralText",1)
	SScorer.Set(id,iname,"Red",   183)
	SScorer.Set(id,iname,"Green", 220)
	SScorer.Set(id,iname,"Blue",  255)
	SScorer.Set(id,iname,"Effect", "Shadow")
	SScorer.Set(id,iname,"OnAccept", "PCMenu.ApplyChanges")




	# Back Tab

	SScorer.Set(id,"TitleBarL","Visible",0)
	SScorer.Set(id,"TitleBarM","Visible",0)
	SScorer.Set(id,"TitleBarR","Visible",0)

	SizeX = 36.5 * Menu.TabQuadSize
	SizeY = 21 * Menu.TabQuadSize
	TabX = 320 - SizeX/2
	TabY = SScorer.Get(id,"TitleBarM","Y")

	iname = "VideoOptionsTab"
	SScorer.Add(id,iname,"Tab")
	Menu.SetTabDefaults(id,iname)
	SScorer.Set(id,iname,"X", TabX)
	SScorer.Set(id,iname,"Y", TabY)
	SScorer.Set(id,iname,"SizeX", SizeX)
	SScorer.Set(id,iname,"SizeY", SizeY)
	SScorer.Set(id,iname,"TabInit",0)
	SScorer.Set(id,iname,"TabEnd", 0)
	SScorer.Set(id,iname,"TabMax", 0)
	SScorer.Set(id,iname,"SizeTabQuad", 0)
	SScorer.Set(id,iname,"Type", 2)	#TAB_MISSION
	SScorer.Set(id,iname,"Alpha", 150)
	SScorer.Set(id,iname,"Red",    60)
	SScorer.Set(id,iname,"Green", 150)
	SScorer.Set(id,iname,"Blue",  200)



	# Enlaces

	Menu.LinkUD(id,"Item2","VideoModePrev")
	Menu.LinkUD(id,"Item2","VideoModeNext")
	Menu.LinkUD(id,"VideoModePrev","TitleTextureFilter")
	Menu.LinkUD(id,"VideoModeNext","TitleTextureFilter")

	Menu.LinkUD(id,"TitleVideoMode","TitleTextureFilter")

	Menu.LinkUD(id,"TitleTextureFilter","TitleTextureDetail")
	Menu.LinkUD(id,"TitleTextureDetail","TitleGamma")

	Menu.LinkUD(id,"TitleShadowsDetail","TitleVSync")
	Menu.LinkUD(id,"TitleVSync","TitleLock")
	Menu.LinkUD(id,"TitleLock","Defaults")

	Menu.LinkLR(id,"TitleShadowsDetail","TitleFog")
	Menu.LinkLR(id,"TitleVSync","TitleMotionBlur")
	Menu.LinkLR(id,"TitleLock","TitleDuDv")

	Menu.LinkUD(id,"TitleGamma","TitleFog")
	Menu.LinkUD(id,"TitleFog","TitleBloom")
	Menu.LinkUD(id,"TitleBloom","TitleMotionBlur")
	Menu.LinkUD(id,"TitleMotionBlur","TitleDuDv")
	Menu.LinkUD(id,"TitleDuDv","Apply")

	Menu.LinkUD(id,"TitleGamma","TitleShadowsDetail")

	Menu.LinkUD(id,"Apply","Item2")
	Menu.LinkUD(id,"Defaults","Item2")

	Menu.LinkLR(id,"Defaults","Item2")
	Menu.LinkLR(id,"Item2","Apply")

	Menu.LinkUD(id,"Item2","TitleVideoMode")

	# Default
	SScorer.SetDefault(id,"TitleVideoMode")


	# Background
	Menu.DrawBackOptionMenu(id)




def ChangeVideoMode(id,control):
	global VideoModes, CurrentVideoMode, SelectedVideoMode, VideoModesValid

	Apply_SetActive(id, control)

	prevmode = SelectedVideoMode
	NextVideoMode(id, control)

	if prevmode == SelectedVideoMode:
		SelectedVideoMode = VideoModesValid[0][0]

	SScorer.Set(id, "VideoMode", "Text", VideoModes[SelectedVideoMode][1] )

def PrevVideoMode(id,control):
	global VideoModes, CurrentVideoMode, SelectedVideoMode, VideoModesValid

	Apply_SetActive(id, control)

	validmodes = len(VideoModesValid)
	for i in range(validmodes) :
		imode = validmodes-1-i
		if VideoModesValid[imode][0] <= VideoModes[SelectedVideoMode][0] :
			if imode>0 :
				SelectedVideoMode = VideoModesValid[imode-1][0]
				break

	SScorer.Set(id, "VideoMode", "Text", VideoModes[SelectedVideoMode][1] )

def NextVideoMode(id,control):
	global VideoModes, CurrentVideoMode, SelectedVideoMode, VideoModesValid

	Apply_SetActive(id, control)

	validmodes = len(VideoModesValid)
	for i in range(validmodes) :
		imode = i
		if VideoModesValid[i][0] >= VideoModes[SelectedVideoMode][0] :
			if imode+1<validmodes :
				SelectedVideoMode = VideoModesValid[imode+1][0]
				break

	SScorer.Set(id, "VideoMode", "Text", VideoModes[SelectedVideoMode][1] )


def FillVideoModes():
	import string
	global VideoModes, CurrentVideoMode, SelectedVideoMode, VideoModesValid

	CurrentVideoMode = Scrap.GetVideoCurrentMode()
	SelectedVideoMode = CurrentVideoMode

	VideoModes = []
	NumModes = Scrap.GetVideoModes(-1)
	for NumMode in range(NumModes):
		ModeDescription = Scrap.GetVideoModes(NumMode)
		VideoModes.append([NumMode,ModeDescription])

	VideoModesValid = []

	for Mode in VideoModes:
		cad = Mode[1]

		width = 0
		height = 0
		bpp = 0

		index1 = string.find(cad, "x")
		index2 = string.find(cad, " (")
		index3 = string.find(cad, " bpp)")

		width = int( cad[0:(index1)] )
		height = int( cad[index1+1:(index2)] )
		bpp = int( cad[index2+2:(index3)] )

		if Mode[0] == SelectedVideoMode or ( bpp==32 and (width>=640 and height>=480) and (width>=height) ):
			VideoModesValid.append( Mode )
			## print cad, " ----> ", width, height, bpp

	# Si ha habido algún problema los añadimos todos a la lista
	if len(VideoModesValid)<=1 :
		VideoModesValid = []
		for Mode in VideoModes:
			VideoModesValid.append( Mode )


def FillTextureFilter():
	global TextureFilterList

	TextureFilterList = []

	TextureFilterList.append("Point")
	TextureFilterList.append("Bilinear")
	TextureFilterList.append("Trilinear")
	TextureFilterList.append("Anisotropic x2")
	TextureFilterList.append("Anisotropic x4")
	TextureFilterList.append("Anisotropic x8")

def ChangeTextureFilter(id, control):
	global TextureFilterList

	Apply_SetActive(id, control)

	actual = SScorer.Get(id, "TextureFilter", "Text")

	i = 0
	iactual = 0
	for t in TextureFilterList:
		if t == actual:
			iactual	= i
		i = i+1

	nuevo = iactual+1
	if nuevo>=len(TextureFilterList) :
		nuevo = 1

	SScorer.Set(id, "TextureFilter", "Text", TextureFilterList[nuevo])

	Apply_SetTextureFilter(id, control)



def FillTextureDetail():
	global TextureDetailList

	TextureDetailList = []

	TextureDetailList.append(Scrap.GetLangStr("Menu_Question_High"))
	TextureDetailList.append(Scrap.GetLangStr("Menu_Question_Medium"))
	TextureDetailList.append(Scrap.GetLangStr("Menu_Question_Low"))

def ChangeTextureDetail(id, control):
	global TextureDetailList

	Apply_SetActive(id, control)

	actual = SScorer.Get(id, "TextureDetail", "Text")

	i = 0
	iactual = 0
	for t in TextureDetailList:
		if t == actual:
			iactual	= i
		i = i+1

	nuevo = iactual+1
	if nuevo>=len(TextureDetailList) :
		nuevo = 0

	SScorer.Set(id, "TextureDetail", "Text", TextureDetailList[nuevo])



def FillShadowsDetail():
	global ShadowsDetailList

	ShadowsDetailList = []

	ShadowsDetailList.append("\2 " + Scrap.GetLangStr("Menu_Question_High"))
	ShadowsDetailList.append("\2 " + Scrap.GetLangStr("Menu_Question_Medium"))
	ShadowsDetailList.append("\2 " + Scrap.GetLangStr("Menu_Question_Low"))
	ShadowsDetailList.append("\3 " + Scrap.GetLangStr("Menu_Question_No"))

def ChangeShadowsDetail(id, control):
	global ShadowsDetailList

	Apply_SetActive(id, control)

	actual = SScorer.Get(id, "ShadowsDetail", "Text")

	i = 0
	iactual = 0
	for t in ShadowsDetailList:
		if t == actual:
			iactual	= i
		i = i+1

	nuevo = iactual+1
	if nuevo>=len(ShadowsDetailList) :
		nuevo = 0

	SScorer.Set(id, "ShadowsDetail", "Text", ShadowsDetailList[nuevo])


def ChangeVSync(id,control):
	Apply_SetActive(id, control)
	ChangeBoolean(id,"VSync")

def ChangeLock(id,control):
	Apply_SetActive(id, control)
	ChangeBoolean(id,"Lock")
	Apply_SetVideoLock(id, control)


def ChangeFog(id,control):
	Apply_SetActive(id, control)
	ChangeBoolean(id,"Fog")
	Apply_SetFog(id, control)


def ChangeBloom(id,control):
	Apply_SetActive(id, control)
	ChangeBoolean(id,"Bloom")

def ChangeMotionBlur(id,control):
	Apply_SetActive(id, control)
	ChangeBoolean(id,"MotionBlur")

def ChangeDuDv(id,control):
	Apply_SetActive(id, control)
	ChangeBoolean(id,"DuDv")



def ChangeBoolean(id,control):
	if SScorer.Get(id, control, "Text") == YesValue :
		SScorer.Set(id, control, "Text", NoValue)
	else:
		SScorer.Set(id, control, "Text", YesValue)


def ChangeGamma(id,control):
	Apply_SetActive(id, control)
	value = SScorer.Get(id, "Gamma", "Value")
	Scrap.Set("VideoGammaRGB", GammaFormula(value=value) )


def GammaFormula(value=-1,gamma=-1):
	if (value>=0):
		gamma = 1.0
		if (value<0.5) :
			gamma = 0.5+value
		else:
			gamma = 1+(value-0.5)*(4)
		return gamma

	if (gamma>=0):
		value = 1.0
		if (gamma<=1) :
			value = gamma-0.5
		else:
			value = 0.5+((gamma-1)/4)
		return value



def GammaSliderFocus_Sub(id,control,prevcontrol):

	slidercontrol = "Gamma"

	value = SScorer.Get(id,slidercontrol,"Value")
	valuestep = SScorer.Get(id,slidercontrol,"ValueStep")

	SScorer.Set(id,slidercontrol,"Value", value - valuestep)
	SScorer.SetDefault(id,prevcontrol)

	ChangeGamma(id, control)


def GammaSliderFocus_Add(id,control,prevcontrol):

	slidercontrol = "Gamma"

	value = SScorer.Get(id,slidercontrol,"Value")
	valuestep = SScorer.Get(id,slidercontrol,"ValueStep")

	SScorer.Set(id,slidercontrol,"Value", value + valuestep)
	SScorer.SetDefault(id,prevcontrol)

	ChangeGamma(id, control)



def UpdateVideoOptions(id):
	global VideoModes, CurrentVideoMode, SelectedVideoMode, TextureFilterList

	iname = "Gamma"
	SScorer.Set(id,iname,"Value", GammaFormula( gamma = Scrap.Get("VideoGammaRGB") ) )

	iname = "TextureFilter"
	if Scrap.Get("R_TexFilter") == 0 :	# Point
		SScorer.Set(id,iname,"Text",TextureFilterList[0])
	elif Scrap.Get("R_TexFilter") == 1 :
		if Scrap.Get("R_MipFilter") == 0 :
			SScorer.Set(id,iname,"Text",TextureFilterList[1])	# Bilinear
		else :
			SScorer.Set(id,iname,"Text",TextureFilterList[2])	# Trilinear
	elif Scrap.Get("R_TexFilter") == 2 :	# Anisotropico
		if Scrap.Get("R_Anisotropy") == 2 :
			SScorer.Set(id,iname,"Text",TextureFilterList[3]) # x2
		elif Scrap.Get("R_Anisotropy") == 4 :
			SScorer.Set(id,iname,"Text",TextureFilterList[4]) # x4
		elif Scrap.Get("R_Anisotropy") == 8 :
			SScorer.Set(id,iname,"Text",TextureFilterList[5]) # x8
		else :
			SScorer.Set(id,iname,"Text",TextureFilterList[3]) # x2
	else:
		SScorer.Set(id,iname,"Text",TextureFilterList[2])

	iname = "TextureDetail"
	if (Scrap.Get("TextureLOD") == 0 or Scrap.Get("TextureLOD") == -1) :	# High
		SScorer.Set(id,iname,"Text",TextureDetailList[0])
	elif Scrap.Get("TextureLOD") == 1 :	# Medium
		SScorer.Set(id,iname,"Text",TextureDetailList[1])
	elif Scrap.Get("TextureLOD") == 2 :	# Low
		SScorer.Set(id,iname,"Text",TextureDetailList[2])

	iname = "VideoMode"
	SScorer.Set(id,iname,"Text", VideoModes[SelectedVideoMode][1] )


	iname = "ShadowsDetail"
	if Scrap.Get("R_StencilShadows") == -1 :
		SScorer.Set(id,iname,"Text",ShadowsDetailList[3])	# No

		SScorer.Set(id,"Title" + iname,"OnAccept","")
		SScorer.Set(id,"Title" + iname,"Red", SScorer.Get(id,"Title" + iname,"Red")*0.75 )
		SScorer.Set(id,"Title" + iname,"Green", SScorer.Get(id,"Title" + iname,"Green")*0.75 )
		SScorer.Set(id,"Title" + iname,"Blue", SScorer.Get(id,"Title" + iname,"Blue")*0.75 )

		SScorer.Set(id,iname,"OnAccept","")
		SScorer.Set(id,iname,"Red", SScorer.Get(id,iname,"Red")*0.75 )
		SScorer.Set(id,iname,"Green", SScorer.Get(id,iname,"Green")*0.75 )
		SScorer.Set(id,iname,"Blue", SScorer.Get(id,iname,"Blue")*0.75 )

	else:
		shadows = (Scrap.Get("R_StencilShadows") == 1)
		self = (Scrap.Get("R_StencilSelf") == 1)
		mult = Scrap.Get("R_StencilMult")

		if shadows :
			if self :
				SScorer.Set(id,iname,"Text",ShadowsDetailList[0])	# High
			else :
				if mult>=1.0:
					SScorer.Set(id,iname,"Text",ShadowsDetailList[1])	# Medium
				else :
					SScorer.Set(id,iname,"Text",ShadowsDetailList[2])	# Low
		else :	# No
			SScorer.Set(id,iname,"Text",ShadowsDetailList[3])


	iname = "VSync"
	if Scrap.Get("VSync") == 1 :
		SScorer.Set(id,iname,"Text",YesValue)
	else:
		SScorer.Set(id,iname,"Text",NoValue)

	iname = "Lock"
	if Scrap.Get("R_VideoLockMode") == 1 :
		SScorer.Set(id,iname,"Text",YesValue)
	else:
		SScorer.Set(id,iname,"Text",NoValue)

	iname = "Fog"
	if Scrap.Get("R_FogEnable") == 1 :
		SScorer.Set(id,iname,"Text",YesValue)
	else:
		SScorer.Set(id,iname,"Text",NoValue)


	SceneEffects = (Scrap.Get("R_SceneRTarget")==1)

	iname = "Bloom"
	if SceneEffects and Scrap.Get("R_SceneBloomRTarget") == 1 :
		SScorer.Set(id,iname,"Text",YesValue)
	else:
		SScorer.Set(id,iname,"Text",NoValue)

	iname = "MotionBlur"
	if SceneEffects and Scrap.Get("R_SceneMotionBlurRTarget") == 1 :
		SScorer.Set(id,iname,"Text",YesValue)
	else:
		SScorer.Set(id,iname,"Text",NoValue)

	iname = "DuDv"
	if SceneEffects and Scrap.Get("R_SceneDuDvRTarget") == 1 :
		SScorer.Set(id,iname,"Text",YesValue)
	else:
		SScorer.Set(id,iname,"Text",NoValue)

	iname = "Shadows"
	SScorer.Set(id,iname,"Text",NoValue)



Last_TexFilter = 0
Last_MipFilter = 0
Last_VideoGamma = 0
Last_Fog = 0
Last_VideoLockMode = 0
Last_VideoLockBuf = 0


def VideoGetLast(id):
	import Menu
	global Last_TexFilter, Last_MipFilter, Last_VideoGamma, Last_Fog, Last_VideoLockMode, Last_VideoLockBuf

	Last_TexFilter = Scrap.Get("R_TexFilter")
	Last_MipFilter = Scrap.Get("R_MipFilter")

	Last_VideoGamma = Scrap.Get("VideoGammaRGB")

	Last_Fog = Scrap.Get("R_FogEnable")

	Last_VideoLockMode = Scrap.Get("R_VideoLockMode")
	Last_VideoLockBuf = Scrap.Get("R_VideoLockBuf")


def VideoMenuBack(id,control):
	import Menu
	global Last_TexFilter, Last_MipFilter, Last_VideoGamma, Last_Fog, Last_VideoLockMode, Last_VideoLockBuf

	Scrap.Set("R_TexFilter", Last_TexFilter)
	Scrap.Set("R_MipFilter", Last_MipFilter)

	Scrap.Set("VideoGammaRGB", Last_VideoGamma)

	Scrap.Set("R_FogEnable", Last_Fog)

	Scrap.Set("R_VideoLockMode", Last_VideoLockMode)
	Scrap.Set("R_VideoLockBuf", Last_VideoLockBuf)

	Menu.OptionsMenu(id, control)



def VideoDefaults(id,control):

	SScorer.Set(id, "Gamma", "Value", GammaFormula( gamma=1 ) )
	ChangeGamma(id, "Gamma")

	SScorer.Set(id, "TextureFilter", "Text", TextureFilterList[2])
	Apply_SetTextureFilter(id, control)

	SScorer.Set(id, "TextureDetail", "Text", TextureDetailList[0])

	SScorer.Set(id, "ShadowsDetail", "Text", ShadowsDetailList[0])
	SScorer.Set(id, "VSync", "Text", NoValue)

	SScorer.Set(id, "Lock", "Text", NoValue)
	Apply_SetVideoLock(id, control)

	SScorer.Set(id, "Fog", "Text", YesValue)
	Apply_SetFog(id, control)

	SScorer.Set(id, "Bloom", "Text", YesValue)
	SScorer.Set(id, "MotionBlur", "Text", YesValue)
	SScorer.Set(id, "DuDv", "Text", YesValue)


def Apply_SetActive(id,control):
	SScorer.Set(id, "Apply", "Effect", "Outline")

	SScorer.Set(id, "Apply", "Red", 255)
	SScorer.Set(id, "Apply", "Green", 255)
	SScorer.Set(id, "Apply", "Blue", 180)

	SScorer.Set(id, "Apply", "OnRender", "!ScorerSpriteFlash")


def Apply_SetTextureFilter(id, control):
	TexFilter = SScorer.Get(id, "TextureFilter", "Text")
	if TexFilter == TextureFilterList[0] : 	# Point
		Scrap.Set("R_TexFilter",0)
		Scrap.Set("R_MipFilter",0)
		Scrap.Set("R_Anisotropy",0)
	elif TexFilter == TextureFilterList[1] :  # Bilinear
		Scrap.Set("R_TexFilter",1)
		Scrap.Set("R_MipFilter",0)
		Scrap.Set("R_Anisotropy",0)
	elif TexFilter == TextureFilterList[2] :  # Trilinear
		Scrap.Set("R_TexFilter",1)
		Scrap.Set("R_MipFilter",1)
		Scrap.Set("R_Anisotropy",0)
	elif TexFilter == TextureFilterList[3] :  # Anisotropic x2
		Scrap.Set("R_TexFilter",2)
		Scrap.Set("R_MipFilter",1)
		Scrap.Set("R_Anisotropy",2)
	elif TexFilter == TextureFilterList[4] :  # Anisotropic x4
		Scrap.Set("R_TexFilter",2)
		Scrap.Set("R_MipFilter",1)
		Scrap.Set("R_Anisotropy",4)
	elif TexFilter == TextureFilterList[5] :  # Anisotropic x8
		Scrap.Set("R_TexFilter",2)
		Scrap.Set("R_MipFilter",1)
		Scrap.Set("R_Anisotropy",8)


def Apply_SetVideoLock(id, control):
	if SScorer.Get(id, "Lock", "Text") == YesValue :
		Scrap.Set("R_VideoLockMode",1)
		Scrap.Set("R_VideoLockBuf",1)
	else :
		Scrap.Set("R_VideoLockMode",2)
		Scrap.Set("R_VideoLockBuf",1)


def Apply_SetFog(id, control):
	if SScorer.Get(id, "Fog", "Text") == YesValue :
		Scrap.Set("R_FogEnable",1)
	else :
		Scrap.Set("R_FogEnable",0)



def ApplyChanges(id,control):
	global VideoModes, CurrentVideoMode, SelectedVideoMode

	NeedEngineReset = 0


	## Gamma
	ChangeGamma(id, "Gamma")


	## Texture Filter
	Apply_SetTextureFilter(id, control)


	## Texture Detail
	TexDetail = SScorer.Get(id, "TextureDetail", "Text")
	if TexDetail == TextureDetailList[0] : 	# High
		if Scrap.Get("TextureLOD") != 0 :
			NeedEngineReset = 1
		Scrap.Set("TextureLOD",0)
	elif TexDetail == TextureDetailList[1] :  # Medium
		if Scrap.Get("TextureLOD") != 1 :
			NeedEngineReset = 1
		Scrap.Set("TextureLOD",1)
	elif TexDetail == TextureDetailList[2] :  # Low
		if Scrap.Get("TextureLOD") != 2 :
			NeedEngineReset = 1
		Scrap.Set("TextureLOD",2)


	## Shadows
	ShadowsDetail = SScorer.Get(id, "ShadowsDetail", "Text")

	if ShadowsDetail == ShadowsDetailList[0] :	# High

		if Scrap.Get("R_StencilShadows") != 1 :
			NeedEngineReset = 1
		Scrap.Set("R_StencilShadows",1)
		Scrap.Set("R_StencilSelf",1)
		Scrap.Set("R_StencilMult",1)

	elif ShadowsDetail == ShadowsDetailList[1] :  # Medium

		if Scrap.Get("R_StencilShadows") != 1 :
			NeedEngineReset = 1
		Scrap.Set("R_StencilShadows",1)
		Scrap.Set("R_StencilSelf",0)
		Scrap.Set("R_StencilMult",1)

	elif ShadowsDetail == ShadowsDetailList[2] :  # Low

		if Scrap.Get("R_StencilShadows") != 1 :
			NeedEngineReset = 1
		Scrap.Set("R_StencilShadows",1)
		Scrap.Set("R_StencilSelf",0)
		Scrap.Set("R_StencilMult",0.8)

	else :

		if Scrap.Get("R_StencilShadows") != 0 :
			NeedEngineReset = 1
		Scrap.Set("R_StencilShadows",0)



	## VSync
	if SScorer.Get(id, "VSync", "Text") == YesValue :
		if Scrap.Get("VSync") != 1 :
			NeedEngineReset = 1
		Scrap.Set("VSync",1)
	else :
		if Scrap.Get("VSync") != 0 :
			NeedEngineReset = 1
		Scrap.Set("VSync",0)


	## Video Lock
	Apply_SetVideoLock(id, control)


	## Fog
	Apply_SetFog(id, control)



	## SceneEffects
	SceneEffects = 0

	if SScorer.Get(id, "Bloom", "Text") == YesValue :
		SceneEffects = 1
		if Scrap.Get("R_SceneBloomRTarget") != 1 :
			NeedEngineReset = 1
		Scrap.Set("R_SceneBloomRTarget",1)
	else:
		if Scrap.Get("R_SceneBloomRTarget") != 0 :
			NeedEngineReset = 1
		Scrap.Set("R_SceneBloomRTarget",0)

	if SScorer.Get(id, "MotionBlur", "Text") == YesValue :
		SceneEffects = 1
		if Scrap.Get("R_SceneMotionBlurRTarget") != 1 :
			NeedEngineReset = 1
		Scrap.Set("R_SceneMotionBlurRTarget",1)
	else:
		if Scrap.Get("R_SceneMotionBlurRTarget") != 0 :
			NeedEngineReset = 1
		Scrap.Set("R_SceneMotionBlurRTarget",0)

	if SScorer.Get(id, "DuDv", "Text") == YesValue :
		SceneEffects = 1
		if Scrap.Get("R_SceneDuDvRTarget") != 1 :
			NeedEngineReset = 1
		Scrap.Set("R_SceneDuDvRTarget",1)
	else:
		if Scrap.Get("R_SceneDuDvRTarget") != 0 :
			NeedEngineReset = 1
		Scrap.Set("R_SceneDuDvRTarget",0)

	if SceneEffects==1 :
		if Scrap.Get("R_SceneRTarget") != 1 :
			NeedEngineReset = 1
		Scrap.Set("R_SceneRTarget",1)
	else :
		if Scrap.Get("R_SceneRTarget") != 0 :
			NeedEngineReset = 1
		Scrap.Set("R_SceneRTarget",0)


	OptionsMenu(id,control)

	if NeedEngineReset or (CurrentVideoMode != SelectedVideoMode) :
		#Scrap.AddScheduledFunc(Scrap.GetTime(),Scrap.SetVideoCurrentMode,(SelectedVideoMode,))
		Scrap.SetVideoCurrentMode(SelectedVideoMode)


	#if (not Init.inMainMenu and not Init.isShipEdit) :
	#	Menu.BackToGame(id)
	#else :
	#	OptionsMenu(id,control)
