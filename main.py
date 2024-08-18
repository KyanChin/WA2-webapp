from flask import Flask, render_template, request
import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


app = Flask(__name__)

#Get students from the text file
def get_students():
    #file closes after with block 
    with open('students.txt', 'r') as file:
        students = file.read().split()
        for i in range(len(students)-1):
            students[i] = students[i][:-1]   
    return students

#Read content of files
def file_content(filename):
    with open(f'{filename}.txt', 'r') as file:
        content = file.readlines()
    return content

#Get today's date 
def get_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

#Write content into files with date infront of it
def write_in_first_line_with_date(filename, contents):
    #file closes after with block 
    with open(f'{filename}.txt', 'r') as file:
        content = file.readlines()
    #file closes after with block 
    with open(f'{filename}.txt', 'w') as file:
        file.write(f'{get_date()}: \n{contents}\n')
        file.writelines(content)

#Write content into files without date
def write_in_first_line_without_date(filename, contents):
    #file closes after with block 
    with open(f'{filename}.txt', 'r') as file:
        content = file.readlines()
    #file closes after with block 
    with open(f'{filename}.txt', 'w') as file:
        file.write(f'{contents}\n')
        file.writelines(content)

#Format the txt files to be blank from the start (Github requires a '\n' at first)
def blank_file(filename):
    if file_content(filename) == ['\n']:
        #file closes after with block 
        with open(f'{filename}.txt', 'w') as file:
            file.write('')

#Seperate the list by dates
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
            if output_list:
                output_list[-1] = output_list[-1] + ' ' + i
    return output_list 

#Edit the google sheets 
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

#Home Page
@app.route('/', methods=['GET', 'POST'])
def home():
    #To avoid having a blank announcement or debrief
    blank_file('announcements')
    blank_file('debrief')
    
    if request.method == 'POST':
        #Get the ticked (going to be deleted) announcements from the form 'add/delete announcements'
        checkbox_values = request.form.getlist('deleted_announcement')
        #Format the checkbox values so that it is "cleaner"
        if checkbox_values:
            delete_announcement = []
            for i in checkbox_values:
                delete_announcement.append(i.rstrip('\r\n')+'\n')
            #Find the remaining announcements by not appending the checked ones
            remaining_annoucements = []
            for i in file_content('announcements'):
                if i not in delete_announcement:
                    remaining_annoucements.append(i)
                else:
                    #for duplicates
                    delete_announcement.remove(i)

            #Write the remaining announcements into the file
            #File closes after with block
            with open('announcements.txt', 'w') as file:
                file.writelines(remaining_annoucements)

        #Get the new announcement entered
        add_announcement = request.form.get('announcement')
        if add_announcement:
            #Add the announcment to the file 'announcement.txt' without the date
            write_in_first_line_without_date('announcements', add_announcement)

        #Get the response from the button 'Show more'
        show = request.form.get('show')
        if show: #if the button is clicked
            return render_template('index.html', announcements=file_content('announcements'), debriefs=file_content('debrief'), students=get_students(), show=True)

        #Get the new debrief entered
        debrief = request.form.get('debrief')
        if debrief:
            #Write the new debrief into file 'debrief.txt' without date
            write_in_first_line_with_date('debrief', debrief)

    #'Show more' button is not clicked
    return render_template('index.html', announcements=file_content('announcements'), debriefs=seperate_list_by_dates(file_content('debrief')), students=get_students(), show=False)

#Schedule Page
@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    #Allocating months to a number to get the order of months
    month_number = {'Jan_Feb': 1, 'Feb_March' : 2, 'March_April': 3, 'April_May': 4, 'May_June': 5, 'June_July': 6, 'July_Aug': 7, 'Aug_Sep': 8, 'Sep_Oct': 9, 'Oct_Nov': 10, 'Nov_Dec': 11, 'Dec_Jan': 12}
    
    #Declaring the folder to store the images
    UPLOAD_FOLDER = 'static'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if request.method == 'POST':
        #Get the month entered and the schedule image uploaded 
        month = request.form.get('month')
        file = request.files['schedule']
        #if both month and file exist
        if file and month:
            #Rename the file name into a certain format to be used later using the dictionary to store the order as the first index of the image file name
            filename = f"{month_number[month]}_{month} Schedule.png"
            #Store the image into the designated folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            #Delete outdated schedule pictures (Save the lastest 2)
            files = os.listdir(app.config['UPLOAD_FOLDER'])
            if len(files) > 3:
                remove_schedule = None
                for file in files:
                    #Exclude the style.css file
                    if file != 'style.css':
                        #Remove the oldest image by by comparing the order of the months
                        if remove_schedule is None or int(file[0]) < int(remove_schedule[0]):
                            remove_schedule = file      
                #remove the oldest image
                os.remove(f'static/{remove_schedule}')

    #Find the files in the static folder 
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    schedules = []
    for file in files:
        if file != 'style.css':
            #Append all the image files into schedules list 
            schedules.append(file)
    #Return the schedule page with the list of schedules
    return render_template('schedule.html', schedules=schedules)

#Reflection Page
@app.route('/reflection', methods=['GET', 'POST'])
def reflection():
    if request.method == 'POST':
        #Find the selected student and their reflections
        select_student = request.form.get('select_student')
        reflections = request.form.get('reflections')

        #formatting the selected student's name
        if select_student:
            select_student = select_student[0] + select_student[1:].lower()

        #Create a new text file for the student if it doesn't exist
        if not os.path.isfile(f'{select_student}.txt'):
            #file closes after with block 
            with open(f'{select_student}.txt', 'w'):
                pass

        #Write the student's reflection in their respective text files
        if reflections:
            write_in_first_line_with_date(select_student, reflections)

        #Return reflection page, the selected student, students and their reflections
        return render_template('reflection.html', select_student=select_student, students=get_students(), student_content=file_content(select_student))
    #Return reflection page, all students in the student.txt file
    return render_template('reflection.html', students=get_students())

#**SETTING UP GOOGLE API**

# Load the JSON credentials from the environment variable
creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# Parse the JSON string
creds_dict = json.loads(creds_json)
# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# Create the credentials object from the dictionary
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
# Authorize the client
client = gspread.authorize(creds)

#Plotter Page
@app.route('/plotter', methods=['GET', 'POST'])
def plotter():
    choice = None
    series = None
    scores = None
    sheet_url = None
    if request.method == 'POST':
        #Get choice of performance or 40series or 60 series
        choice = request.form.get('selection')
        #Set the labels for the scores to be added into the sheet
        if choice == '40series':
            series = ['1st', '2nd', '3rd', '4th']
        elif choice == '60series':
            series = ['1st', '2nd', '3rd', '4th', '5th', '6th']

        #Get competition scores and filter and 'clean' the scores so that it has only numbers
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
            #Edit the scores
           sheet_edit('40series', scores, 4)

        #Get 60 series scores
        scores = request.form.getlist('60scores')
        if scores:
            #Edit the scores
           sheet_edit('60series', scores, 6)

        #Get url to know what sheet to display
        sheet_url = request.form.get('url')        
    return render_template('plotter.html', choice=choice, series=series, sheet_url=sheet_url)

#Announcement Page (Not shown in the navbar)
@app.route('/announcement', methods=['GET', 'POST'])
def announcements():
    #Return the existing announcements so that users can check them if they want to delete it
    return render_template('announcement.html', announcements=file_content('announcements'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
