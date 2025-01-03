# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import socket

import pytest


###############################################################################
# Public API                                                                ###
###############################################################################
@pytest.fixture
def unused_http_port() -> int:
    for port in range(50000, 50100):
        if not _is_port_in_use(port):
            return port
    raise RuntimeError("No unused HTTP port found")

###############################################################################
# Implementation                                                            ###
###############################################################################

def _is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0
