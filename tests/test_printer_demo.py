from deadlock_guardian.demo import main
from deadlock_guardian.models import System
from deadlock_guardian.printer import format_state
from tests.helpers import hold, wait


def test_format_state_icerik():
    s = System.create({"R1": 1}, ["P1", "P2"])
    hold(s, "P1", "R1")
    wait(s, "P2", "R1")
    text = format_state(s)
    assert "P1" in text and "P2" in text and "R1" in text
    assert "WAITING" in text and "RUNNING" in text


def test_demo_senaryoyu_okuyup_yazar(capsys):
    assert main(["scenarios/deadlock.json"]) == 0
    out = capsys.readouterr().out
    assert "2 process" in out and "P1" in out
