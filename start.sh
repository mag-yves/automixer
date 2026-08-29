#!/usr/bin/env bash
set -uo pipefail

cd "$(dirname "$0")"

while true; do
    echo
    echo "=== AutomMixer ==="
    echo
    echo "1) Démarrer l'attribution des sons"
    echo "2) Mettre à jour les usages"
    echo
    echo "Q) Quitter"
    echo
    read -rp "Choix : " choice

    case "$choice" in
        1)
            ./generate.sh || echo "Échec de l'attribution des sons."
            ;;
        2)
            ./update-usage.sh || echo "Échec de la mise à jour des usages."
            ;;
        q|Q)
            echo "Au revoir."
            exit 0
            ;;
        *)
            echo "Choix invalide."
            ;;
    esac
done
