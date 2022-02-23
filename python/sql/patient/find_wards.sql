SELECT ward_id, ward_cat, ward_number, ward_places, count(pat_key) as limited

FROM Ward LEFT JOIN History

ON ward_key = ward_id

WHERE bran_key = '$dep_key'

GROUP BY ward_id;