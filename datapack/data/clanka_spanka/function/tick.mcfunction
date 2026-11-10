# Popups start small, grow and float up on their second tick (the client needs one tick to see the start state), and vanish after 16 ticks.
scoreboard players add @e[type=minecraft:text_display,tag=clanka_whap] clanka_whap 1
execute as @e[type=minecraft:text_display,tag=clanka_whap,scores={clanka_whap=2}] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.5f,0f],scale:[1.5f,1.5f,1.5f]}}
kill @e[type=minecraft:text_display,tag=clanka_whap,scores={clanka_whap=16..}]
