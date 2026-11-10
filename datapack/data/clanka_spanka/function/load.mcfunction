# Runs on server start and every /reload.
scoreboard objectives add clanka_whap dummy
scoreboard objectives add clanka_spanked dummy "Times clanka spanked"
# Create the clankers team only once, so later reloads keep any prefix/color changed by command.
execute store success score #team_created clanka_whap run team add clankers "Clankers"
execute if score #team_created clanka_whap matches 1 run team modify clankers prefix {text:"[CLANKER] ",color:"red"}
execute if score #team_created clanka_whap matches 1 run team modify clankers color red
