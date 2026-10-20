"""Sistemin durumunu okunaklı bir tablo olarak yazar. Sahibi: Üye 4."""


def _fmt(d):
    return ", ".join(f"{k}x{v}" for k, v in d.items()) if d else "-"


def format_state(system):
    """Process ve kaynak tablolarını tek bir metin olarak döndürür."""
    lines = [f"{'Process':<8}{'Durum':<12}{'Tuttuğu':<14}{'Beklediği':<12}"]
    for p in system.processes.values():
        lines.append(f"{p.name:<8}{p.state:<12}{_fmt(p.held):<14}{_fmt(p.waiting_for):<12}")
    lines.append("")
    lines.append(f"{'Kaynak':<8}{'Toplam':<8}{'Boş':<6}{'Bekleme sırası'}")
    for r in system.resources.values():
        queue = ", ".join(system.queues.get(r.name, [])) or "-"
        lines.append(f"{r.name:<8}{r.total:<8}{system.available(r.name):<6}{queue}")
    return "\n".join(lines)
