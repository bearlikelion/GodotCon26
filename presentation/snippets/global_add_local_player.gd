# Add local player to the players dictionary (call this after creating server/client)
func add_local_player() -> void:
	var local_id: int = multiplayer.get_unique_id()
	print("GLOBAL ADD LOCAL PLAYER: %d" % local_id)

	# Get player name from Steam if available
	var player_name: String = str(local_id)
	if SteamInit.steam_running and multiplayer.multiplayer_peer is SteamMultiplayerPeer:
		player_name = Steam.getPersonaName()

	if not players.has(local_id):
		players[local_id] = {
			"character": -1,
			"name": player_name,
			"score": 0
		}

	# Broadcast our name to all clients
	set_player_name.rpc(local_id, player_name)

	# Server doesn't need to wait for sync, emit immediately
	if multiplayer.is_server():
		players_synced.emit()
