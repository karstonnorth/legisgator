import pytest, asyncio
from legisgator.engine import analyze

SAMPLE = """
All contracts are binding.                    # P
This contract was signed under duress.        # D
If signed under duress, contract is void.     # D → ¬P
"""

@pytest.mark.asyncio
async def test_flags_contradiction():
    res = await analyze(SAMPLE)
    assert res["contradictions"], "Should detect contradiction"
    assert res["weakest"], "Scoring should return list"
