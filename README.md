# BP55_Ruins_and_Beyond

BP 55 




**Verwendete Technologien**: Unsere Webanwendung basiert auf Python und als Framework wird Python
Django verwendet. Die Videos, Bilder und PDF’s werden auf einem Server des Rechnerpools des Fachbereichs
Architektur hinterlegt und mittels PostgreSQL verwaltet. Auf dem Server läuft der Webserver Apache2 auf
dem Betriebssystem Debian.

Es wurde sich an dieser [Dokumentation](https://docs.djangoproject.com/en/3.1/) orientiert. 

## Projektstruktur bp55:
Das Projekt ist in Apps ,typische Django Struktur, unterteilt. Die Apps stellen in diesem Proejtk jeweils eine Unterseite der Webseite dar und existieren als Python-Packages. Die Python-Directories werden verwendet um Template- und Static-Files, welche in mehreren Apps benötigt werden, ohne Komplikationen erreichbar zu machen.
Die einzelnen Python-Directory und Python-Packages, die nicht automnatisch beim Start von Django automatisch erstellt werden, werden in der folgenden Struktur erklärt.


|--bp55_ruins_and_beyond <br>
| <br>
|--details_page <br>
|  |----__ pyache__ <br>
|  |----migrations <br>
|  |----static <br>
|  |----templates <br>
|  |----__ init__.py <br>
|  |----admin.py <br>
|  |----apps.py <br>
|  |----country_codes <br>
|  |----models.py <br>
|  |----tests.py <br>
|  |----urls.py <br>
|  |----views.py <br>
| <br>
|--filter_page <br>
| <br>
|--home <br>
| <br>
|--impressum <br>
| <br>
|--materials_page <br>
| <br>
|--search <br>
| <br>
|--static <br>
| <br>
|--templates <br>
| <br>
|--timeline <br>
| <br>
|--video_content <br>

### details_page
Die App details_page ist zuständig für die Darstellung der Detailseite. Auf der Detailseite wird ein  kurzer Steckbrief, sowie Bilder, Grundriss und Videos zu einem betsimmten Gebäude angezeigt. Dafür wurden in models folgende Klassen erzeugt: Era, um die verschiedenen Eras mit ihren jeweiligen Daten darzustellen, Building, die Gebäude mit allen zugehörigen Informationen darstellt, Blueprint, um den Gebäuden einen Grundriss als Bild zuordnen zu können, Picture, um den Gebäuden verschiedene Bilder zuweisen zu können. Für alle Attribute der Klassen wurden getter-Funktionen eingerichtet, um die entsrpechenden Werte auslesen zu können.
### filter_page
Die App filter_page wird verwendet um mit der auf der Bauwerke-Seite vorhandenen Filterfunktion die Gebäude nach bestimmten Attributen zu Filtern. Die Funktionen hierfür sind in der views Datei der App vorhanden. Zur Umsetzung der Filterfunktion wurden die Hilfsfunktionen splitting, one_dict_set_to_string_list und delete_duplicates geschrieben, die Hauptfunktion tragen die Funktionen my_filter und display_building_filter. Die Kommentare dieser Funktionen beschreiben die genaue Umsetzung weiter.
### home
Die App home dient nur zur Darstellung der Startseite und benötigt daher keine weiteren Klassen oder Funktionen.
### impressum
Die App impressum ist zuständig für die Darstellung der Impressum-Seite und die Verfügbarkeit des Kurslinks auf allen Seiten der Webandwendung. Dafür enthält die Datei models die Klasse Impressum. Diese besitzt nur die Attribute course_link, mit dem der Link zum aktuellen Vorlesungskurs festgehalten werden kann, und name um die Objekte der Klasse Impressum unterscheiden zu können. Hier ist anzumerken, dass durch das Überschreiben der Funktion save, nur ein Objekt dieser Klasse erzeugt werden kann. In views wird eine getter Funktion für das Attribut course_link bereitgestellt. Damit der Kurslink auch auf allen anderen Seiten verfügbar ist, wurde diese Funktion in die views aller anderen Apps importiert.
### materials_page
Mithilfe der App materials_page wird die Darstellung der Materialien-Seite umgesetzt. Dafür enthält models die Klasse Material. Dateien können mit Hilfe des Attributs file hinzugefügt werden und mit dem Attribut category können die Dateien verschiedenen Kategorien zugeordnet werden. Um die Dateien gesammelt und sortiert nach Kategorien ausgeben zu können kann mit der Funktion get_categories_and_corresponding_files() ein Dictionary erzeugt werden. Die Funktion get_catgeories_and_corresponding_zip_files funktioniert ähnlich, gibt die Dateien einer Kategorie des Dictionarys aber nicht einzeln aus, sondern in einem zip-Ordner. Beide Funktionen ermöglichen das herunterladen der Dateien.
### search
Die App search ist für die Suchfunktion der Website zuständig. Dafür wird in views die Funktion search ausgeführt, die die Attributre aller Gebäude nach dem entsprechenden Suchwort filtert.
### static
Static enthält alle statischen Dateien der Website, wie z.B. feste Bilder und Darstellungen, die nicht verändert werden sollen.
### templates
Templates enthält die html-Vorlagen für den footer, den header und den default_head, damit diese auf allen Seiten einheitlich dargestellt und umgesetzt werden können.
### timeline
Die App timeline wird zur Darstellung des Zeitstrahl benötigt. Dafür enthält models die Klasse HistoricDate, damit neben den Gebäuden auf dem Zeitstrahl auch bedeutende historische Ereignisse dargestellt werden können. Für die Berechnung des Zeitstrahls wurden in views die Hilfsfunktionen get_date_as_str, get_year_of_item und get_thumbnails_for_buildings implementiert. Die Hauptfunktion tragen aber die Funktionen getting_all_eras_sorted, welche die Eras chronologisch anordnet, sort_into_eras, welche anschließend die Gebäude und Ereignisse in das Era-Dictionary einsortiert. Weitere Informationen zu den Funktionen finden sich in den zugehörigen Kommentaren.
### video_content
Die App video_content wird zum Abspielen der Videos benötigt. Hierfür wurden in models die Klassen Video und Timestamp implementiert. Mit der Klasse Videos können Videos hochgeladen werden und mit der Klasse Timestamp können den Videos Timestamps hinzugefügt werden, durch die man direkt zu einer bestimmten Stelle im Video springen kann. Dafür wurden in den Klassen entsprechende getter-Funktionen umgesetzt.
