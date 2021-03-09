# Ruins and beyond!

Diese Software ist im Rahmen des Pflichtfaches "Bachelor Praktikum" für den Studiengang Informatik
Bachlor of Science im Wintersemester 2020/21 an der TU-Darmstadt entstanden. 

Dieses Projekt ist unter der [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.txt) lizensiert, siehe LICENSE.

**Motivation und Kontext**: Die Auftraggeber, die Veranstalter des Moduls "Klassische Architektur und Städtebau der Antike" des Fachbereichs Architektur der TU-Darmstadt, möchten die Gestaltung ihrer Vorlesung um eine Webanwendung zum digitalen Lernen erweitern. Die Idee ist aufgrund des pandemiebedingten Onlinestudienbetriebs entstanden und soll nun im Rahmen des Bachlorpraktikums umgesetzt werden. Hierfür möchten die Auftraggeber eine digitale Wissensplattform "Ruins and Beyond!" zu Bauwerken der Antike aufbauen, auf der die Studierenden, auf der Basis der zur Verfügung gestellten Materialien, die Lehrinhalte selbstbestimmt kombinieren und absolvieren können. Diese benötigten Videos, Bilder und Gebäudedaten wurden hierfür zu Beginn des Projektes von den Auftraggebern zur Verfügung gestellt.

**Umsetzung**: Sofern der Nutzende noch nicht über den Single-Sign-On der TU-Darmstadt eingeloggt ist, wird er zunächst auf die Login-Seite geleitet, um sich dort anzumelden. Dies stellt die Einhaltung der Urheberrechte sicher und dass nur die gedachte Zielgruppe auf die Inhalte zugreifen kann. Anschließend gelangt man auf die Intro-Seite. Diese enthält ein Intro-Video und einen Beschreibungstext. Das Intro-Video gibt einen Einstieg in die Vorlesung, welche durch die Webanwendung begleitet wird und somit auch das Thema dieser präsentiert. Der Beschreibungstext enthält eine Beschreibung aller verfügbaren Funktionalitäten der Unterseiten, damit Nutzende sich schnell und einfach zurecht finden. Auf jeder Seite, mit Ausnahme der Login-Seite, wird eine Menüleiste angezeigt, die Verlinkungen zu den Unterseiten "Intro", "Zeitachse", "Bauwerke", "Staffel" und "Materialien" bereitstellt. Auf der Zeitachse werden ausgewählte Gebäude und Ereignisse von ca. 1400 v.Chr. bis ca. 600 n.Chr. chronologisch aufgeführt. Dabei werden Bauwerke mit Titel, Datierung und einem Vorschaubild, sowie Ereignisse mit Bezeichnung und Datierung dargestellt. Durch Auswahl eines Bauwerks wird man auf die zugehörige Detailseite geleitet. Auf der Detailseite werden Informationen, Bilder und Grundrisse zu dem jeweiligen Gebäude angezeigt mit der Möglichkeit Videos anzusehen, in denen das Bauwerk behandelt wird. Auf der „Bauwerke“-Seite wird die Möglichkeit geboten, die Gebäude nach bestimmten Kategorien zu filtern. Die Ergebnisse werden daraufhin tabellarisch angezeigt und enthalten ebenfalls eine Verlinkung zur Detailseite. Mittels der Suchfunktion, die auf jeder Unterseite angezeigt wird, kann nach den Attributen "Name", "Stadt", "Region", "Land", "Epoche", "Architekt", "Kontext", "Bauherr", "Bautypus", "Bauform", "Funktion" und "Säulen-ordnung" der Gebäude gesucht werden. Die Ergebnisse werden ähnlich wie bei der Filterfunktion tabellarisch aufgelistet. Die "Staffel"-Unterseite enthält alle Vorlesungsvideos, chronologisch nach Epochen geordnet. Nutzende können hier für eine bessere Übersichtlichkeit, Epochen mit vielen Videos aus- und einklappen. Wählt der Nutzende ein Video aus, wird es in einem Pop-Up geöffnet. Zu jedem Video ist auf der Seite, und im Pop-Up zunächst nur ein aussagekräftiges Vorschaubild zu sehen. Auf der "Materialien" Seite werden weitere in Kategorien eingeteilte Vorlesungsinhalte zum Download angeboten.

**Verwendete Technologien**: Unsere Webanwendung basiert auf [Python](https://python.org) und als Framework wird [Django](https://djangoproject.com) verwendet. Die Videos, Bilder und PDF’s werden auf einem Server des Rechnerpools des Fachbereichs Architektur hinterlegt und mittels [PostgreSQL](https://postgresql.org) verwaltet. Auf dem Server läuft der Webserver [Apache](https://httpd.apache.org) auf dem Betriebssystem Debian.

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

<code>$ ssh NUTZERNAME@SERVER_URL</code>

Beide Angaben auf euren Server anpassen. <code>SERVER_URL</code> werden wir weiterhin als Platzhalter für die URL eures Servers nutzen.

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
		ALLOWED_HOSTS = [SERVER_URL]
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
	
	Mit <code>$ source venv/bin/activate</code> aktiviert man die Virtual Environment. Nun kann man die benötigten Python-Abhängigkeiten installieren. Benötigt werden alle Pakete die in Requirements.txt genannt werden: Django, psycopg2, django-bootstrap4, selenium, model-bakery und Pillow. Installieren:
	
	<code># pip install Django psycopg2 django-bootstrap4 selenium model-bakery Pillow</code>
	
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
		ServerName SERVER_URL
	
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
		WSGIDaemonProcess SERVER_URL python-home=/opt/bp55/venv python-path=/opt/bp55
		WSGIProcessGroup SERVER_URL
		WSGIScriptAlias / /opt/bp55/bp55_ruins_and_beyond/wsgi.py process-group=SERVER_URL
		<Directory /opt/bp55/bp55_ruins_and_beyond>
			<Files wsgi.py>
				Require all granted
			</Files>
		</Directory>
	 
	
	</VirtualHost>
	```
	
	Ein paar wesentliche Punkte:
	- DocumentRoot wird keine benötigt (Kann sogar schädlich sein, falls hier falsch verwendet).
	- Server Namen auf die jeweilige SERVER_URL setzen.
	- Je für Media und Static wird ein Alias zu dem Pfad angelegt, und man erlaubt Apache drauf zuzugreifen.
	- Für unser Python Projekt werden die mod_wsgi Einstellungen gesetzt, und ebenfalls der Zugriff erlaubt.
		
		> Siehe: https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/modwsgi/
	- Notiz: Diese Konfiguration ist nur für HTTP (Port 80), für Notizen zu HTTPS siehe Abschnitt "HTTPS Konfiguration". Dies erfordert die Freigabe des Ports 80 ins Internet (das war bei unserem als Webserver gedachtem Server schon so vorgefertigt).
	
4. Nun haben wir alle Konfigurationen getätigt, doch sie sind noch nicht aktiviert. Um sie zu aktivieren müssten diese Dateien je in die <code>/etc/apache2/*-enabled/</code> Ordner. Das gilt sowohl für <code>sites</code> also auch <code>mods</code>. Das löst man üblicherweise so, dass man symbolische Links in den enabled-Ordnern plaziert, die auch die entsprechenden Dateien aus den available-Ordnern zeigen.
	1. Das also zuerst für die Konfiguration von eben:
		
		<code># ln -s /etc/apache2/sites-available/ruinsandbeyond.conf /etc/apache2/sites-enabled/ruinsandbeyond.conf</code>
		
	2. Und für die mod_wsgi benötigen wir nicht nur die Konfiguration (die schon da ist), sondern auch eine .load Datei, die auch aktiviert werden muss. Wir müssen also <code>/etc/apache2/mods-available/wsgi.conf</code> und <code>/etc/apache2/mods-available/wsgi.load</code> verlinken in den entsprechenden enabled-Ordner:
	
		<code># ln -s /etc/apache2/mods-available/wsgi.conf /etc/apache2/mods-enabled/wsgi.conf</code>
		<code># ln -s /etc/apache2/mods-available/wsgi.load /etc/apache2/mods-enabled/wsgi.load</code>
		
		Ggf. könnten diese Links schon existieren, dann geben die Befehle Fehler aus, dass die Dateien schon existieren würden. Das wäre dann an der Stelle nicht schlimm, Hauptsache die Links existieren. 
		
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
*Wir planen das zuerst mal mit Let's Encrypts Certbot auszuprobieren. Die installation ist ziemlich straight-foreward, und erfolgt aus mittels snap, und dem Certbot snap Package. Da dieses nicht mehr in unsere Zeit der Zuständigkeit des Projektes fiel, können wir hier nicht wirklich sagen, ob und wie das funktioniert, aber dazu gibt es haufenweise Dokumentation im Netz. Ansonsten müssten wir für die Uni über den Verein zur Förderung des deutschen Forschungsnetzes ein Zertifikat beantragen, was langwierige Papierarbeit nach sich zieht und dauert. Alles andere ist leider noch*

**In Arbeit, noch nicht implemtiert, TODO**

> Auch dazu Infos hier: 
> 
> - https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/ 
> - https://docs.djangoproject.com/en/3.1/topics/security/



### Erweitere Administration des Servers

Auch hier werden wir nicht ins Detail gehen, nur ein paar Tipps zu Administration eines Servers die wir sammeln konnten:

- 

### Einbindung eines SSO
**Auch hier: In Arbeit, noch nicht implemtiert, TODO**
			