SELECT ward_id, count(pat_key) as amount

FROM Ward LEFT JOIN History

ON ward_key = ward_id

WHERE bran_key = '$dep_key'
AND dis_date is not NULL

GROUP BY ward_id