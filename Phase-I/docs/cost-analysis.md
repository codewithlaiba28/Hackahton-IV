# Cost Analysis: Course Companion FTE

## Executive Summary

The Course Companion FTE implements a **Zero-Backend-LLM architecture** for Phase 1, achieving **99% cost savings** compared to traditional LLM-backed educational platforms.

---

## Phase 1 Cost Structure (Zero-Backend-LLM)

### Infrastructure Costs (Monthly, 10K Users)

| Component | Service | Cost Model | Est. Monthly Cost |
|-----------|---------|------------|-------------------|
| **Cloudflare R2** | Content Storage | $0.015/GB + $0.36/M reads | ~$5.00 |
| **PostgreSQL** | Neon Serverless | Free tier → $25/mo | $0 - $25.00 |
| **Compute** | Fly.io/Railway | ~$5-20/mo | ~$10.00 |
| **Domain + SSL** | Namecheap | ~$12/year | ~$1.00 |
| **TOTAL** | | | **$16 - $41** |
| **Cost per User** | | | **$0.002 - $0.004** |

### Cost Breakdown Details

#### 1. Cloudflare R2 (~$5/month)

```
Storage: 5 chapters × 50KB each = 250KB → $0.000004/month
Bandwidth: 10K users × 50KB × 3 visits = 1.5GB → $0.02/month
Read Operations: 10K users × 3 reads = 30K reads → $0.01/month
Class A Operations: 30K × $4.00/M = $0.12/month
Class B Operations: Minimal → $0.01/month

Total R2: ~$5/month (with buffer for growth)
```

#### 2. PostgreSQL - Neon (~$0-25/month)

```
Free Tier:
- 0.5 GB storage
- 50,000 compute units/month
- Sufficient for 10K users

Paid Tier (if needed):
- $25/month for 5GB storage
- Higher compute limits
```

#### 3. Compute - Fly.io (~$10/month)

```
Free Tier:
- 3 shared CPU VMs (256MB each)
- 3GB persistent volume

Paid (for production):
- 1x shared-cpu-1x: $5.50/month
- 1GB volume: $0.15/month
- Bandwidth: 160GB outbound (free)

Total: ~$10/month
```

---

## Phase 2 Cost Structure (Hybrid Intelligence)

### Additional LLM Costs (Premium Features Only)

| Feature | Model | Tokens/Request | Cost/Request | Est. Monthly (1K premium users) |
|---------|-------|----------------|--------------|---------------------------------|
| Adaptive Path | Claude Sonnet | ~2,000 | $0.018 | $180 |
| LLM Assessment | Claude Sonnet | ~1,500 | $0.014 | $140 |
| Synthesis | Claude Sonnet | ~3,000 | $0.027 | $270 |
| Mentor Session | Claude Sonnet | ~10,000 | $0.090 | $900 |

### Phase 2 Total (10K users, 1K premium)

| Component | Cost |
|-----------|------|
| Infrastructure (Phase 1) | $41 |
| LLM Costs (premium only) | $1,490 |
| **TOTAL** | **$1,531/month** |
| **Cost per User (avg)** | **$0.15** |
| **Cost per Premium User** | **$1.49** |

---

## Revenue Projections

### Monetization Tiers

| Tier | Price | Features | Target Conversion |
|------|-------|----------|-------------------|
| Free | $0 | First 3 chapters, basic quizzes | 80% (8K users) |
| Premium | $9.99/mo | All chapters, progress tracking | 15% (1.5K users) |
| Pro | $19.99/mo | Premium + Adaptive Path + LLM Assessments | 5% (500 users) |

### Monthly Revenue (10K Users)

```
Premium: 1,500 × $9.99 = $14,985
Pro: 500 × $19.99 = $9,995
Total Revenue: $24,980/month
```

### Profit Margins

| Phase | Revenue | Costs | Profit | Margin |
|-------|---------|-------|--------|--------|
| Phase 1 | $5,000* | $41 | $4,959 | 99.2% |
| Phase 2 | $24,980 | $1,531 | $23,449 | 93.8% |

*Phase 1 assumes only Premium tier (no Pro features)

---

## Cost Optimization Strategies

### Phase 1 (Zero-Backend-LLM)

1. **Use Cloudflare R2** instead of S3 (52% cheaper)
2. **Neon Serverless** for PostgreSQL (free tier for small scale)
3. **Fly.io** for compute (generous free tier)
4. **LRU Caching** in R2 service (reduce read operations)
5. **CDN** for static content (reduce bandwidth costs)

### Phase 2 (Hybrid)

1. **Premium Gating**: Only premium users trigger LLM calls
2. **User-Initiated**: LLM features only on explicit request
3. **Token Optimization**: Careful prompt engineering
4. **Model Selection**: Use cheaper models where possible
5. **Caching**: Cache LLM responses for common queries
6. **Rate Limiting**: Prevent abuse of premium features

---

## Comparison: Human Tutor vs Digital FTE

| Metric | Human Tutor | Digital FTE (Phase 1) | Savings |
|--------|-------------|----------------------|---------|
| Monthly Cost | $2,000 - $5,000 | $41 | 99% |
| Availability | 40 hours/week | 168 hours/week | 320% more |
| Students Served | 20-50 | Unlimited | ∞ |
| Cost per Session | $50 | $0.004 | 99.99% |
| Consistency | 85-95% | 99%+ | +4-14% |

---

## Break-Even Analysis

### Development Costs (One-Time)

| Item | Cost |
|------|------|
| Development Team (4 × 2 weeks) | $16,000 |
| Design & UX | $2,000 |
| Testing & QA | $2,000 |
| **Total** | **$20,000** |

### Break-Even Timeline

```
Phase 1 Revenue: $5,000/month
Phase 1 Costs: $41/month
Phase 1 Profit: $4,959/month

Break-Even: $20,000 / $4,959 = 4 months
```

---

## Key Takeaways

1. **Zero-Backend-LLM is 100x cheaper** than hybrid approaches
2. **Phase 1 achieves 99%+ profit margins**
3. **Hybrid features should be premium-gated** to maintain margins
4. **Cost scales sub-linearly** with user growth
5. **Digital FTE is 99% cheaper** than human tutoring

---

## Appendix: Cost Calculation Formulas

### R2 Costs

```
Storage Cost = GB Stored × $0.015/GB/month
Bandwidth Cost = GB Transferred × $0.01/GB
Read Operations = Millions of Reads × $0.36/M
Write Operations = Millions of Writes × $4.50/M
```

### LLM Costs (Claude Sonnet)

```
Cost per Request = (Input Tokens × $3/M + Output Tokens × $15/M) / 1,000,000
Monthly LLM Cost = Requests per Month × Cost per Request
```

### Profit Margin

```
Margin = (Revenue - Costs) / Revenue × 100
```

---

*Last Updated: January 2026*
*Assumptions: 10K monthly active users, 15% premium conversion*
