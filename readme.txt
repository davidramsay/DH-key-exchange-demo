This is a working wireless DH key exchange demo for micro:bit dev boards.

a DH key exchange takes place here via wireless radio communications. 
Each device has a private key, and there is a shared public key value. 
Each device encrypts its own private key using the public key, and shares that value with the other device, who then adds their own key to the mix. 
This creates a secure shared key.

This example uses simple multiplication and prime numbers, however real DH key exchanges use more complex mathematics based on modular arithmetic, and share a common primitive root and "generator".
The math is significantly more complicated.
