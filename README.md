# dndgen Programmierpraktikum 2018 Projekt
Hier soll ein Generator für Pathfinder-Dungeons entstehen

## Diagramme
Alle [Diagramme](diagrams/) wurden mit PlantUML erstellt (plantuml.com).

Eine Live-Version gibt es unter: 
	[PlantUML Live](http://www.plantuml.com/plantuml/uml/).
Einfach den Text einfügen und auf "Submit" klicken um ein passendes Diagramm zu erzeugen.

## User Storys
Alle [User Storys](User_Storys) wurden in Optional und Normal unterteil. Desweiteren sind diese nicht sortiert.

## Webserver
mywebserver.py ausführen (erforder Python Version 3 oder höher), dieser öffnet lokal einen Webserver, der unter http://localhost:8000/ zu erreichen ist.
Als nächstes http://localhost:8000/index.html öffnen. Dort befindet sich die Eingabefelder für die Parameter. Wird der Knopf "Generate Dungeon" gedrückt, so werden diese Informationen per GET an das Skript /cgi-bin/controller.py gesendet, dieses generiert den Dungeon und dieser wird in einem neuen Fenster im Browser angezeigt.

## Datenbanken

Die Datenbanken benötigen die SQLite3- Library, diese ist gegebenenfalls nachzuinstallieren. 