#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**aces_rgb.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines **Color** package *ACES RGB* colorspace.

**Others:**

"""

from __future__ import unicode_literals

import math

import numpy

import color.illuminants
import color.utilities.exceptions
import color.utilities.data_structures
import color.utilities.verbose
from color.colorspaces.colorspace import Colorspace


__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2013 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["ACES_RGB_PRIMARIES",
           "ACES_RGB_WHITEPOINT",
           "ACES_RGB_TO_XYZ_MATRIX",
           "XYZ_TO_ACES_RGB_MATRIX",
           "ACES_RGB_TRANSFER_FUNCTION",
           "ACES_RGB_INVERSE_TRANSFER_FUNCTION",
           "ACES_RGB_COLORSPACE",
           "ACES_RGB_LOG_CONSTANTS",
           "ACES_RGB_LOG_TRANSFER_FUNCTION",
           "ACES_RGB_LOG_INVERSE_TRANSFER_FUNCTION",
           "ACES_RGB_LOG_COLORSPACE",
           "ACES_RGB_PROXY_10_CONSTANTS",
           "ACES_RGB_PROXY_12_CONSTANTS",
           "ACES_RGB_PROXY_CONSTANTS",
           "ACES_RGB_PROXY_10_TRANSFER_FUNCTION",
           "ACES_RGB_PROXY_10_INVERSE_TRANSFER_FUNCTION",
           "ACES_RGB_PROXY_12_TRANSFER_FUNCTION",
           "ACES_RGB_PROXY_12_INVERSE_TRANSFER_FUNCTION",
           "ACES_RGB_PROXY_10_COLORSPACE",
           "ACES_RGB_PROXY_12_COLORSPACE"]

LOGGER = color.utilities.verbose.install_logger()

# http://www.oscars.org/science-technology/council/projects/aces.html
# http://www.dropbox.com/sh/iwd09buudm3lfod/gyjDF-k7oC/ACES_v1.0.1.pdf: 4.1.2 Color space chromaticities
ACES_RGB_PRIMARIES = numpy.matrix([0.73470, 0.26530,
                                   0.00000, 1.00000,
                                   0.00010, -0.07700]).reshape((3, 2))

ACES_RGB_WHITEPOINT = color.illuminants.ILLUMINANTS.get("Standard CIE 1931 2 Degree Observer").get("D60")

# http://www.dropbox.com/sh/iwd09buudm3lfod/gyjDF-k7oC/ACES_v1.0.1.pdf:
# 4.1.4 Converting ACES RGB values to CIE XYZ values
ACES_RGB_TO_XYZ_MATRIX = numpy.matrix([9.52552396e-01, 0.00000000e+00, 9.36786317e-05,
                                       3.43966450e-01, 7.28166097e-01, -7.21325464e-02,
                                       0.00000000e+00, 0.00000000e+00, 1.00882518e+00]).reshape((3, 3))

XYZ_TO_ACES_RGB_MATRIX = ACES_RGB_TO_XYZ_MATRIX.getI()

ACES_RGB_TRANSFER_FUNCTION = lambda x: x

ACES_RGB_INVERSE_TRANSFER_FUNCTION = lambda x: x

ACES_RGB_COLORSPACE = Colorspace("ACES RGB",
                                 ACES_RGB_PRIMARIES,
                                 ACES_RGB_WHITEPOINT,
                                 ACES_RGB_TO_XYZ_MATRIX,
                                 XYZ_TO_ACES_RGB_MATRIX,
                                 ACES_RGB_TRANSFER_FUNCTION,
                                 ACES_RGB_INVERSE_TRANSFER_FUNCTION)

ACES_RGB_LOG_CONSTANTS = color.utilities.data_structures.Structure(log_unity=32768,
                                                         log_xperstop=2048,
                                                         denorm_trans=math.pow(2., -15),
                                                         denorm_fake0=math.pow(2., -16))


def __aces_rgb_log_transfer_function(value, is_16_bit_integer=False):
    """
    Defines the *ACES RGB Log* colorspace transfer function.

    Reference: http://www.dropbox.com/sh/iwd09buudm3lfod/AAA-X1nVs_XLjWlzNhfhqiIna/ACESlog_v1.0.pdf

    :param value: value.
    :type value: float
    :param is_16_bit_integer: Is value 16 bit integer.
    :type is_16_bit_integer: bool
    :return: Companded value.
    :rtype: float
    """

    if value < 0.:
        return 0.

    if value < ACES_RGB_LOG_CONSTANTS.denorm_trans:
        value = ACES_RGB_LOG_CONSTANTS.denorm_fake0 + (value / 2.)

    value = (math.log10(value) / math.log10(2)) * ACES_RGB_LOG_CONSTANTS.log_xperstop + ACES_RGB_LOG_CONSTANTS.log_unity

    if is_16_bit_integer:
        value = min(math.floor(value) + 0.5, 65535)

    return value


def __aces_rgb_log_inverse_transfer_function(value):
    """
    Defines the *ACES RGB Log* colorspace inverse transfer function.

    Reference: http://www.dropbox.com/sh/iwd09buudm3lfod/AAA-X1nVs_XLjWlzNhfhqiIna/ACESlog_v1.0.pdf

    :param value: value.
    :type value: float
    :return: Companded value.
    :rtype: float
    """

    value = math.pow(2., (value - ACES_RGB_LOG_CONSTANTS.log_unity) / ACES_RGB_LOG_CONSTANTS.log_xperstop)
    if value < ACES_RGB_LOG_CONSTANTS.denorm_trans:
        value = (value - ACES_RGB_LOG_CONSTANTS.denorm_fake0) * 2.

    return value


ACES_RGB_LOG_TRANSFER_FUNCTION = __aces_rgb_log_transfer_function

ACES_RGB_LOG_INVERSE_TRANSFER_FUNCTION = __aces_rgb_log_inverse_transfer_function

ACES_RGB_LOG_COLORSPACE = Colorspace("ACES RGB Log",
                                     ACES_RGB_PRIMARIES,
                                     ACES_RGB_WHITEPOINT,
                                     ACES_RGB_TO_XYZ_MATRIX,
                                     XYZ_TO_ACES_RGB_MATRIX,
                                     ACES_RGB_LOG_TRANSFER_FUNCTION,
                                     ACES_RGB_LOG_INVERSE_TRANSFER_FUNCTION)

ACES_RGB_PROXY_10_CONSTANTS = color.utilities.data_structures.Structure(CV_min=0.,
                                                              CV_max=1023.,
                                                              steps_per_stop=50.,
                                                              mid_CV_offset=425.,
                                                              mid_log_offset=-2.5)

ACES_RGB_PROXY_12_CONSTANTS = color.utilities.data_structures.Structure(CV_min=0.,
                                                              CV_max=4095.,
                                                              steps_per_stop=200.,
                                                              mid_CV_offset=1700.,
                                                              mid_log_offset=-2.5)

ACES_RGB_PROXY_CONSTANTS = {"10 bit": ACES_RGB_PROXY_10_CONSTANTS,
                            "12 bit": ACES_RGB_PROXY_12_CONSTANTS}


def __aces_rgb_proxy_transfer_function(value, bit_depth="10 bit"):
    """
    Defines the *ACES RGB Proxy* colorspace transfer function.

    Reference: http://www.dropbox.com/sh/iwd09buudm3lfod/AAAsl8WskbNNAJXh1r0dPlp2a/ACESproxy_v1.1.pdf

    :param value: value.
    :type value: float
    :param bit_depth: *ACES RGB Proxy* bit depth.
    :type bit_depth: str ("10 bit", "12 bit")
    :return: Companded value.
    :rtype: float
    """

    constants = ACES_RGB_PROXY_CONSTANTS.get(bit_depth)

    if value > 0.:
        return max(constants.CV_min, min(constants.CV_max, (math.log10(value) / (
            math.log10(2)) - constants.mid_log_offset) * constants.steps_per_stop + constants.mid_CV_offset)) + 0.5
    else:
        return constants.CV_min


def __aces_rgb_proxy_inverse_transfer_function(value, bit_depth="10 bit"):
    """
    Defines the *ACES RGB Proxy* colorspace inverse transfer function.

    Reference: http://www.dropbox.com/sh/iwd09buudm3lfod/AAAsl8WskbNNAJXh1r0dPlp2a/ACESproxy_v1.1.pdf

    :param value: value.
    :type value: float
    :param bit_depth: *ACES RGB Proxy* bit depth.
    :type bit_depth: str ("10 bit", "12 bit")
    :return: Companded value.
    :rtype: float
    """

    constants = ACES_RGB_PROXY_CONSTANTS.get(bit_depth)

    return math.pow(2., (((value - constants.mid_CV_offset) / constants.steps_per_stop) + constants.mid_log_offset))


ACES_RGB_PROXY_10_TRANSFER_FUNCTION = lambda x: __aces_rgb_proxy_transfer_function(x, bit_depth="10 bit")

ACES_RGB_PROXY_10_INVERSE_TRANSFER_FUNCTION = lambda x: __aces_rgb_proxy_inverse_transfer_function(x,
                                                                                                   bit_depth="10 bit")

ACES_RGB_PROXY_12_TRANSFER_FUNCTION = lambda x: __aces_rgb_proxy_transfer_function(x, bit_depth="12 bit")

ACES_RGB_PROXY_12_INVERSE_TRANSFER_FUNCTION = lambda x: __aces_rgb_proxy_inverse_transfer_function(x,
                                                                                                   bit_depth="12 bit")

ACES_RGB_PROXY_10_COLORSPACE = Colorspace("ACES RGB Proxy 10",
                                          ACES_RGB_PRIMARIES,
                                          ACES_RGB_WHITEPOINT,
                                          ACES_RGB_TO_XYZ_MATRIX,
                                          XYZ_TO_ACES_RGB_MATRIX,
                                          ACES_RGB_PROXY_10_TRANSFER_FUNCTION,
                                          ACES_RGB_PROXY_10_INVERSE_TRANSFER_FUNCTION)

ACES_RGB_PROXY_12_COLORSPACE = Colorspace("ACES RGB Proxy 12",
                                          ACES_RGB_PRIMARIES,
                                          ACES_RGB_WHITEPOINT,
                                          ACES_RGB_TO_XYZ_MATRIX,
                                          XYZ_TO_ACES_RGB_MATRIX,
                                          ACES_RGB_PROXY_12_TRANSFER_FUNCTION,
                                          ACES_RGB_PROXY_12_INVERSE_TRANSFER_FUNCTION)