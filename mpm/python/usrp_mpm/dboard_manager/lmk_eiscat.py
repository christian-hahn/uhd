#
# Copyright 2017 Ettus Research (National Instruments)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
LMK04828 driver for use with Magnesium
"""

import time
from ..mpmlog import get_logger

LMK_CHIP_ID = 6

class LMK04828EISCAT(object):
    """
    LMK04828 controls for EISCAT daughterboard
    """
    def __init__(self, regs_iface, slot=None):
        slot = slot or "-A"
        self.log = get_logger("LMK04828"+slot)
        self.regs_iface = regs_iface
        self.init()
        self.config()

    def pokes8(self, addr_vals):
        """
        Apply a series of pokes
        """
        for addr, val in addr_vals:
            self.regs_iface.poke8(addr, val)

    def init(self):
        """
        Basic init. Turns it on. Let's us read SPI.
        """
        self.log.info("Init LMK")
        self.pokes8((
            (0x000, 0x90), # Assert reset
            (0x000, 0x10), # De-assert reset
            (0x002, 0x00), # De-assert power down
            (0x16E, 0x3B), # PLL2 Lock Detect Config as SDO
        ))
        if not self.verify_chip_id():
            raise Exception("Unable to locate LMK04828")


    def config(self):
        """
        Write lots of config foo.
        """
        self.log.trace("Setting clkout config...")
        self.pokes8((
            (0x100, 0x6C), # CLKout Config
            (0x101, 0x55), # CLKout Config
            (0x103, 0x00), # CLKout Config
            (0x104, 0x20), # CLKout Config
            (0x105, 0x00), # CLKout Config
            (0x106, 0xF3), # CLKout Config
            (0x107, 0x05), # CLKout Config
            (0x108, 0x6C), # CLKout Config
            (0x109, 0x55), # CLKout Config
            (0x10B, 0x00), # CLKout Config
            (0x10C, 0x20), # CLKout Config
            (0x10D, 0x00), # CLKout Config
            (0x10E, 0xF1), # CLKout Config
            (0x10F, 0x05), # CLKout Config
            (0x110, 0x6C), # CLKout Config
            (0x111, 0x55), # CLKout Config
            (0x113, 0x00), # CLKout Config
            (0x114, 0x20), # CLKout Config
            (0x115, 0x00), # CLKout Config
            (0x116, 0xF1), # CLKout Config
            (0x117, 0x05), # CLKout Config
            (0x118, 0x6C), # CLKout Config
            (0x119, 0x55), # CLKout Config
            (0x11B, 0x00), # CLKout Config
            (0x11C, 0x20), # CLKout Config
            (0x11D, 0x00), # CLKout Config
            (0x11E, 0xF1), # CLKout Config
            (0x11F, 0x05), # CLKout Config
            (0x120, 0x78), # CLKout Config
            (0x121, 0x55), # CLKout Config
            (0x123, 0x00), # CLKout Config
            (0x124, 0x20), # CLKout Config
            (0x125, 0x00), # CLKout Config
            (0x126, 0xF3), # CLKout Config
            (0x127, 0x00), # CLKout Config
            (0x128, 0x6C), # CLKout Config
            (0x129, 0x55), # CLKout Config
            (0x12B, 0x00), # CLKout Config
            (0x12C, 0x20), # CLKout Config
            (0x12D, 0x00), # CLKout Config
            (0x12E, 0xF9), # CLKout Config
            (0x12F, 0x00), # CLKout Config
            (0x130, 0x6C), # CLKout Config
            (0x131, 0x55), # CLKout Config
            (0x133, 0x00), # CLKout Config
            (0x134, 0x20), # CLKout Config
            (0x135, 0x00), # CLKout Config
            (0x136, 0xF9), # CLKout Config
            (0x137, 0x00), # CLKout Config
            (0x138, 0x10), # VCO_MUX to VCO 1; OSCout off
            (0x139, 0x00), # SYSREF Source = MUX; SYSREF MUX = Normal SYNC
            (0x13A, 0x01), # SYSREF Divide [12:8]
            (0x13B, 0xE0), # SYSREF Divide [7:0]
            (0x13C, 0x00), # SYSREF DDLY [12:8]
            (0x13D, 0x08), # SYSREF DDLY [7:0] ... 8 is default, <8 is reserved
            (0x13E, 0x00), # SYSREF Pulse Count = 1 pulse/request
            (0x13F, 0x0B), # Feedback Mux: Enabled, DCLKout6, drives PLL1N divider
            (0x140, 0x00), # POWERDOWN options
            (0x141, 0x00), # Dynamic digital delay enable
            (0x142, 0x00), # Dynamic digital delay step
            (0x143, 0xD1), # SYNC edge sensitive; SYSREF_CLR; SYNC Enabled; SYNC fro
            (0x144, 0x00), # Enable SYNC on all outputs including sysref
            (0x145, 0x7F), # Always program to d127
            (0x146, 0x08), # CLKin Type & En
            (0x147, 0x0E), # CLKin_SEL = CLKin1 manual; CLKin1 to PLL1
            (0x148, 0x01), # CLKin_SEL0 = input with pullup
            (0x149, 0x01), # CLKin_SEL1 = input with pulldown
            (0x14A, 0x02), # RESET type as input w/pulldown
            (0x14B, 0x01), # Holdover & DAC Manual Mode
            (0x14C, 0xF6), # DAC Manual Mode
            (0x14D, 0x00), # DAC Settings (defaults)
            (0x14E, 0x00), # DAC Settings (defaults)
            (0x14F, 0x7F), # DAC Settings (defaults)
            (0x150, 0x03), # Holdover Settings (defaults)
            (0x151, 0x02), # Holdover Settings (defaults)
            (0x152, 0x00), # Holdover Settings (defaults)
            (0x153, 0x00), # CLKin0_R divider [13:8], default = 0
            (0x154, 0x0A), # CLKin0_R divider [7:0], default = d120
            (0x155, 0x00), # CLKin1_R divider [13:8], default = 0
            (0x156, 0x01), # CLKin1_R divider [7:0], default = d120
            (0x157, 0x00), # CLKin2_R divider [13:8], default = 0
            (0x158, 0x01), # CLKin2_R divider [7:0], default = d120
            (0x159, 0x00), # PLL1 N divider [13:8], default = 0
            (0x15A, 0x68), # PLL1 N divider [7:0], default = d120
            (0x15B, 0xCF), # PLL1 PFD
            (0x15C, 0x27), # PLL1 DLD Count [13:8]
            (0x15D, 0x10), # PLL1 DLD Count [7:0]
            (0x15E, 0x00), # PLL1 R/N delay, defaults = 0
            (0x15F, 0x13), # Status LD1 pin = PLL2 LD, push-pull output
            (0x160, 0x00), # PLL2 R divider [11:8];
            (0x161, 0x01), # PLL2 R divider [7:0]
            (0x162, 0x24), # PLL2 prescaler; OSCin freq
            (0x163, 0x00), # PLL2 Cal = PLL2 normal val
            (0x164, 0x00), # PLL2 Cal = PLL2 normal val
            (0x165, 0x0C), # PLL2 Cal = PLL2 normal val
            (0x171, 0xAA), # Write this val after x165
            (0x172, 0x02), # Write this val after x165
            (0x17C, 0x15), # VCo1 Cal; write before x168
            (0x17D, 0x33), # VCo1 Cal; write before x168
            (0x166, 0x00), # PLL2 N[17:16]
            (0x167, 0x00), # PLL2 N[15:8]
            (0x168, 0x0C), # PLL2 N[7:0]
            (0x169, 0x51), # PLL2 PFD
            (0x16A, 0x00), # PLL2 DLD Count [13:8] = default d32
            (0x16B, 0x10), # PLL2 DLD Count [7:0] = default d0
            (0x16C, 0x00), # PLL2 Loop filter r = 200 ohm
            (0x16D, 0x00), # PLL2 loop filter c = 10 pF
            (0x173, 0x00), # Do not power down PLL2 or prescaler
        ))
        time.sleep(0.1)
        self.pokes8((
            (0x182, 0x1), # Clear Lock Detect Sticky
            (0x182, 0x0), # Clear Lock Detect Sticky
            (0x183, 0x1), # Clear Lock Detect Sticky
            (0x183, 0x0), # Clear Lock Detect Sticky
        ))
        time.sleep(0.1)
        self.log.trace("Checking PLL lock bits...")
        def check_pll_lock(pll_id, addr):
            pll_lock_status = self.regs_iface.peek8(addr)
            if (pll_lock_status & 0x7) != 0x02:
                self.log.error("LMK {} did not lock. Status: {:x}".format(pll_id, pll_lock_status))
                raise RuntimeError("LMK {} did not lock.".format(pll_id))
        check_pll_lock("PLL1", 0x182)
        check_pll_lock("PLL2", 0x183)
        self.log.trace("Setting SYNC and SYSREF config...")
        self.pokes8((
            (0x143, 0xF1), # toggle SYNC polarity to trigger SYNC event
            (0x143, 0xD1), # toggle SYNC polarity to trigger SYNC event
            (0x139, 0x02), # SYSREF Source = MUX; SYSREF MUX = pulser
            (0x144, 0xFF), # Disable SYNC on all outputs including sysref
            (0x143, 0x52), # Pulser selected; SYNC enabled; 1 shot enabled
        ))
        self.log.info("LMK init'd and locked!")

    def get_chip_id(self):
        """
        Read back the chip ID
        """
        chip_id = self.regs_iface.peek8(0x03)
        self.log.trace("Read chip ID: {}".format(chip_id))
        return chip_id

    def verify_chip_id(self):
        """
        Returns True if the chip ID matches what we expect, False otherwise.
        """
        chip_id = self.get_chip_id()
        if chip_id != LMK_CHIP_ID:
            self.log.error("wrong chip id {0}".format(chip_id))
            return False
        return True

    # TODO delete this
    # def enable_sysref_pulse(self):
        # """
        # Enable SYSREF pulses
        # """
        # self.poke8(0x139, 0x2)
        # self.poke8(0x144, 0xFF)
        # self.poke8(0x143, 0x52)