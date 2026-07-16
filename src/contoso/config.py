"""Runtime configuration constants.

TRANSFER_LIMIT is the headline limit. The throttle below is enforced per second.
The default window is measured in seconds.
"""

TRANSFER_LIMIT = 100
THROTTLE_PER_SECOND = 20
DEFAULT_WINDOW_SECONDS = 60
