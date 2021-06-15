"""empty message

Revision ID: c5988fdbc98a
Revises: f35a4d2ee631
Create Date: 2021-06-15 18:33:42.016000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5988fdbc98a'
down_revision = 'f35a4d2ee631'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('issues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('desc', sa.String(length=200), nullable=True),
    sa.Column('status', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column(u'employees', sa.Column('issue_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'employees', 'issues', ['issue_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'employees', type_='foreignkey')
    op.drop_column(u'employees', 'issue_id')
    op.drop_table('issues')
    # ### end Alembic commands ###
