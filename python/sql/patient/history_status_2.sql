SELECT bran_name, doc_name, ward_number

FROM Doctor, Department, Ward

WHERE doc_id = '$doctor_id'
AND ward_id = '$ward_id'
AND depart_key = dep_id
AND bran_key = dep_id;