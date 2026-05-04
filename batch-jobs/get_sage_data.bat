@echo off
cmd /k "cd /d C:\projects\leave-system\Scripts & activate & cd /d C:\inetpub\wwwroot\leave-system & python manage.py run_sage_sync"
exit 0