#!/usr/bin/env python3

import multiprocessing
import socket
import time

# Define the port knock sequence
KNOCK_SEQUENCE = [7000, 8000, 9000]

# Dictionary to store knock sequences for each IP address
knock_sequences = {}

def worker(port):
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
    pool = multiprocessing.Pool()
    for port in KNOCK_SEQUENCE:
        pool.apply_async(worker, args=(port,))

    # Check the knock sequences periodically
    while True:
        for ip, sequence in knock_sequences.items():
            if sequence == KNOCK_SEQUENCE:
                print(f"Knock sequence detected from IP address {ip}!")
                # Reset the knock sequence for this IP address
                knock_sequences[ip] = []
        time.sleep(1)  # Sleep to reduce CPU usage

    pool.close()
    pool.join()

if __name__ == "__main__":
    detect_knock_sequence()
