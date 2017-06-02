import binascii
import serial
import time
import logging

class SamsungRemote(object):
    """Class summary here

    More class info
    More class info

    Attributes:
        port_name: A string name of serial port to use for communicating with 
            the TV.  Example: 'COM3'
        baud_rate: An integer specifying the baud rate of the serial port.
            Defaults to 19200, the setting for the Samsung HLS6187W.
        logger: A standard Python logging class instance.
    """
    def __init__(self, port_name, log_level=logging.INFO, baud_rate=19200):
        """Initializes SamsungRemote with the given settings.
        """
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.init_logging(log_level)

    def toggle_power(self):
        """
        """
        self.logger.info('toggling power')
        self.send_receive(0x08, 0x22, 0x00, 0x00, 0x00, 0)

    def set_volume(self, volume_level):
        """
        """
        if volume_level > 100:
            self.logger.error('volume requested out of range: %d', volume_level)
            return

        self.logger.info('setting volume to %d', volume_level)
        self.send_receive(0x08, 0x22, 0x01, 0x00, 0x00, volume_level)

    def set_source(self, source_name):
        """
        """
        source = -1
        if source_name is 'tv':
            source = 0
        elif source_name is 'av1':
            source = 1
        elif source_name is 'av2':
            source = 2
        elif source_name is 'svideo1':
            source = 3
        elif source_name is 'svideo2':
            source = 4
        elif source_name is 'comp1':
            source = 5
        elif source_name is 'comp2':
            source = 6
        elif source_name is 'pc':
            source = 7
        elif source_name is 'hdmi1':
            source = 8
        elif source_name is 'hdmi2':
            source = 9
        elif source_name is 'av3':
            source = 10      
        else:
            self.logger.error('invalid source name %s', source_name)
            return

        self.logger.info('setting source to %s', source_name)
        self.send_receive(0x08, 0x22, 0x0a, 0x00, 0x00, source)

    def open(self):
        """
        """
        self.logger.debug('opening %s', self.port_name)
        self.port = serial.Serial(self.port_name, self.baud_rate, 8, 
            serial.PARITY_NONE, serial.STOPBITS_ONE, xonxoff=0, rtscts=0, 
            timeout=1)

    def close(self):
        """
        """
        self.logger.debug('closing %s', self.port_name)
        self.port.close()

    def send_receive(self, hdr1, hdr2, cmd1, cmd2, cmd3, val):
        """
        """
        if self.port.isOpen() == False:
            self.logger.error('Tried to send a command but port wasn\'t open')
            return

        command = bytearray([hdr1, hdr2, cmd1, cmd2, cmd3, val])

        checksum = -(sum(command) % 256) & 0xff
        command.append(checksum)

        hexstr = str(binascii.hexlify(command))
        formatted_hex = ' '.join(hexstr[i:i+2] for i in range(0, len(hexstr), 2))

        self.port.write(command)        
        self.logger.debug('sent %s', formatted_hex)

        resp = self.port.readline()
        formatted_resp = ' '.join("{:02x}".format(ord(c)) for c in resp)
        self.logger.debug('received %s', formatted_resp)

        if resp == b'\x03\x0c\xf1':
            self.logger.info('command valid')
            return True
        else:
            self.logger.error('command failed')
            return False

    def init_logging(self, log_level):
        """Initialize logging for the remote

        Args:
            log_level: A enum which can be DEBUG, INFO, WARNING, ERROR,
                or CRITICAL.  Example: logging.INFO
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] '
            '%(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.debug('logging initialized')
