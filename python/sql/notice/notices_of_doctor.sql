SELECT pat_id, pat_name, pat_birthday, pat_passport, pat_address, rec_date
FROM History, Patient
WHERE doc_key = '$id'
AND pat_key = pat_id
AND ward_key is NULL