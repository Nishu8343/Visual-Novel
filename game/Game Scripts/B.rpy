# ===================================================
# Define Characters
# ===================================================
define Boss = Character("Boss", color="#A9A9A9")
define boss = Boss
define player = Character("Player", color="#898361")

# ===================================================
# Class B Challenge Flow
# ===================================================

label class_b_challenge:
    scene com with fade
    player "What! One Computer in this big room? Let me know what is this."
    call class_b
    return

label class_b:
    scene com2
    show text "Question: What is the IP range for a Class B network?"
    menu:
        "128-191":
            $ answer = True
            jump class_b_correct
        "128-192":
            $ answer = False
            jump class_b_incorrect

label class_b_correct:
    boss "That's correct! Class B networks typically go from 128.x.x.x up to 191.x.x.x."
    call after_class_b
    return

label class_b_incorrect:
    boss "Not quite. Class B networks start at 128.x.x.x and go up to 191.x.x.x."
    call class_b
    return

label after_class_b:
    scene boss character1
    boss "Well done, Player. Now, let's dive into subnetting for Class B. I will give you an IP address, and you'll answer several questions about it."

    boss "Alright, let's proceed with the challenge."
    call question_b

    return

# ===================================================
# Python Init
# ===================================================
init python:
    import random
    import ipaddress

    CHEAT_SHEET_B = {
        16: {"group_size": 65536, "last_octet": 0},
        17: {"group_size": 32768, "last_octet": 128},
        18: {"group_size": 16384, "last_octet": 192},
        19: {"group_size": 8192,  "last_octet": 224},
        20: {"group_size": 4096,  "last_octet": 240},
        21: {"group_size": 2048,  "last_octet": 248},
        22: {"group_size": 1024,  "last_octet": 252},
        23: {"group_size": 512,   "last_octet": 254},
        24: {"group_size": 256,   "last_octet": 255},
    }

    store.ip_address_b   = None
    store.net_addr_b     = None
    store.first_usable_b = None
    store.last_usable_b  = None
    store.broadcast_b    = None
    store.subnet_mask_b  = None
    store.block_size_b   = None

    def generate_ip_b():
        first_octet  = random.randint(128, 191)
        second_octet = random.randint(0, 255)
        third_octet  = random.randint(0, 255)
        fourth_octet = random.randint(0, 255)
        subnet_cidr  = random.randint(16, 23)
        return f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}/{subnet_cidr}"

    def compute_network_info_b(ip_cidr):
        network = ipaddress.ip_network(ip_cidr, strict=False)
        net_addr   = network.network_address
        broadcast  = network.broadcast_address

        if network.prefixlen < 31:
            first_usable = net_addr + 1
            last_usable  = broadcast - 1
        else:
            first_usable = net_addr
            last_usable  = broadcast

        prefix = network.prefixlen
        if prefix in CHEAT_SHEET_B:
            block_size = CHEAT_SHEET_B[prefix]["group_size"]
            last_octet = CHEAT_SHEET_B[prefix]["last_octet"]
            dotted_mask = f"255.255.{last_octet}.0"
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

label get_new_ip_b:
    $ ip_address_b = generate_ip_b()
    $ (net_addr_b, first_usable_b, last_usable_b, broadcast_b, subnet_mask_b, block_size_b) = compute_network_info_b(ip_address_b)
    scene com2 with fade
    show text "Your task is to analyze the IP address: [ip_address_b]."
    pause
    return

label question_b:
    call get_new_ip_b
    call question1_b
    call question2_b
    call question3_b
    call question4_b
    call question5_b
    call question6_b

    scene boss character1
    boss "Fantastic work, Player! You have mastered the realm of Class B subnetting."
    boss "But the network world is vast—there’s still Class A, Class C, supernetting, IPv6, and so much more."
    boss "Keep your blade of knowledge sharp, for more challenges await!"
    return


# ===================================================
# Question 1 (Class B): First Assignable IP
# ===================================================
label question1_b:
    $ attempt1_b = 1

    $ answer = renpy.input("What is the First Assignable IP Address in this Class B Network?")
    $ answer = answer.strip()

    if answer == first_usable_b:
        boss "Correct! The first assignable IP address is [first_usable_b]."
    else:
        boss "Not quite. The first usable IP is generally the network address + 1 (for /30 or larger subnets)."
        jump question1_b_retry

    return

label question1_b_retry:
    $ attempt1_b += 1
    if attempt1_b > 3:
        jump question1_b_explanation

    call get_new_ip_b

    $ answer = renpy.input("What is the First Assignable IP for THIS NEW Class B Network?")
    $ answer = answer.strip()

    if answer == first_usable_b:
        boss "Correct! The first assignable IP address is [first_usable_b]."
    else:
        boss "Not quite. The first usable IP is generally the network address + 1."
        jump question1_b_retry

    return

label question1_b_explanation:
    boss "You've used all 3 attempts. Would you like to see the explanation or retry?"
    menu:
        "Check Explanation":
            boss "The first usable IP is typically the network address + 1.\nThe correct answer was [first_usable_b]."
            jump question1_b_explanation_extra
        "Retry the question again":
            $ attempt1_b = 1
            jump question1_b

label question1_b_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt1_b = 1
            jump question1_b
        "Continue":
            return


# ===================================================
# Question 2 (Class B): Last Assignable IP
# ===================================================
label question2_b:
    $ attempt2_b = 1

    $ answer = renpy.input("What is the Last Assignable IP Address in this Class B Network?")
    $ answer = answer.strip()

    if answer == last_usable_b:
        boss "Well done! The last assignable IP address is [last_usable_b]."
    else:
        boss "Incorrect. The last usable IP is just before the broadcast address."
        jump question2_b_retry

    return

label question2_b_retry:
    $ attempt2_b += 1
    if attempt2_b > 3:
        jump question2_b_explanation

    call get_new_ip_b

    $ answer = renpy.input("Now with this NEW IP, what's the Last Assignable IP?")
    $ answer = answer.strip()

    if answer == last_usable_b:
        boss "Well done! The last assignable IP address is [last_usable_b]."
    else:
        boss "Incorrect. The last usable IP is just before the broadcast address."
        jump question2_b_retry

    return

label question2_b_explanation:
    boss "You've used all 3 attempts. Would you like the explanation or a retry?"
    menu:
        "Check Explanation":
            boss "For subnets smaller than /31, Last Usable = Broadcast - 1. The correct answer was [last_usable_b]."
            jump question2_b_explanation_extra
        "Retry the question again":
            $ attempt2_b = 1
            jump question2_b

label question2_b_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt2_b = 1
            jump question2_b
        "Continue":
            return


# ===================================================
# Question 3 (Class B): Broadcast Address
# ===================================================
label question3_b:
    $ attempt3_b = 1

    $ answer = renpy.input("What is the Broadcast Address for this Class B Network?")
    $ answer = answer.strip()

    if answer == broadcast_b:
        boss "Exactly! The broadcast address is [broadcast_b]."
    else:
        boss "That's not correct. The broadcast address is the highest IP in the subnet block."
        jump question3_b_retry

    return

label question3_b_retry:
    $ attempt3_b += 1
    if attempt3_b > 3:
        jump question3_b_explanation

    call get_new_ip_b

    $ answer = renpy.input("For this NEW IP, what is the Broadcast Address?")
    $ answer = answer.strip()

    if answer == broadcast_b:
        boss "Exactly! The broadcast address is [broadcast_b]."
    else:
        boss "That's not correct. The broadcast is the highest IP in the subnet block."
        jump question3_b_retry

    return

label question3_b_explanation:
    boss "You've used all 3 attempts. Would you like the explanation or retry?"
    menu:
        "Check Explanation":
            boss "The broadcast is the last IP in the subnet range. The correct was [broadcast_b]."
            jump question3_b_explanation_extra
        "Retry the question again":
            $ attempt3_b = 1
            jump question3_b

label question3_b_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt3_b = 1
            jump question3_b
        "Continue":
            return


# ===================================================
# Question 4 (Class B): Default Subnet Mask
# ===================================================
label question4_b:
    $ attempt4_b = 1

    $ answer = renpy.input("What is the Default Subnet Mask for a Class B Network?")
    $ answer = answer.strip()

    if answer == "255.255.0.0":
        boss "Correct! The default subnet mask for Class B is 255.255.0.0."
    else:
        boss "Incorrect. The default classful mask for Class B is 255.255.0.0."
        jump question4_b_retry

    return

label question4_b_retry:
    $ attempt4_b += 1
    if attempt4_b > 3:
        jump question4_b_explanation

    call get_new_ip_b

    $ answer = renpy.input("Again, what is the Default Subnet Mask for a Class B Network?")
    $ answer = answer.strip()

    if answer == "255.255.0.0":
        boss "Correct! The default subnet mask for Class B is 255.255.0.0."
    else:
        boss "Incorrect. It's 255.255.0.0."
        jump question4_b_retry

    return

label question4_b_explanation:
    boss "You've used all 3 attempts. Want an explanation or a retry?"
    menu:
        "Check Explanation":
            boss "Class B's default mask is 255.255.0.0."
            jump question4_b_explanation_extra
        "Retry the question again":
            $ attempt4_b = 1
            jump question4_b

label question4_b_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt4_b = 1
            jump question4_b
        "Continue":
            return


# ===================================================
# Question 5 (Class B): Subnet Address (Network ID)
# ===================================================
label question5_b:
    $ attempt5_b = 1

    $ answer = renpy.input("What is the Subnet Address (Network ID) of this Class B IP?")
    $ answer = answer.strip()

    if answer == net_addr_b:
        boss "That's right! The network address is [net_addr_b]."
    else:
        boss "Not quite. The subnet address is the base network address of the subnet."
        jump question5_b_retry

    return

label question5_b_retry:
    $ attempt5_b += 1
    if attempt5_b > 3:
        jump question5_b_explanation

    call get_new_ip_b

    $ answer = renpy.input("For this NEW IP, what is the Subnet Address (Network ID)?")
    $ answer = answer.strip()

    if answer == net_addr_b:
        boss "That's right! The subnet (network) address is [net_addr_b]."
    else:
        boss "Not quite. The subnet address is the base network address (host bits = 0)."
        jump question5_b_retry

    return

label question5_b_explanation:
    boss "You've used all 3 attempts. Explanation or retry?"
    menu:
        "Check Explanation":
            boss "To find the network ID, zero out all host bits. The correct was [net_addr_b]."
            jump question5_b_explanation_extra
        "Retry the question again":
            $ attempt5_b = 1
            jump question5_b

label question5_b_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt5_b = 1
            jump question5_b
        "Continue":
            return


# ===================================================
# Question 6 (Class B): Network Address
# ===================================================
label question6_b:
    $ attempt6_b = 1

    $ answer = renpy.input("What is the Network Address of this IP (Class B)?")
    $ answer = answer.strip()

    if answer == net_addr_b:
        boss "Excellent! The network address is [net_addr_b]."
    else:
        boss "Incorrect. The network address is formed by zeroing out the host portion."
        jump question6_b_retry

    return

label question6_b_retry:
    $ attempt6_b += 1
    if attempt6_b > 3:
        jump question6_b_explanation

    call get_new_ip_b

    $ answer = renpy.input("What is the Network Address of THIS new IP?")
    $ answer = answer.strip()

    if answer == net_addr_b:
        boss "Excellent! The network address is [net_addr_b]."
    else:
        boss "Incorrect. The network address is formed by zeroing out the host portion."
        jump question6_b_retry

    return

label question6_b_explanation:
    boss "You've used all 3 attempts. Explanation or retry?"
    menu:
        "Check Explanation":
            boss "The correct network address was [net_addr_b]."
            jump question6_b_explanation_extra
        "Retry the question again":
            $ attempt6_b = 1
            jump question6_b

label question6_b_explanation_extra:
    menu:
        "Retry the question?":
            $ attempt6_b = 1
            jump question6_b
        "Continue":
            return