-- name: get_account_by_email^
SELECT
    a.id,
    a.username,
    a.email,
    a.salt,
    a.hashed_password,
    a.role,
    a.teacher_id,
    a.created_at,
    a.updated_at,
    t.username AS "teacherName",
    t.homeroom_class_id As "classId",
    c.class_name as "className"
FROM
    account a
    LEFT JOIN teacher t ON a.teacher_id = t.id
    LEFT JOIN class c on t.homeroom_class_id = c.id
WHERE
    a.email = :email
LIMIT
    1;

-- name: get_account_by_username^
SELECT
    a.id,
    a.username,
    a.email,
    a.salt,
    a.hashed_password,
    a.role,
    a.teacher_id,
    a.created_at,
    a.updated_at,
    t.username AS "teacherName",
    t.homeroom_class_id As "classId",
    c.class_name as "className"
FROM
    account a
    LEFT JOIN teacher t ON a.teacher_id = t.id
    LEFT JOIN class c On t.homeroom_class_id = c.id
WHERE
    a.username = :username
LIMIT
    1;

-- name: create-new-account<!
INSERT INTO
    account (
        username,
        email,
        salt,
        hashed_password,
        role,
        teacher_id
    )
VALUES
    (
        :username,
        :email,
        :salt,
        :hashed_password,
        :role,
        CASE
            WHEN :role = 0 THEN NULL
            ELSE CAST(:teacher_id AS INTEGER)
        END
    ) RETURNING id,
    created_at,
    updated_at;

-- name: update-user-by-username<!
UPDATE
    users
SET
    username = :new_username,
    email = :new_email,
    salt = :new_salt,
    hashed_password = :new_password,
    bio = :new_bio,
    image = :new_image
WHERE
    username = :username RETURNING updated_at;

--name : teacher_unassigned_account
SELECT
    id,
    username
FROM
    teacher
WHERE
    id NOT IN (
        SELECT
            t.id
        FROM
            teacher AS t
            JOIN account AS a ON t.id = a.teacher_id
    ) --name : get_accounts
SELECT
    a.id,
    -- a.username as "userName",
    a.email as "email",
    a.role,
    a.teacher_id as "teacherId",
    t.username as "nameTeacher"
FROM
    account as a
    LEFT JOIN teacher as t on t.id = a.teacher_id -- name : delete_account_by_id
DELETE FROM
    account
WHERE
    id = :id RETURNING id;