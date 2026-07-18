# Set player character selection via RPC
@rpc("any_peer", "call_local", "reliable")
func set_player_character(peer_id: int, character_index: int) -> void:
	# Reject peers attempting to change another player's character
	var sender: int = multiplayer.get_remote_sender_id()
	if sender != 0 and sender != peer_id:
		return

	if players.has(peer_id):
		players[peer_id]["character"] = character_index
		player_info_updated.emit(peer_id)
