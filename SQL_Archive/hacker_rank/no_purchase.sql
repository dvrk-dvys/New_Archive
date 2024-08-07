SELECT
    ah.user_id,
    ah.username
FROM
    account_holders ah
LEFT JOIN
    purchases p ON ah.user_id = p.user_id
WHERE
    p.user_id IS NULL;