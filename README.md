# Plant Cell Wall KnowledgeBase

Ensure that you have Python 3.8 or higher installed.

To install Python 3.8 on WSL2 (Windows 10), run:

```bash
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.8
```

Create and activate a virtual environment:

```bash
sudo apt install python3-virtualenv
virtualenv --python=3.8 .venv
source .venv/bin/activate
```

Install all dependencies:

```bash
sudo apt-get install python3.8-dev default-libmysqlclient-dev build-essential python3.8-distutils
pip install -r requirements.txt
```
Django has a settings.py documment, heve we supply a settings.template.py, that you can use as model to create a setting.py in the pcwkb folder. Inside it you can change to use your database/user configuration.

To build the documentation, go to `docs/` and run:

```
sphinx-build -b html source/ build/html
```

Note that we changed the default Sphinx builder to use the Markdown parser. This is done by adding the following line to `conf.py` file in the `pcwkb/docs` folder:

```
extensions = ["myst_parser"]
```

## Running the Server

To run the server and access the web page, navigate to the `pcwkb/pcwkb` folder in your terminal and execute the following command:

```bash
python manage.py runserver
```

This will start the Django development server. You can then open your web browser and go to http://127.0.0.1:8000/pcwkb_core to access the web page

# Reseach and Development Team
 
 * João Vitor Leite Novoletti (IFSP, Piracicaba)
 * Bianca Sagiorato (UFSCar, São Carlos)
 * Danielli Teixeira (UFSCar, São Carlos)
 * Dr. Diego M. Riaño Pachón (associate professor, CENA/USP Piracicaba)
 * Dr. Renato Augusto Corrêa dos Santos (post-doctoral researcher, CENA/USP Piracicaba)