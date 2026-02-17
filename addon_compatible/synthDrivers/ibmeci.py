# -*- coding: utf-8 -*-
# Copyright (C) 2009 - 2025 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
# synthDrivers/ibmeci.py - Dispatcher for 32-bit and 64-bit implementations

"""
This file acts as a dispatcher, loading the appropriate implementation
based on the NVDA version and architecture.

- NVDA 2026.1+ (64-bit): Uses _ibmeci64.py (proxy via synthDriverHost32)
- NVDA < 2026.1 (32-bit): Uses _ibmeci32.py (direct ctypes)
"""

import sys
import os

# Detect NVDA version
def get_nvda_version():
	"""Get NVDA version as a tuple (major, minor, patch)"""
	try:
		import globalVars
		if hasattr(globalVars, 'nvdaVersion'):
			version_str = globalVars.nvdaVersion.split('-')[0]  # Handle beta versions like "2026.1-beta1"
			return tuple(map(int, version_str.split('.')))
	except Exception:
		pass
	return (0, 0, 0)

# Detect if we have synthDriverHost32 support
def has_synthdriver_host32():
	"""Check if synthDriverHost32 runtime is available"""
	try:
		from _bridge.clients.synthDriverHost32 import launcher
		return hasattr(launcher, "isSynthDriverHost32RuntimeAvailable") \
		       and launcher.isSynthDriverHost32RuntimeAvailable()
	except ImportError:
		return False

# Version constants
NVDA_2026_1 = (2026, 1, 0)
current_version = get_nvda_version()

# Load appropriate implementation
if current_version >= NVDA_2026_1 and has_synthdriver_host32():
	# ========================================================================
	# NVDA 2026.1+ (64-bit) - Use synthDriverHost32 proxy
	# ========================================================================

	# Import and expose the 64-bit implementation
	from . import _ibmeci64 as _impl

	# Export the SynthDriver class from 64-bit implementation
	SynthDriver = _impl.SynthDriver

elif sys.maxsize > 2**32:
	# ========================================================================
	# NVDA 64-bit but no synthDriverHost32 - Should not happen on 2026.1+
	# ========================================================================

	# Use the 64-bit implementation anyway - it has its own fallback
	from . import _ibmeci64 as _impl
	SynthDriver = _impl.SynthDriver

else:
	# ========================================================================
	# NVDA 32-bit (< 2026.1) - Use direct ctypes implementation
	# ========================================================================

	# Import and expose the 32-bit implementation
	from . import _ibmeci32 as _impl

	# Export the SynthDriver class from 32-bit implementation
	SynthDriver = _impl.SynthDriver


# Export the selected SynthDriver class
__all__ = ['SynthDriver']
