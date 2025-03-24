# ===================================================
# Define Characters
# ===================================================
define Boss = Character("Boss", color="#A9A9A9")
define boss = Boss
define player = Character("Player", color="#898361")
define postText =Position(xpos = 500, xanchor = 0, ypos=320, yanchor=1)

# ===================================================
# Class A Challenge Flow
# ===================================================

label class_a_challenge:
    scene com with fade
    player "One Computer in this big room ? Let's check out this one for Class A!"
    call class_a from _call_class_a
    return


label class_a:
    scene com2
    show text "Question: What is the IP range for a Class A network?" at  postText
    menu:
        "1-126":
            $ answer = True
            jump class_a_correct
        "1-127":
            $ answer = False
            jump class_a_incorrect

label class_a_correct:
    boss "That's correct! Class A networks typically go from 1.x.x.x up to 126.x.x.x."
    call after_class_a from _call_after_class_a
    return

label class_a_incorrect:
    boss "Not quite. Class A networks start at 1.x.x.x and go up to 126.x.x.x."
    call class_a from _call_class_a_1
    return

label after_class_a:
    scene boss character1
    boss "Well done, Player. Now, let's dive into subnetting for Class A. I'll give you a Class A IP address, and you'll answer several questions about it."

    boss "Alright, let's proceed with the challenge."
    call question_a from _call_question_a

    return

# ===================================================
# Python Init
# ===================================================
init python:
    import random
    import ipaddress

    # ================================
    # 1) Define your Cheat Sheet
    # (Same as Class C, because these are the
    #  standard block sizes for /24 through /32, etc.)
    # ================================
    CHEAT_SHEET = {
        8:  {"group_size": 16777216, "last_octet": 0},   # For /8, netmask is 255.0.0.0
        9:  {"group_size": 8388608,  "last_octet": 128}, # Not literally last_octet in a single octet sense,
        10: {"group_size": 4194304,  "last_octet": 192}, # but we keep the same structure for demonstration.
        11: {"group_size": 2097152,  "last_octet": 224},
        12: {"group_size": 1048576,  "last_octet": 240},
        13: {"group_size": 524288,   "last_octet": 248},
        14: {"group_size": 262144,   "last_octet": 252},
        15: {"group_size": 131072,   "last_octet": 254},
        16: {"group_size": 65536,    "last_octet": 255},
        17: {"group_size": 32768,    "last_octet": 255}, # ...
        18: {"group_size": 16384,    "last_octet": 255},
        19: {"group_size": 8192,     "last_octet": 255},
        20: {"group_size": 4096,     "last_octet": 255},
        21: {"group_size": 2048,     "last_octet": 255},
        22: {"group_size": 1024,     "last_octet": 255},
        23: {"group_size": 512,      "last_octet": 255},
        24: {"group_size": 256,      "last_octet": 255},
        25: {"group_size": 128,      "last_octet": 255},
        26: {"group_size": 64,       "last_octet": 255},
        27: {"group_size": 32,       "last_octet": 255},
        28: {"group_size": 16,       "last_octet": 255},
        29: {"group_size": 8,        "last_octet": 255},
        30: {"group_size": 4,        "last_octet": 255},
        31: {"group_size": 2,        "last_octet": 255},
        32: {"group_size": 1,        "last_octet": 255},
    }

    # We'll store these so we can display them easily in the script
    store.ip_address_a   = None
    store.net_addr_a     = None
    store.first_usable_a = None
    store.last_usable_a  = None
    store.broadcast_a    = None
    store.subnet_mask_a  = None
    store.block_size_a   = None

    # ================================
    # 2) Generate Random Class A IP
    # ================================
    def generate_ip_a():
        # Class A range: 1-126
        first_octet  = random.randint(1, 126)
        second_octet = random.randint(0, 255)
        third_octet  = random.randint(0, 255)
        fourth_octet = random.randint(0, 255)

        # Typical Class A can have /8 to /31 subnets
        subnet_cidr  = random.randint(8, 31)
        return f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}/{subnet_cidr}"

    # ================================
    # 3) Compute Network Info
    # ================================
    def compute_network_info_a(ip_cidr):
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
            # For clarity, let's compute the netmask from prefix
            # But keep consistent with the structure above:
            ip_netmask = network.netmask
            dotted_mask = str(ip_netmask)
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
label get_new_ip_a:
    # 1) Generate new IP/CIDR
    $ ip_address_a = generate_ip_a()

    # 2) Compute all the correct answers for that IP
    $ (net_addr_a,
    first_usable_a,
    last_usable_a,
    broadcast_a,
    subnet_mask_a,
    block_size_a
    ) = compute_network_info_a(ip_address_a)

    # Show the user what the new IP is
    scene com2 with fade
    show text "Your task is to analyze the IP address: [ip_address_a]." as iptext

    pause
    return

# ===================================================
# Main Subnetting Questions
# ===================================================

label question_a:

    # Let's generate a random Class A IP + CIDR for the first question
    call get_new_ip_a from _call_get_new_ip_a

    # Now we ask the six questions in order
    call question1_a from _call_question1_a
    call question2_a from _call_question2_a
    call question3_a from _call_question3_a
    call question4_a from _call_question4_a
    call question5_a from _call_question5_a
    call question6_a from _call_question6_a

    scene boss character1
    boss "Outstanding, Player! You've conquered the complexities of Class A subnetting like a true networking champion!"
    boss "But remember, there's always more to explore—Class B, supernetting, VLANs, and even IPv6."

    boss "Will you rise to face the next challenge? The network horizon is vast..."
    return

# ===================================================
# Question 1: First Assignable IP
# ===================================================
label question1_a:
    $ attempt1_a = 1

    # The user sees the current IP from get_new_ip_a above
    $ answer = renpy.input("What is the First Assignable IP Address in this Network?")
    $ answer = answer.strip()

    if answer == first_usable_a:
        boss "Correct! The first assignable IP address is [first_usable_a]."
    else:
        boss "Not quite. The first usable IP is the network address + 1."
        jump question1_a_retry

    return

label question1_a_retry:
    $ attempt1_a += 1
    if attempt1_a > 3:
        jump question1_a_explanation

    # Generate a brand-new IP (and new correct answer!)
    call get_new_ip_a from _call_get_new_ip_a_1

    $ answer = renpy.input("What is the First Assignable IP for THIS NEW Network?")
    $ answer = answer.strip()

    if answer == first_usable_a:
        boss "Correct! The first assignable IP address is [first_usable_a]."
    else:
        boss "Not quite. The first usable IP is generally the network address + 1."
        jump question1_a_retry

    return

label question1_a_explanation:
    boss "You've used all 3 attempts."
    boss"Correct Answer: The first usable IP is [first_usable_a]."

    hide iptext

    menu:
        "Check Explanation":

            boss_monitor_explanation "Not quite. The first usable IP is always the Network IP address + 1. To find the Network IP address, remember:
            \n 1.Identify the subnet block size using 2^(32 - CIDR).
            \n 2.Locate the closest multiple of the block size without exceeding the given IP.

            \n\n For Example: Given IP address: 10.0.5.130/20
            \nStep 1: Block Size = 2^(32 - 20) = 2^12 = 4096
            \nStep 2: The multiples of 4096 in 10.x.x.x networks go up in increments of 16 at the third octet (because 4096 IPs = 16 blocks of 256 in the third octet).
            \nThe subnets start at:
            \n10.0.0.0     (covers 10.0.0.0 – 10.0.15.255)
            \n10.0.16.0    (covers 10.0.16.0 – 10.0.31.255)
            \n10.0.5.130 falls into the 10.0.0.0 – 10.0.15.255 range, so the closest multiple that does not exceed 10.0.5.130 is: Network IP address = 10.0.0.0
            \nStep 3: First usable IP = Network IP address + 1 = 10.0.0.1

            \n\n Keep this in mind for similar problems!"




            jump question1_a_explanation_extra
        "Retry the question again":
            $ attempt1_a = 1
            jump question1_a

label question1_a_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt1_a = 1
            jump question1_a
        "Continue":
            return

# ===================================================
# Question 2: Last Assignable IP
# ===================================================
label question2_a:
    call get_new_ip_a from _call_get_new_ip_a_2
    $ attempt2_a = 1

    $ answer = renpy.input("What is the Last Assignable IP Address in this Network?")
    $ answer = answer.strip()

    if answer == last_usable_a:
        boss "Well done! The last assignable IP address is [last_usable_a]."
    else:
        boss "Incorrect. The last usable IP is just before the broadcast address."
        jump question2_a_retry

    return

label question2_a_retry:
    $ attempt2_a += 1
    if attempt2_a > 3:
        jump question2_a_explanation

    call get_new_ip_a from _call_get_new_ip_a_3

    $ answer = renpy.input("Now with this NEW IP, what's the Last Assignable IP?")
    $ answer = answer.strip()

    if answer == last_usable_a:
        boss "Well done! The last assignable IP address is [last_usable_a]."
    else:
        boss "Incorrect. The last usable IP is just before the broadcast address."
        jump question2_a_retry

    return

label question2_a_explanation:
    boss "You've used all 3 attempts."
    boss"Correct Answer: The last usable IP Address [last_usable_a]."
    hide iptext
    menu:
        "Check Explanation":
            boss_monitor_explanation " Not quite. The last usable (assignable) IP is always the Broadcast IP address - 1. To find the Broadcast IP address, remember:

            \nStep 1: Identify the subnet block size using 2^(32 - CIDR).
            \nStep 2: Locate the next subnet boundary (the next multiple of the block size) to find the Broadcast IP address (which is one IP before that boundary).

            \n
            \nFor Example:
            Given IP address: 10.0.5.130/20

            \nStep 1: Block Size = 2^(32 - 20) = 2^12 = 4096
            \nStep 2: The multiples of 4096 for 10.0.x.x increase in increments of 16 at the third octet. The /20 subnets are:
                \n     10.0.0.0    (covers 10.0.0.0 – 10.0.15.255)
                \n     10.0.16.0   (covers 10.0.16.0 – 10.0.31.255)
                \nSince 10.0.5.130 falls in the first range, its next subnet boundary is 10.0.16.0.
                \nHence, Broadcast IP = (next subnet boundary) - 1 = 10.0.16.0 - 1 = 10.0.15.255

            \nStep 3: Last assignable IP = Broadcast IP - 1 = 10.0.15.254

            \n
            \nKeep this in mind for similar problems!"

            jump question2_a_explanation_extra
        "Retry the question again":
            $ attempt2_a = 0
            jump question2_a

label question2_a_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt2_a = 1
            jump question2_a
        "Continue":
            return

# ===================================================
# Question 3: Broadcast Address
# ===================================================
label question3_a:
    call get_new_ip_a from _call_get_new_ip_a_4
    $ attempt3_a = 1

    $ answer = renpy.input("What is the Broadcast IP Address for this Network?")
    $ answer = answer.strip()

    if answer == broadcast_a:
        boss "Exactly! The broadcast IP address is [broadcast_a]."
    else:
        boss "That's not correct. The broadcast IP address is the highest possible IP in the subnet."
        jump question3_a_retry

    return

label question3_a_retry:
    $ attempt3_a += 1
    if attempt3_a > 3:
        jump question3_a_explanation

    call get_new_ip_a from _call_get_new_ip_a_5

    $ answer = renpy.input("For this NEW IP, what is the Broadcast Address?")
    $ answer = answer.strip()

    if answer == broadcast_a:
        boss "Exactly! The broadcast address is [broadcast_a]."
    else:
        boss "That's not correct. The broadcast address is the highest possible IP in the subnet."
        jump question3_a_retry

    return

label question3_a_explanation:
    boss "You've used all 3 attempts."
    boss"Correct Answer: The broadcast address is [broadcast_a]. "
    hide iptext
    menu:
        "Check Explanation":
            boss_monitor_explanation " Not quite. The Broadcast IP address is one less than the next subnet boundary. To find the Broadcast IP address, remember:

            \nStep 1: Identify the subnet block size using 2^(32 - CIDR).
            \nStep 2: Locate the next subnet boundary (the next multiple of the block size) to find the Broadcast IP (one IP before that boundary).

            \n
            \nFor Example:
            Given IP address: 10.0.5.130/20

            \nStep 1: Block Size = 2^(32 - 20) = 2^12 = 4096
            \nStep 2: For a /20 in 10.x.x.x, the subnets increase in increments of 16 at the third octet (each subnet has 4096 addresses). The /20 subnets are:
                \n     10.0.0.0    (covers 10.0.0.0 – 10.0.15.255)
                \n     10.0.16.0   (covers 10.0.16.0 – 10.0.31.255)
                \nSince 10.0.5.130 falls in the first range (10.0.0.0 – 10.0.15.255), the next subnet boundary is 10.0.16.0.
                \nHence, Broadcast IP = (next subnet boundary) - 1 = 10.0.16.0 - 1 = 10.0.15.255

            \n
            \nKeep this in mind for similar problems!"


            jump question3_a_explanation_extra
        "Retry the question again":
            $ attempt3_a = 1
            jump question3_a

label question3_a_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt3_a = 1
            jump question3_a
        "Continue":
            return

# ===================================================
# Question 4: Default Subnet Mask
# ===================================================
label question4_a:
    call get_new_ip_a from _call_get_new_ip_a_6
    $ attempt4_a = 1

    $ answer = renpy.input("What is the Default Subnet Mask for a Class A Network?")
    $ answer = answer.strip()

    if answer == "255.0.0.0":
        boss "Correct! The default subnet mask for a Class A network is 255.0.0.0."
    else:
        boss "Incorrect. Class A networks use 255.0.0.0 as the default subnet mask."
        jump question4_a_retry

    return

label question4_a_retry:
    $ attempt4_a += 1
    if attempt4_a > 3:
        jump question4_a_explanation

    call get_new_ip_a from _call_get_new_ip_a_7

    $ answer = renpy.input("Again, what is the Default Subnet Mask for a Class A Network?")
    $ answer = answer.strip()

    if answer == "255.0.0.0":
        boss "Correct! The default subnet mask for a Class A network is 255.0.0.0."
    else:
        boss "Incorrect. Class A networks use 255.0.0.0 as the default subnet mask."
        jump question4_a_retry

    return

label question4_a_explanation:
    boss "You've used all 3 attempts."
    boss "Correct! The default subnet mask for a Class A network is 255.0.0.0."

    hide iptext
    menu:
        "Check Explanation":
            boss_monitor_explanation "The default subnet mask for a Class A is 255.0.0.0."
            jump question4_a_explanation_extra
        "Retry the question again":
            $ attempt4_a = 1
            jump question4_a

label question4_a_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt4_a = 1
            jump question4_a
        "Continue":
            return

# ===================================================
# Question 5: Subnet Address
# ===================================================
label question5_a:
    call get_new_ip_a from _call_get_new_ip_a_8
    $ attempt5_a = 1

    $ answer = renpy.input("What is the Subnet Address / Network Address of this IP Address?")
    $ answer = answer.strip()

    if answer == net_addr_a:
        boss "That's right! The subnet/ Network address of this Ip address is [net_addr_a]."
    else:
        boss "Not quite. The subnet address is the network address of the subnet."
        jump question5_a_retry

    return

label question5_a_retry:
    $ attempt5_a += 1
    if attempt5_a > 3:
        jump question5_a_explanation

    call get_new_ip_a from _call_get_new_ip_a_9

    $ answer = renpy.input("For this NEW IP, what is the Subnet Address (Network ID)?")
    $ answer = answer.strip()

    if answer == net_addr_a:
        boss "That's right! The subnet address is [net_addr_a]."
    else:
        boss "Not quite. The subnet address is the network address of the subnet."
        jump question5_a_retry

    return

label question5_a_explanation:
    boss "You've used all 3 attempts. "
    boss"Correct Answer: The network IP address is [net_addr_a]"

    hide iptext
    menu:
        "Check Explanation":
            boss_monitor_explanation " Not quite. The Subnet (Network) IP address is the multiple of the block size that does not exceed the given IP. To find the Subnet (Network) IP address, remember:

            \nStep 1: Identify the subnet block size using 2^(32 - CIDR).
            \nStep 2: Locate the closest multiple of that block size (within the relevant octet(s)) without exceeding the given IP address.

            \n
            \nFor Example:
            Given IP address: 10.0.5.130/20

            \nStep 1: Block Size = 2^(32 - 20) = 2^12 = 4096
            \nStep 2: For a /20 in a 10.x.x.x network, subnets increase in 4096-address blocks, which corresponds to increments of 16 in the third octet:
                \n     10.0.0.0    (covers 10.0.0.0 – 10.0.15.255)
                \n     10.0.16.0   (covers 10.0.16.0 – 10.0.31.255)
                \nSince 10.0.5.130 falls between 10.0.0.0 and 10.0.15.255, the largest multiple of the block size that does not exceed 10.0.5.130 is:
                \nSubnet (Network) IP address = 10.0.0.0

            \n
            \nKeep this in mind for similar problems!"

            jump question5_a_explanation_extra
        "Retry the question again":
            $ attempt5_a = 1
            jump question5_a

label question5_a_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt5_a = 1
            jump question5_a
        "Continue":
            return

# ===================================================
# Question 6: Network Address
# ===================================================
label question6_a:
    call get_new_ip_a from _call_get_new_ip_a_10
    $ attempt6_a = 1

    $ answer = renpy.input("What is the Subnet Mask for this IP address?")
    $ answer = answer.strip()

    if answer == net_addr_a:
        boss "Excellent! The network address is [net_addr_a]. It represents the entire Class A subnet."
    else:
        boss "Incorrect. The network address is formed by zeroing out the host portion bits."
        jump question6_a_retry

    return

label question6_a_retry:
    $ attempt6_a += 1
    if attempt6_a > 3:
        jump question6_a_explanation

    call get_new_ip_a from _call_get_new_ip_a_11

    $ answer = renpy.input("What is the Network Address of THIS new IP?")
    $ answer = answer.strip()

    if answer == net_addr_a:
        boss "Excellent! The network address is [net_addr_a]. It represents the entire Class A subnet."
    else:
        boss "Incorrect. The network address is formed by zeroing out the host portion bits."
        jump question6_a_retry

    return

label question6_a_explanation:
    boss "You've used all 3 attempts."
    boss "Correct Answer: The subnet mask for this IP was [subnet_mask_a]. "
    hide iptext
    menu:
        "Check Explanation":
            boss_monitor_explanation " Not quite. The Subnet Mask is derived from the CIDR. To find the subnet mask in dotted-decimal notation, remember:

            \nStep 1: Identify the CIDR (for example, /20).
            \nStep 2: Convert the first (CIDR) bits to 1, and the rest to 0 in a 32-bit binary form.
            \nStep 3: Convert that 32-bit binary form into dotted-decimal notation.

            \n
            \nFor Example:
            Given IP address: 10.0.5.130/20

            \nStep 1: CIDR = 20
            \nStep 2: In binary, /20 means the first 20 bits are 1, and the remaining 12 bits are 0:
                \n    11111111.11111111.11110000.00000000
            \nStep 3: Converting this binary to dotted-decimal gives:
                \n    255.255.240.0

            \nHence, the subnet mask for /20 is 255.255.240.0.

            \n
            \nKeep this in mind for similar problems!"

            jump question6_a_explanation_extra
        "Retry the question again":
            $ attempt6_a = 1
            jump question6_a

label question6_a_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt6_a = 1
            jump question6_a
        "Continue":
            return
