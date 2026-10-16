# DH-key-exchange-demo
A working wireless Diffie-Hellman (DH) key exchange demo for micro:bit dev boards.

Two micro:bits, Alice and Bob, agree on a shared secret number over radio without ever sending that number, or their private keys, over the air.

## How it works
Both boards share two **public** values (anyone listening is allowed to know these values):
- `p = 29`, a prime number called the **modulus**. In a real DH exchange, this would be a 2048 bit prime number, here it is just a small prime number that is easier to wrap out human brains around.
- `g = 2`, the **generator**. This is the number each board starts with, and raises to the power of its private key, e.g. 2^12 in Bob's case.

- Not every number works well as a generator. If you keep multiplying 2 by itself and taking the remainder after dividing by 29, you get 2, 4, 8, 16, 3, 6, 12, 24, 19, 9, … and you land on **every number from 1 to 28** once before the pattern repeats.
- That matters because it means a board's public value could be any of those 28 numbers, so an eavesdropper has the most possibilities to guess from. A poor choice, like `g = 28`, only ever produces 28 or 1 (28 × 28 = 784, which is 1 more than 27 × 29), so there would be just two possible public values and nothing to hide. (Mathematicians call a number like 2 that reaches every value a *primitive root* of 29.)
  
Each board also has a **private key** that it never sends, which is typically a 256 bit random value generated fresh for each session.

| Step | Alice | Bob |
|---|---|---|
| Private key (secret) | a = 23 | b = 12 |
| Public value: gˣ mod p | 2²³ mod 29 = **10** | 2¹² mod 29 = **7** |
| Sends over radio | 10 | 7 |
| Shared secret: (received value)ˣ mod p | 7²³ mod 29 = **20** | 10¹² mod 29 = **20** |

Both boards arrive at the same number because
(gᵇ)ᵃ = (gᵃ)ᵇ = gᵃᵇ (mod p).

The generator raised to the power of b, then multiplied by a is equal to the generator raised to the power of a, then multiplied by b. 

That makes sense when you look at it as a formula:
- Alice: (2¹²)²³ = 2^(12 × 23) = 2²⁷⁶
- Bob: (2²³)¹² = 2^(23 × 12) = 2²⁷⁶

The trippy and crazy math law that this takes advantage of is that the remainder of the generator raised to the power of a multiplied by b, is also equal to the same value.

An eavesdropper sees p (public key, 29), g (generator, 2), 10 and 7. To get the shared secret they would need a private key, which means solving 2ˣ mod 29 = 10. This is the **discrete logarithm problem**. Unlike undoing multiplication, which is just division, there is no known shortcut for it.

## This is a teaching demo, not secure crypto
With p = 29 there are only 28 possible keys, so an eavesdropper can try them all instantly. Real DH uses the same steps but with:
- a 2048-bit (or larger) safe prime for p, or elliptic curves (e.g. X25519)
- large random private keys, regenerated for every session
- a key derivation function (e.g. HKDF) to turn the shared secret into an encryption key
- authentication (e.g. signatures/certificates), since plain DH can't detect a man-in-the-middle

With p = 29 there were 28 possible values. With a 2048-bit p, the number of possible values is about p itself:

≈ 2²⁰⁴⁷ ≈ 1.6 × 10⁶¹⁶. That’s a 1 followed by 616 zeros.

## Running it
Upload `alicesMicroBit.py` to one micro:bit and `bobsMicroBit.py` to another, then power both on.

Each board scrolls **K** followed by its private key (`K23` / `K12`) while it waits. Once it receives the other board's public value, it switches to **S** followed by the shared secret. Both boards should show `S20`.

## Note on choosing keys
Because g²⁸ mod 29 = 1, exponents effectively wrap around modulo 28. If a × b leaves a remainder of 1 when divided by 28 (e.g. 23 × 11 = 253 = 9 × 28 + 1), the shared secret will always equal g. Pick keys that avoid this to keep the demo less confusing.
