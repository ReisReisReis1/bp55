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
