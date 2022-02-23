SELECT pat_id, pat_name, pat_passport, pat_birthday, pat_address, (COUNT(rec_date) - COUNT(dis_date)) as sum_index

FROM Patient LEFT JOIN History

ON pat_id = pat_key

WHERE pat_name LIKE '$surname% $name%'

GROUP BY pat_id