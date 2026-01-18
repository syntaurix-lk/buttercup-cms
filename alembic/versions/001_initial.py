"""Initial migration - Create CMS, News, and Assets tables

Revision ID: 001_initial
Revises:
Create Date: 2026-01-18 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _created_at_column() -> sa.Column:
    return sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def _updated_at_column() -> sa.Column:
    return sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        server_onupdate=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def upgrade() -> None:
    """Create all database tables."""

    # =========================================================================
    # CMS Tables - Single-row configuration tables
    # =========================================================================

    op.create_table(
        "cms_site_branding",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("tagline", sa.String(length=500), nullable=True),
        sa.Column("logo_image_path", sa.String(length=500), nullable=True),
        sa.Column("logo_white_image_path", sa.String(length=500), nullable=True),
        sa.Column("favicon_path", sa.String(length=500), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_header_config",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("operating_hours", sa.String(length=255), nullable=True),
        sa.Column("nav_items", sa.JSON(), nullable=True),
        sa.Column("social_links", sa.JSON(), nullable=True),
        sa.Column("cta_text", sa.String(length=100), nullable=False),
        sa.Column("cta_link", sa.String(length=500), nullable=False),
        sa.Column("sidebar_description", sa.Text(), nullable=True),
        sa.Column("contact_address", sa.String(length=500), nullable=True),
        sa.Column("contact_email", sa.String(length=255), nullable=True),
        sa.Column("contact_phone", sa.String(length=50), nullable=True),
        sa.Column("contact_hours", sa.String(length=255), nullable=True),
        sa.Column("offcanvas_gallery_images", sa.JSON(), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_hero_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("slides", sa.JSON(), nullable=True),
        sa.Column("shape_images", sa.JSON(), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_about_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("section_subtitle", sa.String(length=255), nullable=True),
        sa.Column("section_title", sa.String(length=500), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("highlight_points", sa.JSON(), nullable=True),
        sa.Column("cta_text", sa.String(length=100), nullable=False),
        sa.Column("cta_link", sa.String(length=500), nullable=False),
        sa.Column("background_image_path", sa.String(length=500), nullable=True),
        sa.Column("shape_images", sa.JSON(), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_services_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("section_subtitle", sa.String(length=255), nullable=True),
        sa.Column("section_title", sa.String(length=500), nullable=True),
        sa.Column("items", sa.JSON(), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_stats_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("items", sa.JSON(), nullable=True),
        sa.Column("background_image_path", sa.String(length=500), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_testimonials_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("section_subtitle", sa.String(length=255), nullable=True),
        sa.Column("section_title", sa.String(length=500), nullable=True),
        sa.Column("items", sa.JSON(), nullable=True),
        sa.Column("video_url", sa.String(length=500), nullable=True),
        sa.Column("video_thumbnail_path", sa.String(length=500), nullable=True),
        sa.Column("background_image_path", sa.String(length=500), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_gallery_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("images", sa.JSON(), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_footer_config",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("address", sa.String(length=500), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("social_links", sa.JSON(), nullable=True),
        sa.Column("quick_links", sa.JSON(), nullable=True),
        sa.Column("menu_links", sa.JSON(), nullable=True),
        sa.Column("weekday_hours", sa.String(length=100), nullable=True),
        sa.Column("saturday_hours", sa.String(length=100), nullable=True),
        sa.Column("copyright_text", sa.String(length=500), nullable=True),
        sa.Column("terms_link", sa.String(length=500), nullable=True),
        sa.Column("privacy_link", sa.String(length=500), nullable=True),
        sa.Column(
            "newsletter_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("1"),
        ),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_seo_config",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("meta_title", sa.String(length=255), nullable=True),
        sa.Column("meta_description", sa.Text(), nullable=True),
        sa.Column("meta_keywords", sa.Text(), nullable=True),
        sa.Column("og_title", sa.String(length=255), nullable=True),
        sa.Column("og_description", sa.Text(), nullable=True),
        sa.Column("og_image_path", sa.String(length=500), nullable=True),
        sa.Column("canonical_url", sa.String(length=500), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_offer_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("offers", sa.JSON(), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_popular_dishes_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("section_subtitle", sa.String(length=255), nullable=True),
        sa.Column("section_title", sa.String(length=500), nullable=True),
        sa.Column("dishes", sa.JSON(), nullable=True),
        sa.Column("cta_text", sa.String(length=100), nullable=False),
        sa.Column("cta_link", sa.String(length=500), nullable=False),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_cta_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("label", sa.String(length=255), nullable=True),
        sa.Column("title", sa.String(length=500), nullable=True),
        sa.Column("subtitle", sa.String(length=500), nullable=True),
        sa.Column("cta_text", sa.String(length=100), nullable=False),
        sa.Column("cta_link", sa.String(length=500), nullable=False),
        sa.Column("image_path", sa.String(length=500), nullable=True),
        sa.Column("background_image_path", sa.String(length=500), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_food_menu_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("section_subtitle", sa.String(length=255), nullable=True),
        sa.Column("section_title", sa.String(length=500), nullable=True),
        sa.Column("categories", sa.JSON(), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_special_offer_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("section_subtitle", sa.String(length=255), nullable=True),
        sa.Column("section_title", sa.String(length=500), nullable=True),
        sa.Column("countdown_target", sa.String(length=50), nullable=True),
        sa.Column("cta_text", sa.String(length=100), nullable=False),
        sa.Column("cta_link", sa.String(length=500), nullable=False),
        sa.Column("image_path", sa.String(length=500), nullable=True),
        sa.Column("background_image_path", sa.String(length=500), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_chef_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("section_subtitle", sa.String(length=255), nullable=True),
        sa.Column("section_title", sa.String(length=500), nullable=True),
        sa.Column("members", sa.JSON(), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    op.create_table(
        "cms_client_logos_section",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("logos", sa.JSON(), nullable=True),
        _created_at_column(),
        _updated_at_column(),
    )

    # =========================================================================
    # News/Blog Table
    # =========================================================================

    op.create_table(
        "news",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("slug", sa.String(length=191), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("cover_image_path", sa.String(length=500), nullable=True),
        sa.Column("author", sa.String(length=255), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("tags", sa.String(length=500), nullable=True),
        sa.Column(
            "is_published",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("meta_title", sa.String(length=255), nullable=True),
        sa.Column("meta_description", sa.Text(), nullable=True),
        sa.Column(
            "view_count",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        _created_at_column(),
        _updated_at_column(),
    )
    op.create_index("ix_news_slug", "news", ["slug"], unique=True)
    op.create_index("ix_news_is_published", "news", ["is_published"])
    op.create_index("ix_news_category", "news", ["category"])
    op.create_index("ix_news_published_at", "news", ["published_at"])

    # =========================================================================
    # Assets Table
    # =========================================================================

    op.create_table(
        "assets",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.String(length=191), nullable=False),
        sa.Column("mime_type", sa.String(length=100), nullable=True),
        sa.Column("file_size", sa.Integer(), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("alt_text", sa.String(length=500), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("1"),
        ),
        _created_at_column(),
        _updated_at_column(),
        sa.UniqueConstraint("file_path", name="uq_assets_file_path"),
    )
    op.create_index("ix_assets_filename", "assets", ["filename"])
    op.create_index("ix_assets_category", "assets", ["category"])
    op.create_index("ix_assets_is_active", "assets", ["is_active"])


def downgrade() -> None:
    """Drop all tables."""

    op.drop_index("ix_assets_is_active", table_name="assets")
    op.drop_index("ix_assets_category", table_name="assets")
    op.drop_index("ix_assets_filename", table_name="assets")
    op.drop_table("assets")

    op.drop_index("ix_news_published_at", table_name="news")
    op.drop_index("ix_news_category", table_name="news")
    op.drop_index("ix_news_is_published", table_name="news")
    op.drop_index("ix_news_slug", table_name="news")
    op.drop_table("news")

    op.drop_table("cms_client_logos_section")
    op.drop_table("cms_chef_section")
    op.drop_table("cms_special_offer_section")
    op.drop_table("cms_food_menu_section")
    op.drop_table("cms_cta_section")
    op.drop_table("cms_popular_dishes_section")
    op.drop_table("cms_offer_section")
    op.drop_table("cms_seo_config")
    op.drop_table("cms_footer_config")
    op.drop_table("cms_gallery_section")
    op.drop_table("cms_testimonials_section")
    op.drop_table("cms_stats_section")
    op.drop_table("cms_services_section")
    op.drop_table("cms_about_section")
    op.drop_table("cms_hero_section")
    op.drop_table("cms_header_config")
    op.drop_table("cms_site_branding")
