	object_const_def
	const VIRIDIANFORESTGATESOUTH_LASS
	const VIRIDIANFORESTGATESOUTH_TWIN

ViridianForestGateSouth_MapScripts:
	def_scene_scripts

	def_callbacks

VirdianForestGateSouthLassScript:
	jumptextfaceplayer VirdianForestGateSouthLassText

VirdianForestGateSouthLassText:
	text "Are you going to"
	line "VIRIDIAN FOREST?"
	
	para "Be careful, it's"
	line "a natural maze!"
	done

VirdianForestGateSouthTwinScript:
	jumptextfaceplayer VirdianForestGateSouthTwinText

VirdianForestGateSouthTwinText:
	text "RATTATA may be"
	line "small, but its"
	cont "bite is wicked!"
	
	para "Did you get one?"
	done



ViridianForestGateSouth_MapEvents:
	db 0, 0 ; filler

	def_warp_events
	warp_event  4,  7, ROUTE_2, 6
	warp_event  5,  7, ROUTE_2, 6
	warp_event  4,  0, VIRIDIAN_FOREST, 1
	warp_event  5,  0, VIRIDIAN_FOREST, 2

	def_coord_events

	def_bg_events

	def_object_events
	object_event  9,  4, SPRITE_LASS, SPRITEMOVEDATA_STANDING_LEFT, 0, 0, -1, -1, PAL_NPC_BLUE, OBJECTTYPE_SCRIPT, 0, VirdianForestGateSouthLassScript, -1
	object_event  3,  4, SPRITE_LASS, SPRITEMOVEDATA_WALK_UP_DOWN, 0, 2, -1, -1, 0, OBJECTTYPE_SCRIPT, 0, VirdianForestGateSouthTwinScript, -1
