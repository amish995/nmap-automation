import argparse
import os
from subprocess import check_output
import threading
import logging
import time

parser = argparse.ArgumentParser(description='Nmap automation script to scan a list of IPs to perform SSL checks and export an excel sheet with the highligted weak ciphers')
parser.add_argument('--ip_list_file', type=str, help='Provide the filname for the list of IPs to scan. Ensure the file is in the same directory as this script')

args = parser.parse_args()

dirpath = os.getcwd()
print(dirpath)

with open(args.ip_list_file) as f:
    ip_list = f.readlines()

ip_list = [line.rstrip('\n') for line in ip_list]
print("The following IPs will be scanned:")
for i in ip_list:
    print(i)

def run_nmap_scan(IP):
    logging.info("Starting scan on {}".format(IP))
    nmap_cmd = 'nmap -p- -T4 -Pn --script=+ssl-cert,+ssh2-enum-algos,+ssl-enum-ciphers {} -oN {}_out.txt'.format(IP, IP)
    check_output(nmap_cmd, shell=True)
    logging.info("Scan on {} completed".format(IP))

if __name__ == "__main__":
    scan_proc = threading.Thread(target=run_nmap_scan, args=ip_list)
    logging.info("Scans starting")
    scan_proc.start
    logging.info("Scans completed")