SELECT pat_name, pat_birthday, rec_date, rec_diag, doc_name

FROM patient, history, department, doctor

WHERE pat_key = pat_id
AND depart_key = dep_id
AND doc_key = doc_id
AND dis_date IS NULL

ORDER BY rec_date