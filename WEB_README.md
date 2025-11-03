# Garten-Spiel - Web Version

## Übersicht
Das Garten-Spiel wurde erfolgreich für das Web portiert mittels pygbag (Pygame für WebAssembly).

## Voraussetzungen
- Python 3.12 oder höher
- Virtual Environment mit pygbag installiert

## Installation
```bash
# Virtual Environment aktivieren (falls nicht aktiv)
source venv/bin/activate

# Dependencies installieren (falls noch nicht geschehen)
pip install -r requirements.txt
```

## Build-Prozess
Um eine neue Web-Version zu erstellen:
```bash
# Build-Verzeichnis aufräumen
rm -rf build/

# Spiel für Web bauen
source venv/bin/activate && pygbag main.py
```

Dies erstellt:
- `build/web/index.html` - Die Hauptseite
- `build/web/towngame.apk` - Das gepackte Spiel (~15MB)
- `build/web/favicon.png` - Das Icon

## Lokales Testen

### Option 1: Mit npm (empfohlen)
```bash
npm run serve
```
Startet automatisch den Server auf Port 8000 und beendet alte Instanzen.

### Option 2: Mit Python direkt (Alternative)
```bash
cd build/web
python -m http.server 8000
```
Wenn du bereits einen Server auf Port 8000 laufen hast, beende ihn zuerst:
```bash
pkill -f 'python -m http.server 8000'
```

### Zugriff
Öffne deinen Browser und gehe zu:
```
http://localhost:8000
```

**Hinweis:** Das Spiel benötigt einen HTTP-Server, da Browser lokale Dateien mit CORS-Einschränkungen versehen.

## Spielanleitung
Das Spiel ist identisch zur Desktop-Version:
- **Linksklick**: Ernten / Unkraut entfernen
- **Rechtsklick**: Feld auswählen
- **Shop**: Items kaufen (Samen, Dünger, Wasser, etc.)
- **Tools**: Tool auswählen → Feld anklicken zum Verwenden

## Dateistruktur
- `main.py` - Web-kompatible Version mit asyncio
- `garden_game.py` - Original Desktop-Version
- `build/web/` - Gebaute Web-Version
- `venv/` - Virtual Environment mit pygbag

## Troubleshooting

### Build schlägt fehl
- Stelle sicher, dass pygbag installiert ist: `pip install pygbag`
- Lösche den Cache: `rm -rf build/web-cache`

### Spiel lädt nicht im Browser
- Prüfe die Browser-Konsole (F12) auf Fehler
- Stelle sicher, dass der Server läuft: `lsof -i :8000`
- Verwende einen modernen Browser (Chrome, Firefox, Edge)

### Spiel ist langsam
- pygbag/WebAssembly hat eine geringere Performance als native Python
- Versuche einen anderen Browser
- Schließe andere Tabs für mehr RAM

## npm Scripts
- `npm run build` - Baut die Web-Version
- `npm run serve` - Startet lokalen Server
- `npm run dev` - Baut und startet Server
- `npm run clean` - Löscht Build-Verzeichnis

## Deployment
Um das Spiel online zu hosten:
1. Lade den Inhalt von `build/web/` auf einen Webserver hoch
2. Alternativ: Nutze GitHub Pages, Netlify, oder Vercel
3. Stelle sicher, dass WASM-Dateien korrekt served werden

## Unterschiede zur Desktop-Version
- Verwendet WebAssembly statt native Python
- Etwas geringere Performance
- Läuft in jedem modernen Browser
- Keine Installation erforderlich

## Bekannte Einschränkungen
- Sound könnte verzögert sein
- Keine Gamepad-Unterstützung im Web
- File-I/O funktioniert anders (virtuelles Dateisystem)
