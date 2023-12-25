-- name: get_attend_infors
SELECT *
FROM (
    SELECT 
        a.id,
        a.student_id AS "studentId",
        a.check_in AS "timeCheckIn",
        a.check_out AS "timeCheckOut",
        a.status,
        a.note,
        a.create_at,
        s.name,
        s.phone,
        s.date_of_birth AS student_dob,
        s.gender AS student_gender,
        s.class_id
    FROM attendance a
    JOIN student s ON a.student_id = s.id
) AS subquery
WHERE 
    class_id = :class_id
    AND DATE(create_at) >= CURRENT_DATE; 



-- name: get_statistic
SELECT
    c.id AS "classId",
    c.class_name AS "className",
    g.grade_name As "grade",
    c.quantity,
    COALESCE(a.present_count, 0) AS present,
    COALESCE(a.absent_count, 0) AS "absenceWithoutPermission",
    COALESCE(a.late_count, 0) AS late,
    COALESCE(a.excused_absence_count, 0) AS "absenceWithPermission",
    t.id AS teacherId,
    t.username AS "homeroomTeacher"
FROM
    class c
LEFT JOIN
    (
        SELECT
            s.class_id,
            COUNT(CASE WHEN ar.status = 1 THEN 1 END) AS present_count,
            COUNT(CASE WHEN ar.status = 2 THEN 1 END) AS absent_count,
            COUNT(CASE WHEN ar.status = 3 THEN 1 END) AS late_count,
            COUNT(CASE WHEN ar.status = 4 THEN 1 END) AS excused_absence_count
        FROM
            attendance ar
        JOIN
            student s ON ar.student_id = s.id
        GROUP BY
            s.class_id
    ) a ON c.id = a.class_id
LEFT JOIN
    teacher t ON c.id = t.homeroom_class_id
LEFT JOIN
    grades g ON c.grade_id = g.id;




