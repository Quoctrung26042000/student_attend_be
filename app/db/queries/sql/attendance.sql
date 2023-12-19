-- name: get_attend_infors
SELECT *
FROM (
    SELECT a.id AS attendance_id,
           a.student_id,
           a.check_in,
           a.check_out,
           a.status,
           a.note,
           s.name AS student_name,
           s.date_of_birth AS student_dob,
           s.gender AS student_gender,
           s.class_id
    FROM attendance a
    JOIN student s ON a.student_id = s.id
) AS subquery
WHERE class_id = :class_id;
