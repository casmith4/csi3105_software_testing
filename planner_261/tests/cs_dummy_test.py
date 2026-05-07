import pytest
from logic.Organization import Organization
from logic.Planner import Planner


# ── Dummy main / fixture ──────────────────────────────────────────────────────
@pytest.fixture
def planner():
    """Creates a fresh Planner instance for each test."""
    return Planner()


def run_schedvac(monkeypatch, capsys, planner, name, start_month, start_day, end_month, end_day):
    """Helper: patches input() and runs schedvac(), returns captured stdout."""
    inputs = iter([name, str(start_month), str(start_day), str(end_month), str(end_day)])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    planner.schedvac()
    return capsys.readouterr().out


# ── Weak Robust EP Tests ──────────────────────────────────────────────────────
def test_WR1_valid(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 5, 3, 7)
    assert "Vacation is now booked!" in out

def test_WR2_invalid_name(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "John Doe", 3, 5, 3, 7)
    assert "Vacation is now booked!" not in out

def test_WR3_start_month_below(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 0, 5, 3, 7)
    assert "Vacation is now booked!" not in out

def test_WR4_start_month_above(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 13, 5, 3, 7)
    assert "Vacation is now booked!" not in out

def test_WR5_start_day_below(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 0, 3, 7)
    assert "Vacation is now booked!" not in out

def test_WR6_start_day_above_bug(monkeypatch, capsys, planner):
    # Known bug: day 32 should be rejected but is accepted
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 32, 3, 32)
    assert "Vacation is now booked!" not in out  # Documents the bug — this will FAIL

def test_WR7_end_month_below(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 5, 0, 7)
    assert "Vacation is now booked!" not in out

def test_WR8_end_month_above(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 5, 13, 7)
    assert "Vacation is now booked!" not in out

def test_WR9_end_day_below(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 5, 3, 0)
    assert "Vacation is now booked!" not in out

def test_WR10_end_day_above_bug(monkeypatch, capsys, planner):
    # Known bug: day 32 should be rejected but is accepted
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 5, 3, 32)
    assert "Vacation is now booked!" not in out  # Documents the bug — this will FAIL


# ── BVA Tests — Month ─────────────────────────────────────────────────────────
def test_BVA_M1_month_0(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 0, 5, 3, 7)
    assert "Vacation is now booked!" not in out

def test_BVA_M2_month_1(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 1, 5, 1, 7)
    assert "Vacation is now booked!" in out

def test_BVA_M3_month_2(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 2, 5, 2, 7)
    assert "Vacation is now booked!" in out

def test_BVA_M4_month_11(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 11, 5, 11, 7)
    assert "Vacation is now booked!" in out

def test_BVA_M5_month_12(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 12, 5, 12, 7)
    assert "Vacation is now booked!" in out

def test_BVA_M6_month_13(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 13, 5, 3, 7)
    assert "Vacation is now booked!" not in out


# ── BVA Tests — Day ───────────────────────────────────────────────────────────
def test_BVA_D1_day_0(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 0, 3, 5)
    assert "Vacation is now booked!" not in out

def test_BVA_D2_day_1(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 1, 3, 5)
    assert "Vacation is now booked!" in out

def test_BVA_D3_day_2(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 2, 3, 5)
    assert "Vacation is now booked!" in out

def test_BVA_D4_day_29(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 29, 3, 29)
    assert "Vacation is now booked!" in out

def test_BVA_D5_day_30(monkeypatch, capsys, planner):
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 30, 3, 30)
    assert "Vacation is now booked!" in out

def test_BVA_D6_day_31(monkeypatch, capsys, planner):
    # checkTimes uses > 30, so day 31 raises ConflictsException
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 31, 3, 31)
    assert "Vacation is now booked!" not in out

def test_BVA_D7_day_32_bug(monkeypatch, capsys, planner):
    # Known bug: 32 should fail but is accepted
    out = run_schedvac(monkeypatch, capsys, planner, "Ashley Martin", 3, 32, 3, 32)
    assert "Vacation is now booked!" not in out  # This will FAIL — documents the bug
