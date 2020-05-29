from flask import Flask, render_template, request, session, url_for, redirect, Response
from gestchauffage.bdd_login import *
from gestchauffage.temperature import *
from datetime import datetime
import json
import time

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def login():
    user = str(request.form['username'])
    password = str(request.form['password'])
    var = "SELECT login, password FROM user WHERE login = '" + user + "' AND password = '" + password + "'"
    cur = bdd_login()
    result = cur.execute(var)
    if result:
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        return render_template('page_404.html')


@app.route('/index', methods=['GET'])
def index():
    #Temperature du DS1631 convertie en dizaine
     app.temp1 = "%.2f" % room.get_temperature()
     app.temp2 = "%.2f" % bedroom.get_temperature()
     app.temp3 = "%.2f" % bedroom2.get_temperature()
     app.temp4 = "%.2f" % bedroom3.get_temperature()
     app.temp5 = "%.2f" % kitchen.get_temperature()
     app.temp6 = "%.2f" % garage.get_temperature()


     change = "UPDATE data_temp SET tempT1 = '" + app.temp1 + "',tempT2 = '" + app.temp2 + "', tempT3 = '" + app.temp3 + "', tempT4 = '" + app.temp4+ "',tempT5 = '" + app.temp5 + "', tempT6 = '" + app.temp6 + "' WHERE ID = '4'"
     insert = "INSERT INTO data_temp (ID, tempT1, tempT2, tempT3, tempT4, tempT5, tempT6, tempEXT) VALUES ('NULL', '" + app.temp1 + "','" + app.temp2 + "','" + app.temp3 + "','" + app.temp4 + "','" + app.temp5 + "','" + app.temp6 + "','15')"
     cur = bdd_login()
     cur.execute(insert)
     templateData = {'temp': app.temp1, 'temp1': app.temp2, 'temp2': app.temp3, 'temp3': app.temp4,'temp4': app.temp5, 'temp5': app.temp6}

     return render_template('index.html', **templateData)


# Fonction Graphique

@app.route('/sejour')
def graph1():
    def generate_sejour():
        app.temp = "%.2f" % room.get_temperature()
        app.temp2 = "%.2f" % bedroom.get_temperature()
        app.temp3 = "%.2f" % bedroom2.get_temperature()
        app.temp4 = "%.2f" % bedroom3.get_temperature()
        app.temp5 = "%.2f" % kitchen.get_temperature()
        app.temp6 = "%.2f" % garage.get_temperature()
        json_data = json.dumps(
            {'time': datetime.now().strftime('%H:%M:%S'), 'temp1': app.temp, 'temp2': app.temp2, 'temp3': app.temp3,
             'temp4': app.temp4, 'temp5': app.temp5, 'temp6': app.temp6})
        yield f"data:{json_data}\n\n"
        time.sleep(1)

    return Response(generate_sejour(), mimetype='text/event-stream')

#Ajax temperature
@app.route('/temp_rooms', methods=['GET'])
def rooms():
    def generate_room():
        app.temp = "%.2f" % room.get_temperature()
        app.temp2 = "%.2f" % bedroom.get_temperature()
        app.temp3 = "%.2f" % bedroom2.get_temperature()
        app.temp4 = "%.2f" % bedroom3.get_temperature()
        app.temp5 = "%.2f" % kitchen.get_temperature()
        app.temp6 = "%.2f" % garage.get_temperature()
        json_data = json.dumps(
            {'time': datetime.now().strftime('%H:%M:%S'), 'temp1': app.temp, 'temp2': app.temp2, 'temp3': app.temp3,
             'temp4': app.temp4, 'temp5': app.temp5, 'temp6': app.temp6})
        yield f"{json_data}\n\n"
        time.sleep(3)

    return Response(generate_room(), mimetype='text/event-stream')


@app.route('/ON_OFF', methods=['GET'])
def consigne():
    def generate_ONOFF():

        app.temp = "%.2f" % room.get_temperature()
        app.temp2 = "%.2f" % bedroom.get_temperature()
        app.temp3 = "%.2f" % bedroom2.get_temperature()
        app.temp4 = "%.2f" % bedroom3.get_temperature()
        app.temp5 = "%.2f" % kitchen.get_temperature()
        app.temp6 = "%.2f" % garage.get_temperature()
        state_sejour = None
        state_chambre1 = None
        state_chambre2 = None
        state_chambre3 = None
        state_cuisine = None
        bonsoir = True
        if bonsoir:
            if app.temp > str(room.get_tlow()):
                state_sejour = 0
            else:
                state_sejour = 1
            if app.temp2 > str(bedroom.get_tlow()):
                state_chambre1 = 0
            else:
                state_chambre1 = 1
            if app.temp3 > str(bedroom2.get_tlow()):
                state_chambre2 = 0
            else:
                state_chambre2 = 1
            if app.temp4 > str(bedroom3.get_tlow()):
                state_chambre3 = 0
            else:
                state_chambre3 = 1
            if app.temp5 > str(kitchen.get_tlow()):
                state_cuisine = 0
            else:
                state_cuisine = 1

        json_data = json.dumps(
            {'time': datetime.now().strftime('%H:%M:%S'), 'temp1': app.temp, 'temp2': app.temp2, 'temp3': app.temp3,
             'temp4': app.temp4, 'temp5': app.temp5, 'state_sejour': state_sejour, 'state_chambre1': state_chambre1,
             'state_chambre2': state_chambre2, 'state_chambre3': state_chambre3, 'state_cuisine': state_cuisine,'consigne_sejour' : room.get_tlow()})
        yield f"{json_data}\n\n"
        time.sleep(1)

    return Response(generate_ONOFF(), mimetype='text/event-stream')


# Page 404
@app.route('/404')
def error():
    return render_template('page_404.html')


@app.route('/index2.html', methods=['GET','POST','DELETE'])
def index2():
    if request.method == 'POST':
        #On test si on peut bien se login sur la bdd
        try:
            cur = bdd_login()
            #si il y a une erreur, on renvoit à la page d'erreur 404
        except pymysql.Error as e :
            return render_template('page_404.html')

        if request.form['Tlow_sejour']:
            temp_low = request.form['Tlow_sejour']
            # On oblige temp_low à se convertir en int
            temp_low = int(temp_low)
            # On donne donc la valeur de temps_low + 1 = temp_high
            temp_high = temp_low +1
            # La valeur de la piece depend de celle qu'on a choisit grâce aux boutons
            ID_piece = str(1)

            print("temp haute : " + str(temp_high) + " temp basse : " + str(temp_low) + "")
            update_temp_consigne = "UPDATE temp_consigne SET tlow = '" + str(temp_low) + "', thigh = '" + str(temp_high) + "' WHERE ID_room = '" + str(ID_piece) + "'"
            result = cur.execute(update_temp_consigne)
            initilisation_consigne_all_room()

            templateData = {'consigne_sejour': room.get_tlow(), 'consigne_bedroom': bedroom.get_tlow(), 'consigne_bedroom2': bedroom2.get_tlow(), 'consigne_bedroom3': bedroom3.get_tlow(), 'consigne_cuisine': kitchen.get_tlow()}
            return render_template('index2.html', **templateData)

        if request.form['Tlow_bedroom']:
            temp_low = request.form['Tlow_bedroom']
            # On oblige temp_low à se convertir en int
            temp_low = int(temp_low)
            # On donne donc la valeur de temps_low + 1 = temp_high
            temp_high = temp_low + 1
            # La valeur de la piece depend de celle qu'on a choisit grâce aux boutons
            ID_piece = str(2)

            print("temp haute : " + str(temp_high) + " temp basse : " + str(temp_low) + "")
            update_temp_consigne = "UPDATE temp_consigne SET tlow = '" + str(temp_low) + "', thigh = '" + str(temp_high) + "' WHERE ID_room = '" + str(ID_piece) + "'"
            result = cur.execute(update_temp_consigne)
            initilisation_consigne_all_room()

            templateData = {'consigne_sejour': room.get_tlow(), 'consigne_bedroom': bedroom.get_tlow(), 'consigne_bedroom2': bedroom2.get_tlow(),'consigne_bedroom3': bedroom3.get_tlow(), 'consigne_cuisine': kitchen.get_tlow()}
            return render_template('index2.html', **templateData)

        if request.form['Tlow_bedroom2']:
            temp_low = request.form['Tlow_bedroom2']
            # On oblige temp_low à se convertir en int
            temp_low = int(temp_low)
            # On donne donc la valeur de temps_low + 1 = temp_high
            temp_high = temp_low + 1
            # La valeur de la piece depend de celle qu'on a choisit grâce aux boutons
            ID_piece = str(3)

            print("temp haute : " + str(temp_high) + " temp basse : " + str(temp_low) + "")
            update_temp_consigne = "UPDATE temp_consigne SET tlow = '" + str(temp_low) + "', thigh = '" + str(temp_high) + "' WHERE ID_room = '" + str(ID_piece) + "'"
            result = cur.execute(update_temp_consigne)
            initilisation_consigne_all_room()

            templateData = {'consigne_sejour': room.get_tlow(), 'consigne_bedroom': bedroom.get_tlow(), 'consigne_bedroom2': bedroom2.get_tlow(),'consigne_bedroom3': bedroom3.get_tlow(), 'consigne_cuisine': kitchen.get_tlow()}
            return render_template('index2.html', **templateData)

        if request.form['Tlow_bedroom3']:
            temp_low = request.form['Tlow_bedroom3']
            # On oblige temp_low à se convertir en int
            temp_low = int(temp_low)
            # On donne donc la valeur de temps_low + 1 = temp_high
            temp_high = temp_low + 1
            # La valeur de la piece depend de celle qu'on a choisit grâce aux boutons
            ID_piece = str(4)

            print("temp haute : " + str(temp_high) + " temp basse : " + str(temp_low) + "")
            update_temp_consigne = "UPDATE temp_consigne SET tlow = '" + str(temp_low) + "', thigh = '" + str(temp_high) + "' WHERE ID_room = '" + str(ID_piece) + "'"
            result = cur.execute(update_temp_consigne)
            initilisation_consigne_all_room()

            templateData = {'consigne_sejour': room.get_tlow(), 'consigne_bedroom': bedroom.get_tlow(), 'consigne_bedroom2': bedroom2.get_tlow(),'consigne_bedroom3': bedroom3.get_tlow(), 'consigne_cuisine': kitchen.get_tlow()}
            return render_template('index2.html', **templateData)

        if request.form['Tlow_cuisine']:
            temp_low = request.form['Tlow_cuisine']
            # On oblige temp_low à se convertir en int
            temp_low = int(temp_low)
            # On donne donc la valeur de temps_low + 1 = temp_high
            temp_high = temp_low + 1
            # La valeur de la piece depend de celle qu'on a choisit grâce aux boutons
            ID_piece = str(5)

            print("temp haute : " + str(temp_high) + " temp basse : " + str(temp_low) + "")
            update_temp_consigne = "UPDATE temp_consigne SET tlow = '" + str(temp_low) + "', thigh = '" + str(temp_high) + "' WHERE ID_room = '" + str(ID_piece) + "'"
            result = cur.execute(update_temp_consigne)
            initilisation_consigne_all_room()

            templateData = {'consigne_sejour': room.get_tlow(), 'consigne_bedroom': bedroom.get_tlow(), 'consigne_bedroom2': bedroom2.get_tlow(), 'consigne_bedroom3': bedroom3.get_tlow(), 'consigne_cuisine': kitchen.get_tlow()}
            return render_template('index2.html', **templateData)

        templateData = {'consigne_sejour': room.get_tlow(), 'consigne_bedroom': bedroom.get_tlow(),'consigne_bedroom2': bedroom2.get_tlow(), 'consigne_bedroom3': bedroom3.get_tlow(), 'consigne_cuisine': kitchen.get_tlow()}
        return render_template('index2.html', **templateData)


    if request.method == 'GET':
        print("GET")
        templateData = {'consigne_sejour': room.get_tlow(), 'consigne_bedroom': bedroom.get_tlow(), 'consigne_bedroom2' : bedroom2.get_tlow(),'consigne_bedroom3': bedroom3.get_tlow(), 'consigne_cuisine': kitchen.get_tlow() }
        return render_template('index2.html',  **templateData )


@app.route('/index3.html', methods=['GET','POST','DELETE'])
def index3():
    if request.method == 'POST':
        #On test si on peut bien se login sur la bdd
        try:
            cur = bdd_login()
            #si il y a une erreur, on renvoit à la page d'erreur 404
        except pymysql.Error as e :
            return render_template('page_404.html')
        print("POST")

        if request.form['prog_sejour_temp_1'] and request.form['prog_sejour_hours_1'] and request.form ['prog_sejour_checkbox_true_1'] :
            temp_low = request.form['prog_sejour_temp_1']
            temp_high = int(temp_low) + 1
            hours = request.form['prog_sejour_hours_1']
            monday = request.form['prog_sejour_checkbox_monday_1']
            tuesday = request.form['prog_sejour_checkbox_tuesday_1']
            wednesday = request.form['prog_sejour_checkbox_wednesday_1']
            thursday = request.form['prog_sejour_checkbox_thursday_1']
            friday = request.form['prog_sejour_checkbox_friday_1']
            saturday = request.form['prog_sejour_checkbox_saturday_1']
            sunday = request.form['prog_sejour_checkbox_sunday_1']
            ID_piece = 1
            ID_ligne = 1
            initilisation_jours = "UPDATE programmation_thermostat SET monday = '"+str(monday)+"', tuesday = '"+str(tuesday)+"', wednesday = '"+str(wednesday)+"', thursday = '"+str(thursday)+"', friday = '"+str(friday)+"', saturday = '"+str(saturday)+"', sunday = '"+str(sunday)+"' WHERE ID_room = '" + str(ID_piece) + "' AND ID_ligne = '" + str(ID_ligne) + "' "
            result_initilisation_jours = cur.execute(initilisation_jours)
            update = "UPDATE programmation_thermostat SET tlow = '" + str(temp_low) + "', thigh = '" + str(temp_high) + "', hours = '" + str(hours) + "'  WHERE ID_room = '" + str(ID_piece) + "' AND ID_ligne = '" + str(ID_ligne) + "' "
            result_update = cur.execute(update)



            prog_sejour_temp_1 = "SELECT tlow FROM programmation_thermostat WHERE ID_room = '1' AND ID_ligne = '1' "
            resultat_prog_sejour_temp_1 = cur.execute(prog_sejour_temp_1)
            for row in cur:
                print(row)
        return render_template('index3.html')

    if request.method == 'GET':
        print("GET")
        return render_template('index3.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
