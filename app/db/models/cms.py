"""
CMS Content Models
==================

These models store all content for the home page sections.
Most tables are single-row (singleton pattern) for CMS content that gets "replaced".

Based on the Fresheat restaurant HTML template sections:
- Site Branding (logo, favicon, company name)
- Header (navigation, social links, operating hours)
- Hero/Banner Slider
- Best Food Items
- Offer Section
- About Us
- Popular Dishes
- CTA Section
- Food Menu (tabbed)
- Special Offer with Timer
- Chef/Team Section
- Client Logos
- Testimonials
- Gallery
- Footer
- SEO Meta
"""

from typing import Optional
from sqlalchemy import String, Text, Boolean, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class SiteBranding(Base, TimestampMixin):
    """
    Site branding information (logo, favicon, company name).
    Single-row table - content is replaced, not appended.
    """
    __tablename__ = "cms_site_branding"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_name: Mapped[str] = mapped_column(String(255), default="Fresheat")
    tagline: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    logo_image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    logo_white_image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    favicon_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


class HeaderConfig(Base, TimestampMixin):
    """
    Header configuration including navigation, social links, and CTA.
    """
    __tablename__ = "cms_header_config"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    operating_hours: Mapped[Optional[str]] = mapped_column(String(255), default="09:00 am - 06:00 pm")
    
    # Navigation items as JSON array
    # Example: [{"label": "Home", "link": "/", "has_dropdown": true, "children": [...]}]
    nav_items: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Social links as JSON object
    # Example: {"facebook": "https://...", "twitter": "https://...", ...}
    social_links: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    cta_text: Mapped[str] = mapped_column(String(100), default="ORDER NOW")
    cta_link: Mapped[str] = mapped_column(String(500), default="/menu")
    
    # Offcanvas/Sidebar content
    sidebar_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    contact_hours: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Gallery images in offcanvas
    offcanvas_gallery_images: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class HeroSection(Base, TimestampMixin):
    """
    Hero/Banner slider section with multiple slides.
    """
    __tablename__ = "cms_hero_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Slides as JSON array
    # Example: [{"subtitle": "...", "title": "...", "cta_text": "...", "cta_link": "...", "image_path": "..."}]
    slides: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Shape/decoration images
    shape_images: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class AboutSection(Base, TimestampMixin):
    """
    About Us section content.
    """
    __tablename__ = "cms_about_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    section_subtitle: Mapped[Optional[str]] = mapped_column(String(255), default="About US")
    section_title: Mapped[Optional[str]] = mapped_column(String(500), default="Variety of flavours from american cuisine")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Highlight points as JSON array
    # Example: ["Fresh Ingredients", "Expert Chefs", "Fast Delivery"]
    highlight_points: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    cta_text: Mapped[str] = mapped_column(String(100), default="ORDER NOW")
    cta_link: Mapped[str] = mapped_column(String(500), default="/menu")
    
    # Background/decoration images
    background_image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    shape_images: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class ServicesSection(Base, TimestampMixin):
    """
    Services/Features section (Best Food Items in the template).
    """
    __tablename__ = "cms_services_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    section_subtitle: Mapped[Optional[str]] = mapped_column(String(255), default="Best Food")
    section_title: Mapped[Optional[str]] = mapped_column(String(500), default="Popular Food Items")
    
    # Items as JSON array
    # Example: [{"name": "...", "description": "...", "price": "...", "image_path": "..."}]
    items: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class StatsSection(Base, TimestampMixin):
    """
    Statistics/Counter section.
    """
    __tablename__ = "cms_stats_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Stats as JSON array
    # Example: [{"label": "Happy Customers", "value": "1500", "icon": "users"}]
    items: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    background_image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


class TestimonialsSection(Base, TimestampMixin):
    """
    Customer testimonials section.
    """
    __tablename__ = "cms_testimonials_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    section_subtitle: Mapped[Optional[str]] = mapped_column(String(255), default="Testimonials")
    section_title: Mapped[Optional[str]] = mapped_column(String(500), default="What our Clients Say")
    
    # Testimonials as JSON array
    # Example: [{"name": "...", "role": "...", "message": "...", "avatar_path": "...", "rating": 5}]
    items: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Video link
    video_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    video_thumbnail_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    background_image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


class GallerySection(Base, TimestampMixin):
    """
    Image gallery/slider section.
    """
    __tablename__ = "cms_gallery_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Images as JSON array
    # Example: [{"image_path": "...", "caption": "...", "link": "..."}]
    images: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class FooterConfig(Base, TimestampMixin):
    """
    Footer configuration and content.
    """
    __tablename__ = "cms_footer_config"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Contact info
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Footer description
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Social links as JSON
    social_links: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Quick links as JSON array
    # Example: [{"label": "About Us", "link": "/about"}]
    quick_links: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Menu links as JSON array
    menu_links: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Contact hours
    weekday_hours: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    saturday_hours: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Copyright text
    copyright_text: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Legal links
    terms_link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    privacy_link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Newsletter settings
    newsletter_enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class SEOConfig(Base, TimestampMixin):
    """
    SEO meta information.
    """
    __tablename__ = "cms_seo_config"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meta_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    meta_keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    og_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    og_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    og_image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    canonical_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


class OfferSection(Base, TimestampMixin):
    """
    Promotional offer cards section.
    """
    __tablename__ = "cms_offer_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Offers as JSON array
    # Example: [{"label": "...", "title": "...", "subtitle": "...", "cta_text": "...", "cta_link": "...", "image_path": "...", "bg_image_path": "..."}]
    offers: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class PopularDishesSection(Base, TimestampMixin):
    """
    Popular dishes/menu items section.
    """
    __tablename__ = "cms_popular_dishes_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    section_subtitle: Mapped[Optional[str]] = mapped_column(String(255), default="POPULAR DISHES")
    section_title: Mapped[Optional[str]] = mapped_column(String(500), default="Best selling Dishes")
    
    # Dishes as JSON array
    # Example: [{"name": "...", "description": "...", "price": "...", "image_path": "...", "link": "..."}]
    dishes: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    cta_text: Mapped[str] = mapped_column(String(100), default="VIEW ALL ITEM")
    cta_link: Mapped[str] = mapped_column(String(500), default="/menu")


class CTASection(Base, TimestampMixin):
    """
    Call-to-action promotional section.
    """
    __tablename__ = "cms_cta_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    label: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    subtitle: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cta_text: Mapped[str] = mapped_column(String(100), default="ORDER NOW")
    cta_link: Mapped[str] = mapped_column(String(500), default="/menu")
    image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    background_image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


class FoodMenuSection(Base, TimestampMixin):
    """
    Tabbed food menu section.
    """
    __tablename__ = "cms_food_menu_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    section_subtitle: Mapped[Optional[str]] = mapped_column(String(255), default="FOOD MENU")
    section_title: Mapped[Optional[str]] = mapped_column(String(500), default="Fresheat Foods Menu")
    
    # Menu categories/tabs as JSON array
    # Example: [{"id": "fast-food", "name": "Fast Food", "icon_path": "...", "items": [...]}]
    categories: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class SpecialOfferSection(Base, TimestampMixin):
    """
    Special offer section with countdown timer.
    """
    __tablename__ = "cms_special_offer_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    section_subtitle: Mapped[Optional[str]] = mapped_column(String(255), default="Special Offer")
    section_title: Mapped[Optional[str]] = mapped_column(String(500), default="Get 30% Discount Every Item")
    
    # Countdown target date (ISO format)
    countdown_target: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    cta_text: Mapped[str] = mapped_column(String(100), default="ORDER NOW")
    cta_link: Mapped[str] = mapped_column(String(500), default="/menu")
    image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    background_image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


class ChefSection(Base, TimestampMixin):
    """
    Chef/Team members section.
    """
    __tablename__ = "cms_chef_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    section_subtitle: Mapped[Optional[str]] = mapped_column(String(255), default="OUR CHEFE")
    section_title: Mapped[Optional[str]] = mapped_column(String(500), default="Meet Our Expert Chefe")
    
    # Team members as JSON array
    # Example: [{"name": "...", "role": "...", "image_path": "...", "social_links": {...}}]
    members: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class ClientLogosSection(Base, TimestampMixin):
    """
    Client/Partner logos slider section.
    """
    __tablename__ = "cms_client_logos_section"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Logos as JSON array
    # Example: [{"image_path": "...", "alt_text": "...", "link": "..."}]
    logos: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
