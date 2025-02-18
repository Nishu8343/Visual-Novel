# ===================================================
# Define Characters
# ===================================================
define Boss = Character("Boss", color="#A9A9A9")
define boss = Boss
define player = Character("Player", color="#898361")

# ===================================================
# Class A Challenge Flow
# ===================================================

label class_a_challenge:
    scene com with fade
    player "One Computer in this big room ? Let's check out this one for Class A!"
    call class_a
    return


label class_a:
    scene com2
    show text "Question: What is the IP range for a Class A network?"
    menu:
        "1-126":
            $ answer = True
            jump class_a_correct
        "1-127":
            $ answer = False
            jump class_a_incorrect

label class_a_correct:
    boss "That's correct! Class A networks typically go from 1.x.x.x up to 126.x.x.x."
    call after_class_a
    return

label class_a_incorrect:
    boss "Not quite. Class A networks start at 1.x.x.x and go up to 126.x.x.x."
    call class_a
    return

label after_class_a:
    scene boss character1
    boss "Well done, Player. Now, let's dive into subnetting for Class A. I'll give you a Class A IP address, and you'll answer several questions about it."

    boss "Alright, let's proceed with the challenge."
    call question_a

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
    show text "Your task is to analyze the IP address: [ip_address_a]."

    pause
    return

# ===================================================
# Main Subnetting Questions
# ===================================================

label question_a:

    # Let's generate a random Class A IP + CIDR for the first question
    call get_new_ip_a

    # Now we ask the six questions in order
    call question1_a
    call question2_a
    call question3_a
    call question4_a
    call question5_a
    call question6_a

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
    call get_new_ip_a

    $ answer = renpy.input("What is the First Assignable IP for THIS NEW Network?")
    $ answer = answer.strip()

    if answer == first_usable_a:
        boss "Correct! The first assignable IP address is [first_usable_a]."
    else:
        boss "Not quite. The first usable IP is generally the network address + 1."
        jump question1_a_retry

    return

label question1_a_explanation:
    boss "You've used all 3 attempts. Would you like to see the explanation or retry the question?"
    menu:
        "Check Explanation":
            show text "Not quite. The first usable IP is always Network Address + 1. To find the network address, remember:

            Step 1: Identify the subnet block size using 2^(32 - CIDR).
            Step 2: Locate the closest multiple of the block size without exceeding the given IP.

            Example: For IP 192.168.1.67/26:

            Block size = 64 (since 2^(32 - 26) = 64)
            Network address = 192.168.1.64 (closest multiple of 64 below 67)
            First usable IP = 192.168.1.65
            Correct Answer: The first usable IP here was [first_usable_a]. Keep this in mind for similar problems!"


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

    call get_new_ip_a

    $ answer = renpy.input("Now with this NEW IP, what's the Last Assignable IP?")
    $ answer = answer.strip()

    if answer == last_usable_a:
        boss "Well done! The last assignable IP address is [last_usable_a]."
    else:
        boss "Incorrect. The last usable IP is just before the broadcast address."
        jump question2_a_retry

    return

label question2_a_explanation:
    boss "You've used all 3 attempts. Would you like to see the explanation or retry the question?"
    menu:
        "Check Explanation":
            boss "Not quite. The last assignable IP is always Broadcast Address - 1, as the broadcast address is reserved for communication with all devices in the subnet.

        Step 1: Find the block size using 2^(32 - CIDR).
        Step 2: Add the block size to the network address, then subtract 1 to get the broadcast address.
        Step 3: Subtract 1 from the broadcast address to get the last usable IP.

        Example: For 192.168.1.128/27:

        Block size = 32
    Network address = 192.168.1.128
    Broadcast address = 192.168.1.159
    Last usable IP = 192.168.1.158
    Correct Answer: The last usable IP here was [last_usable_a]. Keep this method in mind for similar questions!"
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
    $ attempt3_a = 1

    $ answer = renpy.input("What is the Broadcast Address for this Network?")
    $ answer = answer.strip()

    if answer == broadcast_a:
        boss "Exactly! The broadcast address is [broadcast_a]."
    else:
        boss "That's not correct. The broadcast address is the highest possible IP in the subnet."
        jump question3_a_retry

    return

label question3_a_retry:
    $ attempt3_a += 1
    if attempt3_a > 3:
        jump question3_a_explanation

    call get_new_ip_a

    $ answer = renpy.input("For this NEW IP, what is the Broadcast Address?")
    $ answer = answer.strip()

    if answer == broadcast_a:
        boss "Exactly! The broadcast address is [broadcast_a]."
    else:
        boss "That's not correct. The broadcast address is the highest possible IP in the subnet."
        jump question3_a_retry

    return

label question3_a_explanation:
    boss "You've used all 3 attempts. Would you like to see the explanation or retry the question?"
    menu:
        "Check Explanation":
            boss "Not quite. The broadcast address is the last IP in the subnet, used to communicate with all devices in the subnet.

            Step 1: Find the block size using 2^(32 - CIDR).
            Step 2: Add the block size to the network address, then subtract 1 to get the broadcast address.

            Example: For 10.0.0.128/28:

            Block size = 16 (since 2^(32 - 28) = 16)
            Network address = 10.0.0.128
            Broadcast address = 10.0.0.143
            Correct Answer: The broadcast address here was [broadcast_a]. Keep this method in mind for future questions!"

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

    call get_new_ip_a

    $ answer = renpy.input("Again, what is the Default Subnet Mask for a Class A Network?")
    $ answer = answer.strip()

    if answer == "255.0.0.0":
        boss "Correct! The default subnet mask for a Class A network is 255.0.0.0."
    else:
        boss "Incorrect. Class A networks use 255.0.0.0 as the default subnet mask."
        jump question4_a_retry

    return

label question4_a_explanation:
    boss "You've used all 3 attempts. Would you like to see the explanation or retry the question?"
    menu:
        "Check Explanation":
            boss "The default classful mask for a Class A is 255.0.0.0."
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

    call get_new_ip_a

    $ answer = renpy.input("For this NEW IP, what is the Subnet Address (Network ID)?")
    $ answer = answer.strip()

    if answer == net_addr_a:
        boss "That's right! The subnet address is [net_addr_a]."
    else:
        boss "Not quite. The subnet address is the network address of the subnet."
        jump question5_a_retry

    return

label question5_a_explanation:
    boss "You've used all 3 attempts. Would you like to see the explanation or retry the question?"
    menu:
        "Check Explanation":
            boss "To find the subnet address, zero out the host bits. The correct answer was [net_addr_a]."
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

    call get_new_ip_a

    $ answer = renpy.input("What is the Network Address of THIS new IP?")
    $ answer = answer.strip()

    if answer == net_addr_a:
        boss "Excellent! The network address is [net_addr_a]. It represents the entire Class A subnet."
    else:
        boss "Incorrect. The network address is formed by zeroing out the host portion bits."
        jump question6_a_retry

    return

label question6_a_explanation:
    boss "You've used all 3 attempts. Would you like to see the explanation or retry the question?"
    menu:
        "Check Explanation":
            boss "The correct network address was [net_addr_a]."
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
