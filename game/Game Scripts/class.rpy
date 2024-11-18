
define Boss = Character(_("Boss"), color="#A9A9A9")
define Hacker = Character("Hacker", color="#FFD700")

label start:

menu:
    "Choose Class A network":
        jump class_a_challenge
    "Choose Class B network":
        jump class_b_challenge
    "Choose Class C network":
        jump class_c_challenge



# Dialogue for the initial setup
label class_a_challenge:
    show hacker character

    show boss character
    # Move to the challenge for Class A network
    "Boss" "Choose your path wisely, Hacker. Each choice leads you deeper into the network, but the wrong one will close your door to victory."
    # Add subnetting challenge for Class A here (e.g., questions, mini-games, or calculations)
    call class_a
    return

label class_b_challenge:
    show hacker character
    "Hacker"  "Class B... more practical for most networks. A balanced choice, but it brings its own complexities."
    "Hacker" "But am I ready for a medium-sized network's intricacies?"
    show boss character
    "Boss" "Choose your path wisely, Hacker. Each choice leads you deeper into the network, but the wrong one will close your door to victory."
    # Add subnetting challenge for Class B here
    jump class_b

label class_c_challenge:
    show hacker character
    "Hacker" "Class C... for the smaller operations. The smallest subnetting range, but requires precision."

    show boss character
    "Boss" "Choose your path wisely, Hacker. Each choice leads you deeper into the network, but the wrong one will close your door to victory."
    # Add subnetting challenge for Class C here
    jump class_c

label class_a:
    show text "Question: What is the subnet mask for a Class A network?"
    menu:
        "0-127":
            $ answer = True
            jump class_a_correct
        "0-128 ":
            $ answer = False
            jump class_a_incorrect




label class_b:
    show text "What is the class range for Class B?"
    menu:
        "128-191":
            $ answer = True
            jump class_b_correct
        "127-191":
            $ answer = False
            jump class_b_incorrect




    # Question displayed on the big screen

label class_a_correct:
    hacker "Got it! Class A networks have a large address space. This is manageable."
    # Continue with more questions or challenges


label class_a_incorrect:
    "Boss" "That's incorrect."
    # Optionally, you can loop back or give additional hints




label class_b_correct:
    hacker "Yes! The Class B network has an ideal balance for many organizations."


label class_b_incorrect:
    hacker "Not quite. I’ll need to re-evaluate my subnet calculations."

# Scene for Class C network
