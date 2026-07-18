func _physics_process(delta: float) -> void:
	# Only process input for the player we control
	if not is_multiplayer_authority():
		return
