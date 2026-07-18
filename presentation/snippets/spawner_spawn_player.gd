func spawn_player(peer_id: int) -> Player:
	var player: Player = PLAYER_SCENE.instantiate()
	var spawn_point: Marker2D = spawn_points.pop_back()

	player.set_multiplayer_authority(peer_id)
	player.name = str(peer_id)
	player.global_position = spawn_point.position
# [...]
	player.animated_sprite_2d.sprite_frames = character_sprite
	return player
