import sys

import pymysql
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import logging
import hashlib
from APP_Timbrage import obj_mon_application
from APP_Timbrage.database.connect_db_context_manager import MaBaseDeDonnee

@obj_mon_application.route("/", methods=['GET', 'POST'])
@obj_mon_application.route("/login", methods=['GET', 'POST'])
def login():
    obj_mon_application.logger.warning("login")
     # Message de sortie si quelque chose ne va pas ...
    msg = ''
    # Vérifiez si des requêtes POST "nom d'utilisateur" et "mot de passe" existent (formulaire soumis par l'utilisateur)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        obj_mon_application.logger.warning("LOGIN 2")
        # Créez des variables pour un accès facile
        username = request.form['username']
        password = request.form['password']
        hs = hashlib.sha256(password.encode("utf-8")).hexdigest()
        # Vérifier si le compte existe en utilisant MySQL
        with MaBaseDeDonnee().connexion_bd.cursor() as cursor:
            cursor.execute('SELECT * FROM t_identification WHERE nom_utilisateur = %s AND mot_de_passe = %s', (username, hs,))
            # Récupérer un enregistrement et renvoyer le résultat
            account = cursor.fetchone()
            # Si le compte existe dans la table des comptes dans la base de données externe
            if account:
                obj_mon_application.logger.warning('loggedin')
                # Créer des données de session, nous pouvons accéder à ces données dans d'autres itinéraires
                session['loggedin'] = True
                session['id_identification'] = account['id_identification']
                session['nom_utilisateur'] = account['nom_utilisateur']
                # Redirection à l'accueil
                return redirect(url_for('homepage', order_by='ASC', id_horaire_sel=1))
            else:
                obj_mon_application.logger.warning('Not loggedin')
                # Le compte n'existe pas ou le nom d'utilisateur / mot de passe est incorrect
                msg = 'Incorrect username/password!'
    # Afficher le formulaire de connexion avec un message (le cas échéant)
    return render_template('index.html', msg=msg)
