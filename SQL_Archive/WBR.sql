WITH ap AS (

SELECT 

job_id,
icims_id,
person_id,
--status,
MIN(convert_timezone('US/Pacific',cast((TIMESTAMP 'epoch' + CAST(icims_updated_timestamp AS BIGINT)/1000 * INTERVAL '1 Second') as timestamp))) as application_date

FROM

ads.worksteps
GROUP BY job_id, icims_id, person_id
),

status as(
 
SELECT 

job_id,
icims_id,
person_id,
status

FROM

ads.worksteps
GROUP BY job_id, icims_id, person_id, status
)

select distinct 
ap.application_date, 
DATEDIFF (d , offer.requisition_final_approval_date::timestamp,offer_accepted_date::timestamp) as TTF,

hc.job_level_name as recruiter_level,
offer.*,
reqs.current_job_state as reqscurrentjobstate,
reportingdays.calendar_day,
team.team_flag 


from masterhr.offer_accepts offer
inner join opsdw.ops_ta_team_wk team on team.emplid = offer.recruiter_employee_id
inner join masterhr.requisition reqs on reqs.job_icims_id = offer.job_icims_id
left join hrmetrics.o_reporting_days reportingdays ON reportingdays.calendar_day = offer.offer_accepted_date

inner join ap on ap.job_id = offer.job_icims_id and ap.person_id = offer.candidate_icims_id 
left join status on status.job_id = ap.job_id and status.person_id = ap.person_id
left join lookup.icims_recruiting_states s on status.status=s.icims_status 
left join masterhr.employee_hc hc on hc.emplid = offer.recruiter_employee_id

WHERE 
offer.enter_state_time::date between team.wk_begin_dt AND team.wk_end_dt
AND offer.offer_accepted_count = 1
AND reqs.current_transaction_flag = 'Y'
AND team.team_flag IN ('EU', 'ADECCO Recruiters')
AND reqs.country NOT IN ('USA', 'CAN', 'MEX')
AND team.team_flag = 'ADECCO Recruiters'
--AND offer.candidate_icims_id = 26978523
--AND offer.job_icims_id = 1116888
