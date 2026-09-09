from __future__ import annotations

from pathlib import Path

from automixer.sound_usage import load_usage_counts

BAR_WIDTH = 30


def _bar(count: int, max_count: int) -> str:
    if max_count <= 0:
        return ""
    filled = round((count / max_count) * BAR_WIDTH)
    return "#" * filled


def build_dashboard_lines(usage_counts: dict[str, int], top_n: int = 10) -> list[str]:
    """Construit les lignes texte du dashboard d'utilisation des sons."""
    total_sounds = len(usage_counts)
    total_usages = sum(usage_counts.values())
    unused = sorted(name for name, count in usage_counts.items() if count == 0)
    used_counts = {name: count for name, count in usage_counts.items() if count > 0}

    lines: list[str] = [
        "=== Dashboard d'utilisation des sons ===",
        "",
        f"Sons référencés     : {total_sounds}",
        f"Utilisations totales: {total_usages}",
        f"Sons jamais utilisés: {len(unused)}",
        f"Sons déjà utilisés  : {len(used_counts)}",
        "",
    ]

    if used_counts:
        max_count = max(used_counts.values())

        most_used = sorted(used_counts.items(), key=lambda item: (-item[1], item[0]))[:top_n]
        lines.append(f"Top {len(most_used)} des sons les plus utilisés :")
        for name, count in most_used:
            lines.append(f"  {name:<20} {count:>4}  {_bar(count, max_count)}")
        lines.append("")

        least_used = sorted(used_counts.items(), key=lambda item: (item[1], item[0]))[:top_n]
        lines.append(f"Top {len(least_used)} des sons les moins utilisés (hors jamais utilisés) :")
        for name, count in least_used:
            lines.append(f"  {name:<20} {count:>4}  {_bar(count, max_count)}")
        lines.append("")

    if unused:
        preview = unused[:top_n]
        lines.append(f"Sons jamais utilisés ({len(unused)}), extrait :")
        for name in preview:
            lines.append(f"  {name}")
        remaining = len(unused) - len(preview)
        if remaining > 0:
            lines.append(f"  ... et {remaining} autre(s)")

    return lines


def print_dashboard(log_path: Path, top_n: int = 10) -> None:
    """Affiche dans le terminal un résumé de l'usage des sons à partir du journal JSON."""
    usage_counts = load_usage_counts(log_path)
    if not usage_counts:
        print(f"Aucun journal d'utilisation trouvé ou vide : {log_path}")
        return

    for line in build_dashboard_lines(usage_counts, top_n=top_n):
        print(line)
