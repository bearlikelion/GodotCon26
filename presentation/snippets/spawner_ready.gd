func _ready() -> void:
	spawn_function = spawn_player

	multiplayer.peer_disconnected.connect(_on_peer_disconnected)

	# Only the server should spawn players
	if multiplayer.is_server():
		# Spawn all players (including server)
		for peer_id: int in Global.players.keys():
			call_deferred("spawn", peer_id)
