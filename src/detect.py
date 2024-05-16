#!/usr/bin/env python3

import multiprocessing
import socket
import time

from main import Config

# Define the port knock sequence
# KNOCK_SEQUENCE = [7000, 8000, 9000]

# Dictionary to store knock sequences for each IP address
knock_sequences = {}

def _worker(port):
    """Worker function to listen on a specific port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connection received from {addr[0]} on port {port}")
                # Add the port to the knock sequence for this IP address
                if addr[0] not in knock_sequences:
                    knock_sequences[addr[0]] = []
                knock_sequences[addr[0]].append(port)

def detect_knock_sequence():
    """Detect the port knock sequence using multiprocessing."""

    knock_sequence: list[int] = Config.vars[knock_sequences]
    max_knock_attempts: int = Config.vars['max_knock_attempts']

    pool = multiprocessing.Pool()
    for port in knock_sequence:
        pool.apply_async(_worker, args=(port,))

    attempts = 0
    while attempts < max_knock_attempts:
        for ip, sequence in knock_sequences.items():
            if sequence == knock_sequence:
                print(f"Knock sequence detected from IP address {ip}!")
                # Reset the knock sequence for this IP address
                knock_sequences[ip] = []
        time.sleep(1)  # Sleep to reduce CPU usage
        attempts += 1

    pool.close()
    pool.join()


if __name__ == "__main__":
    detect_knock_sequence()
