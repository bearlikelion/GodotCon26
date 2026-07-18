# Called when this client successfully connects to server
func _on_connected_to_server() -> void:
	print("GLOBAL CONNECTED TO SERVER")
	var local_id: int = multiplayer.get_unique_id()

	# Send our player name to the server
	# The server will sync back to us after receiving our name
	var player_name: String = str(local_id)
	if multiplayer.multiplayer_peer is SteamMultiplayerPeer:
		player_name = SteamInit.steam_name

	Global.players[local_id] = {
		"character": -1,
		"name": player_name,
		"score": 0
	}

	send_player_to_server.rpc_id(1, Global.players[local_id])
