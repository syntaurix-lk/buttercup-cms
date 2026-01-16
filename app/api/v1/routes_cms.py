"""
CMS API Routes
==============

Endpoints for managing CMS content.

PUBLIC READ ENDPOINTS (for frontend):
- GET endpoints return current content for each section

ADMIN REPLACE/UPSERT ENDPOINTS (no auth, but clean validation):
- PUT endpoints replace content for each section
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.cms_service import CMSService
from app.utils.api_response import success_response
from app.schemas.cms import (
    SiteBrandingCreate, SiteBrandingResponse,
    HeaderConfigCreate, HeaderConfigResponse,
    HeroSectionCreate, HeroSectionResponse,
    AboutSectionCreate, AboutSectionResponse,
    ServicesSectionCreate, ServicesSectionResponse,
    StatsSectionCreate, StatsSectionResponse,
    TestimonialsSectionCreate, TestimonialsSectionResponse,
    GallerySectionCreate, GallerySectionResponse,
    FooterConfigCreate, FooterConfigResponse,
    SEOConfigCreate, SEOConfigResponse,
    OfferSectionCreate, OfferSectionResponse,
    PopularDishesSectionCreate, PopularDishesSectionResponse,
    CTASectionCreate, CTASectionResponse,
    FoodMenuSectionCreate, FoodMenuSectionResponse,
    SpecialOfferSectionCreate, SpecialOfferSectionResponse,
    ChefSectionCreate, ChefSectionResponse,
    ClientLogosSectionCreate, ClientLogosSectionResponse,
    HomePageResponse,
)

router = APIRouter()


def get_cms_service(db: Session = Depends(get_db)) -> CMSService:
    """Dependency to get CMS service instance."""
    return CMSService(db)


# =============================================================================
# Aggregated Home Page
# =============================================================================

@router.get("/home", summary="Get all home page content")
def get_home_page(service: CMSService = Depends(get_cms_service)):
    """
    Get all home page content in a single response.
    
    Optimized for frontend page load - one API call gets everything.
    """
    data = service.get_home_page()
    return success_response(data=data, message="Home page content retrieved")


# =============================================================================
# Site Branding
# =============================================================================

@router.get("/site-branding", response_model=dict, summary="Get site branding")
def get_site_branding(service: CMSService = Depends(get_cms_service)):
    """Get site branding configuration (logo, favicon, company name)."""
    data = service.get_site_branding()
    return success_response(data=SiteBrandingResponse.model_validate(data))


@router.put("/site-branding", response_model=dict, summary="Update site branding")
def update_site_branding(
    data: SiteBrandingCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace site branding configuration."""
    result = service.upsert_site_branding(data)
    return success_response(
        data=SiteBrandingResponse.model_validate(result),
        message="Site branding updated"
    )


# =============================================================================
# Header Config
# =============================================================================

@router.get("/header", response_model=dict, summary="Get header config")
def get_header_config(service: CMSService = Depends(get_cms_service)):
    """Get header configuration (navigation, social links, CTA)."""
    data = service.get_header_config()
    return success_response(data=HeaderConfigResponse.model_validate(data))


@router.put("/header", response_model=dict, summary="Update header config")
def update_header_config(
    data: HeaderConfigCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace header configuration."""
    result = service.upsert_header_config(data)
    return success_response(
        data=HeaderConfigResponse.model_validate(result),
        message="Header config updated"
    )


# =============================================================================
# Hero Section
# =============================================================================

@router.get("/hero", response_model=dict, summary="Get hero section")
def get_hero_section(service: CMSService = Depends(get_cms_service)):
    """Get hero/banner slider content."""
    data = service.get_hero_section()
    return success_response(data=HeroSectionResponse.model_validate(data))


@router.put("/hero", response_model=dict, summary="Update hero section")
def update_hero_section(
    data: HeroSectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace hero/banner slider content."""
    result = service.upsert_hero_section(data)
    return success_response(
        data=HeroSectionResponse.model_validate(result),
        message="Hero section updated"
    )


# =============================================================================
# About Section
# =============================================================================

@router.get("/about", response_model=dict, summary="Get about section")
def get_about_section(service: CMSService = Depends(get_cms_service)):
    """Get about us section content."""
    data = service.get_about_section()
    return success_response(data=AboutSectionResponse.model_validate(data))


@router.put("/about", response_model=dict, summary="Update about section")
def update_about_section(
    data: AboutSectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace about us section content."""
    result = service.upsert_about_section(data)
    return success_response(
        data=AboutSectionResponse.model_validate(result),
        message="About section updated"
    )


# =============================================================================
# Services Section (Best Food Items)
# =============================================================================

@router.get("/services", response_model=dict, summary="Get services section")
def get_services_section(service: CMSService = Depends(get_cms_service)):
    """Get services/food items section content."""
    data = service.get_services_section()
    return success_response(data=ServicesSectionResponse.model_validate(data))


@router.put("/services", response_model=dict, summary="Update services section")
def update_services_section(
    data: ServicesSectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace services/food items section content."""
    result = service.upsert_services_section(data)
    return success_response(
        data=ServicesSectionResponse.model_validate(result),
        message="Services section updated"
    )


# =============================================================================
# Stats Section
# =============================================================================

@router.get("/stats", response_model=dict, summary="Get stats section")
def get_stats_section(service: CMSService = Depends(get_cms_service)):
    """Get statistics/counter section content."""
    data = service.get_stats_section()
    return success_response(data=StatsSectionResponse.model_validate(data))


@router.put("/stats", response_model=dict, summary="Update stats section")
def update_stats_section(
    data: StatsSectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace statistics/counter section content."""
    result = service.upsert_stats_section(data)
    return success_response(
        data=StatsSectionResponse.model_validate(result),
        message="Stats section updated"
    )


# =============================================================================
# Testimonials Section
# =============================================================================

@router.get("/testimonials", response_model=dict, summary="Get testimonials section")
def get_testimonials_section(service: CMSService = Depends(get_cms_service)):
    """Get customer testimonials section content."""
    data = service.get_testimonials_section()
    return success_response(data=TestimonialsSectionResponse.model_validate(data))


@router.put("/testimonials", response_model=dict, summary="Update testimonials section")
def update_testimonials_section(
    data: TestimonialsSectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace customer testimonials section content."""
    result = service.upsert_testimonials_section(data)
    return success_response(
        data=TestimonialsSectionResponse.model_validate(result),
        message="Testimonials section updated"
    )


# =============================================================================
# Gallery Section
# =============================================================================

@router.get("/gallery", response_model=dict, summary="Get gallery section")
def get_gallery_section(service: CMSService = Depends(get_cms_service)):
    """Get image gallery section content."""
    data = service.get_gallery_section()
    return success_response(data=GallerySectionResponse.model_validate(data))


@router.put("/gallery", response_model=dict, summary="Update gallery section")
def update_gallery_section(
    data: GallerySectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace image gallery section content."""
    result = service.upsert_gallery_section(data)
    return success_response(
        data=GallerySectionResponse.model_validate(result),
        message="Gallery section updated"
    )


# =============================================================================
# Footer Config
# =============================================================================

@router.get("/footer", response_model=dict, summary="Get footer config")
def get_footer_config(service: CMSService = Depends(get_cms_service)):
    """Get footer configuration and content."""
    data = service.get_footer_config()
    return success_response(data=FooterConfigResponse.model_validate(data))


@router.put("/footer", response_model=dict, summary="Update footer config")
def update_footer_config(
    data: FooterConfigCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace footer configuration and content."""
    result = service.upsert_footer_config(data)
    return success_response(
        data=FooterConfigResponse.model_validate(result),
        message="Footer config updated"
    )


# =============================================================================
# SEO Config
# =============================================================================

@router.get("/seo", response_model=dict, summary="Get SEO config")
def get_seo_config(service: CMSService = Depends(get_cms_service)):
    """Get SEO meta information."""
    data = service.get_seo_config()
    return success_response(data=SEOConfigResponse.model_validate(data))


@router.put("/seo", response_model=dict, summary="Update SEO config")
def update_seo_config(
    data: SEOConfigCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace SEO meta information."""
    result = service.upsert_seo_config(data)
    return success_response(
        data=SEOConfigResponse.model_validate(result),
        message="SEO config updated"
    )


# =============================================================================
# Offer Section
# =============================================================================

@router.get("/offers", response_model=dict, summary="Get offers section")
def get_offer_section(service: CMSService = Depends(get_cms_service)):
    """Get promotional offers section content."""
    data = service.get_offer_section()
    return success_response(data=OfferSectionResponse.model_validate(data))


@router.put("/offers", response_model=dict, summary="Update offers section")
def update_offer_section(
    data: OfferSectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace promotional offers section content."""
    result = service.upsert_offer_section(data)
    return success_response(
        data=OfferSectionResponse.model_validate(result),
        message="Offers section updated"
    )


# =============================================================================
# Popular Dishes Section
# =============================================================================

@router.get("/popular-dishes", response_model=dict, summary="Get popular dishes section")
def get_popular_dishes_section(service: CMSService = Depends(get_cms_service)):
    """Get popular dishes section content."""
    data = service.get_popular_dishes_section()
    return success_response(data=PopularDishesSectionResponse.model_validate(data))


@router.put("/popular-dishes", response_model=dict, summary="Update popular dishes section")
def update_popular_dishes_section(
    data: PopularDishesSectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace popular dishes section content."""
    result = service.upsert_popular_dishes_section(data)
    return success_response(
        data=PopularDishesSectionResponse.model_validate(result),
        message="Popular dishes section updated"
    )


# =============================================================================
# CTA Section
# =============================================================================

@router.get("/cta", response_model=dict, summary="Get CTA section")
def get_cta_section(service: CMSService = Depends(get_cms_service)):
    """Get call-to-action section content."""
    data = service.get_cta_section()
    return success_response(data=CTASectionResponse.model_validate(data))


@router.put("/cta", response_model=dict, summary="Update CTA section")
def update_cta_section(
    data: CTASectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace call-to-action section content."""
    result = service.upsert_cta_section(data)
    return success_response(
        data=CTASectionResponse.model_validate(result),
        message="CTA section updated"
    )


# =============================================================================
# Food Menu Section
# =============================================================================

@router.get("/food-menu", response_model=dict, summary="Get food menu section")
def get_food_menu_section(service: CMSService = Depends(get_cms_service)):
    """Get tabbed food menu section content."""
    data = service.get_food_menu_section()
    return success_response(data=FoodMenuSectionResponse.model_validate(data))


@router.put("/food-menu", response_model=dict, summary="Update food menu section")
def update_food_menu_section(
    data: FoodMenuSectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace tabbed food menu section content."""
    result = service.upsert_food_menu_section(data)
    return success_response(
        data=FoodMenuSectionResponse.model_validate(result),
        message="Food menu section updated"
    )


# =============================================================================
# Special Offer Section
# =============================================================================

@router.get("/special-offer", response_model=dict, summary="Get special offer section")
def get_special_offer_section(service: CMSService = Depends(get_cms_service)):
    """Get special offer with countdown section content."""
    data = service.get_special_offer_section()
    return success_response(data=SpecialOfferSectionResponse.model_validate(data))


@router.put("/special-offer", response_model=dict, summary="Update special offer section")
def update_special_offer_section(
    data: SpecialOfferSectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace special offer with countdown section content."""
    result = service.upsert_special_offer_section(data)
    return success_response(
        data=SpecialOfferSectionResponse.model_validate(result),
        message="Special offer section updated"
    )


# =============================================================================
# Chef Section
# =============================================================================

@router.get("/chef", response_model=dict, summary="Get chef section")
def get_chef_section(service: CMSService = Depends(get_cms_service)):
    """Get chef/team members section content."""
    data = service.get_chef_section()
    return success_response(data=ChefSectionResponse.model_validate(data))


@router.put("/chef", response_model=dict, summary="Update chef section")
def update_chef_section(
    data: ChefSectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace chef/team members section content."""
    result = service.upsert_chef_section(data)
    return success_response(
        data=ChefSectionResponse.model_validate(result),
        message="Chef section updated"
    )


# =============================================================================
# Client Logos Section
# =============================================================================

@router.get("/client-logos", response_model=dict, summary="Get client logos section")
def get_client_logos_section(service: CMSService = Depends(get_cms_service)):
    """Get client/partner logos section content."""
    data = service.get_client_logos_section()
    return success_response(data=ClientLogosSectionResponse.model_validate(data))


@router.put("/client-logos", response_model=dict, summary="Update client logos section")
def update_client_logos_section(
    data: ClientLogosSectionCreate,
    service: CMSService = Depends(get_cms_service)
):
    """Replace client/partner logos section content."""
    result = service.upsert_client_logos_section(data)
    return success_response(
        data=ClientLogosSectionResponse.model_validate(result),
        message="Client logos section updated"
    )
