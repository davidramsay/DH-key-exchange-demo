# Python code for Bob's micro:bit
#
p = 29             # public prime modulus (shared, not secret)
g = 2              # public generator (shared, not secret)
keyPrivate = 12    # Bob's secret, never sent
sharedSecret = 0   # 0 means "haven't received Alice's value yet"
radio.set_group(1)

def modpow(base, exp, mod):
    result = 1
    for i in range(exp):
        result = (result * base) % mod
    return result

bobKeyPublic = modpow(g, keyPrivate, p)     # 2^11 % 29 = 18

def on_forever():
    # always keep broadcasting, so Alice gets it even if she started late
    radio.send_value("bobKey", bobKeyPublic)
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
    if name == "aliceKey":
        sharedSecret = modpow(value, keyPrivate, p)   # 10^11 % 29 = 2
radio.on_received_value(on_radio_received_value)
