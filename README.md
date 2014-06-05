ASG Website
===========

Management commands
-------------------
The following commands delete all existing members before adding the ones in the CSV files. Make sure the CSV files are complete lists.
- `./manage.py update_exec EXEC.csv` updates the list of Exec Board members on the Contact and Cabinet pages. `EXEC.csv` should be a CSV file without headers containing two columns: position, personal Northwestern email. This command creates positions as needed based on name, so make sure that consistent abbreviations e.g. 'Sustainability VP' instead of 'Sustainability Vice President' are used. This command also updates the order of the positions based on the order in the csv file.
- `./manage.py update_senators SENATORS.csv` updates the list of Senators on the Senators page. `SENATORS.csv` should be a CSV file without headers containing two columns: groups represented, personal Northwestern email
- `./manage.py update_committees COMMITTEE_MEMBERS.csv` first column is committee name, second column is the official Northwestern email of the the committee member. Make sure the committee names are consistent with the ones already on the website (and are capitalized correctly)


Troubleshooting
---------------
- If there are errors like `decoder zip not available`, try reinstalling Pillow with `pip install -I Pillow` after installing zlib-devel and libjpeg-devel with your package manager. 
