"""empty message

Revision ID: 67def15c086d
Revises: None
Create Date: 2016-07-05 14:11:10.563000

"""

# revision identifiers, used by Alembic.
revision = '67def15c086d'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('body_html', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_timestamp'), 'comments', ['timestamp'], unique=False)
    op.create_foreign_key(None, 'follows', 'users', ['followed_id'], ['id'])
    op.create_foreign_key(None, 'follows', 'users', ['follower_id'], ['id'])
    op.create_foreign_key(None, 'posts', 'users', ['author_id'], ['id'])
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_constraint(None, 'follows', type_='foreignkey')
    op.drop_constraint(None, 'follows', type_='foreignkey')
    op.drop_index(op.f('ix_comments_timestamp'), table_name='comments')
    op.drop_table('comments')
    ### end Alembic commands ###