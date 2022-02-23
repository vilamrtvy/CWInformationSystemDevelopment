SELECT *

FROM History

WHERE pat_key = '$id'
AND doc_key = '$doctor'
AND rec_date = '$date'
AND ward_key is NULL