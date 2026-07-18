func _ready() -> void:
	# Set player name from Global
	var peer_id: int = int(name)
	if player_name:
		player_name.text = Global.get_player_name(peer_id)

	if not is_multiplayer_authority():
		physics_interpolation_mode = Node.PHYSICS_INTERPOLATION_MODE_ON

	# Server-only infection collision detection
	if multiplayer.is_server() and infection_area:
		infection_area.body_entered.connect(_on_infection_area_body_entered)
