SELECT doc_id, login, doc_name, post, gender, depart_key, bran_name
FROM Doctor, Department
WHERE login = '$login'
AND password = '$password'
AND depart_key = dep_id;