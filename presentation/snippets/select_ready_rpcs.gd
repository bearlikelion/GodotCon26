# Called when ready button is toggled
func _on_ready_button_toggled(toggled_on: bool) -> void:
	_set_ready.rpc(toggled_on)


# Updates ready state across all clients
@rpc("any_peer", "call_local", "reliable")
func _set_ready(player_ready: bool) -> void:
	is_ready = player_ready
# [...]
	# Notify lobby to check if all players are ready
	var lobby: Lobby = get_tree().get_first_node_in_group("lobby")
	if lobby:
		lobby.check_all_ready()
