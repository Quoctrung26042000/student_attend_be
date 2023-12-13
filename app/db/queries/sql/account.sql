-- name: get_account_by_email^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       bio,
       image,
       role,
       created_at,
       updated_at
FROM account
WHERE email = :email
LIMIT 1;


-- name: get_account_by_username^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       bio,
       image,
       role,
       created_at,
       updated_at
FROM account
WHERE username = :username
LIMIT 1;


-- name: create-new-account<!
INSERT INTO account (username, email, salt, hashed_password, role)
VALUES (:username, :email, :salt, :hashed_password, :role)
RETURNING
    id, created_at, updated_at;


-- name: update-user-by-username<!
UPDATE
    users
SET username        = :new_username,
    email           = :new_email,
    salt            = :new_salt,
    hashed_password = :new_password,
    bio             = :new_bio,
    image           = :new_image
WHERE username = :username
RETURNING
    updated_at;
