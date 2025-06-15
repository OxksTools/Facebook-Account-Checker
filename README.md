# 🔐 Facebook Account Verifier - OxksTools

A threaded Facebook login verifier built with Python. This tool checks email:password combos against Facebook's login flow, using rotating proxies and intelligently crafted request headers. It can detect valid logins, 2FA requirements, and common error responses.

---

## 🧩 Key Capabilities

- ⚡ **Concurrent login checks** (multi-threaded)
- 🌐 **Smart proxy cycling** to reduce request blocking
- 🔍 **Response analysis** to identify:
  - ✅ Logged-in accounts
  - 🔐 Two-factor authentication prompts
  - ❌ Invalid credentials
  - 🚫 Rate-limited responses
- 🧬 Uses **Base64-encoded session payloads** for obfuscation and realism

---

## 📁 Included Resources

| File Name      | Purpose                                         |
|----------------|-------------------------------------------------|
| `combo.txt`    | Your list of `email:password` combos to test    |
| `proxies.txt`  | HTTP proxies to be used (one per line)          |
| `valids.txt`   | All successful login credentials are saved here |
| `2fa.txt`      | Accounts requiring 2FA are recorded here        |

---

## 🧪 How It Works

1. **Loads input** from combo and proxy files.
2. **Encodes** a special session payload (`privacy_mutation_token`) using Base64.
3. **Generates spoofed headers**, including a dynamic user-agent string.
4. **Performs POST requests** to Facebook’s login endpoint.
5. **Parses responses** to determine login result (success, 2FA, invalid, etc.).
6. **Logs results** to the appropriate output file.

---



📌 **Note:** Make sure `combo.txt` and `proxies.txt` are in the same directory as `main.py`.

---

## 🔍 Advanced Notes

- 🧠 **Session Payload Encoding**: This tool crafts a `privacy_mutation_token` by encoding a small JSON payload. This simulates part of a Facebook session token and can help mimic real login behavior.
- 🦾 **Proxy Handling**: Proxies are looped in a cycle so that every request gets a new proxy in sequence.
- ⚠️ Avoid using public or slow proxies for better accuracy and speed.

---

## ⚖️ Legal Notice

This project is intended **strictly for educational, testing, and cybersecurity research purposes**.  
Misuse of this tool may violate laws or terms of service.  
**You are responsible** for how you use this code.

---

## 🌟 Credits

Part of the `OxksTools` collection. Designed for learning about web request flows and login handling mechanisms.
