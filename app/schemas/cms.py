"""
CMS Content Schemas
===================

Pydantic schemas for CMS content validation.
These schemas handle both request validation and response serialization.
"""

from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field


# =============================================================================
# Base Schemas
# =============================================================================

class TimestampSchema(BaseModel):
    """Base schema with timestamp fields."""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


# =============================================================================
# Site Branding Schemas
# =============================================================================

class SiteBrandingBase(BaseModel):
    """Base site branding schema."""
    company_name: str = Field(default="Fresheat", max_length=255)
    tagline: Optional[str] = Field(default=None, max_length=500)
    logo_image_path: Optional[str] = Field(default=None, max_length=500)
    logo_white_image_path: Optional[str] = Field(default=None, max_length=500)
    favicon_path: Optional[str] = Field(default=None, max_length=500)


class SiteBrandingCreate(SiteBrandingBase):
    """Schema for creating/updating site branding."""
    pass


class SiteBrandingResponse(SiteBrandingBase, TimestampSchema):
    """Schema for site branding response."""
    id: int


# =============================================================================
# Header Config Schemas
# =============================================================================

class NavItem(BaseModel):
    """Navigation item structure."""
    label: str
    link: str
    has_dropdown: bool = False
    children: Optional[List["NavItem"]] = None


class HeaderConfigBase(BaseModel):
    """Base header config schema."""
    operating_hours: Optional[str] = Field(default="09:00 am - 06:00 pm", max_length=255)
    nav_items: Optional[List[NavItem]] = None
    social_links: Optional[dict] = None
    cta_text: str = Field(default="ORDER NOW", max_length=100)
    cta_link: str = Field(default="/menu", max_length=500)
    sidebar_description: Optional[str] = None
    contact_address: Optional[str] = Field(default=None, max_length=500)
    contact_email: Optional[str] = Field(default=None, max_length=255)
    contact_phone: Optional[str] = Field(default=None, max_length=50)
    contact_hours: Optional[str] = Field(default=None, max_length=255)
    offcanvas_gallery_images: Optional[List[str]] = None


class HeaderConfigCreate(HeaderConfigBase):
    """Schema for creating/updating header config."""
    pass


class HeaderConfigResponse(HeaderConfigBase, TimestampSchema):
    """Schema for header config response."""
    id: int


# =============================================================================
# Hero Section Schemas
# =============================================================================

class HeroSlide(BaseModel):
    """Hero slide structure."""
    subtitle: Optional[str] = None
    title: str
    cta_text: Optional[str] = "ORDER NOW"
    cta_link: Optional[str] = "/menu"
    image_path: Optional[str] = None
    background_image_path: Optional[str] = None


class HeroSectionBase(BaseModel):
    """Base hero section schema."""
    slides: Optional[List[HeroSlide]] = None
    shape_images: Optional[List[str]] = None


class HeroSectionCreate(HeroSectionBase):
    """Schema for creating/updating hero section."""
    pass


class HeroSectionResponse(HeroSectionBase, TimestampSchema):
    """Schema for hero section response."""
    id: int


# =============================================================================
# About Section Schemas
# =============================================================================

class AboutSectionBase(BaseModel):
    """Base about section schema."""
    section_subtitle: Optional[str] = Field(default="About US", max_length=255)
    section_title: Optional[str] = Field(default="Variety of flavours from american cuisine", max_length=500)
    description: Optional[str] = None
    highlight_points: Optional[List[str]] = None
    cta_text: str = Field(default="ORDER NOW", max_length=100)
    cta_link: str = Field(default="/menu", max_length=500)
    background_image_path: Optional[str] = Field(default=None, max_length=500)
    shape_images: Optional[List[str]] = None


class AboutSectionCreate(AboutSectionBase):
    """Schema for creating/updating about section."""
    pass


class AboutSectionResponse(AboutSectionBase, TimestampSchema):
    """Schema for about section response."""
    id: int


# =============================================================================
# Services Section Schemas (Best Food Items)
# =============================================================================

class ServiceItem(BaseModel):
    """Service/food item structure."""
    name: str
    description: Optional[str] = None
    price: Optional[str] = None
    image_path: Optional[str] = None
    link: Optional[str] = None


class ServicesSectionBase(BaseModel):
    """Base services section schema."""
    section_subtitle: Optional[str] = Field(default="Best Food", max_length=255)
    section_title: Optional[str] = Field(default="Popular Food Items", max_length=500)
    items: Optional[List[ServiceItem]] = None


class ServicesSectionCreate(ServicesSectionBase):
    """Schema for creating/updating services section."""
    pass


class ServicesSectionResponse(ServicesSectionBase, TimestampSchema):
    """Schema for services section response."""
    id: int


# =============================================================================
# Stats Section Schemas
# =============================================================================

class StatItem(BaseModel):
    """Stat item structure."""
    label: str
    value: str
    icon: Optional[str] = None


class StatsSectionBase(BaseModel):
    """Base stats section schema."""
    items: Optional[List[StatItem]] = None
    background_image_path: Optional[str] = Field(default=None, max_length=500)


class StatsSectionCreate(StatsSectionBase):
    """Schema for creating/updating stats section."""
    pass


class StatsSectionResponse(StatsSectionBase, TimestampSchema):
    """Schema for stats section response."""
    id: int


# =============================================================================
# Testimonials Section Schemas
# =============================================================================

class TestimonialItem(BaseModel):
    """Testimonial item structure."""
    name: str
    role: Optional[str] = None
    message: str
    avatar_path: Optional[str] = None
    rating: Optional[int] = Field(default=5, ge=1, le=5)


class TestimonialsSectionBase(BaseModel):
    """Base testimonials section schema."""
    section_subtitle: Optional[str] = Field(default="Testimonials", max_length=255)
    section_title: Optional[str] = Field(default="What our Clients Say", max_length=500)
    items: Optional[List[TestimonialItem]] = None
    video_url: Optional[str] = Field(default=None, max_length=500)
    video_thumbnail_path: Optional[str] = Field(default=None, max_length=500)
    background_image_path: Optional[str] = Field(default=None, max_length=500)


class TestimonialsSectionCreate(TestimonialsSectionBase):
    """Schema for creating/updating testimonials section."""
    pass


class TestimonialsSectionResponse(TestimonialsSectionBase, TimestampSchema):
    """Schema for testimonials section response."""
    id: int


# =============================================================================
# Gallery Section Schemas
# =============================================================================

class GalleryImage(BaseModel):
    """Gallery image structure."""
    image_path: str
    caption: Optional[str] = None
    link: Optional[str] = None


class GallerySectionBase(BaseModel):
    """Base gallery section schema."""
    images: Optional[List[GalleryImage]] = None


class GallerySectionCreate(GallerySectionBase):
    """Schema for creating/updating gallery section."""
    pass


class GallerySectionResponse(GallerySectionBase, TimestampSchema):
    """Schema for gallery section response."""
    id: int


# =============================================================================
# Footer Config Schemas
# =============================================================================

class FooterLink(BaseModel):
    """Footer link structure."""
    label: str
    link: str


class FooterConfigBase(BaseModel):
    """Base footer config schema."""
    address: Optional[str] = Field(default=None, max_length=500)
    phone: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    social_links: Optional[dict] = None
    quick_links: Optional[List[FooterLink]] = None
    menu_links: Optional[List[FooterLink]] = None
    weekday_hours: Optional[str] = Field(default=None, max_length=100)
    saturday_hours: Optional[str] = Field(default=None, max_length=100)
    copyright_text: Optional[str] = Field(default=None, max_length=500)
    terms_link: Optional[str] = Field(default=None, max_length=500)
    privacy_link: Optional[str] = Field(default=None, max_length=500)
    newsletter_enabled: bool = True


class FooterConfigCreate(FooterConfigBase):
    """Schema for creating/updating footer config."""
    pass


class FooterConfigResponse(FooterConfigBase, TimestampSchema):
    """Schema for footer config response."""
    id: int


# =============================================================================
# SEO Config Schemas
# =============================================================================

class SEOConfigBase(BaseModel):
    """Base SEO config schema."""
    meta_title: Optional[str] = Field(default=None, max_length=255)
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    og_title: Optional[str] = Field(default=None, max_length=255)
    og_description: Optional[str] = None
    og_image_path: Optional[str] = Field(default=None, max_length=500)
    canonical_url: Optional[str] = Field(default=None, max_length=500)


class SEOConfigCreate(SEOConfigBase):
    """Schema for creating/updating SEO config."""
    pass


class SEOConfigResponse(SEOConfigBase, TimestampSchema):
    """Schema for SEO config response."""
    id: int


# =============================================================================
# Offer Section Schemas
# =============================================================================

class OfferItem(BaseModel):
    """Offer item structure."""
    label: Optional[str] = None
    title: str
    subtitle: Optional[str] = None
    cta_text: Optional[str] = "ORDER NOW"
    cta_link: Optional[str] = "/menu"
    image_path: Optional[str] = None
    bg_image_path: Optional[str] = None
    style: Optional[str] = None


class OfferSectionBase(BaseModel):
    """Base offer section schema."""
    offers: Optional[List[OfferItem]] = None


class OfferSectionCreate(OfferSectionBase):
    """Schema for creating/updating offer section."""
    pass


class OfferSectionResponse(OfferSectionBase, TimestampSchema):
    """Schema for offer section response."""
    id: int


# =============================================================================
# Popular Dishes Section Schemas
# =============================================================================

class DishItem(BaseModel):
    """Dish item structure."""
    name: str
    description: Optional[str] = None
    price: str
    image_path: Optional[str] = None
    link: Optional[str] = None


class PopularDishesSectionBase(BaseModel):
    """Base popular dishes section schema."""
    section_subtitle: Optional[str] = Field(default="POPULAR DISHES", max_length=255)
    section_title: Optional[str] = Field(default="Best selling Dishes", max_length=500)
    dishes: Optional[List[DishItem]] = None
    cta_text: str = Field(default="VIEW ALL ITEM", max_length=100)
    cta_link: str = Field(default="/menu", max_length=500)


class PopularDishesSectionCreate(PopularDishesSectionBase):
    """Schema for creating/updating popular dishes section."""
    pass


class PopularDishesSectionResponse(PopularDishesSectionBase, TimestampSchema):
    """Schema for popular dishes section response."""
    id: int


# =============================================================================
# CTA Section Schemas
# =============================================================================

class CTASectionBase(BaseModel):
    """Base CTA section schema."""
    label: Optional[str] = Field(default=None, max_length=255)
    title: Optional[str] = Field(default=None, max_length=500)
    subtitle: Optional[str] = Field(default=None, max_length=500)
    cta_text: str = Field(default="ORDER NOW", max_length=100)
    cta_link: str = Field(default="/menu", max_length=500)
    image_path: Optional[str] = Field(default=None, max_length=500)
    background_image_path: Optional[str] = Field(default=None, max_length=500)


class CTASectionCreate(CTASectionBase):
    """Schema for creating/updating CTA section."""
    pass


class CTASectionResponse(CTASectionBase, TimestampSchema):
    """Schema for CTA section response."""
    id: int


# =============================================================================
# Food Menu Section Schemas
# =============================================================================

class MenuItem(BaseModel):
    """Menu item structure."""
    name: str
    description: Optional[str] = None
    price: str
    image_path: Optional[str] = None


class MenuCategory(BaseModel):
    """Menu category structure."""
    id: str
    name: str
    icon_path: Optional[str] = None
    items: Optional[List[MenuItem]] = None


class FoodMenuSectionBase(BaseModel):
    """Base food menu section schema."""
    section_subtitle: Optional[str] = Field(default="FOOD MENU", max_length=255)
    section_title: Optional[str] = Field(default="Fresheat Foods Menu", max_length=500)
    categories: Optional[List[MenuCategory]] = None


class FoodMenuSectionCreate(FoodMenuSectionBase):
    """Schema for creating/updating food menu section."""
    pass


class FoodMenuSectionResponse(FoodMenuSectionBase, TimestampSchema):
    """Schema for food menu section response."""
    id: int


# =============================================================================
# Special Offer Section Schemas
# =============================================================================

class SpecialOfferSectionBase(BaseModel):
    """Base special offer section schema."""
    section_subtitle: Optional[str] = Field(default="Special Offer", max_length=255)
    section_title: Optional[str] = Field(default="Get 30% Discount Every Item", max_length=500)
    countdown_target: Optional[str] = Field(default=None, max_length=50)
    cta_text: str = Field(default="ORDER NOW", max_length=100)
    cta_link: str = Field(default="/menu", max_length=500)
    image_path: Optional[str] = Field(default=None, max_length=500)
    background_image_path: Optional[str] = Field(default=None, max_length=500)


class SpecialOfferSectionCreate(SpecialOfferSectionBase):
    """Schema for creating/updating special offer section."""
    pass


class SpecialOfferSectionResponse(SpecialOfferSectionBase, TimestampSchema):
    """Schema for special offer section response."""
    id: int


# =============================================================================
# Chef Section Schemas
# =============================================================================

class ChefMember(BaseModel):
    """Chef/team member structure."""
    name: str
    role: Optional[str] = None
    image_path: Optional[str] = None
    social_links: Optional[dict] = None


class ChefSectionBase(BaseModel):
    """Base chef section schema."""
    section_subtitle: Optional[str] = Field(default="OUR CHEFE", max_length=255)
    section_title: Optional[str] = Field(default="Meet Our Expert Chefe", max_length=500)
    members: Optional[List[ChefMember]] = None


class ChefSectionCreate(ChefSectionBase):
    """Schema for creating/updating chef section."""
    pass


class ChefSectionResponse(ChefSectionBase, TimestampSchema):
    """Schema for chef section response."""
    id: int


# =============================================================================
# Client Logos Section Schemas
# =============================================================================

class ClientLogo(BaseModel):
    """Client logo structure."""
    image_path: str
    alt_text: Optional[str] = None
    link: Optional[str] = None


class ClientLogosSectionBase(BaseModel):
    """Base client logos section schema."""
    logos: Optional[List[ClientLogo]] = None


class ClientLogosSectionCreate(ClientLogosSectionBase):
    """Schema for creating/updating client logos section."""
    pass


class ClientLogosSectionResponse(ClientLogosSectionBase, TimestampSchema):
    """Schema for client logos section response."""
    id: int


# =============================================================================
# Aggregated Home Page Schema
# =============================================================================

class HomePageResponse(BaseModel):
    """Aggregated response for entire home page."""
    site_branding: Optional[SiteBrandingResponse] = None
    header: Optional[HeaderConfigResponse] = None
    hero: Optional[HeroSectionResponse] = None
    services: Optional[ServicesSectionResponse] = None
    offers: Optional[OfferSectionResponse] = None
    about: Optional[AboutSectionResponse] = None
    popular_dishes: Optional[PopularDishesSectionResponse] = None
    cta: Optional[CTASectionResponse] = None
    food_menu: Optional[FoodMenuSectionResponse] = None
    special_offer: Optional[SpecialOfferSectionResponse] = None
    chef: Optional[ChefSectionResponse] = None
    client_logos: Optional[ClientLogosSectionResponse] = None
    testimonials: Optional[TestimonialsSectionResponse] = None
    gallery: Optional[GallerySectionResponse] = None
    footer: Optional[FooterConfigResponse] = None
    seo: Optional[SEOConfigResponse] = None


# Enable forward references for recursive types
NavItem.model_rebuild()
