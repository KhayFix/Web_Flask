"""added author_published to news

Revision ID: 1580aa1f39e7
Revises: 1dc2e7bab0ac
Create Date: 2020-01-21 17:08:49.639868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1580aa1f39e7'
down_revision = '1dc2e7bab0ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('author_published', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'news', ['author_published'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'news', type_='unique')
    op.drop_column('news', 'author_published')
    # ### end Alembic commands ###
