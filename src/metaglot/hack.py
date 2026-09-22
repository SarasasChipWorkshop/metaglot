"""Runtime hacks over third-party dependencies.

Each hack should be applied at the very start of ``main`` and
documents why it exists and when it can be dropped.
"""

import sys
import liquid.builtin.expressions.primitive as _primitive

# TODO:
# When python-liquid relax the boundary of range literal,
# remove this hack.


def relax_liquid_range_literal_boundary() -> None:
    """Relax python-liquid's range literal bounds.

    python-liquid (pinned to 2.3.1) clamps the endpoints of range literals
    such as ``(1000..1028)`` to plus/minus 1024, silently truncating the
    loop to 1000..1023. Windows RC string identifiers legitimately go up
    to 65535, so templates iterating numeric ID ranges lose entries
    without any error. Relax the bounds the library itself defines
    to a more large boundary (as its commented)
    """
    _primitive.MAX_RANGE = sys.maxsize
    _primitive.MIN_RANGE = -sys.maxsize
