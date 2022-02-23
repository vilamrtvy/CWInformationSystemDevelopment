SELECT pat_name, pat_birthday, rec_date, rec_diag, doc_name

FROM patient, history, department, ward, doctor

WHERE pat_key = pat_id
AND ward_key = ward_id
AND bran_key = dep_id
AND doc_key = doc_id
AND dep_id = '$id'
AND dis_date IS NULL

ORDER BY pat_name;