##########################################################
#                   Initialization engine
##########################################################

#    Cam = Scrap.GetEntity(Scrap.GetCam(0))
# Scrap.GetEntity(Scrap.GetCam(0)).CamDist = 0
# Scrap.GetEntity(Scrap.GetCam(0)).FreeCam = 1
# Scrap.GetEntity("net256").Descriptor
# Scrap.GetEntity(Scrap.GetEntity("Player1").Target).Life = 0
# Scrap.GetEntity("Player1").EMICounter = 1.0
# Scrap.GetEntity("Player1").Upgrd01 = 3;Scrap.GetEntity("Player1").UAmmo01 = 200
# import Vehicles;Vehicles.ReSpawnShip("Player1")
# Scrap.GetEntity("Player1").FireRemainTime = 10.0;Scrap.GetEntity("Player1").FireDelayTime = 0.2
# import Net;Net.Spectate(0,1)
# Scrap.GetEntity("Player1").ActCtrl = "Mosquito"

import Scrap

logger = None

PlaySpacelords = not Scrap.IsApp(436180)  # 1 to activate the cross promotion
##################################
## All the built in functions
##################################
import SInput,SNet,SWeap,SScorer,SSound,SAct,sys,SAI,SFX

Scrap.CreateSaveVar("CreateBertos", "0")
Scrap.CreateSaveVar("MercsHelpDtritus", "0")
Scrap.CreateSaveVar("RobotsControlledByBoss", "0")
Scrap.CreateSaveVar("Player.InfiniteLives", "1")

# WARNING : Never import any pyhton source library at the start up!
#
SUPERDEALSMAPS = ["TUCZONE","QF","OM","FZ","CA"]
OUTMAPS = ["TUCZONE","AB","COMMERCIAL","DOWNTOWN","GDB","OUTSKIRTS","SCRAPYARD"]+SUPERDEALSMAPS
INMAPS  = ["NANO","ABINDOOR","BANK","GAMBLINDEN","ORBIT","POLICE","PRESS","TEMPLE","TOWNHALL"]

ExtraExecs ={
	"JUNKYARD":(
	(Scrap.PreloadLibrary,('RustySound',          'Sound/RustySound.pyc'           )),
	(Scrap.PreloadLibrary,('SputnikJunkyardSound','Sound/SputnikJunkyardSound.pyc' )),
	(Scrap.PreloadLibrary,('MaintenanceSound',    'Sound/MaintenanceSound.pyc'     )),

	(Scrap.PreloadLibrary,('Rusty',               'Chars/Rusty.pyc'                )),
	(Scrap.PreloadLibrary,('SputnikJunkyard',     'Chars/SputnikJunkyard.pyc'      )),
	(Scrap.PreloadLibrary,('Maintenance',         'Chars/Maintenance.pyc'          )),
				),

	"GAMBLINDEN":(
	(Scrap.PreloadLibrary,('MercenarySound',      'Sound/MercenarySound.pyc'       )),
	(Scrap.PreloadLibrary,('CrazyGamblerSound',   'Sound/CrazyGamblerSound.pyc'    )),


	(Scrap.PreloadLibrary,('MercenaryA',          'Chars/MercenaryA.pyc'           )),
	(Scrap.PreloadLibrary,('MercenaryB',          'Chars/MercenaryB.pyc'           )),
	(Scrap.PreloadLibrary,('MercenaryC',          'Chars/MercenaryC.pyc'           )),
	(Scrap.PreloadLibrary,('MercenaryL',          'Chars/MercenaryL.pyc'           )),
	(Scrap.PreloadLibrary,('CrazyGambler',        'Chars/CrazyGambler.pyc'         )),
				),

	"ABINDOOR":(
	(Scrap.PreloadLibrary,('CrazyGamblerSound',   'Sound/CrazyGamblerSound.pyc'    )),
	(Scrap.PreloadLibrary,('CrazyGambler',        'Chars/CrazyGambler.pyc'         )),
				),

	"PRESS":(
	(Scrap.PreloadLibrary,('SebastianSound',      'Sound/SebastianSound.pyc'       )),
	(Scrap.PreloadLibrary,('BossSound',           'Sound/BossSound.pyc'            )),


	(Scrap.PreloadLibrary,('Sebastian',           'Chars/Sebastian.pyc'            )),
	(Scrap.PreloadLibrary,('Boss',                'Chars/Boss.pyc'                 )),
				),
}

OffLineGame = Scrap.GetNetFlags()==(0,0,0)
MultiPlayer = not OffLineGame or Scrap.Get("SplitScreen") != 0

############################################################################################################
#################################### Preload all the built in libraries ####################################
############################################################################################################
# todos los paths
sys.path.append('Scripts/Scorer')
sys.path.append('Scripts/ShipEdit')
sys.path.append('Scripts/Python')
sys.path.append('Scripts/Weapons')
sys.path.append('Scripts/Vehicles')
sys.path.append('Scripts/Net')
sys.path.append('Scripts/FX')
sys.path.append('Scripts/Sound')
sys.path.append('Scripts/Chars')
sys.path.append('Scripts/Missions')
sys.path.append('Scripts/SuperDeals')
sys.path.append('Scripts/Split')

###### Librerias standard de python  ######
Scrap.PreloadLibrary('string','Python/string.pyc')

# determinar el ambito de los mapas...
import string
UpperMap = string.upper(Scrap.GetLevelPath()[7:])
SuperDealModule = None
sDealType       = Scrap.GetSaveVar("SuperDealType")
HasSuperDeal    = OffLineGame and sDealType and sDealType != "" and (UpperMap in SUPERDEALSMAPS)
OutMapSkip      = OffLineGame and (UpperMap in OUTMAPS)
InMapSkip       = OffLineGame and (UpperMap in INMAPS)

###### Preloading custom stuff ######
Scrap.PreloadLibrary('Logger','Custom/Logger.pyc')

import Logger
logger = Logger.Logger('Loader')
logger.info('Logger initialized')
logger.debug(logger)

logger.info('Preloading MyMenu...')
Scrap.PreloadLibrary('MyMenu','Scorer/MyMenu.pyc')
logger.info('MyMenu preloaded')

#Scrap.PreloadLibrary('QuickConsole','QuickConsole.pyc') # QuickConsole no es una libreria para el sistema

###### Librerias basicas del sistema raiz ######
Scrap.PreloadLibrary('Items','Items.pyc')
Scrap.PreloadLibrary('SaveGame','SaveGame.pyc')

###### Sistema de menues y scorer ######
if (Scrap.Get("IsXbox") == 1):
	Scrap.PreloadLibrary('XBMenu','Scorer/XBMenu.pyc')
else:
	Scrap.PreloadLibrary('PCMenu','Scorer/PCMenu.pyc')

Scrap.PreloadLibrary('Menu','Scorer/Menu.pyc')
Scrap.PreloadLibrary('Scorer','Scorer/Scorer.pyc')
Scrap.PreloadLibrary('CharScorer','Scorer/CharScorer.pyc')

###### Librerias de red ######
Scrap.PreloadLibrary('Net', 'Net/Net.pyc')

###### Efectos especiales ######
Scrap.PreloadLibrary('Fx', 'FX/Fx.pyc' )

###### Sistema de sonidos ######
Scrap.PreloadLibrary('Sound',         'Sound/Sound.pyc'        )
Scrap.PreloadLibrary('DoorSound',     'Sound/DoorSound.pyc'    )

###### Sistema de personajes ######
Scrap.PreloadLibrary('Chars',     'Chars/Chars.pyc'   )
Scrap.PreloadLibrary('MakeChar',  'Chars/MakeChar.pyc')
Scrap.PreloadLibrary('Speech',    'Chars/Speech.pyc'  )
Scrap.PreloadLibrary('CharAct',   'Chars/CharAct.pyc' )

###### Librerias ######
Scrap.PreloadLibrary('Teleport',      'Missions/Teleport.pyc'      )
Scrap.PreloadLibrary('Elevator',      'Missions/Elevator.pyc'      )
Scrap.PreloadLibrary('RaceMaker',     'Missions/RaceMaker.pyc'     )
Scrap.PreloadLibrary('Doors',         'Missions/Doors.pyc'         )
Scrap.PreloadLibrary('Alarm',         'Missions/Alarm.pyc'         )
Scrap.PreloadLibrary('MisItems',      'Missions/MisItems.pyc'      )
Scrap.PreloadLibrary('Traffic',       'Missions/Traffic.pyc'       )
Scrap.PreloadLibrary('Scene',         'Missions/Scene.pyc'         )
Scrap.PreloadLibrary('Challenge',     'Missions/Challenge.pyc'     )
Scrap.PreloadLibrary('MissionsFuncs', 'Missions/MissionsFuncs.pyc' )
Scrap.PreloadLibrary('Metro',         'Missions/Metro.pyc'         )


def LoadCharLib(filename):
	Scrap.PreloadLibrary(filename,        'Chars/'+filename+'.pyc' )
	filename = filename+"Sound"
	Scrap.PreloadLibrary(filename,        'Sound/'+filename+'.pyc')

if not InMapSkip:  # no es interiores
	###### Armas de naves preparadas para red ######
	Scrap.PreloadLibrary('Weapons',   'Weapons/Weapons.pyc'   )
	Scrap.PreloadLibrary('Vulcan',    'Weapons/Vulcan.pyc'    )
	Scrap.PreloadLibrary('Swarm',     'Weapons/Swarm.pyc'     )
	Scrap.PreloadLibrary('Tesla',     'Weapons/Tesla.pyc'     )
	Scrap.PreloadLibrary('Cloud',     'Weapons/Cloud.pyc'     )
	Scrap.PreloadLibrary('Sonic',     'Weapons/Sonic.pyc'     )
	Scrap.PreloadLibrary('EMI',       'Weapons/EMI.pyc'       )
	Scrap.PreloadLibrary('Devastator','Weapons/Devastator.pyc')
	Scrap.PreloadLibrary('ATPC',      'Weapons/ATPC.pyc'      )
	Scrap.PreloadLibrary('Inferno',   'Weapons/Inferno.pyc'   )
	Scrap.PreloadLibrary('Laser',     'Weapons/Laser.pyc'     )
	###### Naves y afines ######
	Scrap.PreloadLibrary('Vehicles',     'Vehicles/Vehicles.pyc'     )
	Scrap.PreloadLibrary('ShipMaker',    'Vehicles/ShipMaker.pyc'    )
	Scrap.PreloadLibrary('OutMap',       'Vehicles/OutMap.pyc'       )
	Scrap.PreloadLibrary('VehiclesNPC',  'Vehicles/VehiclesNPC.pyc'  )
	Scrap.PreloadLibrary('Parking',      'Vehicles/Parking.pyc'      )
	Scrap.PreloadLibrary('Accelerator',  'Vehicles/Accelerator.pyc'  )

	####### scorer solo de exteriores ######
	Scrap.PreloadLibrary('RacerScorer','Scorer/RacerScorer.pyc')

	#######  Sputnick y sus naves  #######
	LoadCharLib('Sputnik')
	Scrap.PreloadLibrary('SputnikInterface', 'ShipEdit/SputnikInterface.pyc'  )

	#######  sonidos de exteriores  #######
	Scrap.PreloadLibrary('OutSound',      'Sound/OutSound.pyc'     )

	###### mas misiones de exteriores ######
	Scrap.PreloadLibrary('OutPolice',     'Missions/OutPolice.pyc' )
	Scrap.PreloadLibrary('PhoneCab',      'Missions/PhoneCab.pyc'  )

	###### Sistema de edicion de naves ######
	Scrap.PreloadLibrary('ShipEdit',  'ShipEdit/ShipEdit.pyc'   )
	Scrap.PreloadLibrary('HangarTab', 'ShipEdit/HangarTab.pyc'  )

	if not OutMapSkip: # tampoco interiores (mapas de edicion de naves)
		Scrap.PreloadLibrary('EnginesTab','ShipEdit/EnginesTab.pyc')
		Scrap.PreloadLibrary('WeaponsTab','ShipEdit/WeaponsTab.pyc')
		Scrap.PreloadLibrary('HullTab',   'ShipEdit/HullTab.pyc'   )

if not OutMapSkip:


	for fn in ('Nurse','Police','Desktop','Gear','Sentinel','Berto',
		'BankDirector','Mayor','GateKeeper','Betty','Dtritus',
		'Bishop','Functionary','Humphrey','PoliceBoss',
		'Messenger','Human','BankMaster'):
		LoadCharLib(fn)

	# logica varias de interiores
	Scrap.PreloadLibrary('CrazyWing',     'Missions/CrazyWing.pyc'     )
	Scrap.PreloadLibrary('Bureaucracy',   'Chars/Bureaucracy.pyc'      )
	Scrap.PreloadLibrary('CharsNPC',      'Chars/CharsNPC.pyc'         )
	Scrap.PreloadLibrary('InMap',         'Chars/InMap.pyc'            )
	Scrap.PreloadLibrary('InTraffic',     'Vehicles/InTraffic.pyc'     )
	Scrap.PreloadLibrary('DTritusDesktop','Missions/DTritusDesktop.pyc')

	# Sistema de misiones para single player
	Scrap.PreloadLibrary('InPolice',      'Missions/InPolice.pyc'      )
	Scrap.PreloadLibrary('CharConversor', 'Missions/CharConversor.pyc' )

	Scrap.PreloadLibrary('NewsPanel', 'Missions/NewsPanel.pyc' )

else: # debo cargar si es un mapa exterior solo mi personaje...
	LoadCharLib(Scrap.GetSaveVar("Char"))

if Scrap.Get("SplitScreen") != 0 or (Scrap.Get("isXbox") and UpperMap in ("MENU","SHIPEDIT")):
	Scrap.PreloadLibrary('Split','Split/Split.pyc')
	SplitModeGameMod = Scrap.Get("ServerType")
	Scrap.PreloadLibrary('S'+SplitModeGameMod,'Split/S'+SplitModeGameMod+'.pyc')
	import Split
	Split.ModLib = __import__('S'+SplitModeGameMod)


if not OffLineGame:
	Scrap.PreloadLibrary('Chat','Scorer/Chat.pyc')
	Scrap.PreloadLibrary('Ffa', 'Net/Ffa.pyc')

	# cargar la libreria del tipo de juego...
	import Ffa
	GameLibName = "N"+Scrap.Get("ServerType")
	if not Scrap.FileExist('Scripts/Net/'+GameLibName+'.pyc') and not Scrap.FileExist('Scripts/Net/'+GameLibName+'.py'):
		GameLibName = "NDeathMatch"

	Scrap.PreloadLibrary(GameLibName, 'Net/'+GameLibName+'.pyc')
	Ffa.ModLib = __import__(GameLibName)


if ExtraExecs.has_key(UpperMap):
	for func in ExtraExecs[UpperMap]:
		apply(apply,func)


isDemo     = Scrap.Get("isDemo")

Path       = "" # el path del mapa actual
Outdoor    = 1  # 1 si el mapa es exterior 0 si es interior. En red debe ser 1
inMainMenu = 0  # 1 si el mapa no es mas que una miserable demo si graficos ni nada
isShipEdit = 0  # 1 si el mapa es el edicion de naves. inMainMenu = 0 Outdoor = 1 para que sea valido
isJunkYard = 0  # 1 en el caso particular del mapa junkyard
OutArea    = "DownTown" # este es el mapa exterior en el que se encuentra (si esta en un interior) no vale para exteriores ni mapa del chatarrero.
isScrapYard = 0

XboxSavingMsgTime = 3.5

if (HasSuperDeal):
	Scrap.PreloadLibrary(sDealType, 'SuperDeals/' + sDealType + '.pyc' )
	SuperDealModule = __import__(sDealType)

######## Maplibs functions ########
MapLibs = [] # esta es la lista de las librerias propias del mapa. Se especifican para su inicializacion

# agrega una libreria a la lista de librerias del mapa
def AddMLib(library):
	global MapLibs
	MapLibs.append(library)

def MLibInitStatus(LevelPath):
	global MapLibs

	for lib in MapLibs:
		lib.InitStatus(LevelPath)

def MLibInit(LevelPath):
	global MapLibs

	for lib in MapLibs:
		lib.Init(LevelPath)

def isMission():
	import string
	return string.upper(Scrap.GetSaveVar("Mission.Map")) ==  string.upper(Scrap.GetLevelPath()[7:])

def PreloadMlibs(LevelPath):
	import Map

	if isMission():
		Map.Libraries.append(Scrap.GetSaveVar("Mission.Library"))

	if "Libraries" in dir(Map):
		for LibName in Map.Libraries:
			Scrap.PreloadLibrary(LibName,LibName+'.pyc')
			AddMLib(__import__(LibName))


Arrows = "Models/Misc/Action/Action","Models/Misc/MMission/MMission","Models/Misc/SMission/SMission","Models/Misc/MMission/BMMission","Models/Misc/SMission/BSMission"

Scrap.Set("ArrowUseFile",        Arrows[0])
Scrap.Set("ArrowMissionFile",    Arrows[1])
Scrap.Set("ArrowTargetFile",     Arrows[2])

def SetArrowSize():
	global Arrows
	for varnam in Arrows:
		Nam = varnam
		Scrap.Preload3DObject(Nam+".M3D",1,1,1)
		Scrap.PreloadAnm(Nam+".M3D",Nam+".anim.M3D")

####################################
##  Initialization routines
####################################
def Init(LevelPath):
	global Path
	global Outdoor
	global inMainMenu
	global isShipEdit

	# graba el path
	Path = LevelPath

	# load default libraries
	import sys
	sys.path.append(LevelPath+"/Scripts")
	Scrap.OpenPack(LevelPath+"/Scripts")
	Scrap.PreloadLibrary('Map','Map.pyc')
	Scrap.PreloadLibrary('MapSnd','MapSnd.pyc')
	PreloadMlibs(LevelPath)
	Scrap.ClosePack()

	if Scrap.Get("IsXbox") and not Scrap.Get("ShowCredits") and UpperMap in ("SHIPEDIT","MENU"):
		Scrap.PreloadLibrary('XboxMenu',       'Scripts/Scorer/XboxMenu.pyc')
		AddMLib(__import__('XboxMenu'))

	import Map
	import MapSnd

	# Load map Status
	Map.InitStatus(LevelPath)
	MLibInitStatus(LevelPath)

	###################################################################
	# Para arreglar el que se vea a la nave del jefe de policia dando #
	# rulos por ahн despuйs de muerto y no tener que hacer cambios en #
	# todos los scripts de exteriores.                                #
	###################################################################
	ga = Scrap.GetSaveVar("GameAct")
	if (ga != "Prologue" and ga != "1stMurder"):
		import string
		cad = Scrap.GetSaveVar("Traffic.AcShips")
		if (cad and string.find(cad, "SPoliBoss1") != -1):
			import Traffic
			cad = string.replace(cad, "SPoliBoss1", "SPoli6", 1)
			Scrap.SetSaveVar("Traffic.AcShips", cad)
			Traffic.AcShips = eval(cad)
	#######################################################


	if (SuperDealModule):
		SuperDealModule.InitStatus(LevelPath)

	# modifica el tamaсo de las flechas de mision
	if not inMainMenu and not isShipEdit:
		SetArrowSize()

	#inicializaciуn AI
	SAI.IniAI(LevelPath, Outdoor)

	# initialize the language
	#Scrap.SetLanguage("English")

	# Initialize menu
	Scrap.Set("EscapeEvent","Menu.Init")
	import Menu; Menu.Initialize()

	# Assign Mission Info callback func
	if Scrap.GetNetFlags()==(0,0,0):
		Scrap.Set("MainMissionEvent", "MissionsFuncs.ShowMissionInfo")
	else:
		Scrap.Set("MainMissionEvent", "Ffa.ShowHelp")

	if not OffLineGame:
		# Initialize chat system
		import Chat;Chat.SetChatProc();

	# Initialize the sound system
	import Sound;Sound.Init()

	# elementos decorativos
	Scrap.CreateElements()

	if not inMainMenu:
		if not Outdoor:
			import Bureaucracy; Bureaucracy.Init()

		if UpperMap in SUPERDEALSMAPS or MultiPlayer:
			Scrap.Set("isActionMusic",1)

		# Initialize Character Controller (en exteriores al menos se carga un set para el single player, nada para el multi)
		if not isShipEdit and not MultiPlayer:
			import Chars; Chars.Init()
			if (not isJunkYard):
				if (Outdoor):
					import PhoneCab
					PhoneCab.CreatePhoneCabClass()
					PhoneCab.CreateAudioComClass()

		#else:
		#	Scrap.SetMoney(1000000)

		if Outdoor or isJunkYard: # lo que son interiores no cargan nada de esto (exepto Junkyard)
			# Initialize Vehicle Controller
			import Vehicles;Vehicles.Init()

			# Initialize Weapons Controller
			import Weapons;Weapons.Init()

		# Initialize Special FX Controller (generico para exteriores e interiores)
		import Fx;Fx.Init()

		if not isShipEdit:

			# sistema de alarma
			import Alarm;Alarm.Init()

			# Items propios de las misiones
			import MisItems;MisItems.Init()

		# puertas y ventanas
		import Doors;Doors.Init()

		if not isShipEdit:
			# Set de los mapas ya sean exteriores o interiores.
			if Outdoor:
				import OutMap;OutMap.Init(LevelPath)
			else:
				import InMap;InMap.Init(LevelPath)

			if not MultiPlayer:
				import SaveGame
				SaveGame.InitVars()

				import MissionsFuncs;MissionsFuncs.Init()


	###Scrap.Set( "VideoGammaRGB", 1.0 )

	if (Outdoor and Scrap.GetSaveVar("CreateBertos") == "1" and UpperMap != "GDB" and not HasSuperDeal):
		import MissionsFuncs, Parking
		MissionsFuncs.CreateBertos()
		Parking.SwitchVehicleMissionCallbackAux = MissionsFuncs.ReassignBertosPlayerTarget
		Parking.SwitchCharMissionCallbackAux = MissionsFuncs.ReassignBertosPlayerTarget

	if (Scrap.GetSaveVar("RobotsControlledByBoss") == "1"):

		if (Scrap.GetSaveVar("MercsHelpDtritus") == "1"):
			Scrap.SetSaveVar("MercFriends.MercenaryA_Smartie", "1")
			Scrap.SetSaveVar("MercFriends.MercenaryC_Brutus",  "1")
			Scrap.SetSaveVar("MercFriends.MercenaryB_Dumber",  "1")

		if UpperMap in eval(Scrap.GetSaveVar("ComSatsMissionsMapsFinished")):
			Scrap.Set("AlarmFallDelta", -0.05)
			Scrap.SetAlarm(0)
		else:
			Scrap.SetAlarm(1)
			Scrap.Set("AlarmFallDelta",0)

	Scrap.Set("OnCrazyDealFinished", "MissionsFuncs.OnCrazyDealFinishedMessage")
	Scrap.Set("OnCrazyDealTarget", "MissionsFuncs.OnCrazyDealTarget")

	# initialize the map
	Map.Init(LevelPath)
	MapSnd.Init(LevelPath)
	MLibInit(LevelPath)
	if (SuperDealModule):
		SuperDealModule.Init(LevelPath)

	Scrap.AddScheduledFunc(Scrap.GetTime() + 0.5, SetMapLabelText, ())

	if (isDemo and Scrap.GetSaveVar("Player.NumLives") == "-1"):
		Scrap.SetSaveVar("Player.NumLives", "0")

	Scrap.Set("R_SceneBlurValue",0)

	if OffLineGame and not inMainMenu and not isShipEdit:
		Scrap.CreateSaveVar("GameSkill",  "1")
		Scrap.Set("GameSkill",int(Scrap.GetSaveVar("GameSkill")))
	print "Actual Level at : ",LevelPath


def SetMapLabelText():

	import Scorer

	vis = SScorer.Get(0, Scorer.MissionScorerName, "Visible")
	if (vis and vis == 1):
		status = SScorer.Get(0, Scorer.MissionScorerName, "Status0")
		if (status != 1 or (status == 1 and Scrap.GetSaveVar("Mission.Map") == Scrap.GetLevelPath()[7:])):
			SScorer.SetLabelText(Scrap.GetLangStr("Station_" + Scrap.GetLevelPath()[7:]), Scrap.GetTime() + 10)


# Scrap.CreateSaveVar("Mission01","Searching")
# Scrap.CreateSaveVar("Mission01.Objetive","BadGuy")
# Scrap.GetSaveVar("Mission01")
# Scrap.DelSaveVars("Mission01.")
# Scrap.SetSaveVar("Mission01","Eliminate")
# Scrap.SaveGameVars("Save/Save01.sav")
# Scrap.LoadGameVars("Save/Save01.sav")



####################################
##  Closing routines
####################################

PROGRESSBAR_PC = {
	"MENU":200,
	"ORBIT":1070,
	"SCRAPYARD":1693,
	"BANK":1641,
	"JUNKYARD":1434,
	"SHIPEDIT":1265,
	"DOWNTOWN":1745,
	"OUTSKIRTS":1775,
	"GAMBLINDEN":1252,
	"COMMERCIAL":1790,
	"FAKE":1462,
	"PRESS":1691,
	"POLICE":1764,
	"TEMPLE":1382,
	"TOWNHALL":1742,
	"AB":1366,
	"ABINDOOR":868,
	"QF":1474,
	"GDB":1517,
	"FZ":1488,
	"OM":1537,
	"CA":1487,
	"MCA":1553,
	"MCB":1553,
	"MDA":1553,
	"MDB":1553,
	"MOA":1553,
	"MOB":1553,
	"MSA":1553,
	"MSB":1553,
}

PROGRESSBAR_XBOX = {
	"MENU":200,
	"ORBIT":845,
	"SCRAPYARD":1189,
	"BANK":1327,
	"JUNKYARD":990,
	"SHIPEDIT":589,
	"DOWNTOWN":1208,
	"OUTSKIRTS":1182,
	"GAMBLINDEN":995,
	"COMMERCIAL":1214,
	"FAKE":1208,
	"PRESS":1448,
	"POLICE":1533,
	"TEMPLE":1162,
	"TOWNHALL":1539,
	"AB":844,
	"ABINDOOR":690,
	"QF":968,
	"GDB":964,
	"FZ":975,
	"OM":1014,
	"CA":953,
	"MCA":1042,
	"MCB":1016,
	"MDA":1046,
	"MDB":1048,
	"MOA":945,
	"MOB":985,
	"MSA":987,
	"MSB":857,
}

def Close():
	# Guarda el nъmero de ficheros a leer en el siguiente nivel
	UpperMap = string.upper(Scrap.GetNewLevelPath()[7:])
	print "Next level: %s" % UpperMap

	PROGRESSBAR = ""
	if Scrap.Get("IsXbox") == 1 :
		PROGRESSBAR = PROGRESSBAR_XBOX
	else :
		PROGRESSBAR = PROGRESSBAR_PC

	if PROGRESSBAR.has_key(UpperMap):
		Scrap.Set("ProgressBar", PROGRESSBAR[UpperMap])
	else:
		Scrap.ConsoleError("ERROR: '%s' progress bar info not found \n" % UpperMap)
		Scrap.Set("ProgressBar", Scrap.Def("ProgressBar"))
