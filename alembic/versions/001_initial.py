"""Initial migration - Create all CMS, News, and Assets tables

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all database tables."""
    
    # =========================================================================
    # CMS Tables - Single-row configuration tables
    # =========================================================================
    
    # Site Branding
    op.create_table('cms_site_branding',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('tagline', sa.String(length=500), nullable=True),
        sa.Column('logo_image_path', sa.String(length=500), nullable=True),
        sa.Column('logo_white_image_path', sa.String(length=500), nullable=True),
        sa.Column('favicon_path', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Header Config
    op.create_table('cms_header_config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('business_hours', sa.String(length=255), nullable=True),
        sa.Column('nav_items', sa.JSON(), nullable=True),
        sa.Column('cta_text', sa.String(length=100), nullable=True),
        sa.Column('cta_link', sa.String(length=500), nullable=True),
        sa.Column('social_links', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Hero Section
    op.create_table('cms_hero_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slides', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # About Section
    op.create_table('cms_about_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subtitle', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cta_text', sa.String(length=100), nullable=True),
        sa.Column('cta_link', sa.String(length=500), nullable=True),
        sa.Column('image_path', sa.String(length=500), nullable=True),
        sa.Column('highlight_points', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Services Section
    op.create_table('cms_services_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subtitle', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('items', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Stats Section
    op.create_table('cms_stats_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('items', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Testimonials Section
    op.create_table('cms_testimonials_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subtitle', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('video_url', sa.String(length=500), nullable=True),
        sa.Column('video_thumbnail_path', sa.String(length=500), nullable=True),
        sa.Column('items', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Gallery Section
    op.create_table('cms_gallery_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('images', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Footer Config
    op.create_table('cms_footer_config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('social_links', sa.JSON(), nullable=True),
        sa.Column('quick_links', sa.JSON(), nullable=True),
        sa.Column('menu_links', sa.JSON(), nullable=True),
        sa.Column('business_hours', sa.JSON(), nullable=True),
        sa.Column('copyright_text', sa.String(length=500), nullable=True),
        sa.Column('bottom_links', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # SEO Config
    op.create_table('cms_seo_config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meta_title', sa.String(length=255), nullable=True),
        sa.Column('meta_description', sa.String(length=500), nullable=True),
        sa.Column('meta_keywords', sa.String(length=500), nullable=True),
        sa.Column('og_title', sa.String(length=255), nullable=True),
        sa.Column('og_description', sa.String(length=500), nullable=True),
        sa.Column('og_image_path', sa.String(length=500), nullable=True),
        sa.Column('canonical_url', sa.String(length=500), nullable=True),
        sa.Column('robots', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Offer Section
    op.create_table('cms_offer_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('items', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Popular Dishes Section
    op.create_table('cms_popular_dishes_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subtitle', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('cta_text', sa.String(length=100), nullable=True),
        sa.Column('cta_link', sa.String(length=500), nullable=True),
        sa.Column('items', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # CTA Section
    op.create_table('cms_cta_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subtitle', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cta_text', sa.String(length=100), nullable=True),
        sa.Column('cta_link', sa.String(length=500), nullable=True),
        sa.Column('image_path', sa.String(length=500), nullable=True),
        sa.Column('background_image_path', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Food Menu Section
    op.create_table('cms_food_menu_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subtitle', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('categories', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Special Offer/Timer Section
    op.create_table('cms_special_offer_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subtitle', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('discount_percentage', sa.Integer(), nullable=True),
        sa.Column('offer_end_date', sa.DateTime(), nullable=True),
        sa.Column('cta_text', sa.String(length=100), nullable=True),
        sa.Column('cta_link', sa.String(length=500), nullable=True),
        sa.Column('image_path', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Chef Section
    op.create_table('cms_chef_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subtitle', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('items', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Client Logos Section
    op.create_table('cms_client_logos_section',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('logos', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # =========================================================================
    # News/Blog Table
    # =========================================================================
    
    op.create_table('news',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('slug', sa.String(length=500), nullable=False),
        sa.Column('summary', sa.String(length=1000), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('cover_image_path', sa.String(length=500), nullable=True),
        sa.Column('author', sa.String(length=255), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=False, default=False),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('view_count', sa.Integer(), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index('ix_news_slug', 'news', ['slug'], unique=True)
    op.create_index('ix_news_is_published', 'news', ['is_published'])
    op.create_index('ix_news_published_at', 'news', ['published_at'])
    op.create_index('ix_news_category', 'news', ['category'])
    
    # =========================================================================
    # Assets Table
    # =========================================================================
    
    op.create_table('assets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=True),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('file_url', sa.String(length=500), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('alt_text', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_assets_filename', 'assets', ['filename'])
    op.create_index('ix_assets_mime_type', 'assets', ['mime_type'])


def downgrade() -> None:
    """Drop all tables."""
    
    # Drop indexes first
    op.drop_index('ix_assets_mime_type', table_name='assets')
    op.drop_index('ix_assets_filename', table_name='assets')
    op.drop_index('ix_news_category', table_name='news')
    op.drop_index('ix_news_published_at', table_name='news')
    op.drop_index('ix_news_is_published', table_name='news')
    op.drop_index('ix_news_slug', table_name='news')
    
    # Drop tables
    op.drop_table('assets')
    op.drop_table('news')
    op.drop_table('cms_client_logos_section')
    op.drop_table('cms_chef_section')
    op.drop_table('cms_special_offer_section')
    op.drop_table('cms_food_menu_section')
    op.drop_table('cms_cta_section')
    op.drop_table('cms_popular_dishes_section')
    op.drop_table('cms_offer_section')
    op.drop_table('cms_seo_config')
    op.drop_table('cms_footer_config')
    op.drop_table('cms_gallery_section')
    op.drop_table('cms_testimonials_section')
    op.drop_table('cms_stats_section')
    op.drop_table('cms_services_section')
    op.drop_table('cms_about_section')
    op.drop_table('cms_hero_section')
    op.drop_table('cms_header_config')
    op.drop_table('cms_site_branding')
