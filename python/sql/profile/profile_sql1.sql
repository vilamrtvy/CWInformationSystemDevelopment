SELECT pat_name, pat_birthday, rec_date, rec_diag, dis_date, doc_name
FROM Patient, History, Doctor, Department, Ward
WHERE pat_key = pat_id
AND doc_key = doc_id
AND ward_key = ward_id
AND bran_key = dep_id
AND bran_name = '$bran_name'
ORDER BY rec_date
