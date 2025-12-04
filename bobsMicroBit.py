# Python code for Bob's micro:bit
#
keyPrivate = 11
keyPublic = 29
value = 0
key = ""
sharedSecret = 0
radio.set_group(1)
aliceKeyPublic = 0
bobKeyPublic = (keyPrivate * keyPublic)

def on_forever():
  global bobKeyPublic
  basic.show_number(keyPrivate)
  radio.send_value("bobKey", bobKeyPublic)
  basic.pause(1000)  

basic.forever(on_forever)

def on_radio_received_value(arg0, arg1):
  global bobKeyPublic
  global sharedSecret
  global key
  global value
  key = arg0
  value = arg1
  if key + "" == "aliceKey" + "":
    aliceKeyPublic = value
    basic.pause(1000)
    sharedSecret = (aliceKeyPublic * keyPrivate)
    basic.show_number(sharedSecret)
radio.on_received_value(on_radio_received_value)
