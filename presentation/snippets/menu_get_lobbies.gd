func get_lobbies() -> void:
	print("Requesting lobby list")
	Steam.addRequestLobbyListDistanceFilter(Steam.LOBBY_DISTANCE_FILTER_WORLDWIDE) # Get ALL lobbies
	Steam.addRequestLobbyListStringFilter("game", "GodotCootiesMPTutorial", Steam.LobbyComparison.LOBBY_COMPARISON_EQUAL)
	Steam.requestLobbyList()
