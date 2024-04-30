#!/usr/bin/env python3
"""
Author:  Iain
Purpose: Multipass TU
"""

# Files
from functions import *
# Libraries
import argparse
from typing import Dict, Any


def get_args():
    """ Get passed args """

    parser = argparse.ArgumentParser(description='Get Help')
    parser.add_argument('-h', '--help', metavar='help',
                        default='Runs a Text Interface for Multipass',
                        help='Info on this util')
    return parser.parse_args()


def main():
    """ Execute program """

    print("*** Program Started ***")
    mp_version = get_multipass_version()
    print(f"MP Version is: {mp_version}")
    print("*** Program Ended ***")


if __name__ == '__main__':
    main()
