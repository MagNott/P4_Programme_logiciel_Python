# P4_Programme_logiciel_Python
Développez un programme logiciel en Python

# Mise en place de l'environnement
python3 -m venv env

# Activation de l'environnement
source env/bin/activate

# Convention de nommage
Utilisation de la notation hongroise
- Les paramétres de fonctions sont préfixés avec p_
- Les objets sont préfixés avec o_

# Configuration de l’analyse de code 
**Flake8 : vérification de la PEP 8**
Le projet utilise Flake8 pour vérifier la conformité du code aux normes PEP 8, avec une limite de 119 caractères par ligne définie dans le fichier setup.cfg.

Pour lancer le programme :
`python main.py`

Pour régénérer le rapport Flake8 :
`flake8 --config=.flake8 --format=html --htmldir=flake8_rapport`

**Black : formateur automatique**
Le projet utilise Black pour formater automatiquement le code avec la même limite de 119 caractères par ligne.

Pour formater le code avec Black :
`black .`