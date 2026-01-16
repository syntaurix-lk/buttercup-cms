"""
CMS Service
===========

Business logic for CMS content management.
Handles UPSERT/REPLACE operations for single-row content tables.
"""

import logging
from typing import Optional, Type, TypeVar, Any
from sqlalchemy.orm import Session

from app.db.models.cms import (
    SiteBranding,
    HeaderConfig,
    HeroSection,
    AboutSection,
    ServicesSection,
    StatsSection,
    TestimonialsSection,
    GallerySection,
    FooterConfig,
    SEOConfig,
    OfferSection,
    PopularDishesSection,
    CTASection,
    FoodMenuSection,
    SpecialOfferSection,
    ChefSection,
    ClientLogosSection,
)
from app.schemas.cms import (
    SiteBrandingCreate,
    HeaderConfigCreate,
    HeroSectionCreate,
    AboutSectionCreate,
    ServicesSectionCreate,
    StatsSectionCreate,
    TestimonialsSectionCreate,
    GallerySectionCreate,
    FooterConfigCreate,
    SEOConfigCreate,
    OfferSectionCreate,
    PopularDishesSectionCreate,
    CTASectionCreate,
    FoodMenuSectionCreate,
    SpecialOfferSectionCreate,
    ChefSectionCreate,
    ClientLogosSectionCreate,
    HomePageResponse,
)

logger = logging.getLogger(__name__)

# Type variable for generic model handling
T = TypeVar("T")


class CMSService:
    """
    Service class for CMS content management.
    
    Provides UPSERT/REPLACE functionality for single-row content tables.
    Most CMS tables have only one row that gets replaced on update.
    """
    
    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
    
    # =========================================================================
    # Generic Helper Methods
    # =========================================================================
    
    def _get_or_create(self, model_class: Type[T]) -> T:
        """
        Get existing record or create new one.
        
        For single-row tables, returns the first record or creates one.
        """
        instance = self.db.query(model_class).first()
        if not instance:
            instance = model_class()
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
        return instance
    
    def _upsert(self, model_class: Type[T], data: dict) -> T:
        """
        Update existing record or insert new one.
        
        For single-row tables, updates the first record or creates one.
        """
        instance = self.db.query(model_class).first()
        
        if instance:
            # Update existing record
            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
        else:
            # Create new record
            instance = model_class(**data)
            self.db.add(instance)
        
        self.db.commit()
        self.db.refresh(instance)
        logger.info(f"Upserted {model_class.__name__}")
        return instance
    
    # =========================================================================
    # Site Branding
    # =========================================================================
    
    def get_site_branding(self) -> Optional[SiteBranding]:
        """Get site branding configuration."""
        return self._get_or_create(SiteBranding)
    
    def upsert_site_branding(self, data: SiteBrandingCreate) -> SiteBranding:
        """Update or insert site branding configuration."""
        return self._upsert(SiteBranding, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Header Config
    # =========================================================================
    
    def get_header_config(self) -> Optional[HeaderConfig]:
        """Get header configuration."""
        return self._get_or_create(HeaderConfig)
    
    def upsert_header_config(self, data: HeaderConfigCreate) -> HeaderConfig:
        """Update or insert header configuration."""
        return self._upsert(HeaderConfig, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Hero Section
    # =========================================================================
    
    def get_hero_section(self) -> Optional[HeroSection]:
        """Get hero section content."""
        return self._get_or_create(HeroSection)
    
    def upsert_hero_section(self, data: HeroSectionCreate) -> HeroSection:
        """Update or insert hero section content."""
        return self._upsert(HeroSection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # About Section
    # =========================================================================
    
    def get_about_section(self) -> Optional[AboutSection]:
        """Get about section content."""
        return self._get_or_create(AboutSection)
    
    def upsert_about_section(self, data: AboutSectionCreate) -> AboutSection:
        """Update or insert about section content."""
        return self._upsert(AboutSection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Services Section (Best Food Items)
    # =========================================================================
    
    def get_services_section(self) -> Optional[ServicesSection]:
        """Get services section content."""
        return self._get_or_create(ServicesSection)
    
    def upsert_services_section(self, data: ServicesSectionCreate) -> ServicesSection:
        """Update or insert services section content."""
        return self._upsert(ServicesSection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Stats Section
    # =========================================================================
    
    def get_stats_section(self) -> Optional[StatsSection]:
        """Get stats section content."""
        return self._get_or_create(StatsSection)
    
    def upsert_stats_section(self, data: StatsSectionCreate) -> StatsSection:
        """Update or insert stats section content."""
        return self._upsert(StatsSection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Testimonials Section
    # =========================================================================
    
    def get_testimonials_section(self) -> Optional[TestimonialsSection]:
        """Get testimonials section content."""
        return self._get_or_create(TestimonialsSection)
    
    def upsert_testimonials_section(self, data: TestimonialsSectionCreate) -> TestimonialsSection:
        """Update or insert testimonials section content."""
        return self._upsert(TestimonialsSection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Gallery Section
    # =========================================================================
    
    def get_gallery_section(self) -> Optional[GallerySection]:
        """Get gallery section content."""
        return self._get_or_create(GallerySection)
    
    def upsert_gallery_section(self, data: GallerySectionCreate) -> GallerySection:
        """Update or insert gallery section content."""
        return self._upsert(GallerySection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Footer Config
    # =========================================================================
    
    def get_footer_config(self) -> Optional[FooterConfig]:
        """Get footer configuration."""
        return self._get_or_create(FooterConfig)
    
    def upsert_footer_config(self, data: FooterConfigCreate) -> FooterConfig:
        """Update or insert footer configuration."""
        return self._upsert(FooterConfig, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # SEO Config
    # =========================================================================
    
    def get_seo_config(self) -> Optional[SEOConfig]:
        """Get SEO configuration."""
        return self._get_or_create(SEOConfig)
    
    def upsert_seo_config(self, data: SEOConfigCreate) -> SEOConfig:
        """Update or insert SEO configuration."""
        return self._upsert(SEOConfig, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Offer Section
    # =========================================================================
    
    def get_offer_section(self) -> Optional[OfferSection]:
        """Get offer section content."""
        return self._get_or_create(OfferSection)
    
    def upsert_offer_section(self, data: OfferSectionCreate) -> OfferSection:
        """Update or insert offer section content."""
        return self._upsert(OfferSection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Popular Dishes Section
    # =========================================================================
    
    def get_popular_dishes_section(self) -> Optional[PopularDishesSection]:
        """Get popular dishes section content."""
        return self._get_or_create(PopularDishesSection)
    
    def upsert_popular_dishes_section(self, data: PopularDishesSectionCreate) -> PopularDishesSection:
        """Update or insert popular dishes section content."""
        return self._upsert(PopularDishesSection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # CTA Section
    # =========================================================================
    
    def get_cta_section(self) -> Optional[CTASection]:
        """Get CTA section content."""
        return self._get_or_create(CTASection)
    
    def upsert_cta_section(self, data: CTASectionCreate) -> CTASection:
        """Update or insert CTA section content."""
        return self._upsert(CTASection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Food Menu Section
    # =========================================================================
    
    def get_food_menu_section(self) -> Optional[FoodMenuSection]:
        """Get food menu section content."""
        return self._get_or_create(FoodMenuSection)
    
    def upsert_food_menu_section(self, data: FoodMenuSectionCreate) -> FoodMenuSection:
        """Update or insert food menu section content."""
        return self._upsert(FoodMenuSection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Special Offer Section
    # =========================================================================
    
    def get_special_offer_section(self) -> Optional[SpecialOfferSection]:
        """Get special offer section content."""
        return self._get_or_create(SpecialOfferSection)
    
    def upsert_special_offer_section(self, data: SpecialOfferSectionCreate) -> SpecialOfferSection:
        """Update or insert special offer section content."""
        return self._upsert(SpecialOfferSection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Chef Section
    # =========================================================================
    
    def get_chef_section(self) -> Optional[ChefSection]:
        """Get chef section content."""
        return self._get_or_create(ChefSection)
    
    def upsert_chef_section(self, data: ChefSectionCreate) -> ChefSection:
        """Update or insert chef section content."""
        return self._upsert(ChefSection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Client Logos Section
    # =========================================================================
    
    def get_client_logos_section(self) -> Optional[ClientLogosSection]:
        """Get client logos section content."""
        return self._get_or_create(ClientLogosSection)
    
    def upsert_client_logos_section(self, data: ClientLogosSectionCreate) -> ClientLogosSection:
        """Update or insert client logos section content."""
        return self._upsert(ClientLogosSection, data.model_dump(exclude_unset=True))
    
    # =========================================================================
    # Aggregated Home Page
    # =========================================================================
    
    def get_home_page(self) -> dict:
        """
        Get all home page content in a single response.
        
        This is optimized for frontend page load - one API call gets everything.
        """
        return {
            "site_branding": self.get_site_branding(),
            "header": self.get_header_config(),
            "hero": self.get_hero_section(),
            "services": self.get_services_section(),
            "offers": self.get_offer_section(),
            "about": self.get_about_section(),
            "popular_dishes": self.get_popular_dishes_section(),
            "cta": self.get_cta_section(),
            "food_menu": self.get_food_menu_section(),
            "special_offer": self.get_special_offer_section(),
            "chef": self.get_chef_section(),
            "client_logos": self.get_client_logos_section(),
            "testimonials": self.get_testimonials_section(),
            "gallery": self.get_gallery_section(),
            "footer": self.get_footer_config(),
            "seo": self.get_seo_config(),
        }
