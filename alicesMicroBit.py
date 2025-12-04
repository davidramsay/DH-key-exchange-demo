# Python code for Alice's Micro:bit
#
bobKeyPublic = 0
value = 0
key = ""
keyPrivate = 23
keyPublic = 29
sharedSecret = 0
aliceKeyPublic = 0
radio.set_group(1)

def on_forever():
  global aliceKeyPublic
  basic.show_number(keyPrivate)
  aliceKeyPublic = (keyPrivate * keyPublic)
  radio.send_value("aliceKey", aliceKeyPublic)
  basic.pause(1000)
basic.forever(on_forever)

def on_radio_received_value(arg0, arg1):
  global bobKeyPublic
  global sharedSecret
  global key
  global value
  key = arg0
  value = arg1
  if key + "" == "bobKey" + "":
    bobKeyPublic = value
    sharedSecret = (bobKeyPublic * keyPrivate)
    basic.pause(1000)
    basic.show_number(sharedSecret)
    basic.pause(1000)
radio.on_received_value(on_radio_received_value)
