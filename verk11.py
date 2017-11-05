#Sandra Dögg Kristmundsdóttir
#3.11.17
#verkefni 11

from bottle import *
import pymysql


@route ("/static/<filename>")
def staticFile(filename):
    return static_file ( filename, root="./static/" )


@route("/")
def index():
    return template ("index.tpl")


@post("/nidurstada")
def index():
    if request.forms.get ("bilnumer"):
        m = (request.forms.get("bilnumer")).upper()
        connection = pymysql.connect (host='tsuts.tskoli.is', port=3306, user='1105922489', passwd='mypassword', db='1105922489_vef2verk11')
        with connection.cursor() as cursor:
            sql = "SELECT skraningarnumer, Tegund, verksmidjunumer, skraningardagur, co2, þyngd, skodun, stada FROM bilar WHERE skraningarnumer = '" + m + "'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                bilnumer = result[0]
                tegund = result[1]
                verksmidjunr = result[2]
                skraningardagur = result[3]
                co2 = result[4]
                thyngd = result[5]
                skodun = result[6]
                stada = result[7]
                if str (result[0]) == str (m):
                    return template ("info.tpl", a=bilnumer, b=tegund, c=verksmidjunr, d=skraningardagur, e=co2, f=thyngd, g=skodun, h=stada)
            else:
                return template ("popup.tpl", text="Bíll ekki til")
        connection.close()
    return template ("index.tpl")

@get("/innskraning")
def innskraning():
    return template ("innskraning.tpl")


@post("/athuga")
def athuga():
    connection = pymysql.connect (host='tsuts.tskoli.is', port=3306, user='1105922489', passwd='mypassword', db='1105922489_vef2verk10')
    username = (request.forms.get("username"))
    password = str(request.forms.get( "password" ))
    with connection.cursor() as cursor:
        sql = "SELECT pass FROM user WHERE user = '" + username + "'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            print (result[0])
            print (password)
            if str (result[0]) == str (password):
                response.set_cookie("account", username, secret=password)
                return template ("leynisida.tpl", username=username)
            else:
                uttak = "Rangt lykilorð"
        else:
            uttak = "Notandinn er ekki til"
    connection.close()
    if uttak == "Rangt lykilorð":
        return template("buinnadskrainn.tpl", uttak=uttak)
    elif uttak == "Notandinn er ekki til":
        return template ("buinnadskrainn.tpl", uttak=uttak)


@post("/breytabil")
def index():
    if request.forms.get("bilnumer"):
        m = (request.forms.get("bilnumer")).upper()
        connection = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1105922489', passwd='mypassword', db='1105922489_vef2verk11')
        with connection.cursor() as cursor:
            sql = "SELECT skraningarnumer, Tegund, verksmidjunumer, skraningardagur, co2, þyngd, skodun, stada FROM bilar WHERE skraningarnumer = '" + m + "'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                bilnumer = result[0]
                tegund = result[1]
                verksmidjunr = result[2]
                skraningardagur = result[3]
                co2 = result[4]
                thyngd = result[5]
                skodun = result[6]
                stada = result[7]
                if str(result[0]) == str(m):
                    return template ("breytabil.tpl", a=bilnumer, b=tegund, c=verksmidjunr, d=skraningardagur, e=co2, f=thyngd, g=skodun, h=stada)
            else:
                return template ("popup.tpl", text="Bíll ekki til")
        connection.close()
    return template ("index.tpl")

@post("/baetabil")
def index():
    if request.forms.get("bilnumer"):
        m = (request.forms.get("bilnumer")).upper()
        connection = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1105922489', passwd='mypassword', db='1105922489_vef2verk11')
        with connection.cursor () as cursor:
            sql = "SELECT skraningarnumer FROM bilar WHERE skraningarnumer = '" + m + "'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                uttak = "bíll nú þegar í gagnagrunni!"
            else:
                sql = "INSERT INTO bilar (skraningarnumer) VALUES ('" + m + "')"
                cursor.execute(sql)
                connection.commit()
                uttak = "bill hefur verið bætt við!"
        connection.close()
        return template("buinnadskrainn.tpl", uttak=uttak)


@route("/utskra")
def utskraning():
    response.set_cookie("account", "", expires=0)
    return template ("index.tpl")


if __name__ == "__main__":
    run ( host='localhost', port=5000, debug=True )