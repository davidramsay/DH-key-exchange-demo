# Python code for Alice's Micro:bit
#
p = 29             # public prime modulus (shared, not secret)
g = 2              # public generator (shared, not secret)
keyPrivate = 23    # Alice's secret, never sent
sharedSecret = 0   # 0 means "haven't received Bob's value yet"
radio.set_group(1)

def modpow(base, exp, mod):
    result = 1
    for i in range(exp):
        result = (result * base) % mod
    return result

aliceKeyPublic = modpow(g, keyPrivate, p)   # 2^23 % 29 = 10

def on_forever():
    # always keep broadcasting, so Bob gets it even if he started late
    radio.send_value("aliceKey", aliceKeyPublic)
    if sharedSecret == 0:
        basic.show_string("K")
        basic.show_number(keyPrivate)
    else:
        basic.show_string("S")
        basic.show_number(sharedSecret)
    basic.pause(1000)
basic.forever(on_forever)

def on_radio_received_value(name, value):
    global sharedSecret
    if name == "bobKey":
        sharedSecret = modpow(value, keyPrivate, p)   # 18^23 % 29 = 2
radio.on_received_value(on_radio_received_value)
