import Scrap
import SInput
import SNet
import SWeap
import SScorer
import SSound
import SVec
import SAct
import sys



def log(msg):
	Scrap.Print("[STRNG][Police] " + str(msg) + "\n")


# WARNING : Never import any pyhton source library at the start up!

FXPoliceStealFile		= "Models/GFX/Police/PoliceSteal.M3D"
FXPoliceGearConversionFile 	= "Models/GFX/Police/Conversion.M3D"

def LoadSirenActs():

	# inicio de la sirena
	SAct.CreateAction("SirenInit")
	SAct.SetAct("isLoop",0)
	SAct.SetAct("Chanel",1)
	SAct.SetAct("AnmFilePath","Models/Chars/Police/Anm/Police_SirenInit.M3D")

	SAct.SetAct("AddEventAtTime",SAct.GetAct("AnmTotalTime"))
	SAct.SetAct("EventName","Siren")
	SAct.SetAct("EventFunc","!AnmSetAction")

	SAct.SetAct("AddEventAtTime",SAct.GetAct("TimeOfFrame"+"6"))
	SAct.SetAct("EventName","FXPoliceAlarmInit")
	SAct.SetAct("EventFunc","!FXPoliceAlarmInit")


	# loop de la sirena
	SAct.CreateAction("Siren")
	SAct.SetAct("isLoop",1)
	SAct.SetAct("Chanel",1)
	SAct.SetAct("AnmFilePath","Models/Chars/Police/Anm/Police_Siren.M3D")
	SAct.SetAct("MaxSpeed",1.3)
	SAct.SetAct("MinSpeed",1.4)


	# final de la sirena
	SAct.CreateAction("SirenEnd")
	SAct.SetAct("isLoop",0)
	SAct.SetAct("Chanel",1)
	SAct.SetAct("AnmFilePath","Models/Chars/Police/Anm/Police_SirenEnd.M3D")

	SAct.SetAct("AddEventAtTime",SAct.GetAct("TimeOfFrame"+"65"))
	SAct.SetAct("EventName","FXPoliceAlarmEnd")
	SAct.SetAct("EventFunc","!FXPoliceAlarmEnd")


def Init():
	import MakeChar, Init, string

	MakeChar.InitChar       ("Police")

	# ajustes varios de velocidad
	MakeChar.MaxSpeed = 1.2
	MakeChar.MinSpeed = 0.6

	MakeChar.AddRelaxActions("Police",0)
	SAct.GetAction("Relax0")
	SAct.SetAct("anmConeView",1)

	MakeChar.AddWalkActions ("Police",360,1)
	MakeChar.AddFallAction  ("Police",45,1,0)
	MakeChar.AddDazeAction  ("Police")
	MakeChar.AddTalkAction  ("Police",nExtraActions=3)
	MakeChar.AddDiscover    ("Police")
	MakeChar.AddInitWalkActions("Police",360,0,1,["StrLeftInit","StrRightInit"])

	MakeChar.AddFlashedAction("Police")
	MakeChar.AddCrazyAction  ("Police")

	SAct.GetCls("Police")
	SAct.SetCls("WRadius",69)         # Radio de colision con el mundo
	SAct.SetCls("VRadius",60)         # Radio de colision con el mundo
	SAct.SetCls("SRadius",20)         # Radio de la capsula de soporte

	SAct.SetCls("MinFallDist",20)     # tamaño maximo que acepta como escalon para las caidas



	#### Lista de modificadores de nodos del policia ####
	SAct.SetCls("Node0Name","Bip PoliceNoArmor Head")       # Cabeza
	SAct.SetCls("Node1Name","Bip PoliceNoArmor Spine1")     # Tronco

	# Relax
	MakeChar.SetNodeRotation(0,0,   25,   50)  # Cabeza
	MakeChar.SetNodeRotation(0,1,   25,   50)  # Tronco

	#### Cuando le dan en la cabeza, la sirena se hunde
	SAct.GetAction("DazedInit")
	SAct.SetAct("AddEventAtTime",SAct.GetAct("AnmTotalTime"))
	SAct.SetAct("EventName","AbortSiren")
	SAct.SetAct("EventFunc","Police.AbortSiren")

	#### Acciones Extra ####

	# animavion de andandara
	MakeChar.CreateRelaxAction("Police",90,"AlertCheck","Relax0")
	SAct.GetAction("AlertCheck")
	SAct.SetAct("anmConeView",1)

	for ActName in (("",0),("NPC",360)):
		# try get money
		SAct.CreateAction("ActionInit"+ActName[0])
		SAct.SetAct("AnmFilePath","Models/Chars/Police/Anm/Police_ActionInit.M3D")
		SAct.SetAct("isLoop",0)
		SAct.SetAct("RotSpeed",ActName[1])
		SAct.SetAct("UseDisp",0)
		SAct.SetAct("PriorityLevel",100)

		# evento de "Te succiono el dinero"
		SAct.SetAct("AddEventAtTime",0.3)
		SAct.SetAct("EventName","PoliceRestoreFreeTurn")
		SAct.SetAct("EventFunc","!PoliceRestoreFreeTurn")
		SAct.SetAct("EventDiscardable",0)

		# trying to get money
		SAct.CreateAction("Action"+ActName[0])
		SAct.SetAct("AnmFilePath","Models/Chars/Police/Anm/Police_Action.M3D")
		SAct.SetAct("isLoop",1)
		SAct.SetAct("RotSpeed",ActName[1])
		SAct.SetAct("UseDisp",0)
		SAct.SetAct("PriorityLevel",101)

		# evento de "Te succiono el dinero"
		SAct.SetAct("AddEventAtTime",SAct.GetAct("AnmTotalTime")*1.5)
		SAct.SetAct("EventName","ShowMeTheMoney")
		SAct.SetAct("EventFunc","!PoliceEndActionMoney")


	# Bad luck getting money
	SAct.CreateAction("ActionBad")
	SAct.SetAct("AnmFilePath","Models/Chars/Police/Anm/Police_ActionBad.M3D")
	SAct.SetAct("isLoop",0)
	SAct.SetAct("RotSpeed",0)
	SAct.SetAct("UseDisp",0)
	SAct.SetAct("PriorityLevel",101)

	# Bad luck getting money
	SAct.CreateAction("ActionOK")
	SAct.SetAct("AnmFilePath","Models/Chars/Police/Anm/Police_ActionOK.M3D")
	SAct.SetAct("isLoop",0)
	SAct.SetAct("RotSpeed",0)
	SAct.SetAct("UseDisp",0)
	SAct.SetAct("PriorityLevel",101)

	# We laugh, and cry too
	SAct.CreateAction("Laugh")
	SAct.SetAct("AnmFilePath","Models/Chars/Police/Anm/Police_Laugh.M3D")
	SAct.SetAct("isLoop",0)
	SAct.SetAct("RotSpeed",360)
	SAct.SetAct("UseDisp",0)
	SAct.SetAct("PriorityLevel",102)
	SAct.SetAct("NodeModifier",-1)
	SAct.SetAct("AngleModifierSpeed",1.0)
	SAct.SetAct("AutoFaceSpeed",  10)
	SAct.SetAct("AutoFaceOffsetH", 0)
	SAct.SetAct("AutoFaceOffsetV", 0)

	import Init
	if not Init.Outdoor:
		# Police Fusion
		SAct.CreateAction("Fusion")
		SAct.SetAct("AnmFilePath","Models/Chars/Police/Anm/Police_Fusion.M3D")
		SAct.SetAct("isLoop",0)
		SAct.SetAct("PriorityLevel",200)

		# evento de conversión de Policia en Gear
		SAct.SetAct("AddEventAtTime",0)
		SAct.SetAct("EventName","FusionInit")
		SAct.SetAct("EventFunc","!FXPoliceGearConversion")
		SAct.SetAct("EventDiscardable",0)

		# evento de cambiazo efectivo y brutal!
		SAct.SetAct("AddEventAtTime",SAct.GetAct("AnmTotalTime"))
		SAct.SetAct("EventName","FusionInit")
		# SAct.SetAct("EventFunc","Police.GotGear")
		SAct.SetAct("EventFunc","!Police2GearEnd")
		SAct.SetAct("EventDiscardable",0)


		SAct.CreateAction("ActionFusion")
		SAct.SetAct("AnmFilePath","Models/Chars/Police/Anm/Police_Fusion.M3D")
		SAct.SetAct("isLoop",0)
		SAct.SetAct("PriorityLevel",200)

		# evento de conversión de Policia en Gear
		SAct.SetAct("AddEventAtTime",0)
		SAct.SetAct("EventName","ActionFusionInit")
		SAct.SetAct("EventFunc","!FXPoliceGearConversion")
		SAct.SetAct("EventDiscardable",0)

		# evento de cambiazo efectivo y brutal!
		SAct.SetAct("AddEventAtTime",SAct.GetAct("AnmTotalTime"))
		SAct.SetAct("EventName","ActionFusionInit")
		# SAct.SetAct("EventFunc","Police.GotGear")
		# SAct.SetAct("EventFunc","!Police2GearEnd")
		SAct.SetAct("EventDiscardable",0)

	if string.upper(Init.Path) == 'LEVELS/GAMBLINDEN':
		#MakeChar.CreateRelaxAction("Police",180,"Dance0",   "Dance0"   )
		MakeChar.CreateRelaxAction("Police",180,"Dance",    "Dance"    )
		SAct.SetAct("isLoop",1)

	LoadSirenActs()
	SAct.SetCls("OnCreate","Police.OnCreate")

	SAct.SetCls("OnFreeResources","Police.OnFreeResources")

	#### Police actions ######
	SAct.SetCls("ActionPress","Police.GetGear")


	##### Police Sounds #####
	import PoliceSound;PoliceSound.Init("Police")

	##### Police Effects #####
	import Fx

	if not Init.OutMapSkip :
		Scrap.Set("FXPoliceStealFile",FXPoliceStealFile)
		Scrap.SetDebrisSys(FXPoliceStealFile,1,0,0,1,0,0,Fx.FXPOLICESTEAL)

		Scrap.Set("FXPoliceGearConversionFile",FXPoliceGearConversionFile)
		Scrap.SetDebrisSys(FXPoliceGearConversionFile,2,0,0,1,0,0,Fx.FXPOLICEGEARCONVERSION)

	##### Police Speech #####
	import Speech
	Speech.SpeechRoutines["Police"] = PoliceSpeech


def OnCreate(EntityName):
	e = Scrap.GetEntity(EntityName)
	e.TgType = "Green"

	import CharAct;CharAct.OnCreate(EntityName)
	import PoliceSound; PoliceSound.InitLoops(EntityName)


def OnFreeResources():
	import Fx

	Scrap.SetDebrisSys(FXPoliceStealFile,0,0,0,1,0,0,Fx.FXPOLICESTEAL)
	Scrap.SetDebrisSys(FXPoliceGearConversionFile,0,0,0,1,0,0,Fx.FXPOLICEGEARCONVERSION)



def AbortSiren(EntityName,EventName,Time):
	char = Scrap.GetEntity(EntityName)
	if char.ActChan1:
		char.Action = "SirenEnd" #cuchuflon!

def GetGear(EntityName):
	me = Scrap.GetEntity(EntityName)
	me.Action = "ActionFusion"
	# changeTime = Scrap.GetTime() + SAct.GetAct("AnmTotalTime") + 0.1
	# Scrap.AddScheduledFunc(changeTime, ChangeToGear, ())


def ChangeToGear():
	import Chars
	# Chars.LoadRes("Gear")
	# Scrap.UsrEntity(0).ActCtrl="Gear"


# def GetGear(EntityName):
# 	import Chars, Menu
# 	global Cam, AuxInterp, newme, me
#
#  	char = Scrap.GetEntity(EntityName)
# 	char.Action = "Fusion"
#
# 	me = Scrap.GetEntity(EntityName)
#
# 	Cam = Scrap.GetEntity(Scrap.GetCam(0))
#
# 	# crea el interpolador intermedio
# 	AuxInterp = Scrap.CreateEntity("AuxInterp",me.Pos[0],me.Pos[1],me.Pos[2],"Obj")
# 	AuxInterp.Ang    = me.ViewAng
#
# 	if me.Name == "PlayerZ":
# 		PlName = "Player0"
# 	else:
# 		PlName = "PlayerZ"
#
# 	newme = Chars.CreateMainChar(PlName,Scrap.GetSaveVar("Char"),me.Pos,me.Ang)
#
# 	AuxInterp.CamTgt      = newme.CamTgt
# 	AuxInterp.MovePos     = newme.Pos
# 	AuxInterp.MoveAng     = newme.ViewAng
# 	AuxInterp.MoveFade    = 3
# 	AuxInterp.MoveTime    = SAct.GetAct('AnmTotalTime')
# 	SAct.GetClass(me.ActCtrl)
# 	Cam.Fov     = SAct.GetCls("FOV")
# 	Cam.CamDist = SAct.GetCls("CamDist")
# 	Cam.CamAng  = SAct.GetCls("CamAng")
# 	Cam.CamRot  = SAct.GetCls("CamRot")
# 	Menu.MovieScorer(0)
# 	SInput.SetActionSet("Inactive")


def GotGear(EntityName, b, c):
	import Chars, Menu, CharScorer
	global Cam, AuxInterp, newme, me

	SInput.SetActionSet("Walk")

	Cam.MainTarget   = Cam.Target = newme.Name
	newme.Energy = me.Energy-1.0
	newme.Life = 100
	newme.UsrControl  = 0

	ActCtrl = me.ActCtrl
	me.Active = 0
	me.ActCtrl = ""
	me.Del()

	Chars.DiscardRes(ActCtrl)
	AuxInterp.Del()
	del Cam
	del AuxInterp
	CharScorer.Create(0)



# comienza a pedir dinero
# def ActionPress(EntityName):
# 	char = Scrap.GetEntity(EntityName)
# 	if not char.isFalling:
# 		char.Action      = "ActionInit"
# 		if char.Action == "ActionInit":
# 			char.DefLoop     = "Action"

# cuando termina el loop de pedir dinero
# def EndActionMoney(EntityName,EventName,Time):
# 	char = Scrap.GetEntity(EntityName)
# 	if not char.ActionPress:
# 		char.ForceDefLoop = "Relax"
# 		char.ForceAction  = "Relax"


# Scrap.GetEntity("DM_Door_Elevator_00").RadarShow = 1

def GoToMission(CharName):
	ch = Scrap.GetEntity(CharName)
	ch.LLogicGotoMainMission = 1

ResState = 0

##
## Rutina de parloteo del Policia
####################################
def PoliceSpeech(UsrName,CharName,optId,FullOption):
	global ResState
	import Speech, Chars, Challenge, Menu, CharsNPC

	ch = Scrap.GetEntity(CharName)
	Speech.PlayerName = UsrName
	Speech.NPCName    = CharName

	charType = "Police"

	if   (optId == "Talk"):
		CharsNPC.CheckActualEntity(CharName)

		if ch.LLogicState==10:
			Speech.OnSpch("Generics_PoliceWereIsGoInitMsg1","Generics_PoliceWereIsGoInitAns1")
		else:
			rndval = apply(Scrap.Rand, (1.0 , 3.9) )

			if (Speech.OnSpch("Generics_" + charType + "_InitMsg1","Generics_" + charType + "_InitAns"+`int(rndval)`)):
				CharsNPC.optionsList, CharsNPC.subOptionsList = CharsNPC.ClassifyOptions(charType)
				Speech.StdAnsLst(CharsNPC.optionsList+["Generics_PoliceWereIs"])
				numOpts  = len(CharsNPC.optionsList)+1
				index = 0

				if (Scrap.GetSaveVar("Player.InfiniteLives") == "0"):
					Challenge.AddChallenge(ch, UsrName, numOpts)

	elif (optId in CharsNPC.optionsList):

		if Speech.OnSpch(optId + "Msg", optId + "Ans"):

			index = CharsNPC.optionsList.index(optId)
			index = index + 1

			CharsNPC.IncludeSubOptions(optId)
			Speech.StdAnsLst(CharsNPC.optionsList+["Generics_PoliceWereIs"])
			numOpts = len(CharsNPC.optionsList)+1
			ch.ArriOpt = index
			if (Scrap.GetSaveVar("Player.InfiniteLives") == "0"):
				Challenge.AddChallenge(ch, UsrName, numOpts)

	elif optId=="Generics_PoliceWereIs":
		ch.LLogicGotoMainMission = 1
		ch.LLogicState           = 0
		ch.LLogicIdle            = 1
		if ch.LLogicPoliceResult == 0:
			Speech.OnSpch("Generics_PoliceWereIsMsg","Generics_PoliceWereIsNo")
			ch.ArriOpt = 0
		else:
			Speech.OnEndOfSpeech = GoToMission
			Speech.OnEndOfSpeechParams = (ch.Name,)
			Speech.OnSpch("Generics_PoliceWereIsMsg","Generics_PoliceWereIsYes")
			Speech.RestoreState(CharName)

	elif optId=="ChallengeRaceStdOpt0":
		if Speech.OnSpch("ChallengeRace" + charType + "Opt1","ChallengeRace" + charType + "Msg1"):
			Challenge.challengeType = "Race"
			Challenge.foeType = charType
			Challenge.SetChallengeOptions(ch)

	elif optId=="ChallengeCombatStdOpt0":
		if Speech.OnSpch("ChallengeCombat" + charType + "Opt1","ChallengeCombat" + charType + "Msg1"):
			Challenge.challengeType = "Combat"
			Challenge.foeType = charType
			Challenge.SetChallengeOptions(ch)

	elif optId=="ChallengeRaceStdOpt1":
		Challenge.OnChallengeOpt(1, ch)

	elif optId=="ChallengeRaceStdOpt2":
		Challenge.OnChallengeOpt(2, ch)

	elif optId=="ChallengeRaceStdOpt3":
		Challenge.OnChallengeOpt(3, ch)

	elif optId=="ChallengeRaceStdOpt4":
		if Speech.OnSpch("ChallengeRaceStdOpt2","ChallengeRace" + charType + "Msg3"):
			Speech.StdAnsLst(CharsNPC.optionsList)
			numOpts  = len(CharsNPC.optionsList)
			Challenge.AddChallenge(ch, UsrName, numOpts)
			index = 0

	elif optId=="GiveWhy": # Preguntarle por que es tan cabron
		if Speech.OnSpch("Generics_PoliceBribeGiveWhyAns","Generics_PoliceBribeGiveWhyMsg"):
			ResState = 0
			ch.ForceAction         = "FaceToTalk"
			ch.ForceDefLoop        = "TalkListenNPC"
			Speech.OnEndOfSpeech   = OnEndOfSpeech
	elif optId=="GiveYes": # darle soborno al policia
		if Scrap.GetMoney()>=Scrap.Get("PoliceStealQuanto"):
			Scrap.SetMoney(Scrap.GetMoney()-Scrap.Get("PoliceStealQuanto"))
			Scrap.SetAlarm(0)
			# pierdes tu preciado dinero
			ResState               = 1
			ch.LLogicState         = 0
			ch.LLogicTarget        = ""
			ch.ForceAction         = "Relax"
			ch.ForceDefLoop        = "Relax"
			if Speech.OnSpch("Generics_PoliceBribeGiveYesAns","Generics_PoliceBribeGiveYesMsg"):
				Speech.OnEndOfSpeech   = OnEndOfSpeech
		else:
			# creo que no puedes pagarle
			if Speech.OnSpch("Generics_PoliceBribeCantDoAns","Generics_PoliceBribeCantDoMsg"):
				ResState               = 0
				ch.ForceAction         = "FaceToTalk"
				ch.ForceDefLoop        = "TalkListenNPC"
				Speech.OnEndOfSpeech   = OnEndOfSpeech
	elif optId=="GiveNo":  # no darle ni una mierda al policia

		if Scrap.Rand(0,100) < 50:
			# se cabrea
			ch = Scrap.GetEntity(Speech.NPCName)
			me = Scrap.GetEntity(Speech.PlayerName)
			if Speech.PlayerAns(me,ch,"Generics_PoliceBribeGiveNoAns",OnEndOfSpeech):
				ResState = -1
				Speech.OnEndOfSpeech   = OnEndOfSpeech
		else:
			# no se cabrea pero te advierte!
			ch.LLogicState         = 0
			ch.LLogicTarget        = ""
			ch.ForceAction         = "Relax"
			ch.ForceDefLoop        = "Relax"
			Speech.OnSpch("Generics_PoliceBribeGiveNoAns","Generics_PoliceBribeGiveNoMsg")
	else:
		print "Error PoliceSpeech(",UsrName,CharName,optId,FullOption,")"
		PoliceSpeech(UsrName,CharName,"Talk",FullOption)


def OnEndOfSpeech():
	import Speech
	ch = Scrap.GetEntity(Speech.NPCName)
	me = Scrap.GetEntity(Speech.PlayerName)

	if ResState==1:
		if (ch):
			ch.ForceAction        = "ActionOK"
		Scrap.SetCallFunc("!FXPoliceSteal")
		Scrap.AddParams(Speech.NPCName)
		Scrap.AddParams(me.Name)
		Scrap.Execute()
	elif ResState==-1:
		if (ch):
			ch.LLogicPoliceResult = -1
		me.ForceAction        = "Relax"
		me.ForceDefLoop       = "Relax"
		me.AutoSelect         = 1
	else:
		if (ch):
			if ch.Action[0:5] == "Relax":
				ch.LLogicIdle         = ResState
				ch.LLogicPoliceResult = ResState
				ch.ForceAction        = "ActionNPC"
				ch.ForceDefLoop       = "ActionNPC"
			ch.SelectedEntity  = Scrap.UsrEntity(0).Name
                                                                                                              
