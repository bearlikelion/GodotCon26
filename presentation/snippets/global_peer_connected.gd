# Called when a peer connects
func _on_peer_connected(peer_id: int) -> void:
	print("GLOBAL PEER CONNECTED: %d" % peer_id)
	if not players.has(peer_id):
		players[peer_id] = {
			"character": -1,
			"name": str(peer_id),
			"score": 0
		}

		if multiplayer.multiplayer_peer is SteamMultiplayerPeer:
			get_player_from_server.rpc(peer_id)
