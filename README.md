# TimeSheet_Application
<h2>Project Description</h2>
<p>This is a CRUD application that has been created using Python/PyQt and MySQL. The application was built to use a MySQL database as storage, however, for demonstration purposes I have refactored the database structure to be used with SQLite3. This application was created as a highly tailored solution for employees of a Kelowna based office to record their working hours between legal entities.</p>
<h2>How to Run</h2>
<ol>
<li>Clone this repo from master branch</li>
<li>Run "pip install -r requirements.txt" to install necessary packages</li>
<li>Run "TimeSheet.py"</li>
<li>Use username "TestUser" to login to application (the application does not require a password due to clients request)</li>
</ol>

<h2>How to Use</h2>
<ol>
  <li>The drop-down lists are meant to be filled out left to right (The data you see has been made up for this demonstration)</li>
  <li>Once all 3 (or 4) of drop-downs have been filled, input the hours worked on that task under the respective days column</li>
  <li>Once happy with time sheet, hit submit to push your data to the database (SQL Lite in this case)</li>
  <li>The progress bar on the right should now show some status</li>
  <li>You can also view your current weeks submisson by clicking the "Current Clock" button</li>
  <li>Admin users also have the ability to add users and update records</li>
</ol>
