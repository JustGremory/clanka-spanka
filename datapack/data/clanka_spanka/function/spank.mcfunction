# WHAT A SPANK DOES. Edit this file to change it, then run /reload.
# Runs as and at a clanker (anything on the "clankers" team) right after it is hit with the Clanka Spanka.
# The extra damage is not set here: it is the "value" under "minecraft:damage" in
# enchantment/clanker_spanking.json, because damage has to be part of the hit itself.

# Count spanks per bot. Read it with: scoreboard players get <name> clanka_spanked
scoreboard players add @s clanka_spanked 1

# Red comic popup over the clanker's head (tick.mcfunction grows it, floats it up, and removes it).
execute anchored eyes run summon minecraft:text_display ^ ^0.6 ^ {Tags:["clanka_whap"],billboard:"center",background:0,shadow:1b,brightness:{sky:15,block:15},text:{text:"CLANKA SPANKA!",color:"red",bold:true},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.4f,0.4f,0.4f]}}

# More ideas; remove the leading # to turn one on:
# effect give @s minecraft:slowness 3 1
# effect give @s minecraft:levitation 1 2
# tellraw @a [{selector:"@s",color:"red"},{text:" got clanka spanked!",color:"gray"}]
