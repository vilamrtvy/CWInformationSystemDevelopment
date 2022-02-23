SELECT pat_id, pat_name, pat_birthday, pat_passport, COUNT(dis_date) as count_dis, COUNT(rec_date) as count_rec
FROM Patient, History, Ward
WHERE pat_key = pat_id
AND ward_key = ward_id
AND doc_key = '$doc_id'
AND ward_id is not NULL
GROUP BY pat_id
ORDER BY pat_name