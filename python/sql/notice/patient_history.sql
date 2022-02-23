SELECT his_id, rec_date, bran_name, doc_name

FROM History, Department, Doctor

WHERE pat_key = '$pat_id'
AND doc_key = '$doc_id'
AND doc_key = doc_id
AND depart_key = dep_id
AND ward_key is NULL
