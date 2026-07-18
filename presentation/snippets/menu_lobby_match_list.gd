func _on_lobby_match_list(lobbies: Array) -> void:
	print("Lobbies Found: %s" % lobbies.size())

	for lobby_id: int in lobbies:
		var lobby_name: String = Steam.getLobbyData(lobby_id, "name")
		var lobby_players: int = Steam.getNumLobbyMembers(lobby_id)

		# Create join lobby button
		var lobby_button: Button = Button.new()
		lobby_button.text = "%s - %d players" % [lobby_name, lobby_players]
		lobby_button.name = "lobby_" + str(lobby_id)
		lobby_button.add_to_group("lobby_button")
		lobby_button.pressed.connect(join_lobby.bind(lobby_id))
		lobby_list.add_child(lobby_button)
