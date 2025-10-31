# Sound-Effekte für Garten-Spiel

## Benötigte Sound-Dateien

Lege folgende Dateien im `sounds/` Ordner ab. Alle Sounds sollten im **.ogg** Format sein (für beste Web-Kompatibilität).

### Pflicht-Sounds:
1. **harvest.ogg** - Ernten (Pop/Pluck Sound, ~0.3s)
2. **water.ogg** - Gießen (Wasser plätschern, ~0.5s)
3. **weed.ogg** - Unkraut entfernen (Ziehen/Reißen, ~0.4s)
4. **fertilize.ogg** - Düngen (Schütteln/Streuen, ~0.5s)
5. **buy.ogg** - Shop-Kauf (Kassen-Bling, ~0.3s)
6. **plant.ogg** - Samen pflanzen (Grab/Dig Sound, ~0.4s)
7. **error.ogg** - Fehler (Negatives Buzz, ~0.3s)

### Optional:
8. **bgm.ogg** - Hintergrundmusik (Loop, 1-3 Minuten)
9. **rain.ogg** - Regen-Ambient (Loop, ~3s)
10. **birds.ogg** - Vögel-Gezwitscher (Loop, ~3s)

## Kostenlose Sound-Quellen

### Empfohlene Webseiten:
1. **Freesound.org** (Beste Quelle!)
   - https://freesound.org
   - Registrierung erforderlich (kostenlos)
   - Filter: "CC0" oder "CC-BY" Lizenz
   - Suchbegriffe: "harvest", "water", "dig", "coins", "plant"

2. **OpenGameArt.org**
   - https://opengameart.org/art-search-advanced?keys=sound
   - Keine Registrierung nötig
   - Filter: "CC0" Lizenz

3. **Mixkit.co**
   - https://mixkit.co/free-sound-effects/
   - Komplett kostenlos, keine Anmeldung
   - Gute Qualität

4. **Zapsplat.com**
   - https://www.zapsplat.com
   - Registrierung erforderlich (kostenlos)
   - Sehr große Auswahl

### Konkrete Suchbegriffe:
- **harvest.ogg**: "pop", "pluck", "pick fruit", "vegetable"
- **water.ogg**: "water splash", "watering can", "pour water"
- **weed.ogg**: "pull", "grass", "rip paper"
- **fertilize.ogg**: "shake", "seeds", "granular"
- **buy.ogg**: "coin", "purchase", "register", "cha-ching"
- **plant.ogg**: "dig", "shovel", "dirt"
- **error.ogg**: "buzz", "wrong", "negative", "error beep"
- **bgm.ogg**: "farm music", "garden theme", "peaceful", "acoustic"
- **rain.ogg**: "rain ambient", "rainfall loop"
- **birds.ogg**: "birds chirping", "birdsong"

## Konvertierung zu .ogg

Falls du .mp3 oder .wav Dateien hast:

### Mit ffmpeg (empfohlen):
```bash
# Einzelne Datei
ffmpeg -i input.mp3 -c:a libvorbis -q:a 4 output.ogg

# Alle MP3s im Ordner konvertieren
for f in *.mp3; do ffmpeg -i "$f" -c:a libvorbis -q:a 4 "${f%.mp3}.ogg"; done
```

### Online-Konverter:
- https://cloudconvert.com/mp3-to-ogg
- https://convertio.co/mp3-ogg/

## Empfohlene Sound-Settings:
- **Sample Rate**: 44100 Hz oder 22050 Hz
- **Bitrate**: 96-128 kbps (für kleinere Dateien)
- **Kanäle**: Mono (Stereo nur wenn nötig)
- **Länge**: Kurz und knackig (<1s für Effekte)

## Lizenz-Hinweise:
- Achte auf die Lizenz! CC0 oder CC-BY sind am sichersten
- Bei CC-BY musst du den Autor im Spiel erwähnen
- Kommerzielle Nutzung: Achte darauf dass die Lizenz das erlaubt

## Schnellstart:
1. Gehe zu freesound.org
2. Registriere dich (kostenlos)
3. Suche nach "harvest pop"
4. Filter: License → "Creative Commons 0"
5. Download als .ogg oder konvertiere
6. Benenne um zu `harvest.ogg`
7. Wiederhole für alle Sounds

Das Spiel funktioniert auch ohne Sounds - es gibt dann einfach keine Audio-Ausgabe.
