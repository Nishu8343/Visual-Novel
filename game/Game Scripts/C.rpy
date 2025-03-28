# ===================================================
# Define Characters
# ===================================================
define Boss = Character("Boss", color="#A9A9A9")
define boss = Boss
define player = Character("Player", color="#898361")
define postText =Position(xpos = 500, xanchor = 0, ypos=320, yanchor=1)



# ===================================================
# Class C Challenge Flow
# ===================================================

label class_c_challenge:
    scene com with fade
    player "What! One Computer in this big room? Let me know what is this."
    call class_c from _call_class_c
    return


label class_c:
    scene com2
    show text "Question: What is the IP range for a Class C network?" at postText
    menu:
        "192-223":
            $ answer = True
            jump class_c_correct
        "192-224":
            $ answer = False
            jump class_c_incorrect

label class_c_correct:
    boss "That's correct! Class C networks typically go from 192.x.x.x up to 223.x.x.x."
    call after_class_c from _call_after_class_c
    return

label class_c_incorrect:
    boss "Not quite. Class C networks start at 192.x.x.x and go up to 223.x.x.x."
    call class_c from _call_class_c_1
    return

label after_class_c:
    scene boss character1
    boss "Well done, Player. Now, let's dive into subnetting for Class C. I will give you an IP address, and you'll answer several questions about it."


    boss "Alright, let's proceed with the challenge."
    call question_c from _call_question_c

    return

# ===================================================
# Python Init
# ===================================================
init python:
    import random
    import ipaddress

    # ================================
    # 1) Define your Cheat Sheet
    # ================================
    CHEAT_SHEET = {
        24: {"group_size": 256, "last_octet": 0},
        25: {"group_size": 128, "last_octet": 128},
        26: {"group_size": 64,  "last_octet": 192},
        27: {"group_size": 32,  "last_octet": 224},
        28: {"group_size": 16,  "last_octet": 240},
        29: {"group_size": 8,   "last_octet": 248},
        30: {"group_size": 4,   "last_octet": 252},
        31: {"group_size": 2,   "last_octet": 254},
        32: {"group_size": 1,   "last_octet": 255},
    }

    # We'll store these so we can display them easily in the script
    store.ip_address_c   = None
    store.net_addr_c     = None
    store.first_usable_c = None
    store.last_usable_c  = None
    store.broadcast_c    = None
    store.subnet_mask_c  = None
    store.block_size_c   = None

    # ================================
    # 2) Generate Random Class C IP
    # ================================
    def generate_ip_c():
        first_octet  = random.randint(192, 223)  # Class C range
        second_octet = random.randint(0, 255)
        third_octet  = random.randint(0, 255)
        fourth_octet = random.randint(0, 255)

        subnet_cidr  = random.randint(24, 31)   # /24.. /31
        return f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}/{subnet_cidr}"

    # ================================
    # 3) Compute Network Info
    # ================================
    def compute_network_info_c(ip_cidr):
        network = ipaddress.ip_network(ip_cidr, strict=False)

        net_addr   = network.network_address
        broadcast  = network.broadcast_address

        if network.prefixlen < 31:
            first_usable = net_addr + 1
            last_usable  = broadcast - 1
        else:
            # For /31 or /32, "normal" host range doesn't apply
            first_usable = net_addr
            last_usable  = broadcast

        prefix = network.prefixlen
        if prefix in CHEAT_SHEET:
            block_size = CHEAT_SHEET[prefix]["group_size"]
            last_octet = CHEAT_SHEET[prefix]["last_octet"]
            dotted_mask = f"255.255.255.{last_octet}"
        else:
            block_size = None
            dotted_mask = str(network.netmask)

        return (
            str(net_addr),
            str(first_usable),
            str(last_usable),
            str(broadcast),
            dotted_mask,
            block_size
        )

# ===================================================
# Label to Actually Generate & Store a New IP
# ===================================================
label get_new_ip_c:
    # 1) Generate new IP/CIDR
    $ ip_address_c = generate_ip_c()

    # 2) Compute all the correct answers for that IP
    $ (net_addr_c,
    first_usable_c,
    last_usable_c,
    broadcast_c,
    subnet_mask_c,
    block_size_c
    ) = compute_network_info_c(ip_address_c)

    # Show the user what the new IP is
    scene com2 with fade
    show text "Your task is to analyze the IP address: [ip_address_c]." as iptext
    play sound "part2.mp3" loop


    pause
    return

# ===================================================
# Main Subnetting Questions
# ===================================================


label question_c:

    # Let's generate a random Class C IP + CIDR for the first question
    # Now we ask the six questions in order
    call question1_c from _call_question1_c
    call question2_c from _call_question2_c
    call question3_c from _call_question3_c
    call question4_c from _call_question4_c
    call question5_c from _call_question5_c
    call question6_c from _call_question6_c

    scene boss character1
    boss "Outstanding, Player! You've conquered the complexities of Class C subnetting like a true networking warrior! Your skills shine bright in the digital battlefield."
    boss "But remember, this is only the beginning. Beyond Class C lies a world of greater challenges—supernetting, VLANs, and the vast oceans of IPv6."

    boss "Will you rise again to claim your next victory? The network awaits your next move....."
    return

# ===================================================
# Question 1: First Assignable IP
# ===================================================
label question1_c:
    call get_new_ip_c from _call_get_new_ip_c
    $ attempt1_c = 1

    # The user sees the current IP from get_new_ip_c above
    $ answer = renpy.input("What is the First Assignable IP Address in this Network?")
    $ answer = answer.strip()

    if answer == first_usable_c:
        boss "Correct! The first assignable IP address is [first_usable_c]."
    else:
        boss "Not quite. The first usable IP is the network IP address + 1."
        jump question1_c_retry

    return

label question1_c_retry:
    $ attempt1_c += 1
    if attempt1_c > 3:
        jump question1_c_explanation

    # Generate a brand-new IP (and new correct answer!)
    call get_new_ip_c from _call_get_new_ip_c_1

    $ answer = renpy.input("What is the First Assignable IP for THIS NEW Network?")
    $ answer = answer.strip()

    if answer == first_usable_c:
        boss "Correct! The first assignable IP address is [first_usable_c]."
    else:
        boss "Not quite. The first usable IP is the network IP address + 1."
        jump question1_c_retry

    return

label question1_c_explanation:
    boss "You've used all 3 attempts."
    boss "Correct Answer: The first usable IP address is [first_usable_c]."
    hide iptext

    menu:
        "Check Explanation":

            boss_monitor_explanation " Not quite. The first usable IP is always Network IP address + 1. To find the network IP address, remember:

            \nStep 1: Identify the subnet block size using 2^(32 - CIDR).
            \nStep 2: Locate the closest multiple of the block size without exceeding the given IP.
            \n
            \n For Example:
            Given IP address: 192.168.1.130/26

            \nStep 1: Block Size = 2^(32 - 26) = 2^6 = 64
            \nStep 2: The multiples of 64 in 192.168.1.x are:
                \n     192.168.1.0
                \n     192.168.1.64
                \n     192.168.1.128 (Closest and does not exceed 192.168.1.130)
                \nSo, Network IP address = 192.168.1.128
            \nStep 3: First usable IP = Network IP address + 1 = 192.168.1.129


            \n
            \nKeep this in mind for similar problems!"

            jump question1_c_explanation_extra
        "Retry the question again":
            $ attempt1_c = 1
            jump question1_c

label question1_c_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt1_c = 1
            jump question1_c
        "Continue":
            return



# ===================================================
# Question 2: Last Assignable IP
# ===================================================
label question2_c:
    call get_new_ip_c from _call_get_new_ip_c_2
    $ attempt2_c = 1

    $ answer = renpy.input("What is the Last Assignable IP  address in this Network?")
    $ answer = answer.strip()

    if answer == last_usable_c:
        boss "Well done! The last assignable IP  address is [last_usable_c]."
    else:
        boss "Incorrect. The last usable IP is just before the broadcast IP address."
        jump question2_c_retry

    return

label question2_c_retry:
    $ attempt2_c += 1
    if attempt2_c > 3:
        jump question2_c_explanation

    call get_new_ip_c from _call_get_new_ip_c_3

    $ answer = renpy.input("Now with this NEW IP, what's the Last Assignable IP?")
    $ answer = answer.strip()

    if answer == last_usable_c:
        boss "Well done! The last assignable IP address is [last_usable_c]."
    else:
        boss "Incorrect. The last usable IP is just before the broadcast IP address."
        jump question2_c_retry

    return

label question2_c_explanation:
    boss "You've used all 3 attempts?"

    boss "Correct Answer: The Last usable IP address is [last_usable_c]."


    hide iptext



    menu:

        "Check Explanation":

            boss_monitor_explanation "Not quite. The last assignable IP is always Broadcast IP address - 1, as the broadcast IP address is reserved for communication with all devices in the subnet.

            \nStep 1: Find the block size using 2^(32 - CIDR).

            \nStep 2: Add the block size to the network IP address, then subtract 1 to get the broadcast IP address.
            \nStep 3: Subtract 1 from the broadcast IP address to get the last usable IP.


            \n\n For Example:
            Given IP  address: 192.168.1.130/26
            \nStep 1: Block Size = 2^(32 - 26) = 2^6 = 64
            \nStep 2: The multiples of 64 in 192.168.1.x are:
        \n     192.168.1.0
        \n     192.168.1.64
        \n     192.168.1.128 (Closest and does not exceed 192.168.1.130)
        \nSo, Network IP address = 192.168.1.128

        \nStep 3: Broadcast IP address = Network IP address + (Block Size - 1) = 192.168.1.128 + (64 - 1) = 192.168.1.191
        \nStep 4: Last Assignable IP = Broadcast IP address - 1 = 192.168.1.190

        \n\nKeep this method in mind for similar questions!"
            jump question2_c_explanation_extra
        "Retry the question again":
            $ attempt2_c = 0
            jump question2_c

label question2_c_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt2_c = 1
            jump question2_c
        "Continue":
            return

# ===================================================
# Question 3: Broadcast IP address
# ===================================================
label question3_c:
    call get_new_ip_c from _call_get_new_ip_c_4
    $ attempt3_c = 1

    $ answer = renpy.input("What is the Broadcast IP address for this Network?")
    $ answer = answer.strip()

    if answer == broadcast_c:
        boss "Exactly! The broadcast IP address is [broadcast_c]."
    else:
        boss "That's not correct. The broadcast IP address is the highest possible IP in the subnet."
        jump question3_c_retry

    return

label question3_c_retry:
    $ attempt3_c += 1
    if attempt3_c > 3:
        jump question3_c_explanation

    call get_new_ip_c from _call_get_new_ip_c_5

    $ answer = renpy.input("For this NEW IP, what is the Broadcast IP address?")
    $ answer = answer.strip()

    if answer == broadcast_c:
        boss "Exactly! The broadcast IP address is [broadcast_c]."
    else:
        boss "That's not correct. The broadcast IP address is the highest possible IP in the subnet."
        jump question3_c_retry

    return

label question3_c_explanation:
    boss "You've used all 3 attempts."

    boss "Correct Answer: The broadcast IP address is [broadcast_c]. "

    hide iptext
    menu:
        "Check Explanation":

            boss_monitor_explanation "Not quite. The broadcast IP address is the last IP in the subnet, reserved for sending messages to all devices in that subnet.

            \nStep 1: Find the block size using 2^(32 - CIDR).
            \nStep 2: Add the block size to the network IP address, then subtract 1 to get the broadcast IP address.

            \n\n For Example:
            Given IP address: 192.168.1.130/26
            \nStep 1: Block Size = 2^(32 - 26) = 2^6 = 64
            \nStep 2: The multiples of 64 in 192.168.1.x are:
            \n     192.168.1.0
            \n     192.168.1.64
            \n     192.168.1.128 (Closest and does not exceed 192.168.1.130)
            \nSo, Network IP address = 192.168.1.128

            \nStep 3: Broadcast IP address = Network IP address + (Block Size - 1) = 192.168.1.128 + (64 - 1) = 192.168.1.191


            \n\nUse this method to solve similar questions!"

            jump question3_c_explanation_extra
        "Retry the question again":
            $ attempt3_c = 1
            jump question3_c

label question3_c_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt3_c = 1
            jump question3_c
        "Continue":
            return

# ===================================================
# Question 4: Default Subnet Mask
# ===================================================
label question4_c:
    call get_new_ip_c from _call_get_new_ip_c_6
    $ attempt4_c = 1

    $ answer = renpy.input("What is the Default Subnet Mask for a Class C Network?")
    $ answer = answer.strip()

    if answer == "255.255.255.0":
        boss "Correct! The default subnet mask for a Class C network is 255.255.255.0."
    else:
        boss "Incorrect. Class C networks use 255.255.255.0 as the subnet mask."
        jump question4_c_retry

    return

label question4_c_retry:
    $ attempt4_c += 1
    if attempt4_c > 3:
        jump question4_c_explanation

    # For question 4, you might or might not want a new IP. We'll keep it consistent:
    call get_new_ip_c from _call_get_new_ip_c_7

    $ answer = renpy.input("Again, what is the Default Subnet Mask for a Class C Network?")
    $ answer = answer.strip()

    if answer == "255.255.255.0":
        boss "Correct! The default subnet mask for a Class C network is 255.255.255.0."
    else:
        boss "Incorrect. Class C networks use 255.255.255.0 as the subnet mask."
        jump question4_c_retry

    return

label question4_c_explanation:
    boss "You've used all 3 attempts."
    boss "Correct! The default subnet mask for a Class C network is 255.255.255.0."
    hide iptext
    menu:
        "Check Explanation":

            boss_monitor_explanation "The default subnet mask for a Class C is 255.255.255.0."
            jump question4_c_explanation_extra
        "Retry the question again":
            $ attempt4_c = 1
            jump question4_c

label question4_c_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt4_c = 1
            jump question4_c
        "Continue":
            return

# ===================================================
# Question 5: Subnet IP address
# ===================================================
label question5_c:
    call get_new_ip_c from _call_get_new_ip_c_8
    $ attempt5_c = 1

    $ answer = renpy.input("What is the Subnet IP address (Network IP address) of this IP address?")
    $ answer = answer.strip()

    if answer == net_addr_c:
        boss "That's right! The subnet (network) IP address is [net_addr_c]."
    else:
        boss "Not quite. The subnet IP address is the network IP address of the subnet."
        jump question5_c_retry

    return

label question5_c_retry:
    $ attempt5_c += 1
    if attempt5_c > 3:
        jump question5_c_explanation

    call get_new_ip_c from _call_get_new_ip_c_9

    $ answer = renpy.input("For this NEW IP, what is the Subnet IP address (Network ID)?")
    $ answer = answer.strip()

    if answer == net_addr_c:
        boss "That's right! The subnet/network IP address here is  [net_addr_c]."
    else:
        boss "Not quite! The subnet/network IP address is the first IP in the subnet, used to identify the entire network. It is found by zeroing out the host bits."
        jump question5_c_retry

    return

label question5_c_explanation:
    boss "You've used all 3 attempts."

    boss"Correct Answer: The network IP address is [net_addr_c]."
    hide iptext
    menu:
        "Check Explanation":

            boss_monitor_explanation "Not quite. The subnet/network IP address is the first IP in the subnet, used to identify the entire network. It is found by zeroing out the host bits.



        \nStep 1: Determine the block size: Use 2^(32 - CIDR).
        \n Step 2: Find the closest multiple of the block size that does not exceed the given IP address.


        \n\n For Example:
            Given IP  address: 192.168.1.130/26
            \nStep 1: Block Size = 2^(32 - 26) = 2^6 = 64
            \nStep 2: The multiples of 64 in 192.168.1.x are:
        \n     192.168.1.0
        \n     192.168.1.64
        \n     192.168.1.128 (Closest and does not exceed 192.168.1.130)
        \nSo, Network IP address = 192.168.1.128

        \n \nKeep this method in mind for similar questions!"
            jump question5_c_explanation_extra
        "Retry the question again":
            $ attempt5_c = 1
            jump question5_c

label question5_c_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt5_c = 1
            jump question5_c
        "Continue":
            return

# ===================================================
# Question 6: Subnet Mask
# ===================================================
label question6_c:
    call get_new_ip_c from _call_get_new_ip_c_10
    $ attempt6_c = 1

    $ answer = renpy.input("What is the Subnet Mask of this IP Address?")
    $ answer = answer.strip()

    if answer == subnet_mask_c:
        boss "Excellent! The subnet mask is [subnet_mask_c]. It defines the network portion of the IP address."
    else:
        boss "Incorrect. The subnet mask determines which part of the IP address is the network and which is the host."
        jump question6_c_retry

    return

label question6_c_retry:
    $ attempt6_c += 1
    if attempt6_c > 3:
        jump question6_c_explanation

    call get_new_ip_c from _call_get_new_ip_c_11

    $ answer = renpy.input("What is the Subnet Mask of THIS new IP?")
    $ answer = answer.strip()

    if answer == subnet_mask_c:
        boss "Excellent! The subnet mask is [subnet_mask_c]. It defines the network portion of the IP address."
    else:
        boss "Incorrect. The subnet mask determines which part of the IP address is the network and which is the host."
        jump question6_c_retry

    return

label question6_c_explanation:
    boss "You've used all 3 attempts."
    boss "Correct Answer: The subnet mask for this IP was [subnet_mask_c]. "
    hide iptext
    menu:
        "Check Explanation":

            boss_monitor_explanation "Not quite. The subnet mask defines the network portion of an IP

            \nStep 1: Determine the CIDR notation.
            \nStep 2: Identify the number of bits in the network portion (1s).
            \nStep 3:  Convert those bits into a dotted decimal format.




            \n\nFor Example: Given IP Address: 192.168.1.130/26

            \nStep 1: CIDR = /26

            \nStep 2: A /26 subnet mask has 26 bits set to 1, followed by 6 bits of 0s:

            \n11111111.11111111.11111111.11000000

            \nStep 3: Convert to Decimal
            \n    11111111 = 255
            \n    11111111 = 255
            \n    11111111 = 255
            \n    11000000 = 192
            \nSo, Subnet Mask = 255.255.255.192


            \n\nKeep practicing these methods for Class C networks!"

            jump question6_c_explanation_extra
        "Retry the question again":
            $ attempt6_c = 1
            jump question6_c

label question6_c_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt6_c = 1
            jump question6_c
        "Continue":
            return
