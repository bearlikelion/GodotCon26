# Making Games Multiplayer (Cooties) : Content Outline

- **Deck:** Making Games Multiplayer, A Guide to Understanding Godot's Multiplayer (GodotCon Boston 2026)
- **Figma Slides file:** KBdzYMqjebUYAdnH58g0cw
- **Extracted:** 2026-07-17
- **Slide count:** 31 slides in 5 sections (Intro, Connection, RPCs, Spawn & Sync, Wrap Up)

Note: most slides share a common textured background image fill (deck theme). Only content-bearing media is listed per slide.

## Slide 1: MAKING GAMES MULTIPLAYER

**Section:** Intro
**Layout:** Title slide, centered text stack over a full-bleed background image, large avatar image top center
**Content:**
- MAKING GAMES MULTIPLAYER (Bangers, 130pt)
- A Guide to Understanding Godot's Multiplayer
- by Mark Arneman / @bearlikelion

**Media:** Full-bleed background image, avatar image (502x502, "avatar 1")

## Slide 2: HI, I'M MARK

**Section:** Intro
**Layout:** Left column of asterisk bullets, avatar image top right, inline game capsule images
**Content:**
- HI, I'M MARK
- I am a full stack and independent game developer
- Two games on Steam: (2025) (2024) (game names shown as inline logo images)
- 24 games on Itch.io - 11 in the last year - 9 featuring multiplayer
- Contributed multiple fixes to GodotSteam & SteamMultiplayerPeer

**Media:** 5 images: avatar (498x498, "26CaLWA2dcqz6hS4U 1"), two game capsule/logo images (162x194 and 162x195), a 417x273 image and a 612x64 image (Steam/itch banners)

## Slide 3: WHAT IS COOTIES?

**Section:** Intro
**Layout:** Left bullet column, gameplay video right of center, two QR codes on the right edge (top and bottom)
**Content:**
- WHAT IS COOTIES?
- An open source (MIT) multiplayer game of tag
- One player get Cooties and spreads it to others
- 5 rounds, highest score wins
- Built with Godot 4's high-level multiplayer
- Download it at: bearlikelion.itch.io/cooties

**Media:** Gameplay video ("CominForYouMark 1", 739x416, VIDEO fill), QR GitHub (200x200), QR itch.io (200x200)

## Slide 4: What we are going to go over

**Section:** Intro
**Layout:** Numbered agenda list, 5 rows, big number left, topic center, subtitle right
**Content:**
1. Establishing a connection (The strength of Godot's MultiplayerPeer)
2. Talking to each other (RPCs: politely yelling functions across the internet)
3. Spawning & authority (MultiplayerSpawner and authority)
4. Staying in sync (MultiplayerSynchronizer, what to replicate)
5. Making it smooth (Adding interpolation)

**Media:** None

## Slide 5: TWO AUTOLOADS RUN THE SHOW

**Section:** Intro
**Layout:** Two stacked info panels (Global.gd, SteamInit.gd), footer pill bottom left, tall editor screenshot on the right
**Content:**
- TWO AUTOLOADS RUN THE SHOW
- Panel Global.gd:
  - players: the Dictionary of everyone connected
  - change_level(), players_synced signal
  - The source of truth living on every peer
- Panel SteamInit.gd:
  - Boots Steam with steamInitEx(480)
  - Processes Steam.run_callbacks() every frame
  - Owns the SteamMultiplayerPeer
- Footer pill: Pro tip: use folder colors. They're awesome.

**Media:** Image (303x472, "image 1", likely FileSystem dock screenshot with colored folders)
**Reminder candidates:**
- steamInitEx(480): appid 480 is Spacewar

## Slide 6: PART ONE: Establishing A CONNECTION

**Section:** Connection
**Layout:** Full-width centered section divider
**Content:**
- PART ONE
- Establishing A CONNECTION
- Understanding the strength of Godot's MultiplayerPeer Class

**Media:** None

## Slide 7: ONE SOCKET, MANY PLUGS

**Section:** Connection
**Layout:** Header plus code one-liner, three cards side by side, footer line, large image bleeding off the right edge
**Content:**
- ONE SOCKET, MANY PLUGS
```gdscript
multiplayer.multiplayer_peer = <any MultiplayerPeer>
```
- Card ENetMultiplayerPeer: IP + port, ships with Godot / Works on every platform / You handle the networking realities
- Card SteamMultiplayerPeer: GodotSteam extension / Lobbies, relays, friends / Players never see an IP
- Card Other peer plugs: NakamaMultiplayerBridge / EOSGMultiplayerPeer / OfflineMultiplayerPeer
- Footer: You can change the connection but keep the code.

**Media:** Large image right side (1138x1049, "image 2", socket/plug artwork)

## Slide 8: ENET VS STEAM

**Section:** Connection
**Layout:** Comparison table, 3 columns (label, ENET, STEAM) by 5 rows
**Content:**
- ENET VS STEAM
- NAT traversal: Requires Port forwarding vs Automatic
- Matchmaking: Send your IP to a friend vs Lobbies built in
- Relay servers: None vs Free, Valve pays
- Platforms: Everywhere Godot runs vs Steam only
- Best for: Prototypes, LAN, local testing vs Released games & Spacewar (480)

**Media:** None
**Reminder candidates:**
- Spacewar appid 480 appears in the table (slide 31 notes reference a Steam key joke pointing back at this slide)

## Slide 9: Hosting with enet

**Section:** Connection
**Layout:** Single large code panel with footer pill bottom left
**Content:**
- Hosting with enet
```gdscript
func _on_host_game_pressed() -> void:
    print("Creating ENET Server")
    var peer: ENetMultiplayerPeer = ENetMultiplayerPeer.new()
    var error: Error = peer.create_server(7777, 4)
    if error:
        print("Server Error: %s" % error)
    else:
        multiplayer.multiplayer_peer = peer
        Global.add_local_player()
        Global.change_level("res://Scenes/Lobby/lobby.tscn")
```
- Footer pill: create_server(7777, 4) = port 7777, four players

**Media:** None

## Slide 10: Joining through enet

**Section:** Connection
**Layout:** Single large code panel with footer pill bottom left
**Content:**
- Joining through enet
```gdscript
func _on_connect_pressed() -> void:
    var peer: ENetMultiplayerPeer = ENetMultiplayerPeer.new()
    var error: Error = peer.create_client(ip_address.text, 7777)
    if error:
        print("Client Error: %s" % error)
    else:
        multiplayer.multiplayer_peer = peer

        # Wait for player data to sync from server via RPC
        await Global.players_synced
        Global.change_level("res://Scenes/Lobby/lobby.tscn")
```
- Footer pill: That await is the difference between a lobby and a crash

**Media:** None

## Slide 11: LEVERAGING STEAM LOBBIES

**Section:** Connection
**Layout:** Single large code panel with footer line
**Content:**
- LEVERAGING STEAM LOBBIES
```gdscript
func _on_lobby_created(connected: int, lobby_id: int) -> void:
    if connected == 1:
        SteamInit.peer.host_with_lobby(lobby_id)
        multiplayer.multiplayer_peer = SteamInit.peer
        Steam.setLobbyData(lobby_id, "game", "GodotCootiesMPTutorial")
        Steam.allowP2PPacketRelay(true)

func _on_lobby_joined(lobby_id: int, _perms: int, _locked: bool, _resp: int) -> void:
    SteamInit.peer.connect_to_lobby(lobby_id)
    multiplayer.multiplayer_peer = SteamInit.peer
    await Global.players_synced
```
- Footer: Same multiplayer_peer property as ENet. The game never knows the difference.

**Media:** None

## Slide 12: PART TWO: TALKING TO EACH OTHER

**Section:** RPCs
**Layout:** Full-width centered section divider
**Content:**
- PART TWO
- TALKING TO EACH OTHER
- Remote Procedure Calls: politely yelling functions across the internet

**Media:** None

## Slide 13: ANATOMY OF AN @RPC

**Section:** RPCs
**Layout:** Big code pill under the header, three explainer cards side by side (who, where, how)
**Content:**
- ANATOMY OF AN @RPC
```gdscript
@rpc("authority", "call_local", "reliable")
```
- Card WHO CALLs IT: "authority" (Peer ID owner of the node), "any_peer" (Anyone. Validate everything.)
- Card WHERE IT RUNS: "call_local" (On you AND everyone else), "call_remote" (Only on the other peers)
- Card HOW IT sends: "reliable" (Guaranteed delivery, in order, but slow), "unreliable" (Fast but might not arrive. YOLO.), "unreliable_ordered" (Drops happen, keeps newest and resends a packet.)

**Media:** None
**Reminder candidates:**
- Build this slide one argument at a time (three reveal steps)
- Mention unreliable_ordered: drops packets but never delivers out of order, great for position streams

## Slide 14: CERTIFIED MAIL VS CONFETTI CANNON

**Section:** RPCs
**Layout:** Two illustrated panels side by side (RELIABLE, UNRELIABLE) with footer line
**Content:**
- CERTIFIED MAIL VS CONFETTI CANNON
- Panel RELIABLE: Like a delivery that requires a signature
  - Infections, scores, round changes
  - Anything the game breaks without
  - TCP energy (but it's all UDP underneath)
- Panel UNRELIABLE: A DELIVERY PERSON'S "BEST EFFORT"
  - Positions (the Synchronizer's whole job)
  - Particles, sounds, cosmetic events
  - If one goes missing, another is right behind it
- Footer: Rule of thumb: state = reliable, streams = unreliable

**Media:** Two illustration images inside the panels (803x575 and 875x569)

## Slide 15: THE READY-UP RPCS

**Section:** RPCs
**Layout:** Two code panels side by side (RAISE YOUR HAND, THE STARTING GUN) with footer line
**Content:**
- THE READY-UP RPCS
- RAISE YOUR HAND:
```gdscript
# Every peer raises their own hand
@rpc("any_peer", "call_local", "reliable")
func set_player_ready(is_ready: bool) -> void:
    var sender: int = multiplayer.get_remote_sender_id()
    players[sender].ready = is_ready

# on the Ready button:
set_player_ready.rpc(true)
```
- THE STARTING GUN:
```gdscript
# Only the host fires the starting gun
@rpc("authority", "call_local", "reliable")
func start_game() -> void:
    get_tree().change_scene_to_file(GAME_SCENE)

# on the host, once every hand is up:
if _everyone_ready():
    start_game.rpc()
```
- Footer: Anyone can say ready. Only peer 1 can say go.

**Media:** None
**Reminder candidates:**
- set_player_ready is any_peer, call_local means the sender's copy updates too
- start_game is authority: only peer 1 can start the match
- Transition: next slide is this exact exchange as a timeline

## Slide 16: READY UP!

**Section:** RPCs
**Layout:** Sequence diagram with 4 numbered rows between two column headers (EVERY PLAYER, THE HOST (PEER 1)), arrows and code labels per row, footer line
**Content:**
- READY UP!
- 1: Everyone's connected to the lobby (multiplayer.peer_connected)
- 2 (arrow right): "I'm ready!" broadcasts to every peer (set_player_ready.rpc(true))
- 3: Each peer stores everyone's ready state (players[sender_id].ready = true)
- 4 (arrow left): All ready? The host starts the game (start_game.rpc())
- Footer: Ready is any_peer. Start is authority. Nobody moves until peer 1 says go.

**Media:** None
**Reminder candidates:**
- The host is just peer 1 with a start button, it only lights up when every entry says ready
- One authority broadcast: every peer changes scene together

## Slide 17: PART THREE: SPAWNING & AUTHORITY

**Section:** Spawn & Sync
**Layout:** Full-width centered section divider
**Content:**
- PART THREE
- SPAWNING & AUTHORITY
- Overriding the spawn function and setting multiplayer authority

**Media:** None

## Slide 18: WHO OWNS WHAT?

**Section:** Spawn & Sync
**Layout:** Two bullet panels side by side (THE SERVER OWNS, EACH PLAYER OWNS) with centered footer
**Content:**
- WHO OWNS WHAT?
- THE SERVER OWNS: Who has Cooties / Scores and the round timer / Spawning and despawning players
- EACH PLAYER OWNS: Their position and movement / Their current animation and sprite flip / Their player name
- Footer: Authority = who writes the truth

**Media:** None

## Slide 19: THE SPAWNER, WIRED UP

**Section:** Spawn & Sync
**Layout:** Two code panels side by side (WIRE IT UP, THE SPAWN FUNCTION) with footer pill
**Content:**
- THE SPAWNER, WIRED UP
- WIRE IT UP:
```gdscript
const PLAYER_SCENE = preload("res://Scenes/Player/player.tscn")

func _ready() -> void:
    spawn_function = spawn_player

    # Only the server calls spawn()
    if multiplayer.is_server():
        for peer_id: int in Global.players.keys():
            call_deferred("spawn", peer_id)
```
- THE SPAWN FUNCTION:
```gdscript
func spawn_player(peer_id: int) -> Player:
    var player: Player = PLAYER_SCENE.instantiate()
    var spawn_point: Marker2D = spawn_points.pop_back()

    player.set_multiplayer_authority(peer_id)
    player.name = str(peer_id)
    player.add_to_group("players")
    player.global_position = spawn_point.position
    
    return player # Do not add_child()! Just return it
```
- Footer pill: Return the node. The spawner calls add_child() for you, on every peer

**Media:** None
**Reminder candidates:**
- The big gotcha: RETURN the node, do NOT add_child() it
- Name the node str(peer_id) so node paths match on every client
- Rule of thumb: always defer the spawn (call_deferred avoids spawning into a scene that hasn't finished _ready)

## Slide 20: (Challenger meme, full-bleed)

**Section:** Spawn & Sync
**Layout:** Full-bleed meme image, no text or child nodes (challenger_appears / Smash Bros style)
**Content:** None (image only)
**Media:** Full-bleed background image fill
**Reminder candidates:**
- JOKE: cue the Smash Bros sting. Mid-game, someone new knocks on the door.
- Beat: the game does not pause for them, so how do they catch up?

## Slide 21: (Late joiner meme, full-bleed)

**Section:** Spawn & Sync
**Layout:** Full-bleed meme image, no text or child nodes (late_joiner meme)
**Content:** None (image only)
**Media:** Full-bleed background image fill
**Reminder candidates:**
- The late joiner gets the exact same handshake: connect, send your player, receive the full dictionary
- Everyone agrees on who exists before anyone spawns, so joining late is just joining

## Slide 22: THE LATE JOINER, UNDER THE HOOD

**Section:** Spawn & Sync
**Layout:** Sequence diagram with 6 numbered rows between two column headers (THE LATE JOINER, HOST + EVERYONE ELSE), arrows and code labels per row, footer line
**Content:**
- THE LATE JOINER, UNDER THE HOOD
- 1 (arrow right): Join the lobby, start loading the level (peer.connect_to_lobby(lobby_id))
- 2 (arrow left): The host sends the current game state (set_map_pool.rpc_id(id) + set_time_remaining)
- 3 (arrow left): Every player introduces themselves (send_peer_data.rpc_id(id, players[me]))
- 4: Level loads: spawn me, puppet every player (spawn_new_player(peer_id) # for each peer)
- 5 (arrow right): "I exist!" Everyone spawns the joiner (connection_successful.rpc_id(sender_id))
- 6 (arrows both ways): Puppets shake hands, sync starts flowing (_sync_handshake() then physics_sync())
- Footer: The "I exist!" ACK is deferred until your surfer is actually in the tree.

**Media:** None
**Reminder candidates:**
- This is SurfsUp v2's flow: same ideas as Cooties but hand-rolled (NetCode and SteamInit autoloads, no MultiplayerSpawner)
- Steps 2 and 3 are direct rpc_id calls, nothing broadcasts
- connection_successful is DEFERRED until the joiner's own surfer exists, then flushed
- physics_sync only targets peers marked ready: a late joiner never gets sprayed with packets they can't handle yet

## Slide 23: PART FOUR: STAYING IN SYNC

**Section:** Spawn & Sync
**Layout:** Full-width centered section divider
**Content:**
- PART FOUR
- STAYING IN SYNC
- MultiplayerSynchronizer, the node that keeps state in sync

**Media:** None
**Reminder candidates:**
- Callback to the flipbook: the Synchronizer is the mailman

## Slide 24: SYNC THIS, NOT THAT

**Section:** Spawn & Sync
**Layout:** Two bullet panels side by side (SYNCHRONIZE, RPC INSTEAD), each item with a small subcaption
**Content:**
- SYNC THIS, NOT THAT
- SYNCHRONIZE:
  - Position and velocity (changes every frame, drops don't matter)
  - Animation state + sprite flip (visual truth everyone needs)
  - Anything continuous (the stream heals itself next tick)
- RPC INSTEAD:
  - One-shot effects (particles and sounds want to fire once)
  - Calculated values and UI (derive locally from real state)
  - Things that never change (send names once, not 30 times a second)

**Media:** None
**Reminder candidates:**
- Synchronizer = streams. RPC = events. If it happens once, it's an event.
- Syncing a health bar's fill percent instead of the health value is the canonical crime

## Slide 25: THE SYNC Config

**Section:** Spawn & Sync
**Layout:** Replication config table panel on the left, inspector screenshot placeholder on the right, footer pill
**Content:**
- THE SYNC Config
- Panel Replication config (player.tscn):
  - .:position : Always
  - AnimatedSprite2D:animation : Always
  - AnimatedSprite2D:flip_h : Always
  - PlayerName:text : Spawn only
- Placeholder text: INSPECTOR SCREENSHOT (replication panel)
- Footer pill: Watches properties, ships only what changed, on spawn or every tick

**Media:** One image (607x203, "image 9"), plus the placeholder frame awaiting the real inspector screenshot
**Reminder candidates:**
- No code on this one: the synchronizer is configured in the inspector. Add the real screenshot from the video assets.
- Delta compression means quiet players cost almost nothing
- Name label is spawn only, it never changes

## Slide 26: RESPECT MY AUTHORITY

**Section:** Spawn & Sync
**Layout:** Single code panel with footer pill
**Content:**
- RESPECT MY AUTHORITY
```gdscript
func _physics_process(delta: float) -> void:
    # Only drive the player we own
    if not is_multiplayer_authority():
        return

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    move_and_slide()
```
- Footer pill: Everyone else's copy of you is a puppet. The Synchronizer pulls the strings.

**Media:** None
**Reminder candidates:**
- The single most important line of gameplay code in the talk: if it's not yours, don't drive it
- Cliffhanger for the next section: synced values arrive 30 times a second, screens draw 60+

## Slide 27: THE JITTER PROBLEM

**Section:** Wrap Up
**Layout:** Header and explainer text left, code panel and footer pill below, jitter GIF placeholder frame on the right
**Content:**
- THE JITTER PROBLEM
- The network ticks at 30 Hz. Your monitor draws at 60+. Without help, remote players teleport 30 times a second.
```gdscript
func _ready() -> void:
    if not is_multiplayer_authority():
        physics_interpolation_mode = \
            Node.PHYSICS_INTERPOLATION_MODE_ON
```
- Footer pill: One line. The engine tweens between network positions.
- Placeholder text: JITTER GIF (before / after)

**Media:** Jitter GIF placeholder frame (620x460), not yet filled
**Reminder candidates:**
- Interpolation ON for every puppet, OFF for yourself (you're already smooth locally)
- Show the before/after gif here; the room should audibly wince at the before
- Engine-level interpolation, free since 4.3 for 2D

## Slide 28: A PHYSICS CONFESSION

**Section:** Wrap Up
**Layout:** Quote block at top, three asterisk bullets, code pill at bottom
**Content:**
- A PHYSICS CONFESSION
- Quote: "Players stomping each other into the ground. Velocity multiplying until someone gets launched across the map."
- Attribution: - me, debugging Cooties at 2am
- Godot's built-in 2D physics + multiplayer = occasional cryptid behavior
- Rapier Physics: drop-in replacement, deterministic, actively maintained
- The whole migration is one project setting:
```text
Project Settings > Physics > 2D > Physics Engine: Rapier2D
```

**Media:** None
**Reminder candidates:**
- Honest aside: "Godot's physics isn't great" for this use case, and that's okay to say out loud
- Rapier fixed the stomping and the velocity explosions without code changes
- Joke beat: "Not sponsored either. Nobody sponsors this talk."

## Slide 29: (Full journey comic, full-bleed)

**Section:** Wrap Up
**Layout:** Full-bleed comic/diagram background image with four numbered Bangers captions placed around the panels
**Content:**
- 1. YOU PRESS JUMP. YOUR MACHINE MOVES YOU INSTANTLY. FEELS GREAT.
- 2. THE SYNCHRONIZER MAILS YOUR POSITION, 30 HZ.
- 3. ON THE SERVER: COLLISION! PLAYER B IS TAGGED. THE REFEREE MAKES THE CALL: infect_player(B)
- 4. _set_player_infected.rpc() - EVERY SCREEN AGREES. INPUT TO INFECTION: ABOUT 100 MILLISECONDS.

**Media:** Full-bleed background image fill (comic artwork)
**Reminder candidates:**
- Victory lap: every concept from the talk in one 100 ms story
- ANIMATION: reveal panels one at a time
- Latency math: 50 ms there, 1 ms of server logic, 50 ms back

## Slide 30: FIVE THINGS TO STEAL

**Section:** Wrap Up
**Layout:** Numbered list, 5 rows, big number left, code identifier center, plain-language gloss right (mirror of the agenda slide)
**Content:**
- FIVE THINGS TO STEAL
1. multiplayer.multiplayer_peer : one property, any backend: ENet, Steam, whatever
2. @rpc(who, where, how) : annotations carry the whole messaging story
3. MultiplayerSpawner : spawn_function + server-only spawning
4. MultiplayerSynchronizer : streams sync, events RPC
5. is_multiplayer_authority() : guard your input, interpolate your puppets

**Media:** None
**Reminder candidates:**
- "If you remember one thing: authority. If you remember five, here they are."

## Slide 31: GO CATCH COOTIES

**Section:** Wrap Up
**Layout:** Closing slide, centered text stack over a full-bleed background image, links footer frame at the bottom
**Content:**
- GO CATCH COOTIES
- Learn from the code. Add to your game. Let me know!
- bearlikelion.com | github.com/bearlikelion | SurfsUp on Steam
- Got Questions? Reach out to me @bearlikelion

**Media:** Full-bleed background image fill
**Reminder candidates:**
- Closing line: Thanks for letting me teach you networking in Godot. I can't WAIT to see what you make.
- Repo and itch links stay up during questions
- JOKE (dead-air fallback): "the Steam key from slide 8 is still unclaimed."

## Placeholders still outstanding

- **Jitter GIF (slide 27):** frame still reads "JITTER GIF (before / after)". Needs the real before/after capture.
- **Synchronizer inspector screenshot (slide 25):** frame still reads "INSPECTOR SCREENSHOT (replication panel)". Notes say to add the real screenshot from the video assets.
- **Steam key joke setup (slides 8 and 31):** slide 31 notes reference "the Steam key from slide 8", but slide 8 (ENET VS STEAM) contains no visible Steam key mention. The setup beat needs to be added to slide 8 (or the notes) for the callback to land.
- **Repo URL confirmation (slides 3 and 31):** slide 3 links bearlikelion.itch.io/cooties plus GitHub and itch.io QR codes; slide 31 shows only github.com/bearlikelion with no repo name. Confirm the final repo URL and that both QR codes point to it.
- **Slide 2 Steam game names:** the bullet reads "Two games on Steam: (2025) (2024)" with the titles supplied as inline images; verify the images render the intended titles (SurfsUp and the 2024 release).
