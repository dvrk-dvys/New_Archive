/*
Enter your query here.
*/
WITH grades AS (
    SELECT
        s.*,
        g.grade
    FROM Students s
    LEFT JOIN grades g ON s.marks >= g.min_mark AND s.marks <= g.max_mark
)

SELECT
CASE WHEN grade < 8 THEN Null ELSE name END AS name,
grade,
marks as mark
FROM grades
ORDER BY
        grade desc,
        CASE WHEN grade < 8 THEN grade END DESC,
        CASE WHEN grade >= 8 THEN name END ASC;


/*
#name, grade, mark
#no names for any one lower than 8 , make it null, ascending order by grade
# if 8 and above descending order by grade name alphabetically
*/
