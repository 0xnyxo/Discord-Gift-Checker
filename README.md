<div align="center">
  <kbd>
  <a href="https://github.com/0xnyxo/Discord-Gift-Checker">
    <img src="https://raw.githubusercontent.com/0xnyxo/Discord-Gift-Checker/main/assets/image.png" alt="Logo" style="width: 110%; height: 110%;">
  </a>
  </kbd>
  
  <h2 align="center">Discord Nitro Checker</h2>
  <p align="center">
    A tool to generate and check the validity of Discord Nitro gift codes.
    <br />
    <a href="https://github.com/0xnyxo/Discord-Gift-Checker#-changelog">📜 ChangeLog</a>
    ·
    <a href="https://github.com/0xnyxo/Discord-Gift-Checker/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/0xnyxo/Discord-Gift-Checker/issues">💡 Request Feature</a>
  </p>
</div>

---

## Discord Gift Checker for Nitro
This script checks for Discord Nitro gift codes and saves valid ones in the `data/valid.txt` file.

### Credits
Made By: @0xnyxo

### Changelog
- **28/05/2024**: Project created

### Description

This script automates the process of generating and validating Discord Nitro gift codes. It generates random codes, checks their validity by making HTTP requests to Discord's API, and logs the results.

### Usage Notes:
- Ensure `xCookie` is populated with a valid session cookie.
- Adjust `max_workers` in `ThreadPoolExecutor` for optimal performance.
