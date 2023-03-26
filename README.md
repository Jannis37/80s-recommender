# Recommener System for songs of the 80s

## Verwendete Features
- name: 
  
  Name des Tracks.
  
  ---
- popularity:
  Die Popularität eines Titels ist ein Wert zwischen 0 und 100, wobei 100 die größte Popularität darstellt. Die Popularität wird von einem Algorithmus berechnet und basiert größtenteils auf der Gesamtzahl der Aufrufe des Titels und darauf, wie aktuell diese Aufrufe sind.
  Im Allgemeinen haben Titel, die jetzt viel gespielt werden, eine höhere Popularität als Titel, die in der Vergangenheit viel gespielt wurden. Doppelte Titel (z. B. derselbe Titel aus einer Single und einem Album) werden unabhängig voneinander bewertet.
  
  ---
- genres: 
  
  Genres die dem Track zugewiesen worden sind.

  ---
- danceability: 
  
  Die Tanzbarkeit beschreibt, wie gut sich ein Titel zum Tanzen eignet, und zwar auf der Grundlage einer Kombination aus musikalischen Elementen wie Tempo, Rhythmusstabilität, Taktstärke und allgemeiner Regelmäßigkeit. Ein Wert von 0,0 ist am wenigsten tanzbar und 1,0 ist am besten tanzbar.

  ---
- energy: 
  
  Energie ist ein Maß von 0,0 bis 1,0 und stellt ein Wahrnehmungsmaß für Intensität und Aktivität dar. Typischerweise fühlen sich energiegeladene Titel schnell, laut und geräuschvoll an. Death Metal hat zum Beispiel eine hohe Energie, während ein Bach-Präludium auf der Skala niedrig bewertet wird. Zu den Wahrnehmungsmerkmalen, die zu diesem Attribut beitragen, gehören der Dynamikbereich, die wahrgenommene Lautstärke, die Klangfarbe, die Einsetzgeschwindigkeit und die allgemeine Entropie.

  ---
- key:
  
  Die Tonart, in der sich der Track befindet. Ganzzahlige Werte entsprechen den Tonlagen in der Standard-Notation für Tonarten. Z.B. 0 = C, 1 = C♯/D♭, 2 = D, usw. Wurde keine Tonart erkannt, ist der Wert -1.

  ---
- loudness
  
  Die Gesamtlautstärke eines Tracks in Dezibel (dB). Die Lautstärke-Werte werden über den gesamten Track gemittelt und sind nützlich für den Vergleich der relativen Lautstärke von Tracks. Die Lautstärke ist die Qualität eines Klangs, die die primäre psychologische Korrelation der physischen Stärke (Amplitude) ist. Die Werte liegen normalerweise zwischen -60 und 0 db.

  ---
- mode
    
  Modus gibt die Modalität (Dur oder Moll) eines Tracks an, d. h. die Art der Tonleiter, von der der melodische Inhalt abgeleitet ist. Dur wird durch 1 dargestellt und Moll durch 0.

  ---
- speechiness
  
  Die Sprachlichkeit erfasst das Vorhandensein von gesprochenen Wörtern in einem Track. Je sprachlastiger die Aufnahme ist (z. B. Talkshow, Hörbuch, Gedicht), desto näher liegt der Attributwert bei 1,0. Werte über 0,66 beschreiben Tracks, die wahrscheinlich vollständig aus gesprochenen Wörtern bestehen. Werte zwischen 0,33 und 0,66 beschreiben Tracks, die sowohl Musik als auch Sprache enthalten können, entweder in Abschnitten oder überlagert, einschließlich solcher Fälle wie Rap-Musik. Werte unter 0,33 stehen höchstwahrscheinlich für Musik und andere nicht gesprochene Tracks.

  ---
- acousticness
  
  Ein Vertrauensmaß von 0,0 bis 1,0, das angibt, ob der Track akustisch ist. 1,0 steht für eine hohe Wahrscheinlichkeit, dass der Titel akustisch ist.

  ---
- instrumentalness
  
  Sagt voraus, ob ein Track keinen Gesang enthält. "Ooh"- und "aah"-Laute werden in diesem Zusammenhang als instrumental behandelt. Rap- oder Spoken-Word-Tracks sind eindeutig "vokal". Je näher der Wert für die Instrumentalität bei 1,0 liegt, desto größer ist die Wahrscheinlichkeit, dass der Titel keinen Gesang enthält. Werte über 0,5 sollen instrumentale Tracks darstellen, aber das Konfidenzniveau ist höher, je mehr sich der Wert 1,0 nähert.

  ---
- liveness
  
  Erkennt die Anwesenheit eines Publikums in der Aufnahme. Höhere Liveness-Werte bedeuten eine höhere Wahrscheinlichkeit, dass der Track live gespielt wurde. Ein Wert über 0,8 bietet eine hohe Wahrscheinlichkeit, dass der Track live ist.

  ---
- valence
  
  Ein Maß von 0,0 bis 1,0, das die von einem Titel vermittelte musikalische Positivität beschreibt. Tracks mit hoher Valenz klingen positiver (z. B. glücklich, fröhlich, euphorisch), während Tracks mit niedriger Valenz eher negativ klingen (z. B. traurig, deprimiert, wütend).

  ---
- tempo
  
  Das geschätzte Gesamttempo eines Tracks in Beats pro Minute (BPM). In der musikalischen Terminologie ist das Tempo die Geschwindigkeit oder das Tempo eines bestimmten Stücks und leitet sich direkt von der durchschnittlichen Taktdauer ab.

  ---
- duration_ms
  
  Die Dauer des Tracks in Millisekunden.

  ---
- time_signature
  
  Eine geschätzte Taktart. Die Taktart (Metrum) ist eine Notationskonvention, die angibt, wie viele Schläge ein Takt (oder ein Takt) hat. Die Taktart reicht von 3 bis 7, was Taktarten von "3/4" bis "7/4" angibt.

  ---
- isrc
  
  International Standard Recording Code. Dient zur Identifikation des Tracks.