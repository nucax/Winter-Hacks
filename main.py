#!/usr/bin/env python3
# Real skids use this one :')
from colorama import init, Fore, Style
import os, shutil, platform, subprocess, sys

init(autoreset=True)
BLUE = Fore.CYAN
DARK = Fore.BLUE
RESET = Style.RESET_ALL

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header(title):
    print(DARK + "\nWinter-HacksV1\n" + BLUE + title + RESET + "\n")

def pause():
    input(BLUE + "\nPress Enter to continue..." + RESET)

def check_nmap():
    return shutil.which("nmap") is not None

def tool_checker():
    header("Tool Checker")
    if check_nmap():
        print(BLUE + "Everything installed and Working!" + RESET)
    else:
        print(BLUE + "You are missing:\nNMAP" + RESET)
    pause()

def detect_package_manager():
    sysname = platform.system().lower()
    if sysname == "linux":
        if shutil.which("apt"):
            return "sudo apt update && sudo apt install -y nmap"
        if shutil.which("pkg"):
            return "pkg install nmap -y"
    elif sysname == "windows":
        return "choco install nmap -y"
    elif sysname == "darwin":
        return "brew install nmap"
    return "Manual install: https://nmap.org/download.html"

def tool_installer():
    header("Tool Installer")
    cmd = detect_package_manager()
    print(BLUE + "Command to fetch newest nmap:\n" + RESET + cmd)
    if check_nmap():
        print(BLUE + "\nNmap already installed." + RESET)
        pause()
        return
    run = input(BLUE + "\nRun install command now? [y/N] " + RESET).lower()
    if run == "y":
        try:
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            print(BLUE + f"Install failed: {e}" + RESET)
    pause()

NMAP_SCANS = [
    ("Normal scan", "-sS -Pn -T4 -v"),
    ("TCP SYN scan", "-sS -T4 -Pn"),
    ("TCP connect scan", "-sT -T4 -Pn"),
    ("UDP scan", "-sU -T3 -Pn"),
    ("Version detection", "-sV -T4 -Pn"),
    ("OS detection", "-O -T4 -Pn"),
    ("Aggressive scan", "-A -T4 -Pn"),
    ("Ping scan", "-sn"),
    ("Top ports scan", "--top-ports 100 -T4 -Pn"),
    ("Full port scan", "-p 1-65535 -T4 -Pn"),
]

def show_nmap_commands():
    header("NMAP Scanning Commands")
    for i, (name, args) in enumerate(NMAP_SCANS, 1):
        print(f"[{i}] {name}\n    nmap {args} <target>\n")
    pause()

def internet_scanning():
    header("Internet Scanning")
    print(BLUE + "[1] NMAP Scanning Commands" + RESET)
    print("[0] Back")
    ch = input(BLUE + "\nChoose: " + RESET)
    if ch == "1":
        show_nmap_commands()

def main_menu():
    while True:
        clear()
        header("Main Menu")
        print(BLUE + "Winter-HacksV1" + RESET)
        print("[1] Internet Scanning")
        print("[2] Tool Installer")
        print("[3] Tool Checker")
        print("[0] Exit")
        ch = input(BLUE + "\nChoose: " + RESET)
        if ch == "1":
            internet_scanning()
        elif ch == "2":
            tool_installer()
        elif ch == "3":
            tool_checker()
        elif ch == "0":
            print(BLUE + "Goodbye!" + RESET)
            break
        else:
            print(BLUE + "Invalid choice." + RESET)
            pause()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(BLUE + "\nInterrupted. Exiting." + RESET)
