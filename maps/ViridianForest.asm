	object_const_def
	const VIRIDIAN_FOREST_YOUNGSTER
	const VIRIDIAN_FOREST_BUG_CATCHER_1
	const VIRIDIAN_FOREST_BUG_CATCHER_2
	const VIRIDIAN_FOREST_BUG_CATCHER_3
	const VIRIDIAN_FOREST_YOUNGSTER_2
	const VIRIDIAN_FOREST_POKE_BALL_1
	const VIRIDIAN_FOREST_POKE_BALL_2

ViridianForest_MapScripts:
	def_scene_scripts

	def_callbacks

ViridianForestDireHit:
	itemball DIRE_HIT

ViridianForestMaxPotion:
	itemball MAX_POTION

ViridianForestHiddenMaxEther:
	hiddenitem MAX_ETHER, EVENT_VIRIDIAN_FOREST_HIDDEN_MAX_ETHER

ViridianForestHiddenFullHeal:
	hiddenitem FULL_HEAL, EVENT_VIRIDIAN_FOREST_HIDDEN_FULL_HEAL

ViridianForestHiddenFullRestore:
	hiddenitem FULL_RESTORE, EVENT_VIRIDIAN_FOREST_HIDDEN_FULL_RESTORE

ViridianForestHiddenRevive:
	hiddenitem REVIVE, EVENT_VIRIDIAN_FOREST_HIDDEN_REVIVE

ViridianForestYoungsterScript:
	jumptextfaceplayer ViridianForestYoungsterText


TrainerBugCatcherSammy:
	trainer BUG_CATCHER, SAMMY, EVENT_BEAT_BUG_CATCHER_SAMMY, BugCatcherSammySeenText, BugCatcherSammyBeatenText, 0, .Script

.Script:
	endifjustbattled
	opentext
	writetext BugCatcherSammyAfterText
	waitbutton
	closetext
	end

TrainerBugCatcherRicky:
	trainer BUG_CATCHER, RICKY, EVENT_BEAT_BUG_CATCHER_RICKY, BugCatcherRickySeenText, BugCatcherRickyBeatenText, 0, .Script

.Script:
	endifjustbattled
	opentext
	writetext BugCatcherRickyAfterText
	waitbutton
	closetext
	end

TrainerBugCatcherJose:
	trainer BUG_CATCHER, JOSE, EVENT_BEAT_BUG_CATCHER_JOSE, BugCatcherJoseSeenText, BugCatcherJoseBeatenText, 0, .Script

.Script:
	endifjustbattled
	opentext
	writetext BugCatcherJoseAfterText
	waitbutton
	closetext
	end

ViridianForestYoungster2Script:
	jumptextfaceplayer ViridianForestYoungster2Text

ViridianForestSign1Script:
	jumptext ViridianForestSign1Text

ViridianForestSign2Script:
	jumptext ViridianForestSign2Text

ViridianForestSign3Script:
	jumptext ViridianForestSign3Text

ViridianForestYoungsterText:
	text "I came here with"
	line "some friends!"

	para "They're out for"
	line "#MON fights!"
	done

BugCatcherSammySeenText:
	text "Hey! You have"
	line "#MON! Come on!"
	cont "Let's battle'em!"
	done

BugCatcherSammyBeatenText:
	text "No!"
	line "BUTTERFREE can't"
	cont "cut it!"
	prompt

BugCatcherSammyAfterText:
	text "Ssh! You'll scare"
	line "the bugs away!"
	done

BugCatcherRickySeenText:
	text "Yo! You can't jam"
	line "out if you're a"
	cont "#MON trainer!"
	done

BugCatcherRickyBeatenText:
	text "Huh?"
	line "I ran out of"
	cont "#MON!"
	prompt

BugCatcherRickyAfterText:
	text "Darn! I'm going"
	line "to catch some"
	cont "stronger ones!"
	done

BugCatcherJoseSeenText:
	text "Hey, wait up!"
	line "What's the hurry?"
	done

BugCatcherJoseBeatenText:
	text "I"
	line "give! You're good"
	cont "at this!"
	prompt

BugCatcherJoseAfterText:
	text "Sometimes, you"
	line "can find stuff on"
	cont "the ground!"

	para "I'm looking for"
	line "the stuff I"
	cont "dropped!"
	done

ViridianForestYoungster2Text:
	text "I ran out of #"
	line "BALLs to catch"
	cont "#MON with!"

	para "You should carry"
	line "extras!"
	done

ViridianForestSign1Text:
	text "TRAINER TIPS"

	para "If you want to"
	line "avoid battles,"
	cont "stay away from"
	cont "grassy areas!"
	done

ViridianForestSign2Text:
	text "TRAINER TIPS"

	para "No stealing of"
	line "#MON from"
	cont "other trainers!"
	cont "Catch only wild"
	cont "#MON!"
	done

ViridianForestSign3Text:
	text "LEAVING"
	line "VIRIDIAN FOREST"
	cont "PEWTER CITY AHEAD"
	done


ViridianForest_MapEvents:
	db 0, 0 ; filler

	def_warp_events
	warp_event 16, 47, VIRIDIAN_FOREST_GATE_SOUTH, 3
	warp_event 17, 47, VIRIDIAN_FOREST_GATE_SOUTH, 4
	warp_event  1,  5, VIRIDIAN_FOREST_GATE_NORTH, 1


	def_coord_events

	def_bg_events
	bg_event 16, 36, BGEVENT_READ, ViridianForestSign1Script
	bg_event 26, 21, BGEVENT_READ, ViridianForestSign2Script
	bg_event  4, 28, BGEVENT_READ, ViridianForestSign3Script
	bg_event 30,  7, BGEVENT_ITEM, ViridianForestHiddenMaxEther
	bg_event 19,  7, BGEVENT_ITEM, ViridianForestHiddenFullHeal
	bg_event 17, 45, BGEVENT_ITEM, ViridianForestHiddenFullRestore
	bg_event  7, 37, BGEVENT_ITEM, ViridianForestHiddenRevive

	def_object_events
	object_event 20, 44, SPRITE_YOUNGSTER, SPRITEMOVEDATA_STANDING_DOWN, 0, 0, -1, -1, PAL_NPC_GREEN, OBJECTTYPE_SCRIPT, 0, ViridianForestYoungsterScript, -1
	object_event 32, 33, SPRITE_BUG_CATCHER, SPRITEMOVEDATA_STANDING_LEFT, 0, 0, -1, -1, 0, OBJECTTYPE_TRAINER, 1, TrainerBugCatcherSammy, -1
	object_event 18, 22, SPRITE_BUG_CATCHER, SPRITEMOVEDATA_STANDING_LEFT, 0, 0, -1, -1, 0, OBJECTTYPE_TRAINER, 4, TrainerBugCatcherRicky, -1
	object_event  2, 18, SPRITE_BUG_CATCHER, SPRITEMOVEDATA_STANDING_LEFT, 0, 0, -1, -1, 0, OBJECTTYPE_TRAINER, 1, TrainerBugCatcherJose, -1
	object_event 27, 40, SPRITE_YOUNGSTER, SPRITEMOVEDATA_STANDING_LEFT, 0, 0, -1, -1, PAL_NPC_BLUE, OBJECTTYPE_SCRIPT, 0, ViridianForestYoungster2Script, -1
	object_event 26,  5, SPRITE_POKE_BALL, SPRITEMOVEDATA_STILL, 0, 0, -1, -1, 0, OBJECTTYPE_ITEMBALL, 0, ViridianForestDireHit, EVENT_VIRIDIAN_FOREST_DIRE_HIT
	object_event 12, 33, SPRITE_POKE_BALL, SPRITEMOVEDATA_STILL, 0, 0, -1, -1, 0, OBJECTTYPE_ITEMBALL, 0, ViridianForestMaxPotion, EVENT_VIRIDIAN_FOREST_MAX_POTION
