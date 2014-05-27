ASG Website
===========

Management commands
-------------------
- `./manage.py update_exec EXEC.csv` updates the list of Exec Board members on the Contact and Cabinet pages. `EXEC.csv` should be a CSV file without headers containing two columns: position, personal Northwestern email. This command creates positions as needed based on name, so make sure that consistent abbreviations e.g. 'Sustainability VP' instead of 'Sustainability Vice President' are used. This command also updates the order of the positions based on the order in the csv file.
- `./manage.py update_senators SENATORS.csv` updates the list of Senators on the Senators page. `SENATORS.csv` should be a CSV file without headers containing two columns: groups represented, personal Northwestern email
- `./manage.py update_committees COMMITTEE_MEMBERS.csv` 


Troubleshooting
---------------
- If there are errors like `decoder zip not available`, try reinstalling Pillow with `pip install -I Pillow` after installing zlib-devel and libjpeg-devel with your package manager. 
