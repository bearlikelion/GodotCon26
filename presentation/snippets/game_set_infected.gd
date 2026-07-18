# RPC: Set player infection state
@rpc("authority", "call_local", "reliable")
func _set_player_infected(peer_id: int, infected: bool) -> void:
	var player: Player = players_node.get_node_or_null(str(peer_id))
	if player:
		player.set_infected(infected)

	if hud:
		hud.update_infection_display(peer_id, infected)

		# Tell the local player they are it
		if infected and peer_id == multiplayer.get_unique_id() and current_state == GameState.PLAYING:
			hud.show_announcement("You have cooties! Tag someone!")
