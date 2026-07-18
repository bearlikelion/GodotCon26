func _on_lobby_created(connected: int, lobby_id: int) -> void:
	if connected == 1:
		print("Created lobby %s" % lobby_id)
		SteamInit.lobby_id = lobby_id
		SteamInit.peer.host_with_lobby(lobby_id) # Use Steam MultiplayerPeer
		multiplayer.multiplayer_peer = SteamInit.peer

		Steam.setLobbyJoinable(lobby_id, true)
		Steam.setLobbyData(lobby_id, "name", Steam.getPersonaName() + "'s lobby")
		Steam.setLobbyData(lobby_id, "game", "GodotCootiesMPTutorial")

		var set_relay: bool = Steam.allowP2PPacketRelay(true)
		print("Allowing Steam to relay backup: %s" % set_relay)

		Global.add_local_player()
