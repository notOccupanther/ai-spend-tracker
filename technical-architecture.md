# Subscription Intelligence Service - Technical Architecture

## System Overview
Automated SaaS pricing monitoring → Change detection → Content generation → Newsletter distribution

## Core Components

### 1. Data Collection Layer
**Web Scrapers**
- Python/Playwright for dynamic pricing pages
- Scheduled scraping (daily/weekly per tool)
- Screenshot capture for visual changes
- Structured data extraction (JSON format)

**Data Sources**
- Primary: Company pricing pages  
- Secondary: Press releases, changelogs, social media
- Tertiary: Industry news sites (TechCrunch, Product Hunt)

**Storage Schema**
```json
{
  "company": "notion",
  "timestamp": "2026-02-17T09:00:00Z",
  "pricing_tiers": [
    {
      "name": "Plus",
      "price_monthly": 10,
      "price_annual": 8,
      "features": ["unlimited_blocks", "30_day_history"],
      "limits": {"guests": 100}
    }
  ],
  "page_hash": "abc123...",
  "screenshot_url": "s3://bucket/notion-2026-02-17.png"
}
```

### 2. Change Detection Engine
**Algorithm**
- JSON diff comparison between scraping runs
- Semantic analysis for feature descriptions  
- Price percentage change thresholds (>5% = alert)
- New tier detection via schema comparison

**Alert Triggers**
- Price increases/decreases >5%
- New tiers introduced
- Features moved between tiers  
- Billing model changes (per-seat → usage-based)
- Terms changes (free trial duration, etc.)

### 3. Content Generation Pipeline
**AI Content Creation**
- GPT-4 for newsletter copy generation
- Template-based sections (alerts, trends, tips)
- Context injection (historical data, market trends)
- Tone consistency (professional but accessible)

**Human-in-the-Loop**
- Review queue for major changes
- Editorial calendar for feature content
- Fact-checking against primary sources

### 4. Distribution System
**Email Platform**
- ConvertKit or Mailchimp for delivery
- Segmentation by subscriber interests
- A/B testing for subject lines
- Analytics tracking (open rates, clicks)

**Web Presence**
- Newsletter archive (public)
- Pricing database (searchable)
- API for pricing data (future monetization)

## Implementation Phases

### Phase 1: Manual MVP (Week 1-2)
- Static website with newsletter signup
- Manual content creation for 3-4 issues
- 25 target SaaS tools identified
- Basic email list via ConvertKit

### Phase 2: Automated Collection (Week 3-4)  
- Web scraping infrastructure
- Database setup (PostgreSQL)
- Change detection algorithms
- Admin dashboard for monitoring

### Phase 3: Content Automation (Week 5-6)
- AI content generation pipeline
- Editorial review workflow
- Automated newsletter scheduling
- Performance analytics

### Phase 4: Scale & Monetization (Week 7+)
- Expand to 50+ tools
- Premium tier (faster alerts, API access)
- Enterprise dashboard for procurement teams
- Industry-specific newsletters

## Technology Stack

**Backend**
- Python (FastAPI) for APIs
- PostgreSQL for data storage
- Redis for caching
- Celery for background tasks

**Scraping & Monitoring**  
- Playwright for browser automation
- Beautiful Soup for HTML parsing
- Selenium for complex JS sites
- Scrapy for large-scale scraping

**Frontend**
- Next.js for newsletter archive
- Tailwind CSS for styling
- Vercel for hosting

**Infrastructure**
- AWS/Railway for hosting
- GitHub Actions for CI/CD
- CloudWatch for monitoring
- S3 for screenshot storage

## Cost Estimates

**Monthly Operating Costs (Phase 1)**
- Hosting: $25-50 (Railway/Vercel)
- Email service: $20-100 (based on subscribers)
- AI API costs: $30-100 (GPT-4 usage)  
- Total: ~$75-250/month

**Development Time**
- Phase 1 (MVP): 40-60 hours
- Phase 2 (Automation): 60-80 hours  
- Phase 3 (AI Content): 40-60 hours
- Phase 4 (Scale): 80-120 hours

## Risk Mitigation

**Anti-Bot Measures**
- Rotate user agents and IP addresses
- Respect robots.txt and rate limits
- Use residential proxies if needed
- Fallback to manual collection for blocked sites

**Data Quality**
- Multiple source verification
- Human review for major changes
- Screenshot comparisons for visual validation
- Subscriber feedback loop for corrections

**Legal Considerations**
- Focus on publicly available pricing information
- Avoid reproducing copyrighted content
- Clear attribution and fair use guidelines
- Terms of service compliance

## Success Metrics

**Phase 1 KPIs**
- 100+ email subscribers
- >25% email open rate
- 3-5 pieces of valuable pricing intel per week
- Positive subscriber feedback

**Growth Targets**
- Month 3: 500 subscribers
- Month 6: 2,000 subscribers  
- Month 12: 10,000 subscribers
- Revenue target: $5K MRR by month 12

## Next Actions
1. **Validate subscriber demand** - Simple landing page + signup
2. **Technical proof-of-concept** - Scrape 5 target sites successfully  
3. **Content validation** - Publish 2-3 manual newsletters
4. **Feedback loop** - Survey early subscribers for content preferences