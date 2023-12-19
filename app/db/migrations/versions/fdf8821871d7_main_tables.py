"""main tables

Revision ID: fdf8821871d7
Revises:
Create Date: 2019-09-22 01:36:44.791880

"""
from typing import Tuple

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

revision = "fdf8821871d7"
down_revision = None
branch_labels = None
depends_on = None

def create_updated_at_trigger() -> None:
    op.execute(
        """
    CREATE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS
    $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """
    )

def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.current_timestamp(),
        ),
    )

def create_account_table() -> None:
    op.create_table(
        "account",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("hashed_password", sa.Text),
        sa.Column("bio", sa.Text, nullable=False, server_default=""),
        sa.Column("image", sa.Text),
        sa.Column("role", sa.Integer),
        sa.Column(
            "teacher_id",
            sa.Integer,
            sa.ForeignKey("teacher.id", ondelete="CASCADE"),
            nullable=False,
        ),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_account_modtime
            BEFORE UPDATE
            ON account
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_teacher_table() -> None:
    op.create_table(
        "teacher",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text),
        sa.Column("phone", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("quantity", sa.Integer, nullable=True),
        sa.Column(
            "homeroom_class_id",
            sa.Integer,
            sa.ForeignKey("class.id", ondelete="CASCADE"),
            nullable=True,
        ),
        *timestamps(),
    )

def create_student_table() -> None :
        op.create_table(
        "student",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, unique=False, nullable=False, index=True),
        sa.Column(
            "class_id",
            sa.Integer,
            sa.ForeignKey("class.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("date_of_birth",sa.Text),
        sa.Column("gender",sa.Integer),
        sa.Column("address",sa.Text),
        sa.Column("phone",sa.Text)
        *timestamps(),
    )
        
def create_class_table() -> None:
    op.create_table(
        "class",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("class_name", sa.Text, unique=True, nullable=False, index=True),
        sa.Column(
            "grade_id",
            sa.Integer,
            sa.ForeignKey("grades.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("quantity", sa.Integer),
        *timestamps(),
    )

def create_grade_table() -> None:
    op.create_table(
        "grades",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("grade_name", sa.Integer, unique=True, nullable=False, index=True),
        *timestamps(),
    )

def upgrade() -> None:
    create_updated_at_trigger()
    create_grade_table()
    create_class_table()
    create_student_table()
    create_teacher_table()
    create_account_table()

def downgrade() -> None:
    op.drop_table("account")
    op.drop_table("teacher")
    op.drop_table("student")
    op.drop_table("class")
    op.drop_table("grades")
    op.execute("DROP FUNCTION update_updated_at_column")
