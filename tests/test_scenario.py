import json

import pytest

from deadlock_guardian.scenario import load_scenario


def test_deadlock_senaryosu_okunur():
    system, steps = load_scenario("scenarios/deadlock.json")
    assert set(system.resources) == {"R1", "R2"}
    assert system.resources["R1"].total == 1
    assert set(system.processes) == {"P1", "P2"}
    assert system.processes["P1"].max_claim == {"R1": 1, "R2": 1}
    assert len(steps) == 4
    assert steps[0] == ("P1", "request", "R1", 1)


def test_normal_senaryo_okunur():
    system, steps = load_scenario("scenarios/normal.json")
    assert len(steps) == 8


def test_dort_elemanli_adim_adedi_okur(tmp_path):
    f = tmp_path / "s.json"
    f.write_text(json.dumps({"resources": {"R1": 3}, "processes": {"P1": {}},
                             "steps": [["P1", "request", "R1", 2]]}), encoding="utf-8")
    _, steps = load_scenario(f)
    assert steps == [("P1", "request", "R1", 2)]


def test_bilinmeyen_islem_hata(tmp_path):
    f = tmp_path / "s.json"
    f.write_text(json.dumps({"resources": {"R1": 1}, "processes": {"P1": {}},
                             "steps": [["P1", "jump", "R1"]]}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_scenario(f)


def test_eksik_bolum_hata(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError):
        load_scenario(f)
