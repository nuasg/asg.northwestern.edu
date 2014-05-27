ASG Website
===========

Management commands
-------------------
- `./manage.py update_exec EXEC.csv` 
- `./manage.py update_senators SENATORS.csv` 
- `./manage.py update_committees COMMITTEE_MEMBERS.csv` 


Troubleshooting
---------------
- If there are errors like `decoder zip not available`, try reinstalling Pillow with `pip install -I Pillow` after installing zlib-devel and libjpeg-devel with your package manager. 
