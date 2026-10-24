# Hospitell

Healthcare Management and Booking Platform built with Flask, SQLAlchemy, and Machine Learning.

## Database Note (Important)
If you have an existing or older MySQL database from a previous version of Hospitell, **you must drop and recreate it** before running the application:
```sql
DROP DATABASE `fit-o-sphere`;
```
Then run the setup script:
```powershell
python setup_db.py
```
*Reason:* New schema columns and models (e.g. `Rating.driver_id`, `User.oauth_provider`, `User.oauth_id`, `AmbulanceDriver`) were added to the ORM schema.

 
