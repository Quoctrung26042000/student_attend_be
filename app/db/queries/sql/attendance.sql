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
        a.create_at ,
        s.name,
        s.phone,
        s.date_of_birth AS student_dob,
        s.gender AS student_gender,
        s.class_id,
        c.class_name As "className",
        c.grade_id
    FROM attendance a
    JOIN student s ON a.student_id = s.id
    JOIN class c ON s.class_id = c.id
) AS subquery
WHERE 
    class_id = :class_id
    AND DATE(create_at) >= CURRENT_DATE;


-- name: get_statistic
SELECT
    c.id AS "classId",
    c.id AS "id",
    c.class_name AS "className",
    g.grade_name AS "grade",
    c.grade_id As "gradeId",
    c.quantity,
    COALESCE(a.present_count, 0) AS present,
    COALESCE(a.absent_count, 0) AS "absenceWithoutPermission",
    COALESCE(a.late_count, 0) AS late,
    COALESCE(a.excused_absence_count, 0) AS "absenceWithPermission",
    t.id AS teacherId,
    t.username AS "homeroomTeacher"
FROM
    class c
INNER JOIN
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
        WHERE 
            DATE(ar.create_at) = CURRENT_DATE
        GROUP BY
            s.class_id
    ) a ON c.id = a.class_id
INNER JOIN
    teacher t ON c.id = t.homeroom_class_id
INNER JOIN
    grades g ON c.grade_id = g.id;





--name : get_statistic_search
SELECT
    c.id AS "id",
    c.class_name AS "className",
    g.grade_name AS "grade",
    c.grade_id AS "gradeId",
    c.quantity,
    COALESCE(a.present_count, 0) AS present,
    COALESCE(a.absent_count, 0) AS "absenceWithoutPermission",
    COALESCE(a.late_count, 0) AS late,
    COALESCE(a.excused_absence_count, 0) AS "absenceWithPermission",
    t.id AS teacherId,
    t.username AS "homeroomTeacher",
    t.homeroom_class_id As "classId"
FROM
    class c
INNER JOIN
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
        WHERE 
            DATE(ar.create_at) >= :from_date AND DATE(ar.create_at) <= :to_date
        GROUP BY
            s.class_id
    ) a ON c.id = a.class_id
INNER JOIN
    teacher t ON c.id = t.homeroom_class_id
INNER JOIN
    grades g ON c.grade_id = g.id
-- WHERE 
--     c.grade_id = :grade_id AND c.id = :class_id;


--name: search_statistic_detail
SELECT
    subquery.student_id As "studentId",
    subquery.name,
    subquery.phone,
    subquery.gender,
    subquery.class_id,
    subquery.grade_id,
    subquery.address,
    subquery.class_name AS "className",
    COUNT(CASE WHEN subquery.status = 1 THEN 1 END) AS "present",
    COUNT(CASE WHEN subquery.status = 2 THEN 1 END) AS "absenceWithoutPermission",
    COUNT(CASE WHEN subquery.status = 3 THEN 1 END) AS "late",
    COUNT(CASE WHEN subquery.status = 4 THEN 1 END) AS "absenceWithPermission"
FROM (
    SELECT 
        a.id,
        a.student_id ,
        a.status,
        a.create_at,
        s.name,
        s.phone,
        s.date_of_birth ,
        s.gender ,
        s.class_id,
        s.address,
        c.class_name,
        c.grade_id
    FROM attendance a
    JOIN student s ON a.student_id = s.id
    JOIN class c ON s.class_id = c.id
) AS subquery
WHERE 
    subquery.class_id = :class_id
    AND DATE(subquery.create_at) >= :from_date
    AND DATE(subquery.create_at) <= :to_date

GROUP BY
    subquery.student_id,
    subquery.name,
    subquery.phone,
    subquery.gender,
    subquery.class_id,
    subquery.grade_id,
    subquery.address,
    subquery.class_name


--name: search_attend_student_detail
SELECT 
    a.note,
    DATE(a.create_at) AS "day",
    SUBSTRING(a.check_in::text, 12, 8) AS "timeCheckIn",
    SUBSTRING(a.check_out::text, 12, 8) AS "timeCheckOut",
    a.status,
    s.name As "nameStudent"
FROM 
    attendance a
JOIN 
    student s ON a.student_id = s.id
WHERE 
    a.student_id = :student_id
    AND DATE(a.create_at) >= :from_date
	AND DATE(a.create_at) <= :to_date;

--name:update_attendance_student<!
UPDATE attendance
SET status = :status,
    note = :note
WHERE 
id = :attendance_id
RETURNING id, create_at, update_at;



