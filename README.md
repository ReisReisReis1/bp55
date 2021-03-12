# Ruins and beyond!

Diese Software ist im Rahmen des Pflichtfaches "Bachelor Praktikum" für den Studiengang Informatik
Bachlor of Science im Wintersemester 2020/21 an der TU-Darmstadt entstanden. 

Dieses Projekt ist unter der [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.txt) lizensiert, siehe LICENSE.

**Motivation und Kontext**: Die Auftraggeber, die Veranstalter des Moduls "Klassische Architektur und Städtebau der Antike" des Fachbereichs Architektur der TU-Darmstadt, möchten die Gestaltung ihrer Vorlesung um eine Webanwendung zum digitalen Lernen erweitern. Die Idee ist aufgrund des pandemiebedingten Onlinestudienbetriebs entstanden und soll nun im Rahmen des Bachlorpraktikums umgesetzt werden. Hierfür möchten die Auftraggeber eine digitale Wissensplattform "Ruins and Beyond!" zu Bauwerken der Antike aufbauen, auf der die Studierenden, auf der Basis der zur Verfügung gestellten Materialien, die Lehrinhalte selbstbestimmt kombinieren und absolvieren können. Diese benötigten Videos, Bilder und Gebäudedaten wurden hierfür zu Beginn des Projektes von den Auftraggebern zur Verfügung gestellt.

**Umsetzung**: Sofern der Nutzende noch nicht über den Single-Sign-On der TU-Darmstadt eingeloggt ist, wird er zunächst auf die Login-Seite geleitet, um sich dort anzumelden. Dies stellt die Einhaltung der Urheberrechte sicher und dass nur die gedachte Zielgruppe auf die Inhalte zugreifen kann. Anschließend gelangt man auf die Intro-Seite. Diese enthält ein Intro-Video und einen Beschreibungstext. Das Intro-Video gibt einen Einstieg in die Vorlesung, welche durch die Webanwendung begleitet wird und somit auch das Thema dieser präsentiert. Der Beschreibungstext enthält eine Beschreibung aller verfügbaren Funktionalitäten der Unterseiten, damit Nutzende sich schnell und einfach zurecht finden. Auf jeder Seite, mit Ausnahme der Login-Seite, wird eine Menüleiste angezeigt, die Verlinkungen zu den Unterseiten "Intro", "Zeitachse", "Bauwerke", "Staffel" und "Materialien" bereitstellt. Auf der Zeitachse werden ausgewählte Gebäude und Ereignisse von ca. 1400 v.Chr. bis ca. 600 n.Chr. chronologisch aufgeführt. Dabei werden Bauwerke mit Titel, Datierung und einem Vorschaubild, sowie Ereignisse mit Bezeichnung und Datierung dargestellt. Durch Auswahl eines Bauwerks wird man auf die zugehörige Detailseite geleitet. Auf der Detailseite werden Informationen, Bilder und Grundrisse zu dem jeweiligen Gebäude angezeigt mit der Möglichkeit Videos anzusehen, in denen das Bauwerk behandelt wird. Auf der „Bauwerke“-Seite wird die Möglichkeit geboten, die Gebäude nach bestimmten Kategorien zu filtern. Die Ergebnisse werden daraufhin tabellarisch angezeigt und enthalten ebenfalls eine Verlinkung zur Detailseite. Mittels der Suchfunktion, die auf jeder Unterseite angezeigt wird, kann nach den Attributen "Name", "Stadt", "Region", "Land", "Epoche", "Architekt", "Kontext", "Bauherr", "Bautypus", "Bauform", "Funktion" und "Säulen-ordnung" der Gebäude gesucht werden. Die Ergebnisse werden ähnlich wie bei der Filterfunktion tabellarisch aufgelistet. Die "Staffel"-Unterseite enthält alle Vorlesungsvideos, chronologisch nach Epochen geordnet. Nutzende können hier für eine bessere Übersichtlichkeit, Epochen mit vielen Videos aus- und einklappen. Wählt der Nutzende ein Video aus, wird es in einem Pop-Up geöffnet. Zu jedem Video ist auf der Seite, und im Pop-Up zunächst nur ein aussagekräftiges Vorschaubild zu sehen. Auf der "Materialien" Seite werden weitere in Kategorien eingeteilte Vorlesungsinhalte zum Download angeboten.

**Verwendete Technologien**: Unsere Webanwendung basiert auf [Python](https://python.org) und als Framework wird [Django](https://djangoproject.com) verwendet. 
Die Videos, Bilder und PDF’s werden auf einem Server des Rechnerpools des Fachbereichs Architektur hinterlegt und mittels [PostgreSQL](https://postgresql.org) verwaltet. 
Auf dem Server läuft der Webserver [Apache2](https://httpd.apache.org) auf dem Betriebssystem [Debian](https://www.debian.org/).

Es wurde sich an dieser [Dokumentation](https://docs.djangoproject.com/en/3.1/) orientiert. 

## Projektstruktur:

Das Projekt ist in Apps, typische Django Struktur, unterteilt. Die Apps stellen in diesem Projekt jeweils eine Unterseite der Webseite dar und existieren als Python-Packages. Die Python-Directories werden verwendet um Template- und Static-Files, welche in mehreren Apps benötigt werden, ohne Komplikationen erreichbar zu machen.

Die einzelnen Python-Directory und Python-Packages, die nicht automnatisch beim Start von Django automatisch erstellt werden, werden in der folgenden Struktur erklärt.


|--bp55_ruins_and_beyond <br>
| <br>
|--details_page <br>
|----|--migrations <br>
|----|--static <br>
|----|--templates <br>
|----|--__ init__.py <br>
|----|--admin.py <br>
|----|--apps.py <br>
|----|--country_codes <br>
|----|--models.py <br>
|----|--tests.py <br>
|----|--urls.py <br>
|----|--views.py <br>
| <br>
|--filter_page <br>
|----|... <br>
| <br>
|--home <br>
|----|... <br>
| <br>
|--impressum <br>
|----|... <br>
| <br>
|--materials_page <br>
|----|... <br>
| <br>
|--search <br>
|----|... <br>
| <br>
|--static <br>
|----|... <br>
| <br>
|--templates <br>
|----|... <br>
| <br>
|--timeline <br>
|----|--templatetags <br>
|----|... <br>
| <br>
|--video_content <br>
|----|... <br>

### details_page

Die App details_page ist zuständig für die Darstellung der Detailseite. Auf der Detailseite wird ein  kurzer Steckbrief, sowie Bilder, Grundriss und Videos zu einem betsimmten Gebäude angezeigt. Dafür wurden in models folgende Klassen erzeugt: Era, um die verschiedenen Eras mit ihren jeweiligen Daten darzustellen, Building, die Gebäude mit allen zugehörigen Informationen darstellt, Blueprint, um den Gebäuden einen Grundriss als Bild zuordnen zu können, Picture, um den Gebäuden verschiedene Bilder zuweisen zu können. Für alle Attribute der Klassen wurden getter-Funktionen eingerichtet, um die entsrpechenden Werte auslesen zu können.

### filter_page

Die App filter_page wird verwendet um mit der auf der Bauwerke-Seite vorhandenen Filterfunktion die Gebäude nach bestimmten Attributen zu Filtern. Die Funktionen hierfür sind in der views Datei der App vorhanden. Zur Umsetzung der Filterfunktion wurden die Hilfsfunktionen splitting, one_dict_set_to_string_list und delete_duplicates geschrieben, die Hauptfunktion tragen die Funktionen my_filter und display_building_filter. Die Kommentare dieser Funktionen beschreiben die genaue Umsetzung weiter.

### home 

Die App home dient nur zur Darstellung der Startseite und benötigt daher keine weiteren Klassen oder Funktionen.

### impressum

Die App impressum ist zuständig für die Darstellung der Impressum-Seite und die Verfügbarkeit des Kurslinks auf allen Seiten der Webandwendung. Dafür enthält die Datei models die Klasse Impressum. Diese besitzt nur die Attribute course_link, mit dem der Link zum aktuellen Vorlesungskurs festgehalten werden kann, und name um die Objekte der Klasse Impressum unterscheiden zu können. Hier ist anzumerken, dass durch das Überschreiben der Funktion save, nur ein Objekt dieser Klasse erzeugt werden kann. In views wird eine getter Funktion für das Attribut course_link bereitgestellt. Damit der Kurslink auch auf allen anderen Seiten verfügbar ist, wurde diese Funktion in die views aller anderen Apps importiert.

### materials_page

Mithilfe der App materials_page wird die Darstellung der Materialien-Seite umgesetzt. Dafür enthält models die Klassen Material und Category. Dateien können mit Hilfe des Attributs file hinzugefügt werden und mit dem Attribut category können die Dateien verschiedenen Kategorien zugeordnet werden. Um die Dateien gesammelt und sortiert nach Kategorien ausgeben zu können kann mit der Funktion get_categories_and_corresponding_files() ein Dictionary erzeugt werden. Die Funktion get_catgeories_and_corresponding_zip_files gibt für eine übergebene Kategorie die zugehörigen Dateien als zip-File zurück. Dieses wird dann direkt heruntergeladen.

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


Die Struktur in einer App ist in diesem Projekt immer gleich. 

**migration-Package** Hier werden die angewandten Modeländerungen gespeichert werden. Es ist wichtig hier den Überblick zu wahren und richtig zu migrieren, damit die Datenbank nicht jedes mal gelöscht werden muss, wenn etwas verändert wurde.

In dem **static-Directory** werden mögliche statische Datein gespeichert, die nur in dieser App verwendet werden.

**template-Directory**: Hier werden die Templates, die in einer App verwendet werden gespeichert.

**__init__-File**: Ist für mögliche Veränderung in der Konfiguration der App zuständig, wird aber auch von Python benötigt.

**admin-File**: Wird verwendet um das Django-Admin-Interface zu konfigurieren und Modelle aus der App zu registrieren.

**apps-File**: Konfiguration der App.

**models-File**: Die Modelle in Django, sind die Datenbankmodelle und erben von der Python-Klasse.

**test-File**: Für alle Funktionen, die in dem Projekt selbst erstellt wurden, existieren hier Tests.

**urls-File**: Da es sich um eine Webseite handelt, werden hier die Weiterleitungen zu den Unterseiten in einer Variable gespeichert, ebenso wie der Appname.

**views-File**: Beinhaltet die Funktion, die beim Aufruf der Webseite verwendet wird.

**Nur in der App timeline der Fall**
**templatetags-File**: Ermöglicht die Verwendung von definierten Funktionen in html-Files.


Für genauere Informationen zu den Files und Directories in den einzelnen Apps, stehen Kommentare und Doc-Strings in diesen, die speziefierte Klassen, Funktionen usw. erklären.


## Installation

Um diese Webanwendung nutzten zu können, muss sie auf einem Server installiert werden. Dieses Verfahren bezeichnet man als Deployment. Im folgenden wird an Hand unserer Server-Architektur beispielhaft erklärt wie dieser Prozess aussehen kann.

Für unser Projekt haben wir einen Server vom Rechnerpool Architektur der TU-Darmstadt gestellt bekommen. Dieser ist ein Debian-Linux auf den wir Secure Shell (SSH) Zugriff hatten.

### Voraussetzungen: 

- Einen Linux-Server. Hier wird dies nur für Debian Server beispielhaft erklärt (Sofern der Fall besteht, dass jemand Erfahrungen auf anderen Distros oder anderen Betriebssystemen des Servers sammelt, gerne Kontakt aufnehmen, und die Erfahrungen teilen. Für die meisten Fälle sollte das hier aber reichen oder zumindest eine Idee geben wie es funktioniert).
- Secure Shell (SSH) Zugriff auf den Server.
- Admin Rechte auf dem Server (sudo-berechtigter Nutzer oder root-Zugriff).

Zusammen mit den einzelnen Schritten sind Auszüge aus Dokumentationen und andere nützliche Quellen verlinkt. 

Alle Befehle gehen davon aus, dass der Nutzer im Besitz von Admin Rechten ist, wie üblich indiziert "$" dass der Befehl als normaler User ausgeführt werden kann, "#" dass er als Super-User bzw. als root-User ausgeführt werden muss. Das kann aber im speziellen Falle variieren, je nachdem wo ihr z.B. welche Ordner anlegt usw..

Allgemein zum Start empfehlen sich die Seiten aus der Django Dokumentation zum Thema Deployment:

> Siehe:
> 
> - Allgemein: https://docs.djangoproject.com/en/3.1/howto/deployment/ und ihre Unterseiten
> - Für Apache2: https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/modwsgi/

Wir werden uns meistens an den unteren Link halten. 

### Vorbereitung:

Zuerst müssen ein paar einmalige Vorbereitungen getroffen werden, damit der Server bereit ist. 

**Installation der Abhängigkeiten**:

- Python 3.x.x (unter Debian zum Zeitpunkt des Verfassens 3.7.3)

	<code># apt-get install python3</code>

- Apache2 Webserver
	
	<code># apt-get install apache2</code>

- PostgreSQL Datenbank

	<code># apt-get install postgresql</code>
	
	Ggf. daran denken den Diesnst zu starten und zu enablen:
	
	<code># systemctl start postgresql</code><br>
	<code># systemctl enable postgresql</code>
	
- Optional: Installieren von git, um das Repo zu klonen

	<code># apt-get install git</code>
	
**Herunterladen oder Klonen des Projektes**: 

<code> $ git clone https://github.com/ReisShape/bp55.git</code>

oder als .zip über dieses GitHub herunterladen, und z.B. per <code>scp</code> auf den Server kopieren.

**Einloggen**:

Nun loggt man sich per ssh auf dem Server ein:

<code>$ ssh NUTZERNAME@SERVER_DOMAIN</code>

Beide Angaben auf euren Server anpassen. <code>SERVER_DOMAIN</code> werden wir weiterhin als Platzhalter für die Domain eures Servers nutzen.

Mit <code>exit</code> kann man sich wieder ausloggen.

**Datenbank aufsetzen**:

Wir verwenden hier PostgreSQL. 

1. Einloggen in den postgres-Nutzer
	
	<code>$ sudo -ui postgres</code>
	
2. Erstellen eines Nutzers:

	<code>$ createuser --interactive</code>
	
	Dabei wird interaktiv nach Eigenschaften des Nutzers gefragt, so kann man einen Namen und ein Passwort festlegen. Man sollte den Nutzer nicht zum Admin-User machen. **Achtung**: Sofern man mit Djangos Test Tools die Tests ausführen möchte, muss man dem User das Recht verleihen Datenbanken erstellen zu dürfen, also die entsprechende Frage mit "	y" beantworten. Natürlich ist außerdem darauf zu achten am besten ein sicheres Passwort zu verwenden.


3. Einloggen in psql (Postgres's SQL Interface)

	<code> $ psql</code>
	
	Tipp: Mit <code>\du</code> kann man nun testen ob das Anlegen des Nutzers in Schritt zwei erfolgreich war. Man erhält eine Ausgabezeile mit dem Namen (wir haben "ruinsandbeyond" gewählt) und dem Recht "Create DB", sowie weiteren Angaben.

4. Erstellen einer Datenbank

	<code>$ CREATE DATABASE ruinsandbeyond;</code>
	
	Tipp: Man kann sich mit <code>\l</code> die existierenden Datenbanken auflisten lassen, so also überprüfen ob die Erstellung geklappt hat. Dabei sieht man auch den Besitzer der Datenbank, was im nächsten Schritt wichtig wird.
	
5. Dem erstellten Nutzer Rechte und Besitz an der erstellten Datenbank geben

	<code>$ GRANT ALL PRIVILEGES ON DATABASE "ruinsandbeyond" TO ruinsandbeyond;</code>
	
	<code>$ ALTER DATABASE ruinsandbeyond OWNER TO ruinsandbeyond;</code>
	
	Tipp: Nun nochmal <code>\l</code> ausführen, um zu sehen ob für die Datenbank "ruinsandbeyond" nun auch der Besitzer "ruinsandbeyond" eingetragen wurde.
	
### Einrichtung:
	
**Projekt und Projektordner einrichten**:

- Den Ordner mit Projektes aus dem Repo kopiert man am besten an einen Ort an dem man solche Dinge auf Linux Systemen erwarten würde (prinzipiell ist aber egal wo es liegt), z.B. nach <code>/opt</code> (so ist es in unserem Beispiel). Den Pfad wo das Projekt liegt sollte man sich merken. 
- Ggf. bekommt man später 403-Fobidden Errors, weil die Rechte am Ordner anders sind als sie sein sollten an dieser Stelle im Filesystem. Das ging uns immer so, wenn wir ihn per <code>scp</code> hoch kopiert haben. Ggf. also <code># chmod -R 755 bp55/</code> ausführen, um die passenden Rechte zu setzten.
- Zusätzlich werden Ordner für static und media Files benötigt. Static Files sind Daten die für die Website und deren Darstellung verwendet werden, wie z.B. HTML, und CSS. Im Media Ordner werden später Inhalte der Website (Bilder, Vorlesungsvideos, ...) gespeichert. 

	Man legt diese Ordner am besten an der zu erwartenden Stelle an, also innerhalb von <code>/var/www</code>, in unserem Fall haben wir uns für <code>/var/www/django/static</code> und <code>/var/www/django/media</code> entschieden. Diese Ordner also zuerst erstellen:
	
	<code># mkdir /var/www/django</code><br>
	<code># mkdir /var/www/django/static</code><br>
	<code># mkdir /var/www/django/media</code><br>
	
	Die Webanwendung soll natürlich Dateien in den media Ordner legen können, also muss www-data darauf zugreifen können, und Schreibrechte haben. Normalerweise ändert man dazu den Besitz des Ordners zu diesem Nutzer:
	
	<code># chown www-data.www-data /var/www/django/media/</code>
	
	Auch diese Pfade sollte man sich wieder merken.
	
- Nun muss die settings.py im Projektordner (Pfad aus Punkt 1) angepasst werden:
	- In ALLOWED_HOSTS muss die URL des Servers eingetragen werden (wir nutzen hier den Platzhalter von oben):
		
		```python:
		ALLOWED_HOSTS = [SERVER_DOMAIN]
		```
		
	- DEBUG auf False setzten:
	
		```pyhton:
		DEBUG = False
		```
		
	- Datenbank-Einstellungen:
		
		```python:
		DATABASES = {
			'default': {
				 'ENGINE': 'django.db.backends.postgresql',
		         'NAME': 'ruinsandbeyond',
		         'USER': 'ruinsandbeyond',
		         'PASSWORD': 'PASSWORT',
		         'HOST': '127.0.0.1',
		         'PORT': '5432',
			}
		}
		```
		
		Dabei die Angaben aus den vorherigen Schritten hier verwenden, anstelle von PASSWORT euer Datenbank Passwort angeben.
	
	- Optional aber Empfohlen: Eure Zeitzone und Sprache einstellen:
		
		```python:
		TIME_ZONE = "Europe/Berlin"
		LANGUAGE_CODE = "de-DE"
		```
		
		Ist das in unserem Fall.
		
	- Damit es nicht zu Fehlern mit dem Static Files später kommt, sollte man in <code>STATICFILES\_DIRS</code> alle Orte im Projekt eintragen an denen sich Static Files befinden. Das sind hier:
	
		```python:
		STATICFILES_DIRS = (
    		os.path.join(BASE_DIR, 'static'),
    		os.path.join(BASE_DIR, 'assets'),
    		os.path.join(BASE_DIR, 'templates'),
		)
		```
		
		Dabei kann man <code>BASE\_DIR</code> für den Ort des Projektes verwenden (Die gezeigte Funktion erfordert das importieren von os, <code>import os</code> oben in der Datei einfügen).
		
	- Static und Media URLs und ROOTs setzen. Dabei zeigt je die URL auf den Unterordner (z.B. /media/), die ROOT auf den vollständigen Pfad:

	
		```python:
		STATIC_URL = '/static/'
		STATIC_ROOT = '/var/www/django/static/'
		MEDIA_URL = '/media/'
		MEDIA_ROOT = '/var/www/django/media/'
		```
		
	Die anschließenden "/" am Ende sind hier notwendig.
		
- Eine Virtual Environment (venv) für das Projekt erstellen. Damit das Projekt läuft braucht man eine Virtual Environment, spezifiziert nach PEP 405. 
	
	> Weiter Infos: https://docs.python.org/3/library/venv.html
	
	Dazu folgt man dieser Anleitung zum erstellen einer virtual environment. Man sollte sich dazu im Ordner des Projektes befinden bzw. sie dort anlegen.
	
	<code>$ cd /opt/bp55</code><br>
	<code># python3 -m venv ./venv</code>
	
	Erzeugt einen Ordner venv innerhalb des Projektordners.
	
- Die erstellte Virtual Environment nutzen und einrichten:
	
	Mit <code>$ source venv/bin/activate</code> aktiviert man die Virtual Environment. Nun kann man die benötigten Python-Abhängigkeiten installieren. Benötigt werden alle Pakete die in Requirements.txt genannt werden: Django, psycopg2, django-bootstrap4, selenium, model-bakery und Pillow. Diese findet man in dem Dokument Requirements.txt, und daraus kann auch einfach mit pip installiert werden:
	
	<code># pip install -r Requirements.txt</code>
	
	Tipp: Mit <code>deactivate</code> kann man die Virtual Enviroment wieder deaktivieren. Da sie aber ab jetzt noch viel gebraucht wird, sollte man dies jetzt nicht tun.
	   
- Nun kann man testen ob alles geklappt hat, bevor es weiter geht.

	<code>$ python manage.py showmigrations</code> sollte eine lange Liste ausgeben, aber keine Fehler schmeißen. Ist dies der Fall kann unser Projekt erfolgreich auf die Datenbank zugreifen.
	
	Mit <code>$ pip list</code> kann man prüfen ob die Python Abhängigkeiten richtig installiert wurden.	
	
- Static Files sammeln:

	Mit <code># python manage.py collectstatic</code> sammelt django alle Static Files des Projektes und legt sie unter dem vorher angelegten und benannten Static Ordner ab. 
	
- Migrations laufen lassen.

	> Was sind Migrations und wie funktionieren sie? Am Beispiel hier:
	>
	> Youtube Video "Why and how to do Database Migrations": https://www.youtube.com/watch?v=Wo0gXUVjy2A.
	>
	> Kurzgesagt: Man kann sich Migrations wie eine Version Control der Datenbank vorstellen.
	
	Um also das richtige Datenbank Layout zu erhalten (gesetz der Test im vorletzten Punkt hat geklappt) muss man <code>$ python manage.py migrate</code> ausführen. Dabei sollten viele Meldungen der Form "applied ... .py ... OK" ausgegeben werden.
	
	Tipp: Führt man danach abermals <code>$ python manage.py showmigrations</code>  aus, sollte man feststellen, dass nun alle Listeneinträge mit einem Kreuz versehen wurden (Aus "[ ]" wird "[X]").

**Apache und mod_wsgi Konfigurieren**:

Nun muss man noch den Webserver konfigurieren. Wir haben uns für Apache2 und die Nutzung von mod_wsgi entschieden. Ähnliches kann man aber auch mit nginx erreichen, dann muss man allerdings zusätzlich uwsgi installieren und konfigurieren. 

Die nötigen Schritte für eine Apache2 Konfiguration:

1. Wir benötigen mod_wsgi für Python 3. Daher sollte man

	<code># apt-get install libapache2-mod-wsgi-py3</code> 
	
	ausführen um die entsprechende Version zu installieren.
	
	Tipp: Danach kann es sinnvoll sein den Server neu zu starten, um die Änderungen in Kraft treten zu lassen. Dies werden wir später aber sowieso nochmal tun, daher ist es hier noch nicht zwingend notwendig:
	
	<code># systemctl restart apache2.service</code> 
	
2. Für die Apache2 Konfiguration sind wie üblich die Dateien in <code>/etc/apache2/site-available/</code> interessant. Dort sollte eine Datei angelegt werden, die die Konfiguration für unsere Seite enthält. Man kann diese benennen wie man möchte, wir haben uns für <code>ruinsandbeyond.conf</code> entschieden (also: <code>/etc/apache2/sites-available/ruinsandbeyond.conf</code>).
3. Dort fügt man nun die Konfiguration ein.
	
	> Erklärungen und Beispielvorgehen sind hier zu finden: https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/modwsgi/ 
	
	Wir werden hier nicht im Detail durch gehen, eine Beispielhafte Konfiguration könnte so aussehen (auch hier werden wieder Platzhalter von oben verwendet):
	
	```
	<VirtualHost *:80>
		ServerName SERVER_DOMAIN
	
		#ServerAdmin webmaster@localhost
	
		#DocumentRoot /var/www
	
		# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
		# error, crit, alert, emerg.
		# It is also possible to configure the loglevel for particular
		# modules, e.g.
		#LogLevel info ssl:warn
		LogLevel info
	
		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined
	
		# ######## /media/ directory ########
		# Will be live in /var/www/ for www-data user to use (and show to the internet)
		Alias /media/ /var/www/django/media/
		<Directory /var/www/django/media>
			Require all granted
		</Directory>
	
		# ######## /static/ directory ########
		# Will be live in /var/www/ for www-data user to use (and show to the internet)
		Alias /static/ /var/www/django/static/
		<Directory /var/www/django/static>
			Require all granted
		</Directory>
	
		# ######## DJANGO APPLICATION #########
		# WSGI Application will be served here with python.
		# Everything that is not static or media will be serverd here.
		# First two lines: to set wsgi to run in daemon mode, wich is better
		WSGIDaemonProcess SERVER_DOMAIN python-home=/opt/bp55/venv python-path=/opt/bp55
		WSGIProcessGroup SERVER_DOMAIN
		WSGIScriptAlias / /opt/bp55/bp55_ruins_and_beyond/wsgi.py process-group=SERVER_DOMAIN
		<Directory /opt/bp55/bp55_ruins_and_beyond>
			<Files wsgi.py>
				Require all granted
			</Files>
		</Directory>
	 
	
	</VirtualHost>
	```
	
	Ein paar wesentliche Punkte:
	- DocumentRoot wird keine benötigt (Kann sogar schädlich sein, falls hier falsch verwendet).
	- Server Namen auf die jeweilige SERVER_DOMAIN setzen.
	- Je für Media und Static wird ein Alias zu dem Pfad angelegt, und man erlaubt Apache drauf zuzugreifen.
	- Für unser Python Projekt werden die mod_wsgi Einstellungen gesetzt, und ebenfalls der Zugriff erlaubt.
		
		> Siehe: https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/modwsgi/
	- Notiz: Diese Konfiguration ist nur für HTTP (Port 80), für Notizen zu HTTPS siehe Abschnitt "HTTPS Konfiguration". Dies erfordert die Freigabe des Ports 80 ins Internet (das war bei unserem als Webserver gedachtem Server schon so vorgefertigt).
	
4. Nun haben wir alle Konfigurationen getätigt, doch sie sind noch nicht aktiviert. Um sie zu aktivieren müssten diese Dateien je in die <code>/etc/apache2/*-enabled/</code> Ordner. Das gilt sowohl für <code>sites</code> also auch <code>mods</code>. Das löst man üblicherweise so, dass man symbolische Links in den enabled-Ordnern plaziert, die auch die entsprechenden Dateien aus den available-Ordnern zeigen. Das kann man manuell machen, oder dafür die apache2 Werkzeuge verwenden:
	1. Das also zuerst für die Konfiguration von eben:
		
		<code># a2ensite ruinsandbeyond</code>
		
	2. Und für die mod_wsgi benötigen wir nicht nur die Konfiguration (die schon da ist), sondern auch eine .load Datei, die auch aktiviert werden muss. Wir müssen also <code>/etc/apache2/mods-available/wsgi.conf</code> und <code>/etc/apache2/mods-available/wsgi.load</code> verlinken in den entsprechenden enabled-Ordner. Auch dazu gibt es ein praktisches Werkzeug:
	
		<code># a2enmod wsgi</code> 
		
	3. Final einmal den Server neu starten: 
	
		<code># systemctl restart apache2.service</code> 
		
		
		Ggf. falls das das System nicht automatisch bei der Installation tut, sollte man auch nicht vergessen den Service zu Aktivieren, dann startet er automatisch neu, sofern man einen Server Reboot macht:
		
		<code># systemctl enable apache2.service</code>
		
**Einen Admin Nutzer einrichten**

Um das Projekt dann auch so nutzen zu können, wie gewollt, braucht der Admin noch einen Account. Über das Admin Interface kann dieser dann Daten einpfelgen usw., siehe Abschnitt "Admin Interface". Mindestens der erste Account für einen Administrator muss über das Terminal auf dem Server angelegt werden, weite kann man dann auch über das Admin Interface selbst hinzufügen. Um einen Admin zu registrieren folgendes Ausführen:

<code>$ python manage.py createsuperuser</code>

und den Anweisungen auf der Konsole folgen, abgefragt werden Nutzername, Passwort und E-Mail. **Achtung**: Noch wichtiger als das Datenbank-Passwort sollte dieses sicher gewählt sein, da jeder über das Internet auf das Interface zugreifen kann. So wäre es nicht gut ein schwaches Passwort zu wählen, weil man sonst leicht den Admin Zugang bekommen könnte. Ab hier siehe dann den Admin Interface Abschnitt.

Voraussetzung ist dass man sich weiterhin im Projektordner befindet (sonst müsste der Pfad zur manage.py angepasst werden), und man die venv weiterhin aktiviert hat.

### Installation sicherer machen

Soweit war das bisher eine Grundlegende Installation, die nur die nötigsten Schritte gezeigt hat. Man kann in Sachen Sicherheit noch einiges tun. Hier werden wir nun noch auf die Dokumentation verweisen, nichts mehr im Detail zeigen. Das Vorgehen hängt auch stark vom bisherigen Aufbau der Installation ab. 

> Siehe hier:
>
> - https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/ 
> - https://docs.djangoproject.com/en/3.1/topics/security/

Zum Beispiel ist es geboten nach dieser Anleitung:

- Die Einstellungen für DEBUG, SECURITY_KEY, die STATIC und MEDIA Dirs, sowie das Datenbank PASSWORD in Environment Variablen des Systems auszulagern.
- HTTPS zu aktivieren (siehe nächster Abschnitt).

### HTTPS Konfiguration
Wir haben uns weil es schneller und einfacher ist darauf verständigt, den Certbot von [Let's Encrypt](https://letsencrypt.org/) zu verwenden.
Diesen installiert man wie folgt aus einem snap Paket:
- Snap installieren:
	
	<code># apt-get install snapd</code>
	
	<code># snap install core</code>
	
	<code># snap refresh core</code>

- Let's Encrypts Certbot installieren:
 
	<code># snap install --classic certbot</code>
	
- Executable richtig verlinken:
	
	<code># ln -s /snap/bin/certbot /usr/local/bin/certbot</code>
	
Nun kann man Zertifikate bekommen:

<code>certbot --apache -d SERVER_DOMAIN</code>

Natürlich muss die Server Domain wieder entsprechend angepasst werden. In diesem Falle verwenden wir wie oben gesagt Apache2. 

Man kann auch nur die Zertifikate bekommen (und nicht die apache Konfiguration ändern lassen) wenn man die Option <code>--certonly</code> verwendet.

Wir mussten dann noch unsere Websiten Konfiguration anpassen. Dies betrifft die oben erstellte Datei <code>/etc/apache2/sites-available/ruinsandbeyond.conf</code>:

```
# Set old http to redirect to https
<VirtualHost *:80>
   # redirect all http requests to https site
    ServerName ruinsandbeyond.architektur.tu-darmstadt.de
    Redirect permanent / https://SERVER_DOMAIN
</VirtualHost>

<IfModule mod_ssl.c>
   <VirtualHost *:443>
   
    ############## SSL STUFF ###############
 
        # SSL Engine Switch:
        # Enable/Disable SSL for this virtual host.
        SSLEngine on
 
        # Path to cert and its key:
        SSLCertificateFile    /etc/letsencrypt/live/SERVER_DOMAIN/fullchain.pem
        SSLCertificateKeyFile /etc/letsencrypt/live/SERVER_DOMAIN/privkey.pem

	# ...
	# ...
	# [Configuration like before here]
	# ...
	# ...
	
    </VirtualHost>
</IfModule>
```

Dabei leitet man sinnvollerweise alles von http nach https um, und setzt den Pfad zu dem Zertifikat und seinem Schlüssel (wird von Certbot ausgegeben, folgt aber in der Regel der Form oben.

> Auch dazu Infos hier: 
> 
> - https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/ 
> - https://docs.djangoproject.com/en/3.1/topics/security/



### Erweitere Administration des Servers

Auch hier werden wir nicht ins Detail gehen, nur ein paar Tipps zu Administration eines Servers die wir sammeln konnten:

- Für Logs kann man Logrotate einrichten, um die Menge und Größe von Logs zu beherrschen.
- SSH Keys erleichtern das ständige Einloggen, ersparen das Passwort dabei.

### Einbindung eines SSO

Informationen zur Einrichtung des SSO auf dem Server empfehlen wir die Project-Description des django-cas-client:
https://pypi.org/project/django-cas-client/

Zur Integration des SSOs in das Projekt wird der Decorator <code> def login_required(func): </code> benötigt. Damit wird überprüft, ob der Nutzer eingeloggt ist und festgelegt, wohin dieser umgeleitet werden soll, wenn das nicht der Fall ist.
Mit Hilfe dieses decorators können dann alle views mit <code> @login_required </code> über den SSO-Login vor unbefugtem Zugriff geschützt werden.

## Contributers:
- [Duy Quang Ngyuen](https://github.com/ReisShape)
- [Jonathan Otto](https://github.com/JonaOtto)
- [Laura Buhleier](https://github.com/CottlestonPie1)
- [Thiemo Ganesha Welsch](https://github.com/ThGaWe)
- [Tobias Frey](https://github.com/FreyTobias)

