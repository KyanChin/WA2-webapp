from flask import Flask, render_template, request
import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)

def get_students():
    #file closes after with block 
    with open('students.txt', 'r') as file:
        students = file.read().split()
        for i in range(len(students)-1):
            students[i] = students[i][:-1]   
    return students

def file_content(filename):
    with open(f'{filename}.txt', 'r') as file:
        content = file.readlines()
    return content

def get_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def write_in_first_line_with_date(filename, contents):
    #file closes after with block 
    with open(f'{filename}.txt', 'r') as file:
        content = file.readlines()
    #file closes after with block 
    with open(f'{filename}.txt', 'w') as file:
        file.write(f'{get_date()}: \n{contents}\n')
        file.writelines(content)

def write_in_first_line_without_date(filename, contents):
    #file closes after with block 
    with open(f'{filename}.txt', 'r') as file:
        content = file.readlines()
    #file closes after with block 
    with open(f'{filename}.txt', 'w') as file:
        file.write(f'{contents}\n')
        file.writelines(content)

def seperate_list_by_dates(list_content):
    refined_list = []
    output_list = []
    for i in list_content:
        refined_list.append(i.rstrip(': \n'))
    for i in refined_list:
        try:
            datetime.datetime.strptime(i, '%Y-%m-%d')
            output_list.append(i + ': ')
        except ValueError:
            output_list[-1] = output_list[-1] + ' ' + i
            
    return output_list 

def sheet_edit(sheet_name, data, max_input):
    converter = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J'}
    # Open the Google Sheet
    sheet = client.open("Plotter").worksheet(sheet_name)  # Open the first sheet of the document
    #clear sheet row 1
    sheet.update('A1:J1',[['' for _ in range(max_input)]])
    #changing data to numeric 
    for i in range(len(data)):
        if not data[i].isdigit():
            return None
        data[i] = int(data[i])
    # Update the sheet
    sheet.update(f'A1:{converter[len(data)]}1', [data])
        
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        checkbox_values = request.form.getlist('deleted_announcement')
        if checkbox_values:
            delete_announcement = []
            for i in checkbox_values:
                delete_announcement.append(i.rstrip('\r\n')+'\n')
            
            remaining_annoucements = []
            for i in file_content('announcements'):
                if i not in delete_announcement:
                    remaining_annoucements.append(i)
                else:
                    delete_announcement.remove(i)
                    
            #file closes after with block
            with open('announcements.txt', 'w') as file:
                file.writelines(remaining_annoucements)

        add_announcement = request.form.get('announcement')
        if add_announcement:
            write_in_first_line_without_date('announcements', add_announcement)

        show = request.form.get('show')
        if show:
            return render_template('index.html', announcements=file_content('announcements'), debriefs=file_content('debrief'), students=get_students(), show=True)

        debrief = request.form.get('debrief')
        if debrief:
            write_in_first_line_with_date('debrief', debrief)
            
    return render_template('index.html', announcements=file_content('announcements'), debriefs=seperate_list_by_dates(file_content('debrief')), students=get_students(), show=False)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/reflection', methods=['GET', 'POST'])
def reflection():
    if request.method == 'POST':
        select_student = request.form.get('select_student')
        reflections = request.form.get('reflections')
        
        if select_student:
            select_student = select_student[0] + select_student[1:].lower()

        if reflections:
            write_in_first_line_with_date(select_student, reflections)
        
        if not os.path.isfile(f'{select_student}.txt'):
            #file closes after with block 
            with open(f'{select_student}.txt', 'w'):
                pass

        return render_template('reflection.html', select_student=select_student, students=get_students(), student_content=file_content(select_student))
    return render_template('reflection.html', students=get_students())

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name("./computing-wa2-webapp-4986adbaa8ce.json", scope)
# Authorize the client sheet 
client = gspread.authorize(creds)

@app.route('/plotter', methods=['GET', 'POST'])
def plotter():
    choice = None
    series = None
    scores = None
    sheet_url = None
    if request.method == 'POST':
        #Get choice of performance or 40series or 60 series
        choice = request.form.get('selection')
        #Set the labels for the scores
        if choice == '40series':
            series = ['1st', '2nd', '3rd', '4th']
        elif choice == '60series':
            series = ['1st', '2nd', '3rd', '4th', '5th', '6th']

        #Get competition scores and filter it 
        scores = request.form.get('scores')
        if scores:
            scores = scores.split(',')
            for i in range(len(scores)):
                scores[i] = scores[i].strip()
            if scores[-1] == '':
                scores = scores[:-1]
            if len(scores) > 10:
                scores = scores[-10:]
            sheet_edit('Performance', scores, 10)
            
        #Get 40 series scores
        scores = request.form.getlist('40scores')
        if scores:
           sheet_edit('40series', scores, 4)

        #Get 60 series scores
        scores = request.form.getlist('60scores')
        if scores:
           sheet_edit('60series', scores, 6)

        #Get url 
        sheet_url = request.form.get('url')        
    return render_template('plotter.html', choice=choice, series=series, sheet_url=sheet_url)


@app.route('/announcement', methods=['GET', 'POST'])
def announcements():
    return render_template('announcement.html', announcements=file_content('announcements'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
