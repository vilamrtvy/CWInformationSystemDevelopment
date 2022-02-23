SELECT ROUND(AVG(
	(YEAR(CURRENT_DATE) - YEAR(pat_birthday)) -
    (DATE_FORMAT(CURRENT_DATE, '%m%d') < DATE_FORMAT(pat_birthday, '%m%d'))
)) AS age

FROM Patient, History, Doctor, Department

WHERE pat_id=pat_key
AND doc_key=doc_id
AND depart_key=dep_id
AND bran_name = '$bran_name'
