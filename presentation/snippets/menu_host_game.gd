func _on_host_game_pressed() -> void:
	match backend.selected:
		MultiplayerBackend.ENET:
			print("Creating ENET Server")
			var peer: ENetMultiplayerPeer = ENetMultiplayerPeer.new()
			var error: Error = peer.create_server(7777, 4)
			if error:
				print("Server Error: %s" % error)
			else:
				multiplayer.multiplayer_peer = peer
				Global.add_local_player()
				Global.change_level("res://Scenes/Lobby/lobby.tscn")
		MultiplayerBackend.STEAM:
			print("Hosting Steam Lobby")
			Steam.createLobby(Steam.LobbyType.LOBBY_TYPE_PUBLIC, 4)
