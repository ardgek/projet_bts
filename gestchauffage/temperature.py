import DS1631
import time
from gestchauffage.bdd_login import *

# virtual device
room = DS1631.DS1631virtualdevice(initial_temperature=17,
                                  thigh=20, tlow=17,
                                  P=3000, R=0.02,
                                  tau=360,
                                  Text_max=15, Text_min=10,
                                  period=24 * 3600)

bedroom = DS1631.DS1631virtualdevice(initial_temperature=17,
                                     thigh=18, tlow=17,
                                     P=1000, R=0.02,
                                     tau=360,
                                     Text_max=15, Text_min=10,
                                     period=24 * 3600)

bedroom2 = DS1631.DS1631virtualdevice(initial_temperature=17,
                                      thigh=20, tlow=17,
                                      P=1000, R=0.02,
                                      tau=360,
                                      Text_max=15, Text_min=10,
                                      period=24 * 3600)

bedroom3 = DS1631.DS1631virtualdevice(initial_temperature=17,
                                      thigh=23, tlow=16,
                                      P=1000, R=0.02,
                                      tau=360,
                                      Text_max=15, Text_min=10,
                                      period=24 * 3600)

kitchen = DS1631.DS1631virtualdevice(initial_temperature=20,
                                     thigh=22, tlow=19,
                                     P=1000, R=0.02,
                                     tau=360,
                                     Text_max=15, Text_min=10,
                                     period=24 * 3600)

garage = DS1631.DS1631virtualdevice(initial_temperature=11,
                                    thigh=14, tlow=10,
                                    P=1000, R=0.02,
                                    tau=360,
                                    Text_max=15, Text_min=10,
                                    period=24 * 3600)

def get_temp():
    time.sleep(0.75)
    temperature = room.get_temp()
    temperature2 = bedroom.get_temp()
    temperature3 = bedroom2.get_temperature()
    temperature4 = bedroom3.get_temperature()
    temperature5 = kitchen.get_temperature()
    temperature6 = garage.get_temperature()


def consigne_room() :
    set_tlow = "SELECT tlow FROM temp_consigne WHERE ID_room = '1'"
    set_thigh = "SELECT thigh FROM temp_consigne WHERE ID_room = '1'"

    # connection à la base de données
    cur = bdd_login()

    result_set_tlow = cur.execute(set_tlow)
    if result_set_tlow:
        for tlow in cur:
            print(tlow)
    else:
        print("Probleme de connection")

    result_set_thigh = cur.execute(set_thigh)
    # Si le résultat est vrai (donc la requete sql fonctionne, alors :
    if result_set_thigh:
        # On va print un tableau de valeur,
        for thigh in cur:
            print(thigh)
    else:
        print("Probleme de connection")

    room.set_tlow(tlow[0])
    room.set_thigh(thigh[0])
    print("Temperature haute sejour (room) : " + str(room.get_thigh()) + " Temperature basse sejour (room) : " + str(room.get_tlow()))

def consigne_bedroom():
    set_tlow = "SELECT tlow FROM temp_consigne WHERE ID_room = '2'"
    set_thigh = "SELECT thigh FROM temp_consigne WHERE ID_room = '2'"

    # connection à la base de données
    cur = bdd_login()

    result_set_tlow = cur.execute(set_tlow)
    if result_set_tlow:
        for tlow in cur:
            print(tlow)
    else:
        print("Probleme de connection")

    result_set_thigh = cur.execute(set_thigh)
    # Si le résultat est vrai (donc la requete sql fonctionne, alors :
    if result_set_thigh:
        # On va print un tableau de valeur,
        for thigh in cur:
            print(thigh)
    else:
        print("Probleme de connection")

    bedroom.set_tlow(tlow[0])
    bedroom.set_thigh(thigh[0])
    print("Temperature haute chambre 1 (bedroom) : " + str(bedroom.get_thigh()) + " Temperature basse chambre 1 (bedroom) : " + str(bedroom.get_tlow()))

def consigne_bedroom2():
    set_tlow = "SELECT tlow FROM temp_consigne WHERE ID_room = '3'"
    set_thigh = "SELECT thigh FROM temp_consigne WHERE ID_room = '3'"

    # connection à la base de données
    cur = bdd_login()

    result_set_tlow = cur.execute(set_tlow)
    if result_set_tlow:
        for tlow in cur:
            print(tlow)
    else:
        print("Probleme de connection")

    result_set_thigh = cur.execute(set_thigh)
    # Si le résultat est vrai (donc la requete sql fonctionne, alors :
    if result_set_thigh:
        # On va print un tableau de valeur,
        for thigh in cur:
            print(thigh)
    else:
        print("Probleme de connection")

    bedroom2.set_tlow(tlow[0])
    bedroom2.set_thigh(thigh[0])
    print("Temperature haute chambre 2 (bedroom2) : " + str(bedroom2.get_thigh()) + " Temperature basse chambre 2 (bedroom2) : " + str(bedroom2.get_tlow()))

def consigne_bedroom3():
    set_tlow = "SELECT tlow FROM temp_consigne WHERE ID_room = '4'"
    set_thigh = "SELECT thigh FROM temp_consigne WHERE ID_room = '4'"

    # connection à la base de données
    cur = bdd_login()

    result_set_tlow = cur.execute(set_tlow)
    if result_set_tlow:
        for tlow in cur:
            print(tlow)
    else:
        print("Probleme de connection")

    result_set_thigh = cur.execute(set_thigh)
    # Si le résultat est vrai (donc la requete sql fonctionne, alors :
    if result_set_thigh:
        # On va print un tableau de valeur,
        for thigh in cur:
            print(thigh)
    else:
        print("Probleme de connection")

    bedroom3.set_tlow(tlow[0])
    bedroom3.set_thigh(thigh[0])
    print("Temperature haute chambre 3 (bedroom 3) : " + str(bedroom3.get_thigh()) + " Temperature basse chambre 3 (bedroom 3) : " + str(bedroom3.get_tlow()))

def consigne_kitchen():
    set_tlow = "SELECT tlow FROM temp_consigne WHERE ID_room = '5'"
    set_thigh = "SELECT thigh FROM temp_consigne WHERE ID_room = '5'"

    # connection à la base de données
    cur = bdd_login()

    result_set_tlow = cur.execute(set_tlow)
    if result_set_tlow:
        for tlow in cur:
            print(tlow)
    else:
        print("Probleme de connection")

    result_set_thigh = cur.execute(set_thigh)
    # Si le résultat est vrai (donc la requete sql fonctionne, alors :
    if result_set_thigh:
        # On va print un tableau de valeur,
        for thigh in cur:
            print(thigh)
    else:
        print("Probleme de connection")

    kitchen.set_tlow(tlow[0])
    kitchen.set_thigh(thigh[0])
    print("Temperature haute cuisine (kitchen) : " + str(kitchen.get_thigh()) + " Temperature basse cuisine (kitchen): " + str(kitchen.get_tlow()))



def initilisation_consigne_all_room():

        consigne_room()
        consigne_bedroom()
        consigne_bedroom2()
        consigne_bedroom3()
        consigne_kitchen()

