#! /usr/bin/env python3

def isiterable(obj):
    """Check if object is iterable."""
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return True
