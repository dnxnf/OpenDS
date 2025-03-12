# -*- coding: utf-8 -*-
import pytest
from DS_Split.utils import safe_print

def test_safe_print_mixed_characters(capsys):
    test_string = "Hello, 世界! 🌍"
    safe_print(test_string)
    captured = capsys.readouterr()
    assert captured.out.strip() == test_string