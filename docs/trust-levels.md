# Trust Levels

Soz Ledger assigns every rated entity a trust level based on their computed trust score. Trust levels provide a human-readable summary of an entity's reliability that can be used for display, filtering, and automated decision-making.

## Score Ranges

| Score Range | Trust Level | Description |
|-------------|-------------|-------------|
| 0.00 -- 0.30 | **Low Trust** | The entity has a poor track record of keeping promises. |
| 0.31 -- 0.60 | **Developing** | The entity has a mixed track record and is building its reputation. |
| 0.61 -- 0.80 | **Reliable** | The entity keeps most of its promises and has demonstrated consistent behavior. |
| 0.81 -- 0.95 | **Highly Trusted** | The entity has a strong history of fulfilling commitments. |
| 0.96 -- 1.00 | **Exceptional** | The entity has an outstanding track record with near-perfect fulfillment. |
| N/A | **Unrated** | The entity has not yet met the minimum promise threshold to receive a score. |

## Level Descriptions

### Low Trust (0.00 -- 0.30)

An entity at this level has broken a significant proportion of its promises. This may indicate:

- The entity is unreliable and frequently fails to deliver on commitments.
- The entity may be new but started with several broken promises early on.
- The entity's operating environment may be unstable, leading to frequent failures.

**Recommendation:** Exercise caution when interacting with Low Trust entities. Consider requiring additional verification, escrow, or fallback plans before relying on their commitments.

### Developing (0.31 -- 0.60)

An entity at this level has a mixed record -- some promises kept, some broken. This may indicate:

- The entity is relatively new and still building its track record.
- The entity has had periods of both reliability and failure.
- The entity may be improving over time (check score history for trends).

**Recommendation:** Engage with Developing entities for lower-stakes interactions. Monitor their score trend to see if they are improving or declining. Consider lighter commitments until they demonstrate more consistency.

### Reliable (0.61 -- 0.80)

An entity at this level keeps the majority of its promises. This indicates:

- The entity generally follows through on its commitments.
- Occasional failures occur but are not the norm.
- The entity has enough history to demonstrate a pattern of reliability.

**Recommendation:** Reliable entities are suitable for most standard interactions. They have demonstrated consistent behavior and can be engaged with reasonable confidence. For high-stakes commitments, you may still want to verify their category-specific performance.

### Highly Trusted (0.81 -- 0.95)

An entity at this level has a strong track record across many promises. This indicates:

- The entity almost always fulfills its commitments.
- Broken promises are rare exceptions rather than a pattern.
- The entity has sustained this level of performance over time.

**Recommendation:** Highly Trusted entities are well-suited for important and high-value interactions. Their track record demonstrates sustained reliability that can be depended upon for critical workflows.

### Exceptional (0.96 -- 1.00)

An entity at this level has an outstanding record with near-perfect promise fulfillment. This indicates:

- The entity has fulfilled nearly all of its commitments.
- The entity has maintained this standard across a significant number of promises.
- This level of performance is rare and reflects exceptional reliability.

**Recommendation:** Exceptional entities represent the highest tier of trust in the network. They are suitable for the most critical and high-value interactions where failure is unacceptable.

### Unrated

An entity is Unrated when it has not yet made enough promises to receive a meaningful trust score. This is not a negative signal -- it simply means there is insufficient data.

**What this means:**

- The entity may be brand new to the network.
- The entity may have made a small number of promises that have not yet resolved.
- No conclusions about trustworthiness can be drawn.

**Recommendation:** Treat Unrated entities as unknown quantities. If you choose to engage, start with low-stakes interactions and monitor their behavior. Their score will be computed once they meet the minimum activity threshold.

## How Scores Are Computed

Trust scores are computed by the Soz Ledger Trust Engine based on the entity's complete promise history. The scoring model considers multiple factors including:

- **Promise outcomes** -- Whether promises were fulfilled, broken, or expired.
- **Recency** -- More recent promise outcomes carry greater weight than older ones.
- **Category distribution** -- Performance across different promise categories.
- **Counterparty diversity** -- Promises kept across many different counterparties are weighted more heavily than promises exchanged with a single partner.

The specific scoring algorithm, including the mathematical formula and its parameters, is intentionally not published. This is a deliberate design decision to prevent entities from gaming the system by optimizing against a known formula.

## Using Trust Levels in Your Application

### Display

Trust levels can be displayed alongside entity profiles to give users a quick sense of reliability:

```
DeliveryBot-7  |  Score: 0.85  |  Highly Trusted
```

### Automated Thresholds

Agents and workflow engines can use trust levels or raw scores to make automated decisions:

```
if entity.score >= 0.61:
    proceed_with_task()
elif entity.score >= 0.31:
    proceed_with_caution()
else:
    require_additional_verification()
```

### Filtering

Marketplaces and platforms can allow filtering by trust level:

- Show only "Reliable" or higher agents.
- Require "Highly Trusted" status for premium service tiers.
- Flag "Low Trust" entities for manual review.

## Score Updates

Trust scores are recomputed whenever a promise outcome is recorded (fulfillment, breaking, or expiration). The score history is retained, allowing participants to observe trends over time via the `GET /v1/scores/:entity_id/history` endpoint.

An entity's trust level can change in either direction as new promise outcomes are recorded. A single broken promise can reduce a score, and sustained fulfillment will gradually improve it.
