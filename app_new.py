
from flask import render_template,request, Flask

import psycopg2

app = Flask(__name__)


def save_db(category, name, total_employees, employees_with_npl, nationality,
            email, phone, sector, facility_to_submit, facility_to_make,
            facility_to_monitor, electronic_calibration,facility_to_check, challenges, comments):

    try:
        # making connection to database
        conn = psycopg2.connect(
            dbname = 'hiteshi_db',
            user= 'postgres',
            password = 8383,
            host = 'localhost',
            port = '5432'
        )
        print("connection to the database hiteshi_db is successful")
 
        cursor = conn.cursor()
 
        # insert_query = """
        #     INSERT INTO npl_new_db (
        #          category, name, total_employees, employees_with_npl, nationality,
        #          email, phone, sector, facility_to_submit, facility_to_make,
        #          facility_to_monitor, electronic_calibration,facility_to_check, challenges, comments, submit_date
        # ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        insert_query = """
            INSERT INTO npl_new_db VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        
        values = (category, name, total_employees, employees_with_npl, nationality,email, phone, sector, facility_to_submit, facility_to_make, facility_to_monitor, electronic_calibration,facility_to_check, challenges, comments )
        
 
        cursor.execute(insert_query,values)
 
        conn.commit()
        cursor.close()
        conn.close()
 
        print("Record saved in npl_new_db")
 
    except Exception as error:
        print("Connection aborted")
        print(error)


@app.route("/submit", methods=['POST'])
def submit():
    try:
        category = request.form.get("category")
        if category == "ANY":
            other_category = request.form.get("other_category")
            if other_category:
                category = other_category

        name = request.form.get("name")
        total_employees = int(request.form.get("total_employees"))
        employees_with_npl = int(request.form.get("employees_with_npl"))
        nationality = request.form.get("nationality")
        email = request.form.get("email")
        phone = request.form.get("phone")
        sector = request.form.get("sector")
        sector = request.form.get("sector")
        if sector == "Other":
            other_sector = request.form.get("other_sector")
            if other_sector:
                category = other_sector

        facility_to_submit= request.form.get("facility_to_submit")
        facility_to_make= request.form.get("facility_to_make")
        facility_to_monitor = request.form.get("facility_to_monitor")
        electronic_calibration = request.form.get("electronic_calibration")
        facility_to_check = request.form.get("facility_to_check")
        challenges = request.form.get("challanges")
        comments = request.form.get("any")
        # submit_date = datetime.now().strftime("%Y-%m-%d")
 
        save_db(
            category, name, total_employees, employees_with_npl, nationality,
            email, phone, sector, facility_to_submit, facility_to_make,
            facility_to_monitor, electronic_calibration,facility_to_check, challenges, comments
        )

        return render_template('response.html')

    except Exception as e:
        print("Error:", e)
        return f"Error while submitting: {e}"


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)      
