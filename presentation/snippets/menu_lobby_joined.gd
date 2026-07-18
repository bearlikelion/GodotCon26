func _on_lobby_joined(lobby_id: int, _permissions: int, _locked: bool, response: int) -> void:
	if response != Steam.CHAT_ROOM_ENTER_RESPONSE_SUCCESS:
# [...]
	if Steam.getLobbyOwner(lobby_id) == Steam.getSteamID():
		Global.change_level("res://Scenes/Lobby/lobby.tscn")
		return

	SteamInit.lobby_id = lobby_id
	SteamInit.peer.connect_to_lobby(lobby_id)
	multiplayer.multiplayer_peer = SteamInit.peer

	# Wait for player data to sync from server before entering the lobby
	connection_status.text = "Connecting..."
	multiplayer.connection_failed.connect(_on_connection_failed, CONNECT_ONE_SHOT)
	Global.players_synced.connect(_on_players_synced, CONNECT_ONE_SHOT)
