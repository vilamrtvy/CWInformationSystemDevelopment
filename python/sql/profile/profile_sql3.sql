SELECT doc_name, doc_recr, doc_dism, bran_name

FROM hospital.doctor left join hospital.department

ON depart_key = dep_id

WHERE YEAR(doc_recr) = '$year'
