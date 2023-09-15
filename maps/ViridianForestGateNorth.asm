	object_const_def
	const VIRIDIANFORESTGATENORTH_SUPER_NERD
	const VIRIDIANFORESTGATENORTH_GRAMPS

ViridianForestGateNorth_MapScripts:
	def_scene_scripts

	def_callbacks

VirdianForestGateNorthSuperNerdScript:
	jumptextfaceplayer VirdianForestGateNorthSuperNerdText

VirdianForestGateNorthSuperNerdText:
	text "Many #MON live"
	line "only in forests "
	cont "and caves."

	para "You need to look"
	line "everywhere to get"
	cont "different kinds!"
	done

VirdianForestGateNorthGrampsScript:
	jumptextfaceplayer VirdianForestGateNorthGrampsText

VirdianForestGateNorthGrampsText:
	text "Have you noticed"
	line "the bushes on the"
	cont "roadside?"

	para "They can be cut"
	line "down by a special"
	cont "#MON move."
	done

ViridianForestGateNorth_MapEvents:
	db 0, 0 ; filler

	def_warp_events
	warp_event  4,  7, VIRIDIAN_FOREST, 3
	warp_event  5,  7, VIRIDIAN_FOREST, 4
	warp_event  4,  0, ROUTE_2, 7
	warp_event  5,  0, ROUTE_2, 8

	def_coord_events

	def_bg_events
	def_object_events
	object_event  9,  4, SPRITE_SUPER_NERD, SPRITEMOVEDATA_STANDING_LEFT, 0, 0, -1, -1, PAL_NPC_BLUE, OBJECTTYPE_SCRIPT, 0, VirdianForestGateNorthSuperNerdScript, -1
	object_event  1,  6, SPRITE_GRAMPS, SPRITEMOVEDATA_WALK_LEFT_RIGHT, 2, 0, -1, -1, 0, OBJECTTYPE_SCRIPT, 0, VirdianForestGateNorthGrampsScript, -1
