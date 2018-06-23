# Software Engineer Project -- Online Exam system (Backend)

This is the backend part of the Online Exam System based on django 2.0

If you want to use MySQL instead of the default database 'sqlite', uncomment line 82-91 in settings.py and run the following commands in MySQL.
```
CREATE DATABASE OnlineExamDB 
GRANT ALL on OnlineExamDB.* to Django
```

### Some Problems/Confusion
- No Login Authentification yet.
- In models, 'teacher' and 'course' fields are represented by an integer id.
- In models, the 'keypoints' field contains a single string rather than an array of strings?
- In models, the 'score' field is float rather than an integer?
- No Error Handling as defined in 'api' document yet. The server simply returns a 404 when encountering an error.
- In api, I assume that class QuestionForExam extends QuestionEntry, otherwise QuestionDetail will not contain 'id' field.