#!/usr/bin/env python

import logging
from samsung_remote import SamsungRemote

def main():
    # TODO argparse
    remote = SamsungRemote('COM3', log_level=logging.DEBUG)
    remote.open()
    remote.set_volume(4)
    # remote.set_source('tv')
    # remote.toggle_power()
    remote.close()

if __name__ == '__main__':
    main()
