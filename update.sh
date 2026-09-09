#!/usr/bin/env sh
# Haalt de nieuwste editie op van de canonieke bron.
set -e
curl -fsSL https://keukeninbeeld.nl/keukenprijs-index.json -o keukenprijs-index-2026.json
echo "bijgewerkt: $(date -u +%F)"
