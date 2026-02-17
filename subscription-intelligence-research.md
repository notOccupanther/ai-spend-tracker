# Subscription Intelligence Service - Research Phase

## Project Overview
**Goal:** Create an automated newsletter tracking SaaS pricing changes across critical business tools
**Target:** Small to medium businesses, freelancers, and team leads who need to budget for SaaS costs
**Value Prop:** Early warning system for price increases + strategic insights on SaaS market trends

## Phase 1: Target SaaS Tools Research

### Selection Criteria
- **High business impact:** Tools that significantly affect operational budgets
- **Volatile pricing:** Services known for frequent price changes or sudden increases  
- **Wide adoption:** Popular tools with large user bases
- **Critical workflow dependency:** Services that are hard to replace quickly

### Target Categories

#### **Productivity & Collaboration (High Priority)**
- Slack (known for pricing volatility)
- Microsoft 365 / Teams
- Google Workspace 
- Notion (frequent tier adjustments)
- Zoom (post-pandemic pricing shifts)
- Asana
- Trello/Atlassian Suite
- Monday.com
- ClickUp

#### **Development & Technical (High Priority)**
- GitHub (Microsoft-owned, pricing changes common)
- GitLab
- AWS (core services - EC2, S3, RDS)
- Google Cloud Platform
- Microsoft Azure
- Vercel
- Netlify
- Heroku
- Docker Hub
- npm Pro

#### **Marketing & Sales (Medium Priority)**
- HubSpot (notorious for price increases)
- Salesforce
- Mailchimp
- ConvertKit
- ActiveCampaign
- Zapier (automation tax gets expensive)
- Canva Pro
- Buffer/Hootsuite
- Typeform

#### **Design & Creative (Medium Priority)**
- Adobe Creative Cloud
- Figma (recent pricing changes)
- Sketch
- InVision
- Loom

#### **Finance & Operations (Lower Priority)**
- QuickBooks
- Xero  
- Stripe (processing fees)
- PayPal Business

## Pricing Page Analysis Results

### Current Pricing Snapshots (Feb 2026)
**Notion:**
- Free: Limited blocks (for teams), 7-day history, 5MB uploads
- Plus: $10/user/month - Unlimited blocks, 30-day history, unlimited uploads  
- Business: $18/user/month - 90-day history, advanced features
- Enterprise: Custom pricing - Unlimited history, enterprise features

**GitHub:** (From documentation review)
- Complex tiered pricing with metered billing for Actions, storage, etc.
- Billing cycles vary by account type
- Both monthly and annual options available

### Scrapability Assessment
- **Notion**: Clean pricing page structure, scrapable ✅
- **GitHub**: More complex, but documentable ✅  
- **Need to test**: Slack, HubSpot, Salesforce pricing pages

### Content Validation
Based on research, valuable newsletter content would include:
1. **Price increase alerts** with percentage changes and timeline
2. **Feature migration warnings** (when features move to higher tiers)
3. **New tier introductions** that affect existing users
4. **Billing model changes** (per-seat to usage-based, etc.)
5. **Historical context** - "Last increase was X years ago"
6. **Cost impact calculator** for different team sizes

## Next Steps
1. **Create sample newsletter** to validate content format
2. **Technical architecture** planning
3. **Validate target list** with Niall
4. **Identify data sources** - pricing pages, changelogs, press releases

## Questions for Niall
- Any specific tools you've been burned by with surprise price increases?
- Should we focus on Irish/EU businesses first or go global from start?
- Preferred newsletter frequency - weekly/bi-weekly/monthly?
- Would you want cost impact analysis per company size (5, 10, 25, 50+ users)?