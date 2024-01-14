import export
from flask import Flask, render_template, request, jsonify
import subprocess as sp
from pymongo import MongoClient
from mongopass import mongopass
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

client = MongoClient(mongopass)
db = client.restaurant1
collectionOfTables = db.tables
collectionOfBookings = db.bookings

#Muestro todas las mesas
@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    documents = collectionOfBookings.find()
    tables = list(documents)
    for table in tables:
        print(table)
    return render_template("index.html", bookings=tables)


@app.route('/bookrestaurant', methods=['POST'])
def booking():
    response = {'message': 'Application Started'}
    print("COMIENZO FUNCION")
    phone = request.json.get("phone")
    email = request.json.get("email")
    str_diners = request.json.get("diners")
    diners = int(str_diners)
    location = request.json.get("location")
    #date = request.json.get("date")
    #time = request.json.get("time")
    datetime = request.json.get("datetime")

    #Busco las mesas que hay con esas características (comensales >= que los proporcionados y localización
    """
    queryTables = {
        "location": location,
        "diners": {"$gte": diners},
        "date": date
    }

    # Execute the query
    resultTables = collectionOfTables.find(queryTables)

    #De estas mesas voy a coger una de ellas para asignarla a la reserva.
    #Voy a buscar en reservas si cada mesa está en bookings
    for table in resultTables:
        numTable = table.get("number")
        #busco en bookings si existe un registro de esa reserva ese día.
        queryBooking = {
            "table" : numTable
        }
        resultBooking = collectionOfBookings.find(queryBooking)
        if resultBooking.count() == 0:
            bookingTable = numTable
        else:
            for table2 in resultBooking:
                start_time = table2.get("time")
                end_time = start_time + timedelta(hours=1)
                formatted_end_time = end_time.strftime("%H:%M:%S")
                queryBooking2 = {
                    "time": {
                        "$not": {
                            "$gte": start_time,
                            "$lte": end_time
                        }
                    }
                }
                resultBooking2 = collectionOfBookings.find_one(queryBooking2)
                if resultBooking2.count() == 0:
                    response = jsonify({"message": "Failed"})
                    response.status_code = 500  # Set the status code explicitly
                else:
                    bookingTable = resultBooking2


                    insert = {
                        "phone": phone,
                        "customer": email,
                        "diners": diners,
                        "date": date,
                        "time": time,
                        "table": bookingTable
                    }

                    # Insert the document into the collection
                    inserted_id = collectionOfBookings.insert_one(insert).inserted_id
                    # Print the inserted document's ID
                    print("Inserted document ID:", inserted_id)

                    #si inserted_id distinto de null devuelvo 200
                    if not inserted_id:
                        response = jsonify({"message": "Failed"})
                        response.status_code = 500  # Set the status code explicitly
                    else:
                        response = jsonify({"message": "Success"})
                        response.status_code = 200  # Set the status code explicitly
        """

    #encuentra una mesa que esté en esa localización y que los comensales sean
    #mayor o igual que los proporcionados
    queryTable = {
        "location": location,
        "diners": {
            "$gte": diners
        }
    }

    resulttable = collectionOfTables.find_one(queryTable)

    num_table = int(resulttable["number"])

    insert = {
        "phone": phone,
        "customer": email,
        "diners": diners,
        "datetime": datetime,
        "table": num_table
    }

    # Insert the document into the collection
    inserted_id = collectionOfBookings.insert_one(insert).inserted_id
    # Print the inserted document's ID
    print("Inserted document ID:", inserted_id)

    return response


if __name__ == '__main__':
    """
    from flask_cors import CORS
    import ssl

    context = ssl.SSLContext()
    context.load_cert_chain("/home/mariajesus/certificados/conversational_ugr_es.pem",
                            "/home/mariajesus/certificados/conversational_ugr_es.key")
    CORS(app)
    app.run(host='0.0.0.0', port=5050, ssl_context=context, debug=False)
    """

    app.run()
