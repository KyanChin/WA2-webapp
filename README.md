# WA2-webapp
H2 computing WA2 Webapp 2023

# Inspiration
This project is inspired by my shooting CCA coach who uses different websites and apps to take note on our progress and reflections such as excel and whatsapp. And I wanted to make a webapp that has everything in a single place.

# What this project does:
This project is made for Shooting cca. It has features such as announcements, debreif, shooting CCA schedule, reflection and a plotter. 

# Why is this project useful:
This project will help shooting CCA have a more organised place for information as announcements, debreifs, schedule, relfection are in one website, instead of being sent to the whatsapp group chat. We can use the plotter to help us track our progress for per series(10 shots) in a competition or compare our many competition scores with each other and see our progress.

# How it's built 
This project is built using python flask and html and by linking an google sheets API to the python, I am able to display the google sheets in the html 

# How to use this webapp:
- Home Page
  In the home page of the webapp, users are able to see announcements made and we can delete or add new announcements by
  pressing the 'add/delete announcements' button. Pressing the button will lead to a page where existing announcements
  have a checkbox beside them and we are able to tick the checkbox and press the 'Delete' button to delete those existing
  announcements. Other than that, there is also a textbox for us to submit a new announcement and the announcement will
  be added after pressing the 'Add' button. After pressing either the 'Delete' or 'Submit' button, users will be lead
  back to the home page.
  Other than the announcement feature on the home page, here is also a Debrief section where users will be able to see
  the latest debrief by default and if users want to see all previous debriefs, they can press the show all button and
  this will show them all previous debriefs posted. To post a debrief, users can write in the text box and press the
  'Add' button to post the debrief. 

- Schedule Page
  In this page, users can see the schedule of upcoming CCA sessions and update the schedules by submitting a picture of the
  new schedule and uploading it. Only the lastest 2 of the schdules would be displayed e.g. February and March would be
  displayed while January would not if all 3 schedules are uploaded.

- Reflection Page
  In this page, users can choose their own reflection page by selecting their name and pressing the 'Select' button.
  After selecting the profile, users can see their previous reflections and upload new ones by typing into the textbox
  given and pressing the 'submit' button to post their reflections. To switch profiles, users can reselect the names and
  press the 'Select' button again to switch profiles.

- Plotter Page
  In this page, users are able to select to plot their overall perfomance over multiple competitons or their series
  performance within the performance (per 10 shots). After selecting their preferred choice, users can enter their scores
  and plot it by pressing the 'Submit' button. This will then show users a graph and they can see the general trend of
  their matches or within the match itself and improve upon it. Users can download or copy the graph if they are on their
  laptop or desktop by right click to save it somewhere else.

# Accomplishments 
I learnt how to use Google API and how to safely store them in github without having my private key comprimised but still having the users able to access my google sheets and edit it.

# What's next for the CCA webapp
I plan to improve on it such that I am able to add more students and remove students so that this app can accommodate other batches of shooters. Other than that, I feel that this app can be improved by having a database to store the student's previous scores so that they do not need to enter their scores repeatedly in the 'performance' choice to plot their improvements over time.
