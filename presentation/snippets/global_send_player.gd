@rpc("any_peer", "call_remote", "reliable")
func send_player_to_server(player: Dictionary) -> void:
	if multiplayer.is_server():
		print("SERVER RECEIVED PLAYER DATA")
		var sender_id: int = multiplayer.get_remote_sender_id()
		players[sender_id] = player

		_sync_players_to_peer.rpc_id(sender_id, players)
