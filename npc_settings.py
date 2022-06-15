import pygame as pg

vec = pg.math.Vector2

# 50 Zeichen pro Zeile bei kleinem Screen
# 110 Zeichen pro Zeile bei full Screen


npc = {}
#   --mode--       --groupe--               --text--
npc["welcome"]      = {     "welcome":          "Hey, schön dich zu treffen... ich bin der gute alte NPC heheh.... :c *hmmm* bin es nicht wert einen Namen zu bekommen",}
npc["random"]       = {     "random1":          "random text1",
                            "random2":          "random text2",
                            "random3":          "random text3"}
npc["story"]        = {     "story1":           "story text1",
                            "story2":           "story text2",
                            "story3":           "story text3",
                            "story5":           "story text5"}

npc_gun = {}
npc_gun["welcome"]  = {     "welcome":          "ich mach dich kaputt "}
npc_gun["random"]   = {     "random1":          "ich liebe dich",
                            "random2":          "deus vult, alla",
                            "random3":          "Abboniert HandOfBlood! Abboniert HandOfBlood! Abboniert HandOfBlood! Abboniert HandOfBlood! Abboniert HandOfBlood!1 " \
                                                "Abboniert HandOfBlood! Abboniert HandOfBlood! Abboniert HandOfBlood! Abboniert HandOfBlood! Abboniert HandOfBlood!2 " \
                                                "Abboniert HandOfBlood! Abboniert HandOfBlood! Abboniert HandOfBlood! Abboniert HandOfBlood! Abboniert HandOfBlood!3 ",
                            "random4":          "MOOOOOOIN.... MAISTAAAA"}
npc_gun["story"]    = {     "story1":           "story text1",
                            "story2":           "story text22",
                            "story3":           "story text333",
                            "story4":           "story text4444"}

npc_quest_boy = {}
npc_quest_boy["welcome"]= { "welcome":      "ich gebe dir quest"}
npc_quest_boy["random"] = { "random1":      "mal schauen was ich für dich habe",
                            "random2":      "ob du das kannst...",
                            "random3":      "wurde aber auch langsam zeit, dass du wieder kommst -.-"}

npc_quest_boy["quest"]  = { "quest1":       "Schau dir direkt deine 1. Quest an!",
                            "quest2":       "Ich hab wieder was im Angebot",
                            "quest3":       "Neue Quest's sind da...",
                            "quest4":       "Wie du es gern hast... frische Lieferung",
                            "quest6":       "Wie ich sehe hast du deine Maximale HP verbessert!"}





















