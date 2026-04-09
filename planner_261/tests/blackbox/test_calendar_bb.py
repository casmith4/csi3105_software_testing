import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import pytest
from planner_261.logic.Calendar import Calendar
from planner_261.logic.ConflictException import ConflictsException


def test_valid_input():
    cal = Calendar()
    cal.check_times(5, 10, 9, 10)


def test_invalid_month_low():
    cal = Calendar()
    with pytest.raises(ConflictsException):
        cal.check_times(0, 10, 9, 10)