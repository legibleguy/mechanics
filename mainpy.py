#!/usr/bin/env python3
import os
import json
import shutil
import yaml

# A dictionary mapping each category to a list of five real-life game mechanics.
# Each mechanic is defined with a unique symbol, name, category, long_description,
# short_description, solved_problems, and examples referencing real games and how they use the mechanic.
mechanics_by_category = {
    "Abilities": [
        {
            "symbol": "InV",
            "name": "Invisibility",
            "category": "Abilities",
            "long_description": "Allows the player to become unseen, enabling stealth approaches and avoiding enemy detection. Featured in games like Metal Gear Solid and Splinter Cell.",
            "short_description": "Become unseen to stealth past enemies.",
            "solved_problems": "Helps players bypass direct combat encounters.",
            "examples": [
                "Metal Gear Solid: Used for sneaking past guards.",
                "Splinter Cell: Emphasizes stealth and hidden movement.",
            ],
        },
        {
            "symbol": "Bt",
            "name": "Bullet Time",
            "category": "Abilities",
            "long_description": "Slows down time to allow precise targeting and evasion, adding cinematic flair. Notable in Max Payne and F.E.A.R.",
            "short_description": "Slow time for precision and evasion.",
            "solved_problems": "Enables players to manage overwhelming situations with precision.",
            "examples": [
                "Max Payne: Allows players to dodge bullets.",
                "F.E.A.R.: Enhances tactical combat moments.",
            ],
        },
        {
            "symbol": "Rg",
            "name": "Regeneration",
            "category": "Abilities",
            "long_description": "Automatically restores health over time, encouraging aggressive play with a safety net. Seen in Halo and Bioshock.",
            "short_description": "Health regenerates over time.",
            "solved_problems": "Reduces downtime and promotes continuous engagement.",
            "examples": [
                "Halo: Shields regenerate after taking damage.",
                "Bioshock: Health regeneration mechanics during gameplay.",
            ],
        },
        {
            "symbol": "Sh",
            "name": "Shield",
            "category": "Abilities",
            "long_description": "Provides temporary protection by absorbing damage. Prominent in games like Halo and Destiny.",
            "short_description": "Temporary damage absorption.",
            "solved_problems": "Mitigates damage during critical combat moments.",
            "examples": [
                "Halo: Energy shields absorb enemy fire.",
                "Destiny: Shields offer extra defense in combat.",
            ],
        },
        {
            "symbol": "Rm",
            "name": "Rage Mode",
            "category": "Abilities",
            "long_description": "Boosts player abilities temporarily under high stress or damage, common in action-adventure games like God of War.",
            "short_description": "Temporary power surge in combat.",
            "solved_problems": "Allows a comeback mechanic when players are overwhelmed.",
            "examples": [
                "God of War: Rage mode enhances strength and speed.",
                "Darksiders: Similar mechanics increase damage output under pressure.",
            ],
        },
    ],
    "Actions": [
        {
            "symbol": "Dg",
            "name": "Dodge",
            "category": "Actions",
            "long_description": "Enables quick evasion maneuvers to avoid attacks. Widely used in games like Dark Souls and Assassin's Creed.",
            "short_description": "Quick evasion to avoid attacks.",
            "solved_problems": "Helps players evade enemy strikes.",
            "examples": [
                "Dark Souls: Rolling dodge to avoid enemy hits.",
                "Assassin's Creed: Agile dodging during combat.",
            ],
        },
        {
            "symbol": "Blk",
            "name": "Block",
            "category": "Actions",
            "long_description": "Allows players to defend against incoming attacks using a shield or weapon. Seen in titles like Batman: Arkham series.",
            "short_description": "Defensive maneuver to mitigate damage.",
            "solved_problems": "Reduces damage from enemy attacks.",
            "examples": [
                "Batman: Arkham series: Blocking enemy strikes with gadgets.",
                "Various fighting games incorporate blocking mechanics.",
            ],
        },
        {
            "symbol": "PrY",
            "name": "Parry",
            "category": "Actions",
            "long_description": "Enables a timed counteraction to enemy attacks, turning defense into offense. Prominent in Dark Souls and Sekiro.",
            "short_description": "Timed counter to enemy attacks.",
            "solved_problems": "Allows players to interrupt enemy attacks and retaliate.",
            "examples": [
                "Dark Souls: Parry to create openings for counterattacks.",
                "Sekiro: Precision parrying for effective counters.",
            ],
        },
        {
            "symbol": "QtE",
            "name": "Quick Time Event",
            "category": "Actions",
            "long_description": "Triggers time-sensitive actions requiring rapid button presses, enhancing cinematic moments. Common in God of War and Heavy Rain.",
            "short_description": "Timed button prompts for cinematic actions.",
            "solved_problems": "Engages players in narrative sequences with interactive moments.",
            "examples": [
                "God of War: QTEs during boss battles.",
                "Heavy Rain: Interactive cutscenes relying on QTEs.",
            ],
        },
        {
            "symbol": "Int",
            "name": "Interact",
            "category": "Actions",
            "long_description": "Context-sensitive actions that allow players to engage with the environment. Found in open-world games like GTA V and Red Dead Redemption.",
            "short_description": "Contextual actions for interacting with the world.",
            "solved_problems": "Simplifies complex interactions into intuitive actions.",
            "examples": [
                "GTA V: Interaction with vehicles and NPCs.",
                "Red Dead Redemption: Contextual interactions in the environment.",
            ],
        },
    ],
    "AI": [
        {
            "symbol": "Pf",
            "name": "Pathfinding",
            "category": "AI",
            "long_description": "Enables non-player characters (NPCs) to navigate complex environments efficiently. Crucial in strategy and simulation games like Age of Empires.",
            "short_description": "Efficient NPC navigation.",
            "solved_problems": "Improves NPC movement in complex maps.",
            "examples": [
                "Age of Empires: NPCs navigate battlefields using pathfinding algorithms.",
                "Real-time strategy games use similar systems.",
            ],
        },
        {
            "symbol": "Flk",
            "name": "Flocking",
            "category": "AI",
            "long_description": "Simulates group behavior by having multiple entities move in a coordinated manner. Seen in games like Battlefield and various simulators.",
            "short_description": "Coordinated group movement.",
            "solved_problems": "Creates realistic crowd or swarm behaviors.",
            "examples": [
                "Battlefield: Units sometimes move in coordinated groups.",
                "Simulation titles use flocking for group AI.",
            ],
        },
        {
            "symbol": "CvR",
            "name": "Cover System",
            "category": "AI",
            "long_description": "Allows AI to take cover during combat to enhance tactical gameplay. Prominent in Gears of War.",
            "short_description": "AI takes cover during combat.",
            "solved_problems": "Improves enemy AI tactics in combat scenarios.",
            "examples": [
                "Gears of War: AI uses cover to avoid damage.",
                "Other shooters incorporate cover systems for enemy behavior.",
            ],
        },
        {
            "symbol": "AaI",
            "name": "Adaptive AI",
            "category": "AI",
            "long_description": "Adjusts enemy behavior dynamically based on player performance. Notable in games like Left 4 Dead.",
            "short_description": "Dynamic adjustment of AI difficulty.",
            "solved_problems": "Keeps gameplay challenging by adapting to player actions.",
            "examples": [
                "Left 4 Dead: AI changes tactics based on player skill.",
                "Other titles use adaptive AI to balance gameplay.",
            ],
        },
        {
            "symbol": "Per",
            "name": "Perception",
            "category": "AI",
            "long_description": "Simulates senses in AI, enabling detection of player actions. Used in games like F.E.A.R.",
            "short_description": "AI detection of player actions.",
            "solved_problems": "Enhances realism in enemy behavior and stealth mechanics.",
            "examples": [
                "F.E.A.R.: Enemies detect subtle player movements.",
                "Stealth games rely on refined AI perception.",
            ],
        },
    ],
    "Audio": [
        {
            "symbol": "Dm",
            "name": "Dynamic Music",
            "category": "Audio",
            "long_description": "Changes the musical score based on in-game actions or events. A staple in The Legend of Zelda: Breath of the Wild.",
            "short_description": "Music adapts to gameplay.",
            "solved_problems": "Enhances immersion by reflecting game intensity.",
            "examples": [
                "Breath of the Wild: Music shifts with exploration and combat.",
                "Other open-world games employ dynamic music.",
            ],
        },
        {
            "symbol": "Pa",
            "name": "Positional Audio",
            "category": "Audio",
            "long_description": "Provides spatial sound cues that help locate sources of sound in the game world. Integral in Hellblade: Senua's Sacrifice.",
            "short_description": "Spatial sound for immersive gameplay.",
            "solved_problems": "Improves situational awareness through sound localization.",
            "examples": [
                "Hellblade: Senua's Sacrifice: Uses positional audio for environmental cues.",
                "Many first-person shooters benefit from this mechanic.",
            ],
        },
        {
            "symbol": "As",
            "name": "Adaptive Soundtrack",
            "category": "Audio",
            "long_description": "Modifies the soundtrack dynamically to match gameplay intensity. Seen in Left 4 Dead.",
            "short_description": "Soundtrack adapts to game intensity.",
            "solved_problems": "Keeps the audio experience aligned with gameplay.",
            "examples": [
                "Left 4 Dead: Changes music based on player tension.",
                "Other survival games use adaptive soundtracks.",
            ],
        },
        {
            "symbol": "Vc",
            "name": "Voice Commands",
            "category": "Audio",
            "long_description": "Allows players to issue commands via voice, enhancing interactivity. Utilized in Tom Clancy's EndWar.",
            "short_description": "Use voice to control in-game actions.",
            "solved_problems": "Introduces an alternative interaction method.",
            "examples": [
                "EndWar: Commands issued through voice inputs.",
                "Some strategy games integrate voice controls.",
            ],
        },
        {
            "symbol": "Aa",
            "name": "Ambient Audio",
            "category": "Audio",
            "long_description": "Creates a background soundscape that enhances the game's atmosphere. Found in games like Limbo.",
            "short_description": "Immersive environmental soundscapes.",
            "solved_problems": "Adds depth to the game world through sound.",
            "examples": [
                "Limbo: Uses ambient audio to build tension.",
                "Other indie games focus on atmospheric sound.",
            ],
        },
    ],
    "Building": [
        {
            "symbol": "Bb",
            "name": "Base Building",
            "category": "Building",
            "long_description": "Allows players to construct and customize their own bases or settlements. Prominent in Fallout 4.",
            "short_description": "Construct and customize bases.",
            "solved_problems": "Offers creative freedom and strategic placement.",
            "examples": [
                "Fallout 4: Settlement building mechanics.",
                "Survival games like ARK also implement base building.",
            ],
        },
        {
            "symbol": "Mc",
            "name": "Modular Construction",
            "category": "Building",
            "long_description": "Enables building with interchangeable components for flexible design. Seen in Fortnite's Save the World mode.",
            "short_description": "Flexible building with modular parts.",
            "solved_problems": "Simplifies complex construction through pre-made modules.",
            "examples": [
                "Fortnite: Build structures with modular pieces.",
                "Other titles use similar construction systems.",
            ],
        },
        {
            "symbol": "Zn",
            "name": "Zoning",
            "category": "Building",
            "long_description": "Involves designating areas for specific functions, common in city-building games like SimCity and Cities: Skylines.",
            "short_description": "Designate areas for different functions.",
            "solved_problems": "Helps manage urban planning and resource allocation.",
            "examples": [
                "SimCity: Zoning for residential and commercial areas.",
                "Cities: Skylines: Detailed zoning mechanics.",
            ],
        },
        {
            "symbol": "Df",
            "name": "Defensive Fortification",
            "category": "Building",
            "long_description": "Allows players to strengthen structures for defense against attacks. Used in tower defense games like They Are Billions.",
            "short_description": "Strengthen structures for defense.",
            "solved_problems": "Enhances survivability during assaults.",
            "examples": [
                "They Are Billions: Build fortifications to withstand hordes.",
                "Other strategy games incorporate fortification mechanics.",
            ],
        },
        {
            "symbol": "Bp",
            "name": "Blueprints",
            "category": "Building",
            "long_description": "Provides pre-designed plans that players can use to construct buildings efficiently. Notable in Fallout 4.",
            "short_description": "Pre-designed construction plans.",
            "solved_problems": "Speeds up building by offering ready-made designs.",
            "examples": [
                "Fallout 4: Blueprints simplify settlement construction.",
                "Other games use blueprint systems for building.",
            ],
        },
    ],
    "Camera": [
        {
            "symbol": "Fc",
            "name": "Free Camera",
            "category": "Camera",
            "long_description": "Allows players to move the camera independently of the character, providing full environmental views. Seen in GTA V.",
            "short_description": "Independent camera control.",
            "solved_problems": "Enhances exploration and scene capture.",
            "examples": [
                "GTA V: Free camera for photo modes.",
                "Other open-world games offer similar features.",
            ],
        },
        {
            "symbol": "Lo",
            "name": "Lock-On",
            "category": "Camera",
            "long_description": "Enables the camera to focus on a target during combat, streamlining attacks. Popular in Dark Souls and Twilight Princess.",
            "short_description": "Camera focuses on combat targets.",
            "solved_problems": "Aids in tracking moving targets.",
            "examples": [
                "Dark Souls: Lock-on for precise combat.",
                "Twilight Princess: Enhanced targeting mechanics.",
            ],
        },
        {
            "symbol": "Cc",
            "name": "Cinematic Camera",
            "category": "Camera",
            "long_description": "Provides pre-set camera angles and movements to deliver cinematic storytelling. Employed in the Uncharted series.",
            "short_description": "Cinematic camera angles and movements.",
            "solved_problems": "Enhances narrative and visual presentation.",
            "examples": [
                "Uncharted: Cinematic sequences during story moments.",
                "Other adventure games adopt similar techniques.",
            ],
        },
        {
            "symbol": "Fp",
            "name": "First-Person View",
            "category": "Camera",
            "long_description": "Offers an immersive perspective by placing the camera at the character's viewpoint. Standard in Call of Duty.",
            "short_description": "Immersive first-person perspective.",
            "solved_problems": "Increases player immersion and situational awareness.",
            "examples": [
                "Call of Duty: First-person shooting experience.",
                "Many shooters use first-person view.",
            ],
        },
        {
            "symbol": "Os",
            "name": "Over-the-Shoulder",
            "category": "Camera",
            "long_description": "Positions the camera behind the character, balancing perspective and immersion. Widely used in Gears of War.",
            "short_description": "Camera positioned over the shoulder.",
            "solved_problems": "Offers a balanced view for combat and exploration.",
            "examples": [
                "Gears of War: Over-the-shoulder camera for cover-based shooting.",
                "Other third-person shooters use this mechanic.",
            ],
        },
    ],
    "Combat": [
        {
            "symbol": "CsH",
            "name": "Cover Shooting",
            "category": "Combat",
            "long_description": "Combines shooting mechanics with cover systems, allowing players to shoot from protected positions. Central to Gears of War.",
            "short_description": "Shoot while in cover.",
            "solved_problems": "Enhances tactical combat by integrating cover.",
            "examples": [
                "Gears of War: Players shoot from behind cover.",
                "Modern shooters often incorporate cover shooting.",
            ],
        },
        {
            "symbol": "CmB",
            "name": "Combo System",
            "category": "Combat",
            "long_description": "Enables chaining attacks into fluid combos, providing depth to melee combat. Signature in Devil May Cry.",
            "short_description": "Chain attacks into combos.",
            "solved_problems": "Rewards skillful play with dynamic attack sequences.",
            "examples": [
                "Devil May Cry: Stylish combo attacks.",
                "Action games use combo systems for dynamic combat.",
            ],
        },
        {
            "symbol": "CtA",
            "name": "Counter Attack",
            "category": "Combat",
            "long_description": "Allows players to counter enemy attacks with precise timing, turning defense into offense. Seen in Sekiro: Shadows Die Twice.",
            "short_description": "Counter enemy attacks effectively.",
            "solved_problems": "Rewards timing and precision in combat.",
            "examples": [
                "Sekiro: Well-timed counters against enemies.",
                "Other action titles employ counter mechanics.",
            ],
        },
        {
            "symbol": "QtC",
            "name": "Quick Time Combat",
            "category": "Combat",
            "long_description": "Integrates quick time events into combat sequences for dramatic and interactive battles. Featured in God of War.",
            "short_description": "QTE integrated combat sequences.",
            "solved_problems": "Adds cinematic flair to combat.",
            "examples": [
                "God of War: Quick time combat moments.",
                "Narrative-driven games use similar mechanics.",
            ],
        },
        {
            "symbol": "ChG",
            "name": "Charge Attack",
            "category": "Combat",
            "long_description": "Builds up attack power over time to deliver a powerful strike. Prominent in games like Bayonetta.",
            "short_description": "Build and release powerful attacks.",
            "solved_problems": "Offers a high-risk, high-reward combat option.",
            "examples": [
                "Bayonetta: Charge attacks for massive damage.",
                "Other action games implement charge attacks.",
            ],
        },
    ],
    "Crafting": [
        {
            "symbol": "Rec",
            "name": "Recipe System",
            "category": "Crafting",
            "long_description": "Allows players to combine ingredients based on recipes to craft items. A core mechanic in The Witcher 3.",
            "short_description": "Craft items using predefined recipes.",
            "solved_problems": "Simplifies item creation with clear guidelines.",
            "examples": [
                "The Witcher 3: Detailed alchemy recipes.",
                "Other RPGs use recipe systems for crafting.",
            ],
        },
        {
            "symbol": "McR",
            "name": "Modular Crafting",
            "category": "Crafting",
            "long_description": "Enables customization by combining interchangeable parts. Notable in Fallout 4's weapon crafting.",
            "short_description": "Customize items with interchangeable parts.",
            "solved_problems": "Enhances creativity in item customization.",
            "examples": [
                "Fallout 4: Modular weapon crafting.",
                "Other games allow for similar crafting systems.",
            ],
        },
        {
            "symbol": "Rc",
            "name": "Resource Combination",
            "category": "Crafting",
            "long_description": "Requires players to combine various resources to create new items, as seen in Minecraft.",
            "short_description": "Combine resources to craft items.",
            "solved_problems": "Encourages exploration and resource management.",
            "examples": [
                "Minecraft: Combining blocks to craft tools.",
                "Survival games use resource combination.",
            ],
        },
        {
            "symbol": "Cus",
            "name": "Customization",
            "category": "Crafting",
            "long_description": "Allows players to modify the appearance or stats of items. Prominent in Skyrim.",
            "short_description": "Modify items to suit your style.",
            "solved_problems": "Provides personalization and strategic variety.",
            "examples": [
                "Skyrim: Customizing weapons and armor.",
                "Many RPGs include item customization.",
            ],
        },
        {
            "symbol": "UpG",
            "name": "Upgrading",
            "category": "Crafting",
            "long_description": "Enables progressive enhancement of items or abilities through resource investment. Seen in Borderlands.",
            "short_description": "Enhance items with upgrades.",
            "solved_problems": "Rewards continued investment in equipment.",
            "examples": [
                "Borderlands: Upgrading weapons and gear.",
                "Many action RPGs incorporate upgrade systems.",
            ],
        },
    ],
    "Economy": [
        {
            "symbol": "IgC",
            "name": "In-Game Currency",
            "category": "Economy",
            "long_description": "Introduces a system of currency for purchasing goods and services. Central to GTA V.",
            "short_description": "Currency for in-game transactions.",
            "solved_problems": "Facilitates trade and economic balance.",
            "examples": [
                "GTA V: Money used for vehicles and properties.",
                "Many open-world games feature in-game currencies.",
            ],
        },
        {
            "symbol": "TrD",
            "name": "Trade System",
            "category": "Economy",
            "long_description": "Allows players to exchange goods with NPCs or other players. Prominent in EVE Online.",
            "short_description": "Exchange goods via trade.",
            "solved_problems": "Enhances player interaction and economic depth.",
            "examples": [
                "EVE Online: Complex trading systems.",
                "MMORPGs often include robust trade mechanics.",
            ],
        },
        {
            "symbol": "Ah",
            "name": "Auction House",
            "category": "Economy",
            "long_description": "Provides a marketplace where players can bid on items. Featured in World of Warcraft.",
            "short_description": "Marketplace for player auctions.",
            "solved_problems": "Facilitates player-driven economies.",
            "examples": [
                "World of Warcraft: Auction House for rare items.",
                "Other MMOs implement auction systems.",
            ],
        },
        {
            "symbol": "Mtx",
            "name": "Microtransactions",
            "category": "Economy",
            "long_description": "Enables players to purchase in-game items with real money. Widely used in Fortnite.",
            "short_description": "Real money purchases for in-game items.",
            "solved_problems": "Generates revenue through cosmetic and functional items.",
            "examples": [
                "Fortnite: In-game store for skins and emotes.",
                "Mobile games frequently use microtransactions.",
            ],
        },
        {
            "symbol": "Sd",
            "name": "Supply and Demand",
            "category": "Economy",
            "long_description": "Simulates economic fluctuations based on player actions and market conditions. Present in SimCity.",
            "short_description": "Dynamic economic fluctuations.",
            "solved_problems": "Reflects realistic market behavior.",
            "examples": [
                "SimCity: Market dynamics based on supply and demand.",
                "Economic sims rely on similar mechanics.",
            ],
        },
    ],
    "Exploration": [
        {
            "symbol": "Ow",
            "name": "Open World",
            "category": "Exploration",
            "long_description": "Provides a vast, seamless world for players to explore. Central to Breath of the Wild.",
            "short_description": "Seamless, expansive environments.",
            "solved_problems": "Eliminates loading screens and promotes free exploration.",
            "examples": [
                "Breath of the Wild: Massive open world.",
                "GTA V: Open world design for exploration.",
            ],
        },
        {
            "symbol": "Ft",
            "name": "Fast Travel",
            "category": "Exploration",
            "long_description": "Allows players to quickly move between discovered locations. Widely used in Skyrim.",
            "short_description": "Instant travel between known points.",
            "solved_problems": "Reduces travel time across large maps.",
            "examples": [
                "Skyrim: Fast travel between waypoints.",
                "Many RPGs include fast travel systems.",
            ],
        },
        {
            "symbol": "Dsc",
            "name": "Discovery",
            "category": "Exploration",
            "long_description": "Encourages exploration by rewarding players with hidden locations and secrets. Common in No Man's Sky.",
            "short_description": "Uncover hidden locations and secrets.",
            "solved_problems": "Incentivizes thorough exploration of the game world.",
            "examples": [
                "No Man's Sky: Discover new planets and anomalies.",
                "Exploration games reward player curiosity.",
            ],
        },
        {
            "symbol": "Sa",
            "name": "Secret Areas",
            "category": "Exploration",
            "long_description": "Hidden zones or easter eggs that reward curious players. Seen in Metroid Prime.",
            "short_description": "Hidden areas with rewards.",
            "solved_problems": "Adds depth and replayability.",
            "examples": [
                "Metroid Prime: Secret rooms and hidden paths.",
                "Many games include easter eggs and hidden zones.",
            ],
        },
        {
            "symbol": "Me",
            "name": "Map Expansion",
            "category": "Exploration",
            "long_description": "Mechanics that reveal new parts of the map as the player progresses. Present in Red Dead Redemption 2.",
            "short_description": "Progressively reveal the game world.",
            "solved_problems": "Keeps the exploration experience fresh and evolving.",
            "examples": [
                "Red Dead Redemption 2: Map grows as missions progress.",
                "Some RPGs feature map expansion mechanics.",
            ],
        },
    ],
    "Input": [
        {
            "symbol": "Ci",
            "name": "Combo Input",
            "category": "Input",
            "long_description": "Requires precise sequences of button presses to execute special moves. Prominent in fighting games like Street Fighter.",
            "short_description": "Execute special moves with button sequences.",
            "solved_problems": "Rewards skillful and precise input.",
            "examples": [
                "Street Fighter: Complex combos for special moves.",
                "Other fighting games rely on combo inputs.",
            ],
        },
        {
            "symbol": "Mtc",
            "name": "Motion Controls",
            "category": "Input",
            "long_description": "Uses physical movement to control game actions, popularized by the Wii Sports series.",
            "short_description": "Control gameplay with physical motion.",
            "solved_problems": "Enhances immersion through active participation.",
            "examples": [
                "Wii Sports: Motion controls for sports actions.",
                "Other motion-enabled games use similar mechanics.",
            ],
        },
        {
            "symbol": "Ti",
            "name": "Touch Input",
            "category": "Input",
            "long_description": "Utilizes touchscreen interactions to control game elements. Widely used in mobile games like Fruit Ninja.",
            "short_description": "Interact via touchscreen.",
            "solved_problems": "Provides intuitive and direct control.",
            "examples": [
                "Fruit Ninja: Touch-based slicing mechanics.",
                "Many mobile games rely on touch input.",
            ],
        },
        {
            "symbol": "Vi",
            "name": "Voice Input",
            "category": "Input",
            "long_description": "Allows players to execute commands using their voice. Featured in Hey You, Pikachu!",
            "short_description": "Control gameplay with voice commands.",
            "solved_problems": "Offers an alternative, hands-free input method.",
            "examples": [
                "Hey You, Pikachu!: Uses voice commands for interaction.",
                "Some modern games incorporate voice input.",
            ],
        },
        {
            "symbol": "Gr",
            "name": "Gesture Recognition",
            "category": "Input",
            "long_description": "Interprets physical gestures as game commands, enhancing interactive gameplay. Seen in Just Dance.",
            "short_description": "Use gestures to control actions.",
            "solved_problems": "Creates an immersive, active gameplay experience.",
            "examples": [
                "Just Dance: Recognizes player movements for scoring.",
                "Various interactive titles use gesture recognition.",
            ],
        },
    ],
    "Modding": [
        {
            "symbol": "UgC",
            "name": "User-Generated Content",
            "category": "Modding",
            "long_description": "Allows players to create and share their own content within the game. Iconic in LittleBigPlanet.",
            "short_description": "Create and share custom content.",
            "solved_problems": "Extends game longevity through community creations.",
            "examples": [
                "LittleBigPlanet: Players design their own levels.",
                "Other sandbox games embrace user-generated content.",
            ],
        },
        {
            "symbol": "ScE",
            "name": "Script Extensibility",
            "category": "Modding",
            "long_description": "Enables modification of game behavior through custom scripts. Widely seen in Skyrim modding.",
            "short_description": "Extend game functionality with custom scripts.",
            "solved_problems": "Allows deep customization and new gameplay experiences.",
            "examples": [
                "Skyrim: Extensive modding with script extenders.",
                "Other moddable games support scripting.",
            ],
        },
        {
            "symbol": "Ast",
            "name": "Asset Import",
            "category": "Modding",
            "long_description": "Permits players to import custom assets such as models and textures. Popularized by Garry's Mod.",
            "short_description": "Import custom models and textures.",
            "solved_problems": "Expands visual variety and personalization.",
            "examples": [
                "Garry's Mod: Importing assets for unique creations.",
                "Community mods often rely on asset import capabilities.",
            ],
        },
        {
            "symbol": "Cst",
            "name": "Customization Tools",
            "category": "Modding",
            "long_description": "Provides in-game tools for customizing game elements. Featured in The Sims series.",
            "short_description": "Tools for in-game customization.",
            "solved_problems": "Empowers players to tailor game content.",
            "examples": [
                "The Sims: Extensive customization of characters and homes.",
                "Other simulation games offer similar tools.",
            ],
        },
        {
            "symbol": "Wi",
            "name": "Workshop Integration",
            "category": "Modding",
            "long_description": "Integrates external mod repositories to simplify content sharing. Common in Minecraft.",
            "short_description": "Easy access to community mods.",
            "solved_problems": "Streamlines mod discovery and installation.",
            "examples": [
                "Minecraft: Steam Workshop for mod sharing.",
                "Other moddable games support workshop integration.",
            ],
        },
    ],
    "Movement": [
        {
            "symbol": "Dj",
            "name": "Double Jump",
            "category": "Movement",
            "long_description": "Allows players to jump a second time while airborne. Iconic in platformers like Super Mario Odyssey.",
            "short_description": "Perform a second jump mid-air.",
            "solved_problems": "Adds vertical mobility and dynamic movement.",
            "examples": [
                "Super Mario Odyssey: Double jump enhances platforming.",
                "Other platformers incorporate double jump mechanics.",
            ],
        },
        {
            "symbol": "Wr",
            "name": "Wall Run",
            "category": "Movement",
            "long_description": "Enables players to run along vertical surfaces. Famously used in Mirror's Edge.",
            "short_description": "Run along walls for dynamic traversal.",
            "solved_problems": "Facilitates agile navigation in urban environments.",
            "examples": [
                "Mirror's Edge: Wall running for acrobatic movement.",
                "Action games incorporate wall run mechanics.",
            ],
        },
        {
            "symbol": "Ds",
            "name": "Dash",
            "category": "Movement",
            "long_description": "Provides a quick burst of speed to cover short distances. Common in titles like Bayonetta.",
            "short_description": "Quick burst of speed.",
            "solved_problems": "Allows rapid repositioning during combat or exploration.",
            "examples": [
                "Bayonetta: Dash for evasive maneuvers.",
                "Other action games use dash mechanics.",
            ],
        },
        {
            "symbol": "Gl",
            "name": "Glide",
            "category": "Movement",
            "long_description": "Enables players to slow their descent by gliding through the air. Seen in games like Just Cause.",
            "short_description": "Slow descent by gliding.",
            "solved_problems": "Offers controlled aerial movement.",
            "examples": [
                "Just Cause: Gliding to traverse large gaps.",
                "Open-world games sometimes include glide mechanics.",
            ],
        },
        {
            "symbol": "Tp",
            "name": "Teleport",
            "category": "Movement",
            "long_description": "Instantly transports the player from one location to another. Utilized in Dishonored's Blink ability.",
            "short_description": "Instantaneous relocation.",
            "solved_problems": "Reduces travel time and adds strategic depth.",
            "examples": [
                "Dishonored: Teleportation for rapid repositioning.",
                "Other games incorporate teleport mechanics.",
            ],
        },
    ],
    "Multiplayer": [
        {
            "symbol": "Coop",
            "name": "Co-op Play",
            "category": "Multiplayer",
            "long_description": "Enables cooperative gameplay, allowing multiple players to work together. Seen in Left 4 Dead.",
            "short_description": "Play cooperatively with others.",
            "solved_problems": "Fosters teamwork and shared experiences.",
            "examples": [
                "Left 4 Dead: Cooperative survival gameplay.",
                "Other co-op games emphasize teamwork.",
            ],
        },
        {
            "symbol": "PvP",
            "name": "PvP",
            "category": "Multiplayer",
            "long_description": "Facilitates competitive gameplay between players. Central to Fortnite and Call of Duty: Warzone.",
            "short_description": "Player versus player combat.",
            "solved_problems": "Encourages competitive strategies.",
            "examples": [
                "Fortnite: Intense PvP battles.",
                "Warzone: Fast-paced player combat.",
            ],
        },
        {
            "symbol": "Mtch",
            "name": "Matchmaking",
            "category": "Multiplayer",
            "long_description": "Automatically pairs players of similar skill levels for balanced matches. Integral to Overwatch.",
            "short_description": "Automatic player pairing.",
            "solved_problems": "Ensures fair and balanced multiplayer games.",
            "examples": [
                "Overwatch: Skill-based matchmaking.",
                "Other competitive games use matchmaking systems.",
            ],
        },
        {
            "symbol": "Spc",
            "name": "Spectator Mode",
            "category": "Multiplayer",
            "long_description": "Allows players to observe matches without participating, enhancing community engagement. Found in CS:GO.",
            "short_description": "Watch games as a spectator.",
            "solved_problems": "Provides insights and entertainment for viewers.",
            "examples": [
                "CS:GO: Spectator mode for tournament viewing.",
                "Other competitive games offer spectator options.",
            ],
        },
        {
            "symbol": "Vch",
            "name": "Voice Chat",
            "category": "Multiplayer",
            "long_description": "Enables real-time voice communication between players. Popular in Among Us.",
            "short_description": "Real-time voice communication.",
            "solved_problems": "Facilitates teamwork and social interaction.",
            "examples": [
                "Among Us: Voice chat to coordinate strategies.",
                "Other multiplayer games support voice communication.",
            ],
        },
    ],
    "Narrative": [
        {
            "symbol": "Bnd",
            "name": "Branching Dialogue",
            "category": "Narrative",
            "long_description": "Provides players with dialogue choices that influence story outcomes. Central to the Mass Effect series.",
            "short_description": "Dialogue choices that affect the story.",
            "solved_problems": "Enhances replayability through multiple outcomes.",
            "examples": [
                "Mass Effect: Branching dialogue impacting narrative paths.",
                "Other RPGs use dialogue trees.",
            ],
        },
        {
            "symbol": "Dw",
            "name": "Dialogue Wheel",
            "category": "Narrative",
            "long_description": "Presents a radial menu for selecting dialogue options, simplifying complex interactions. Popularized by The Walking Dead.",
            "short_description": "Radial menu for dialogue selection.",
            "solved_problems": "Streamlines conversation choices.",
            "examples": [
                "The Walking Dead: Dialogue wheel for quick responses.",
                "Other narrative games implement similar systems.",
            ],
        },
        {
            "symbol": "Nls",
            "name": "Non-linear Story",
            "category": "Narrative",
            "long_description": "Allows players to experience the story in a non-sequential manner, promoting exploration. Seen in The Witcher 3.",
            "short_description": "Experience the story out of order.",
            "solved_problems": "Encourages exploration of multiple story paths.",
            "examples": [
                "The Witcher 3: Non-linear narrative structure.",
                "Other open-world RPGs embrace non-linearity.",
            ],
        },
        {
            "symbol": "Env",
            "name": "Environmental Storytelling",
            "category": "Narrative",
            "long_description": "Conveys narrative elements through the game world itself without explicit dialogue. Used in Bioshock.",
            "short_description": "Story told through environment.",
            "solved_problems": "Immerses players in the lore without overt exposition.",
            "examples": [
                "Bioshock: Environmental details reveal backstory.",
                "Other games use setting to tell stories.",
            ],
        },
        {
            "symbol": "Lrc",
            "name": "Lore Collection",
            "category": "Narrative",
            "long_description": "Encourages players to gather scattered lore items to piece together the game’s history. Common in Dark Souls.",
            "short_description": "Collect lore to uncover history.",
            "solved_problems": "Deepens player engagement with the game world.",
            "examples": [
                "Dark Souls: Lore scattered throughout the world.",
                "Other games use collectibles for lore discovery.",
            ],
        },
    ],
    "Physics": [
        {
            "symbol": "Rp",
            "name": "Ragdoll Physics",
            "category": "Physics",
            "long_description": "Simulates realistic body movements upon impact, adding dynamic visuals. Prominent in Grand Theft Auto IV.",
            "short_description": "Realistic physics-based body movement.",
            "solved_problems": "Enhances visual realism in character interactions.",
            "examples": [
                "GTA IV: Ragdoll effects upon collisions.",
                "Many modern games use ragdoll physics.",
            ],
        },
        {
            "symbol": "De",
            "name": "Destructible Environments",
            "category": "Physics",
            "long_description": "Allows parts of the game world to be damaged or destroyed, increasing interactivity. Seen in Red Faction: Guerrilla.",
            "short_description": "Environmental elements that can be destroyed.",
            "solved_problems": "Creates dynamic battlefields.",
            "examples": [
                "Red Faction: Guerrilla: Destructible structures.",
                "Other shooters incorporate destructible elements.",
            ],
        },
        {
            "symbol": "Gm",
            "name": "Gravity Manipulation",
            "category": "Physics",
            "long_description": "Alters the gravitational force to affect gameplay, adding unique puzzle and combat elements. Notable in Half-Life 2.",
            "short_description": "Alter gameplay through gravity changes.",
            "solved_problems": "Introduces innovative combat and puzzle challenges.",
            "examples": [
                "Half-Life 2: Gravity gun mechanics.",
                "Other games experiment with gravity manipulation.",
            ],
        },
        {
            "symbol": "Rlc",
            "name": "Realistic Collision",
            "category": "Physics",
            "long_description": "Ensures physical interactions follow real-world collision dynamics. Demonstrated in BeamNG.drive.",
            "short_description": "Accurate physical collision simulation.",
            "solved_problems": "Provides believable interactions between objects.",
            "examples": [
                "BeamNG.drive: Realistic collision responses.",
                "Simulation games rely on accurate collision physics.",
            ],
        },
        {
            "symbol": "Fd",
            "name": "Fluid Dynamics",
            "category": "Physics",
            "long_description": "Simulates the movement and interaction of liquids for enhanced realism. Used in the Battlefield series.",
            "short_description": "Realistic simulation of liquids.",
            "solved_problems": "Adds realism to environmental interactions.",
            "examples": [
                "Battlefield: Fluid dynamics in explosion effects.",
                "Other games incorporate fluid simulations.",
            ],
        },
    ],
    "Progression": [
        {
            "symbol": "Xp",
            "name": "Experience Points",
            "category": "Progression",
            "long_description": "Grants points for achievements that contribute to character growth. A staple in World of Warcraft.",
            "short_description": "Earn points to grow stronger.",
            "solved_problems": "Provides a measurable path for character improvement.",
            "examples": [
                "World of Warcraft: XP gained from quests and battles.",
                "RPGs widely use experience systems.",
            ],
        },
        {
            "symbol": "St",
            "name": "Skill Trees",
            "category": "Progression",
            "long_description": "Offers branching paths for character abilities and improvements. Seen in Diablo III.",
            "short_description": "Branching upgrade paths for abilities.",
            "solved_problems": "Allows customized character development.",
            "examples": [
                "Diablo III: Extensive skill trees for build variety.",
                "Other RPGs implement similar systems.",
            ],
        },
        {
            "symbol": "Lu",
            "name": "Leveling Up",
            "category": "Progression",
            "long_description": "Progresses characters through levels based on accumulated experience. Central to Final Fantasy.",
            "short_description": "Advance levels to enhance abilities.",
            "solved_problems": "Provides continuous character growth.",
            "examples": [
                "Final Fantasy: Leveling up through battles.",
                "Many RPGs feature level progression.",
            ],
        },
        {
            "symbol": "Ps",
            "name": "Perk System",
            "category": "Progression",
            "long_description": "Grants unique bonuses or abilities that enhance gameplay. Prominent in the Fallout series.",
            "short_description": "Unique bonuses for character builds.",
            "solved_problems": "Allows specialization and varied playstyles.",
            "examples": [
                "Fallout: Perks improve combat and skills.",
                "Other games use perks for customization.",
            ],
        },
        {
            "symbol": "Ul",
            "name": "Unlockables",
            "category": "Progression",
            "long_description": "Provides additional content or abilities that are unlocked through progression. Seen in Call of Duty.",
            "short_description": "Additional content unlocked over time.",
            "solved_problems": "Encourages continued play to reveal rewards.",
            "examples": [
                "Call of Duty: Unlockables such as weapons and skins.",
                "Other titles reward players with unlockable content.",
            ],
        },
    ],
    "Randomness": [
        {
            "symbol": "Ld",
            "name": "Loot Drops",
            "category": "Randomness",
            "long_description": "Randomly provides items upon defeating enemies or completing challenges. Signature in Borderlands.",
            "short_description": "Random item rewards.",
            "solved_problems": "Adds excitement and replayability through randomness.",
            "examples": [
                "Borderlands: Randomized loot drops with varying rarity.",
                "Other action RPGs feature loot systems.",
            ],
        },
        {
            "symbol": "Pg",
            "name": "Procedural Generation",
            "category": "Randomness",
            "long_description": "Creates game content algorithmically to ensure varied experiences. Central to No Man's Sky.",
            "short_description": "Algorithmic generation of content.",
            "solved_problems": "Offers endless variety without manual design.",
            "examples": [
                "No Man's Sky: Entire universes generated procedurally.",
                "Roguelikes often use procedural generation.",
            ],
        },
        {
            "symbol": "Ch",
            "name": "Critical Hits",
            "category": "Randomness",
            "long_description": "Occasionally delivers extra damage based on chance. Common in Diablo II.",
            "short_description": "Chance-based extra damage.",
            "solved_problems": "Introduces risk-reward dynamics in combat.",
            "examples": [
                "Diablo II: Critical hits change battle outcomes.",
                "Other RPGs implement critical hit mechanics.",
            ],
        },
        {
            "symbol": "Dr",
            "name": "Dice Roll",
            "category": "Randomness",
            "long_description": "Uses random chance similar to rolling dice to determine outcomes. Found in Mario Party.",
            "short_description": "Random outcome determination.",
            "solved_problems": "Adds elements of chance to gameplay.",
            "examples": [
                "Mario Party: Dice rolls decide movement and rewards.",
                "Party games often use chance mechanics.",
            ],
        },
        {
            "symbol": "Re",
            "name": "Random Events",
            "category": "Randomness",
            "long_description": "Triggers unexpected occurrences that alter gameplay dynamics. Seen in Dwarf Fortress.",
            "short_description": "Unexpected in-game events.",
            "solved_problems": "Keeps gameplay unpredictable and engaging.",
            "examples": [
                "Dwarf Fortress: Random events impact settlements.",
                "Simulation games use random events to surprise players.",
            ],
        },
    ],
    "Resources": [
        {
            "symbol": "Rgh",
            "name": "Resource Gathering",
            "category": "Resources",
            "long_description": "Allows players to collect raw materials for crafting and upgrades. Essential in Minecraft.",
            "short_description": "Collect raw materials.",
            "solved_problems": "Facilitates crafting and progression through material collection.",
            "examples": [
                "Minecraft: Gathering wood, stone, and ore.",
                "Survival games emphasize resource collection.",
            ],
        },
        {
            "symbol": "Im",
            "name": "Inventory Management",
            "category": "Resources",
            "long_description": "Enables players to organize and manage collected items. Prominent in Resident Evil.",
            "short_description": "Organize collected items.",
            "solved_problems": "Helps manage limited carrying capacity.",
            "examples": [
                "Resident Evil: Inventory puzzles and item management.",
                "Many survival games focus on inventory management.",
            ],
        },
        {
            "symbol": "Cm",
            "name": "Crafting Materials",
            "category": "Resources",
            "long_description": "Specific resources used in crafting recipes. Common in Fallout 4.",
            "short_description": "Materials for crafting items.",
            "solved_problems": "Defines the resource economy for crafting.",
            "examples": [
                "Fallout 4: Collecting materials for weapon upgrades.",
                "Various RPGs use crafting materials.",
            ],
        },
        {
            "symbol": "Eb",
            "name": "Economy Balancing",
            "category": "Resources",
            "long_description": "Manages the availability and cost of resources within the game. Seen in SimCity.",
            "short_description": "Balance resource availability and cost.",
            "solved_problems": "Ensures a fair and challenging resource economy.",
            "examples": [
                "SimCity: Balancing resources for city growth.",
                "Economic sims rely on resource management.",
            ],
        },
        {
            "symbol": "Ur",
            "name": "Upgrade Resources",
            "category": "Resources",
            "long_description": "Provides special resources dedicated to upgrading equipment or abilities. Found in Borderlands.",
            "short_description": "Special resources for upgrades.",
            "solved_problems": "Encourages strategic resource use for enhancement.",
            "examples": [
                "Borderlands: Upgrade components for weapons.",
                "Other games incorporate upgrade resources.",
            ],
        },
    ],
    "Social": [
        {
            "symbol": "Fl",
            "name": "Friend Lists",
            "category": "Social",
            "long_description": "Maintains a list of in-game friends for social interactions. Common in MMOs like World of Warcraft.",
            "short_description": "Manage your in-game friends.",
            "solved_problems": "Facilitates social connectivity.",
            "examples": [
                "World of Warcraft: In-game friend lists for grouping.",
                "Many online games include friend systems.",
            ],
        },
        {
            "symbol": "Gs",
            "name": "Guild Systems",
            "category": "Social",
            "long_description": "Organizes players into groups or guilds for collaborative gameplay. Prominent in Final Fantasy XIV.",
            "short_description": "Form and manage guilds.",
            "solved_problems": "Enhances team-based play and community building.",
            "examples": [
                "Final Fantasy XIV: Robust guild and raid systems.",
                "MMORPGs often feature guild mechanics.",
            ],
        },
        {
            "symbol": "Gc",
            "name": "In-Game Chat",
            "category": "Social",
            "long_description": "Allows real-time text communication between players. Essential in multiplayer titles like CS:GO.",
            "short_description": "Real-time text communication.",
            "solved_problems": "Enables coordination and social interaction.",
            "examples": [
                "CS:GO: In-game chat for team strategy.",
                "Other multiplayer games integrate chat systems.",
            ],
        },
        {
            "symbol": "Pt",
            "name": "Player Trading",
            "category": "Social",
            "long_description": "Enables players to exchange items directly. Seen in games like EVE Online.",
            "short_description": "Trade items with other players.",
            "solved_problems": "Facilitates a player-driven economy.",
            "examples": [
                "EVE Online: Trading system for spacecraft and modules.",
                "MMORPGs often support player trading.",
            ],
        },
        {
            "symbol": "Shb",
            "name": "Social Hubs",
            "category": "Social",
            "long_description": "Designated areas where players can meet and interact. Notable in Destiny 2.",
            "short_description": "Central locations for player interaction.",
            "solved_problems": "Creates communal spaces within the game world.",
            "examples": [
                "Destiny 2: The Tower as a social hub.",
                "Many MMOs provide social gathering areas.",
            ],
        },
    ],
    "UI": [
        {
            "symbol": "Hud",
            "name": "HUD",
            "category": "UI",
            "long_description": "Displays vital game information on-screen, such as health and ammo. A staple in Call of Duty.",
            "short_description": "On-screen game information display.",
            "solved_problems": "Keeps players informed of critical stats.",
            "examples": [
                "Call of Duty: Comprehensive HUD during combat.",
                "Many shooters utilize detailed HUDs.",
            ],
        },
        {
            "symbol": "Rmn",
            "name": "Radial Menus",
            "category": "UI",
            "long_description": "Uses a circular menu for quick selection of options. Popularized by Borderlands 2.",
            "short_description": "Circular menu for option selection.",
            "solved_problems": "Simplifies navigation of multiple options.",
            "examples": [
                "Borderlands 2: Radial menus for weapon and item selection.",
                "Other games employ radial interfaces.",
            ],
        },
        {
            "symbol": "Mmi",
            "name": "Minimap",
            "category": "UI",
            "long_description": "Provides a small map overlay to help with navigation. Widely used in Grand Theft Auto V.",
            "short_description": "Miniature map for navigation.",
            "solved_problems": "Assists in orientation and strategic planning.",
            "examples": [
                "GTA V: Minimap for tracking objectives.",
                "Other open-world games use minimaps.",
            ],
        },
        {
            "symbol": "Cpr",
            "name": "Contextual Prompts",
            "category": "UI",
            "long_description": "Displays on-screen prompts based on the player's context or environment. Common in The Legend of Zelda: Breath of the Wild.",
            "short_description": "On-screen action prompts.",
            "solved_problems": "Guides player actions without clutter.",
            "examples": [
                "Breath of the Wild: Contextual prompts for interactions.",
                "Many adventure games feature similar UI cues.",
            ],
        },
        {
            "symbol": "Dt",
            "name": "Dynamic Tooltips",
            "category": "UI",
            "long_description": "Shows detailed, real-time information about items or abilities. Featured in World of Warcraft.",
            "short_description": "Real-time detailed information popups.",
            "solved_problems": "Helps players understand game mechanics and stats.",
            "examples": [
                "World of Warcraft: Dynamic tooltips for gear stats.",
                "Other RPGs use tooltips for clarity.",
            ],
        },
    ],
    "World": [
        {
            "symbol": "Dnc",
            "name": "Day-Night Cycle",
            "category": "World",
            "long_description": "Simulates the passage of time with changing day and night. Central to The Legend of Zelda: Breath of the Wild.",
            "short_description": "Cycle between day and night.",
            "solved_problems": "Creates a dynamic and immersive world environment.",
            "examples": [
                "Breath of the Wild: Realistic day-night transitions.",
                "Other open-world games simulate time cycles.",
            ],
        },
        {
            "symbol": "Ws",
            "name": "Weather Systems",
            "category": "World",
            "long_description": "Introduces dynamic weather that affects gameplay and atmosphere. Prominent in Red Dead Redemption 2.",
            "short_description": "Dynamic weather effects.",
            "solved_problems": "Impacts visibility and environmental interactions.",
            "examples": [
                "Red Dead Redemption 2: Changing weather impacting gameplay.",
                "Other titles use weather to enhance realism.",
            ],
        },
        {
            "symbol": "Owm",
            "name": "Open World Map",
            "category": "World",
            "long_description": "Provides a detailed map of a vast, open game world. Featured in Skyrim.",
            "short_description": "Detailed map of a large world.",
            "solved_problems": "Helps players navigate expansive environments.",
            "examples": [
                "Skyrim: Open world map for exploration.",
                "Other RPGs provide detailed world maps.",
            ],
        },
        {
            "symbol": "Eh",
            "name": "Environmental Hazards",
            "category": "World",
            "long_description": "Introduces natural dangers such as lava, quicksand, or toxic zones. Seen in Minecraft.",
            "short_description": "Natural hazards in the game world.",
            "solved_problems": "Adds challenge and realism to exploration.",
            "examples": [
                "Minecraft: Environmental hazards like lava and water.",
                "Survival games incorporate hazardous terrain.",
            ],
        },
        {
            "symbol": "DEc",
            "name": "Dynamic Ecosystem",
            "category": "World",
            "long_description": "Simulates a living world where flora and fauna interact dynamically. Prominent in Far Cry.",
            "short_description": "Living, responsive ecosystems.",
            "solved_problems": "Creates a believable, evolving game environment.",
            "examples": [
                "Far Cry: Wildlife and environment interact dynamically.",
                "Other open-world games feature dynamic ecosystems.",
            ],
        },
    ],
}


def create_mechanic_yaml(mech):
    """
    Given a mechanic dictionary, wrap it under the 'mechanic' key and return a YAML string.
    """
    return yaml.dump({"mechanic": mech}, sort_keys=False)


def update_category_folder(category, mechanics):
    """
    For a given category folder:
    - Remove any subfolder (mechanic folder) not in the new mechanics.
    - Create/update each mechanic folder with a mechanic.yaml file.
    - Overwrite index.json with the five mechanics.
    """
    category_path = os.path.join(os.getcwd(), category)
    # Collect the symbols for the new mechanics
    new_symbols = {m["symbol"] for m in mechanics}

    # Remove any subfolder that is not in the new set of symbols.
    for entry in os.listdir(category_path):
        entry_path = os.path.join(category_path, entry)
        if os.path.isdir(entry_path) and entry not in new_symbols:
            shutil.rmtree(entry_path)
            print(f"Removed folder: {entry_path}")

    # Create/update each mechanic folder with mechanic.yaml.
    for mech in mechanics:
        mech_folder = os.path.join(category_path, mech["symbol"])
        os.makedirs(mech_folder, exist_ok=True)
        yaml_path = os.path.join(mech_folder, "mechanic.yaml")
        with open(yaml_path, "w") as f:
            f.write(create_mechanic_yaml(mech))
        print(f"Created/updated mechanic YAML at: {yaml_path}")

    # Overwrite the index.json with the current mechanics.
    index_data = {
        "index": [
            {
                "symbol": m["symbol"],
                "name": m["name"],
                "short_description": m["short_description"],
            }
            for m in mechanics
        ]
    }
    index_path = os.path.join(category_path, "index.json")
    with open(index_path, "w") as f:
        json.dump(index_data, f, indent=2)
    print(f"Updated index file at: {index_path}")


def main():
    # Iterate over each category in our defined dictionary.
    for category, mechanics in mechanics_by_category.items():
        print(f"Processing category: {category}")
        update_category_folder(category, mechanics)
        print("-" * 40)


if __name__ == "__main__":
    main()
