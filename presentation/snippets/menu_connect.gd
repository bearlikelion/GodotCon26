func _on_connect_pressed() -> void:
	var peer: ENetMultiplayerPeer = ENetMultiplayerPeer.new()
	var error: Error = peer.create_client(ip_address.text, 7777)
	if error:
		print("Client Error: %s" % error)
		connection_status.text = "Client Error: %s" % error_string(error)
		return

	Global.ip_address = ip_address.text
	multiplayer.multiplayer_peer = peer

	# Wait for player data to sync from server before entering the lobby
	connection_status.text = "Connecting..."
	multiplayer.connection_failed.connect(_on_connection_failed, CONNECT_ONE_SHOT)
	Global.players_synced.connect(_on_players_synced, CONNECT_ONE_SHOT)
