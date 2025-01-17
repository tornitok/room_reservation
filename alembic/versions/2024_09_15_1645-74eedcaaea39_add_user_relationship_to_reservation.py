"""Add user relationship to Reservation

Revision ID: 74eedcaaea39
Revises: 6e891922f79a
Create Date: 2024-09-15 16:45:08.261462

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '74eedcaaea39'
down_revision = '6e891922f79a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_reservation_user_id_user', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_constraint('fk_reservation_user_id_user', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
