/*
Enter your query here.
*/
with base as (
    select 
        s.ID,
        s.Name,
        p.salary,
        f.Friend_ID,
        fn.name as friend_name,
        fp.salary AS friend_salary
    from students as s
        LEFT JOIN friends as f on s.ID = f.ID
        LEFT JOIN students AS fn on f.Friend_ID = fn.ID
        LEFT JOIN packages as p on s.ID = p.ID
        LEFT JOIN packages as fp on f.Friend_ID = fp.ID
    where friend_salary > salary


)

select
    name
from base
order by friend_salary asc
    

/*
Write a query to output F.Friend_IDthe names of those students whose best friends got offered a higher salary than them.*/