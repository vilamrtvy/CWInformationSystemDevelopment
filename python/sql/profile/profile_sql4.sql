SELECT pat_name, pat_passport, rec_date, rec_diag, dis_date, doc_name, bran_name

FROM Patient, History, Doctor, Department, Ward

WHERE pat_id=pat_key
AND ward_key=ward_id
AND doc_key=doc_id
AND depart_key=dep_id
AND dis_date >= DATE_ADD(CURDATE(), INTERVAL '-$days' DAY);
