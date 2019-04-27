## While adding new app
- If app requires maintenance then do following.
  - Add app_name in `MAINTENANCE_MODE_APP` of `agrisync/settings.py`
  - Add new field `<APP_NAME>_APP_MAINTENANCE` in `agrisync/settings.py` , `.env.example` and `.env`
  - Add `urls.py` in that app with `app_name=<app_name>` (which is included in `MAINTENANCE_MODE_APP`)
  - Add `kwargs={'MAINTENANCE': '<APP_NAME>_APP_MAINTENANCE'}` in `url(...)` of `agrisync/urls.py`
  
## Before sending Pull Request
- Run `flake8 .` command
- Run `python3 manage.py test` command

## Some Guidelines
- Add comments for any class or method.
