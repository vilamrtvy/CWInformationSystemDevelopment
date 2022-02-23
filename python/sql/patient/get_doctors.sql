SELECT doc_id, doc_name

FROM Doctor, Department

WHERE depart_key = dep_id
AND bran_name = '$depart_name';