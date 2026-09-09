# Keukenprijs-index Nederland (2026)

Open dataset met richtprijzen voor een complete nieuwe keuken in Nederland — per opstelling (recht, hoek, U, kookeiland, parallel), per prijssegment en per keukenmerk, plus regiopatronen voor 57 steden.

Onafhankelijk samengesteld door [Keuken in Beeld](https://keukeninbeeld.nl) (onderdeel van Alfa Reclame, KvK 88606902), dat zelf geen keukens verkoopt. Methodologie, toelichting en de leesbare versie: **https://keukeninbeeld.nl/keukenprijs-index**

## Bestanden

| Bestand | Inhoud |
|---|---|
| `keukenprijs-index-2026.json` | De volledige index (UTF-8 JSON, Nederlandstalige sleutels) |

Canonieke bron (altijd de nieuwste editie): https://keukeninbeeld.nl/keukenprijs-index.json

## Gebruik

```bash
curl -s https://keukeninbeeld.nl/keukenprijs-index.json | jq '.opstellingen'
```

Embed-widget voor websites: https://keukeninbeeld.nl/keukenprijs-index-insluiten

## Licentie en citeren

CC BY 4.0 — vrij te gebruiken en te citeren met bronvermelding:

> Keukenprijs-index 2026, Keuken in Beeld (keukeninbeeld.nl)

## English

Open dataset of indicative prices for a complete new kitchen in the Netherlands, by layout, price segment and brand, with regional patterns for 57 cities. Compiled independently by Keuken in Beeld, which does not sell kitchens. Human-readable version and methodology: https://keukeninbeeld.nl/keukenprijs-index — English guide: https://keukeninbeeld.nl/en/kitchen-prices-netherlands. Licensed CC BY 4.0.
