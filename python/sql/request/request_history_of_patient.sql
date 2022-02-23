SELECT his_id, rec_date, rec_diag, dis_date, bran_name, ward_number, doc_name
FROM Patient, History, Department, Doctor, Ward
WHERE doc_key = doc_id
AND pat_key = pat_id
AND ward_key = ward_id
AND bran_key = dep_id
AND pat_id = '$pat_id'

ORDER BY rec_date