# 📡 Signal Challenge

## Overview

This challenge plays on the concept of encoded communication — your goal is to decode a scrambled signal transmission and recover the flag.

A file named `signal.txt` contains an obfuscated message. Use the provided decryption key in `clue.txt` to retrieve the original flag.

## Files

- `signal.txt` – the scrambled message (encrypted + base64 + reversed)
- `clue.txt` – the Fernet encryption key (base64) and a small hint

## Objective

> Reverse the encoding steps and decrypt the message using the provided key to obtain the flag in the format:
>  
> `HTB{...}`

## Hints

- Data is reversed
- Then base64 encoded
- Then encrypted using [Fernet](https://cryptography.io/en/latest/fernet/)

## Tools You Might Need

- Python (for Fernet decryption)
- Base64 decoder
- Basic string manipulation

---

Decrypt the noise. Hear the signal.
