# Runs as and at whatever got hit with the belt (called by enchantment/clanker_spanking.json on every hit).
particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.5 20
execute if entity @s[team=clankers] run function clanka_spanka:spank
execute unless entity @s[team=clankers] anchored eyes run summon minecraft:text_display ^ ^0.6 ^ {Tags:["clanka_whap"],billboard:"center",background:0,shadow:1b,brightness:{sky:15,block:15},text:{text:"WHAP!",color:"gold",bold:true},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.4f,0.4f,0.4f]}}
