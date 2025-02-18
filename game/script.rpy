define Boss = Character(_("Boss"), color="#A9A9A9")
define player = Character("player", color="#FFD700")

label start:

    # scene the screen flicker effect

    # Boss speaks

scene room 1 with fade
"Player" "Where am I? What's going on?"
"Player" "Hello? Is anyone here?"

scene boss character1 with fade

"Boss" "Welcome, Player. You have been chosen for a test."

scene room 1 with dissolve

"Player" "Who are you? Where am I? What is this place?"

scene boss character1
"Boss" "Questions... so many questions. But you will get no answers until you earn them."


scene room 1
"Player" "Earn them? What do you mean?"

scene boss character1
"Boss" "Patience, Player. You'll soon understand. But first, go closer to the door!"


scene room 2
"Player" "Closer?"

scene boss character1
"Boss" "In front of you are three paths. Choose wisely, as each represents a different class of network."

scene room 3
"Player" "What is my task?"

scene boss character1
"Boss" "Your task? Solve the problems and hack the system. But remember, not everything is as it seems."


scene room 3
"Player" "Alright. Time to prove myself."

    # Menu to choose the network class and initiate subnetting challenges
scene room 4
"Player" "Three paths, three challenges."

scene boss character1

"Boss" "Choose your path wisely, player. Each choice leads you deeper into the network, but the wrong one will start you over."


scene room 4 with fade
menu:
    "Choose Class A network":
        jump class_a_challenge
    "Choose Class B network":
        jump class_b_challenge
    "Choose Class C network":
        jump class_c_challenge

scene boss character1 with fade

"Boss" "Well done Player Now, let's delve deeper into the world of subnetting. I will give you an IP address, and you will answer several questions about it. Pay close attention, as understanding these concepts is crucial."

return
