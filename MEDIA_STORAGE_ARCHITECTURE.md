# 📸 BizFly Media & Content Storage Architecture

## Overview
BizFly uses a hybrid approach for storing visual content and structured data like menus, combining AI-generated descriptions with real media URLs and structured JSON storage.

## 🗄️ Current Storage Architecture

### 1. **Image Storage Strategy**

Currently, BizFly uses a **"descriptive placeholder" approach**:

```json
{
  "images": [
    "Hero image: Cozy restaurant interior with warm lighting",
    "Gallery image: Chef preparing signature dish",
    "Gallery image: Popular menu items display",
    "Gallery image: Outdoor patio seating area"
  ]
}
```

**Why This Approach:**
- No image hosting costs initially
- AI generates contextual descriptions
- Templates use stock photos or gradients as placeholders
- Ready for future image integration

### 2. **Menu Storage Structure**

Menus are stored as **structured JSON** in the `BusinessResearch` table:

```json
{
  "menu_items": [
    {
      "category": "Appetizers",
      "items": [
        {
          "name": "Bruschetta",
          "description": "Fresh tomatoes, basil, garlic on toasted bread",
          "price": "$8.99",
          "tags": ["vegetarian", "popular"],
          "image_description": "Golden toasted bread topped with colorful tomatoes"
        },
        {
          "name": "Calamari Fritti",
          "description": "Crispy fried squid with marinara sauce",
          "price": "$12.99",
          "tags": ["seafood", "signature"]
        }
      ]
    },
    {
      "category": "Main Courses",
      "items": [
        {
          "name": "Margherita Pizza",
          "description": "Fresh mozzarella, tomatoes, basil",
          "price": "$16.99",
          "sizes": ["Small $12.99", "Medium $16.99", "Large $19.99"],
          "tags": ["vegetarian", "classic"]
        }
      ]
    }
  ]
}
```

### 3. **Business Hours & Metadata**

Structured data stored in JSON columns:

```json
{
  "hours": {
    "monday": "11:00 AM - 10:00 PM",
    "tuesday": "11:00 AM - 10:00 PM",
    "wednesday": "11:00 AM - 10:00 PM",
    "thursday": "11:00 AM - 11:00 PM",
    "friday": "11:00 AM - 11:00 PM",
    "saturday": "10:00 AM - 11:00 PM",
    "sunday": "10:00 AM - 9:00 PM",
    "special_hours": {
      "holidays": "Closed on Thanksgiving and Christmas",
      "happy_hour": "Mon-Fri 3-6 PM"
    }
  }
}
```

## 🚀 Production-Ready Enhancement Path

### Phase 1: Image URL Storage
```python
class BusinessMedia(Base):
    __tablename__ = "business_media"
    
    id = Column(String, primary_key=True)
    business_id = Column(String, ForeignKey("businesses.id"))
    
    # Image metadata
    type = Column(Enum(MediaType))  # hero, gallery, menu, logo
    url = Column(String)  # CDN URL
    thumbnail_url = Column(String)
    alt_text = Column(String)
    caption = Column(String)
    
    # Source tracking
    source = Column(String)  # google_places, upload, ai_generated
    source_attribution = Column(String)
    
    # Organization
    display_order = Column(Integer)
    is_featured = Column(Boolean, default=False)
    tags = Column(JSON)  # ["interior", "food", "team"]
```

### Phase 2: CDN Integration
```python
# Using AWS S3 + CloudFront
class MediaService:
    def upload_image(self, file, business_id):
        # 1. Process image (resize, optimize)
        # 2. Generate unique filename
        # 3. Upload to S3
        # 4. Return CloudFront URL
        
    def generate_responsive_urls(self, base_url):
        return {
            "thumbnail": f"{base_url}?w=150&h=150",
            "small": f"{base_url}?w=400",
            "medium": f"{base_url}?w=800",
            "large": f"{base_url}?w=1200",
            "original": base_url
        }
```

### Phase 3: AI Image Generation
```python
class ImageGenerationService:
    def generate_business_images(self, business_research):
        # Use DALL-E 3 or Midjourney API
        prompts = [
            f"Professional photo of {business.name} storefront",
            f"Interior of {business.business_type} with {research.description}",
            f"Food photography of {research.specialties[0]}"
        ]
        
        for prompt in prompts:
            image_url = await self.generate_image(prompt)
            self.store_generated_image(business_id, image_url)
```

## 📊 Menu Management System

### Enhanced Menu Schema
```python
class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id = Column(String, primary_key=True)
    business_id = Column(String, ForeignKey("businesses.id"))
    
    # Basic info
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # Appetizers, Mains, Desserts
    
    # Pricing
    base_price = Column(Float)
    price_display = Column(String)  # "$12.99"
    price_variants = Column(JSON)  # {"small": 9.99, "large": 15.99}
    
    # Media
    image_url = Column(String)
    image_description = Column(String)
    
    # Metadata
    tags = Column(JSON)  # ["vegetarian", "gluten-free", "spicy"]
    nutritional_info = Column(JSON)
    ingredients = Column(JSON)
    allergens = Column(JSON)
    
    # Availability
    is_available = Column(Boolean, default=True)
    available_times = Column(JSON)  # {"lunch": true, "dinner": true}
    seasonal = Column(Boolean, default=False)
    
    # Analytics
    is_popular = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer)
```

## 🔄 Data Flow: Discovery to Display

### 1. **Google Places Discovery**
```python
# Initial data from Google Places
{
    "photos": [
        {
            "photo_reference": "Aap_uEA7vb0...",
            "height": 2268,
            "width": 4032,
            "html_attributions": ["<a href='...'>John Doe</a>"]
        }
    ]
}

# Convert to our storage
business_media.url = google_places.get_photo_url(photo_reference)
business_media.source = "google_places"
business_media.source_attribution = html_attributions[0]
```

### 2. **AI Research Enhancement**
```python
# Claude analyzes business and suggests images
research_agent.suggest_images(business) -> [
    "Modern Italian restaurant interior with exposed brick",
    "Wood-fired pizza oven in action",
    "Fresh pasta being made by hand",
    "Outdoor seating area with string lights"
]
```

### 3. **Template Rendering**
```javascript
// Templates intelligently handle available media
const HeroSection = ({ business }) => {
  if (business.media?.hero) {
    return <img src={business.media.hero.url} alt={business.media.hero.alt_text} />
  } else if (business.images?.length > 0) {
    // Use AI-generated placeholder with description
    return <AIPlaceholder description={business.images[0]} />
  } else {
    // Fallback to gradient or pattern
    return <GradientHero businessType={business.type} />
  }
}
```

## 🎯 Smart Features

### 1. **Automatic Image Sourcing**
- Pull from Google Places photos
- Scrape Facebook/Instagram (with permission)
- Generate with AI (DALL-E 3)
- Accept user uploads
- Use category-based stock photos

### 2. **Menu Intelligence**
- OCR menu photos to extract items
- Parse prices and descriptions
- Categorize automatically
- Identify popular items from reviews
- Generate descriptions with AI

### 3. **Content Versioning**
```python
class ContentVersion(Base):
    __tablename__ = "content_versions"
    
    id = Column(String, primary_key=True)
    business_id = Column(String, ForeignKey("businesses.id"))
    version_number = Column(Integer)
    content_snapshot = Column(JSON)  # Full content at this version
    changed_fields = Column(JSON)    # What changed
    change_source = Column(String)   # "ai_research", "user_edit", "import"
    created_at = Column(DateTime)
```

## 💾 Storage Costs & Optimization

### Current (Development)
- **Images**: Text descriptions only (0 cost)
- **Menus**: JSON in database (~1KB per restaurant)
- **Total**: ~5KB per business

### Production Estimates
- **Images**: 5-10 images × 200KB average = 1-2MB
- **CDN**: $0.085/GB transfer (CloudFront)
- **Storage**: $0.023/GB/month (S3)
- **At 1000 businesses**: ~2GB storage = $0.05/month

### Optimization Strategies
1. **Lazy Loading**: Only load images when needed
2. **Progressive Enhancement**: Low-res → high-res
3. **Smart Caching**: CDN + browser caching
4. **Responsive Images**: Different sizes for different devices
5. **WebP Format**: 30% smaller than JPEG

## 🔮 Future Enhancements

### 1. **360° Virtual Tours**
- Store panoramic images
- Link to Google Street View
- Generate with AI

### 2. **Video Content**
- Welcome videos
- Chef interviews
- Behind-the-scenes

### 3. **Dynamic Menus**
- Real-time availability
- Daily specials API
- Price updates

### 4. **User-Generated Content**
- Customer photos
- Review images
- Social media integration

## Implementation Priority

1. **Phase 1** (Current): JSON storage + AI descriptions ✅
2. **Phase 2** (Next): Google Places photo integration
3. **Phase 3**: User uploads + S3 storage
4. **Phase 4**: AI image generation
5. **Phase 5**: Full media management system

This architecture ensures BizFly can start lean with text-based storage while being ready to scale to full media management as the platform grows!