# Maze-Runner
Das Programm ist nach dem klassischen Spiel-Loop-Muster aufgebaut:
  Initialisierungsphase: Pygame wird gestartet, Fenster wird erstellt, Ressourcen werden geladen.
  Labyrinth-Generierung: Ein zufälliges, perfektes Labyrinth wird mit DFS erstellt.
  Hauptspiel-Schleife:
   Events werden verarbeitet (Steuerung, Pause, Beenden)
   Spielzustand wird aktualisiert (Position, Timer, Animationen)
  Sieg-Bedingung wird geprüft
  Grafik wird neu gezeichnet
  Menü-Phasen: Pause-Menü und Gewinn-Menü unterbrechen die Hauptschleife temporär.

Bei diesem Code handelt es sich um ein Labyrinth-Spiel, das mit der Python-Bibliothek Pygame erstellt wurde. Der Spieler steuert eine gelbe Spielfigur durch ein zufällig generiertes Labyrinth. Das Ziel ist es, von der Startposition (oben links, türkis markiert) zur Zielposition (unten rechts, rot markiert) zu gelangen.

Das Spiel bietet folgende Features:
  Ein prozedural generiertes Labyrinth mit 20x20 Zellen
  Hintergrundmusik und Soundeffekte für Bewegungen und Gewinn
  Eine Squish-Animation der Spielfigur bei jeder Bewegung
  Ein Timer, der die benötigte Zeit misst
  Ein Pause-Menü, das mit der ESC-Taste aufgerufen wird
  Ein Gewinn-Menü mit der Option, neu zu starten oder das Spiel zu beenden
