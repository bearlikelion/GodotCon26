# Checks if all players are ready and starts the game
func check_all_ready() -> void:
	# Only server should check and start game
	if not multiplayer.is_server():
		return

	var all_ready: bool = true

# [...]
	if all_ready and players.get_child_count() > 0:
		print("All players ready! Starting game...")
		_start_game.rpc()
# [...]
# Starts the game on all clients
@rpc("authority", "call_local", "reliable")
func _start_game() -> void:
	Global.change_level("res://Scenes/Game/game.tscn")
