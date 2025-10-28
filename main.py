#!/usr/bin/env python3
from colorama import init, Fore, Style
import os, shutil, platform, subprocess, sys, random, time

init(autoreset=True)
BLUES = [Fore.CYAN, Fore.LIGHTBLUE_EX]
RESET = Style.RESET_ALL

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def blue_text_effect(text, speed=0.004):
    for ch in text:
        if ch not in (" ", "\n"):
            color = random.choice(BLUES)
            print(color + ch + RESET, end="", flush=True)
        else:
            print(ch, end="", flush=True)
        time.sleep(speed)
    print()

def header(title):
    clear()
    blue_text_effect("\nWinter-HacksV1\n" + title + "\n")

def pause():
    blue_text_effect("\nPress Enter to continue...")
    input()

def check_nmap():
    return shutil.which("nmap") is not None

def detect_package_manager():
    sysname = platform.system().lower()
    if sysname == "linux":
        if shutil.which("apt"):
            return "sudo apt update && sudo apt install -y nmap"
        if shutil.which("pkg"):
            return "pkg install nmap -y"
        if shutil.which("dnf"):
            return "sudo dnf install -y nmap"
    if sysname == "windows":
        if shutil.which("choco"):
            return "choco install nmap -y"
        return "Install via https://nmap.org/download.html"
    if sysname == "darwin":
        return "brew install nmap"
    return "Manual install: https://nmap.org/download.html"

NMAP_SCANS = [
    ("Normal scan", ["-sS", "-Pn", "-T4", "-v"]),
    ("TCP SYN scan", ["-sS", "-T4", "-Pn"]),
    ("TCP connect scan", ["-sT", "-T4", "-Pn"]),
    ("UDP scan", ["-sU", "-T3", "-Pn"]),
    ("Version detection", ["-sV", "-T4", "-Pn"]),
    ("OS detection", ["-O", "-T4", "-Pn"]),
    ("Aggressive scan", ["-A", "-T4", "-Pn"]),
    ("Ping scan (hosts only)", ["-sn"]),
    ("Top ports scan (fast)", ["--top-ports", "100", "-sS", "-T4", "-Pn"]),
    ("Full port scan (0-65535)", ["-p", "1-65535", "-sS", "-T4", "-Pn"]),
]

def run_nmap_scan(scan_idx):
    idx = scan_idx - 1
    if idx < 0 or idx >= len(NMAP_SCANS):
        blue_text_effect("Invalid scan selection.")
        pause()
        return
    if not check_nmap():
        header("Run Scan")
        blue_text_effect("Nmap is not installed. Use Tool Installer first.")
        pause()
        return
    scan_name, args = NMAP_SCANS[idx]
    header("Run Scan")
    blue_text_effect(f"Selected scan: {scan_name}")
    target = input(Fore.CYAN + "\nEnter target (IP or hostname): " + RESET).strip()
    if not target:
        blue_text_effect("No target entered. Cancelled.")
        pause()
        return
    confirm = input(Fore.CYAN + "Execute scan now? [y/N] " + RESET).strip().lower()
    if confirm != "y":
        blue_text_effect("Scan cancelled.")
        pause()
        return
    blue_text_effect("\nRunning scan... (output will appear below)\n")
    cmd = ["nmap"] + args + [target]
    try:
        subprocess.run(cmd, check=False)
    except FileNotFoundError:
        blue_text_effect("nmap executable not found in PATH.")
    except Exception as e:
        blue_text_effect(f"Scan failed: {e}")
    blue_text_effect("\nScan finished.")
    pause()

def show_nmap_menu():
    while True:
        header("NMAP Scans")
        blue_text_effect("Choose a scan to run:")
        for i, (name, _) in enumerate(NMAP_SCANS, 1):
            blue_text_effect(f"[{i}] {name}")
        blue_text_effect("[0] Back")
        choice = input(Fore.CYAN + "\nPick a number: " + RESET).strip()
        if not choice.isdigit():
            blue_text_effect("Please enter a number.")
            pause()
            continue
        num = int(choice)
        if num == 0:
            return
        run_nmap_scan(num)

def tool_installer():
    header("Tool Installer")
    cmd = detect_package_manager()
    blue_text_effect("Install command suggestion:")
    blue_text_effect(cmd)
    if check_nmap():
        blue_text_effect("\nNmap already installed.")
        pause()
        return
    run = input(Fore.CYAN + "\nRun the install command now? [y/N] " + RESET).strip().lower()
    if run == "y":
        clear()
        blue_text_effect("Attempting install... (may require sudo/root)\n")
        try:
            subprocess.run(cmd, shell=True, check=True)
            blue_text_effect("\nInstall command finished.")
        except Exception as e:
            blue_text_effect(f"\nInstall failed or needs manual steps: {e}")
    else:
        blue_text_effect("Installer cancelled.")
    pause()

def tool_checker():
    header("Tool Checker")
    if check_nmap():
        blue_text_effect("Everything installed and Working!")
    else:
        blue_text_effect("You are missing:\nNMAP")
    pause()

def internet_scanning():
    show_nmap_menu()

def main_menu():
    while True:
        header("Main Menu")
        blue_text_effect("Winter-HacksV1")
        blue_text_effect("[1] Internet Scanning")
        blue_text_effect("[2] Tool Installer")
        blue_text_effect("[3] Tool Checker")
        blue_text_effect("[0] Exit")
        ch = input(Fore.CYAN + "\nChoose: " + RESET).strip()
        if ch == "1":
            internet_scanning()
        elif ch == "2":
            tool_installer()
        elif ch == "3":
            tool_checker()
        elif ch == "0":
            header("Goodbye!")
            blue_text_effect("Exiting program...")
            break
        else:
            blue_text_effect("Invalid choice.")
            pause()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        clear()
        blue_text_effect("\nInterrupted. Exiting...")
