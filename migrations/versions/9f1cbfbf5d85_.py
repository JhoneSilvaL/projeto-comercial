"""empty message

Revision ID: 9f1cbfbf5d85
Revises: c1a1944af05d
Create Date: 2024-09-19 05:39:21.262138

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9f1cbfbf5d85'
down_revision = 'c1a1944af05d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produtos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('imagem', sa.String(length=100), nullable=True))
        batch_op.drop_column('estado')
        batch_op.drop_column('cidade')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produtos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cidade', mysql.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('estado', mysql.VARCHAR(length=100), nullable=False))
        batch_op.drop_column('imagem')

    # ### end Alembic commands ###
