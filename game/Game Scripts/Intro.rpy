define Boss = Character(_("Boss"), color="#A9A9A9")
define Hacker = Character("Hacker", color="#FFD700")

label start:
    scene dim_room
    with dissolve

    # Show the screen flicker effect
show boss character

    # Boss speaks
"Boss" "Welcome, Player. You've been chosen for a test."
show bg door
"Boss" "In front of you are three paths. Choose wisely, as each represents a different class of network."
"Boss" "Your task? Solve the problems and hack the system. But remember, not everything is as it seems."

show hacker character
"Hacker""Alright. Time to prove myself."

    # Menu to choose the network class and initiate subnetting challenges
scene bg door