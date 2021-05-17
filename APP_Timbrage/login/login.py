import sys

import pymysql
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from APP_Timbrage import obj_mon_application
from APP_Timbrage.database.connect_db_context_manager import MaBaseDeDonnee


@obj_mon_application.route("/", methods=['GET', 'POST'])
def login():
     # Message de sortie si quelque chose ne va pas ...
    msg = ''
    # Vérifiez si des requêtes POST "nom d'utilisateur" et "mot de passe" existent (formulaire soumis par l'utilisateur)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Créez des variables pour un accès facile
        username = request.form['username']
        password = request.form['password']
        # Vérifier si le compte existe en utilisant MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM t_identification WHERE nom_utilisateur = %s AND mot_de_passe = %s', (username, password,))
        # Récupérer un enregistrement et renvoyer le résultat
        account = cursor.fetchone()
        # Si le compte existe dans la table des comptes dans la base de données externe
        if account:
            # Créer des données de session, nous pouvons accéder à ces données dans d'autres itinéraires
            session['loggedin'] = True
            session['id_identification'] = account['id_identification']
            session['nom_utilisateur'] = account['nom_utilisateur']
            # Redirection à l'accueil
            return render_template('home.html')
        else:
            # Le compte n'existe pas ou le nom d'utilisateur / mot de passe est incorrect
            msg = 'Incorrect username/password!'
    # Afficher le formulaire de connexion avec un message (le cas échéant)
    return render_template('index.html', msg=msg)
