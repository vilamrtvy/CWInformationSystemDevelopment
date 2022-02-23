SELECT bran_name, doc_name

FROM Doctor, Department

WHERE doc_id = '$doctor_id'
AND depart_key = dep_id;