# DEBUG - 10
- Detailed information, typically of interest only when diagnosing problems.
- Information that is diagnostically helpful to people more than just developers (IT, sysadmins, etc.).

# INFO - 20
- Confirmation that things are working as expected. 
- Generally useful information to log (service start/stop, configuration assumptions, etc). Info I want to always have available but usually don't care about under normal circumstances. This is my out-of-the-box config level.

# WARNING - 30
- An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
- Anything that can potentially cause application oddities, but for which I am automatically recovering. (Such as switching from a primary to backup server, retrying an operation, missing secondary data, etc.)

# ERROR - 40
- Due to a more serious problem, the software has not been able to perform some function.
- Any error which is fatal to the operation, but not the service or application (can't open a required file, missing data, etc.). These errors will force user (administrator, or direct user) intervention. These are usually reserved (in my apps) for incorrect connection strings, missing services, etc. 

# CRITICAL - 50
- A serious error, indicating that the program itself may be unable to continue running.
- Any error that is forcing a shutdown of the service or application to prevent data loss (or further data loss). I reserve these only for the most heinous errors and situations where there is guaranteed to have been data corruption or loss.