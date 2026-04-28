import pytest
from pathlib import Path
from budget.main import main


def test_budget():
    print("Testing the main categorisation function...")
    result = main([str(Path(__file__).parent/"data"/"Transactions_2025-05-01_2026-04-28 2.csv")])
    assert (abs(result['Groceries']["Balance"][-1]+3369.86)<0.0001)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-s"]))