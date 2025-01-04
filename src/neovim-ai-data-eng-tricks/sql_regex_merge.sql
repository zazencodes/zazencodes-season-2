WITH RankedMatches AS (
    SELECT
        p.url,
        p.revenue,
        pc.category,
        pc.pattern,
        ROW_NUMBER() OVER (
            PARTITION BY p.url
            ORDER BY pc.priority, pc.pattern
        ) as match_rank
    FROM product_urls p
    JOIN product_categories pc
        ON REGEXP_CONTAINS(p.url, pc.pattern)
    /* Add WHERE clause here to pre-filter data if possible */
    WHERE p.revenue > 0
)
SELECT
    url,
    revenue,
    category
FROM RankedMatches
WHERE match_rank = 1
/* Add appropriate ORDER BY if needed for downstream processing */
/* Consider these table optimizations:
- Add clustering on url column in product_urls
- Add partitioning on date columns if they exist
- Create materialized view for frequently accessed patterns
- Index the pattern column in product_categories
- Pre-compile common regex patterns
*/;
