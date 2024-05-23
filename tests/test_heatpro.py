#!/usr/bin/env python

"""Tests for `heatpro` package."""

import pytest
    
def test_import():
    try:
        import heatpro
        
    except ImportError as e:
        assert False, f"Import error : {e}"
        

