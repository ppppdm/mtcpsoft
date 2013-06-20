@echo off
copy /y hb_service\*.py release\hb_service\
copy /y hb_service\*.ini release\hb_service\
copy /y hb_service\*.conf release\hb_service\

copy /y imgInfoGeter\*.py release\imgInfoGeter\
copy /y imgInfoGeter\*.ini release\imgInfoGeter\
copy /y imgInfoGeter\*.conf release\imgInfoGeter\

pause