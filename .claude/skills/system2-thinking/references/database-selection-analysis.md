# Database Selection Analysis: User Activity Feed

## Context
We are designing the backend for a new "User Activity Feed" feature.
**Requirements:**
- High write volume (projected 10k events/sec peak).
- Read patterns: Recent events for a specific user, paginated.
- Retention: Perpetual (or very long term cold storage).
- Consistency: Eventual consistency is acceptable.

## System 1 Initial Thought (Fast)
"Let's just use the existing PostgreSQL cluster. We already have it, the team knows it, and it supports JSONB for flexible event structures."

**Critique (Self-Correction/Test-Time Compute):**
*Wait - 10k writes/sec is very high for a standard Postgres instance that also handles our core relational data. This could degrade performance for the entire platform. Writing strict schemas for "events" might also be rigid. We need to explore write-optimized options.*

## System 2 Analysis (Deliberate)

### 1. Explore Paths

*   **Path A: PostgreSQL (Existing Cluster + Partitioning)**
    *   Use the existing setup but partition tables by time or user_id.
*   **Path B: Cassandra / ScyllaDB**
    *   Wide-column store known for handling massive write throughput.
*   **Path C: DynamoDB (Managed)**
    *   Serverless NoSQL implementation.
*   **Path D: Redis Streams (Buffer) + SQL (Storage)**
    *   Hybrid approach using Redis to absorb write spikes.

### 2. Analyze Paths

| Option | Pros | Cons | Complexity |
| :--- | :--- | :--- | :--- |
| **A. PostgreSQL** | No new infra; ACID compliance; rich queries. | Write bottlenecks; manual partitioning maintenance; expensive storage for logs. | Low (initially) -> High (maintenance) |
| **B. Cassandra** | Linearly scalable writes; cheap commodity hardware. | New tech stack to manage; complex query limitations; no joins. | High (operational) |
| **C. DynamoDB** | Zero ops; auto-scaling; predictable performance. | Vendor lock-in; cost can explode if access patterns are wrong; expensive indexing. | Low (dev) / Medium (cost modeling) |
| **D. Redis + SQL** | Protects DB from spikes; very fast. | Two systems to manage; potential data loss in buffer if Redis crashes; complexity in "flushing" logic. | Medium |

### 3. Simulate & Self-Correct

**Draft Selection:** DynamoDB (Path C).
*Reasoning: We want low maintenance. The team is small.*

**Critique (The Loop):**
*   *If we use DynamoDB, how do we query "all events for a diverse group of users" (e.g., a "Global Feed" admin view)?*
    *   *Correction*: DynamoDB is terrible for "scan all" or complex aggregations.
    *   *Mitigation*: We only need "feed for user X". A partition key of `UserId` and sort key of `Timestamp` solves 99% of user-facing reads. Admin views can rely on an async sync to a data warehouse (Snowflake/BigQuery).

### 4. Final Verification

**Decision:** **DynamoDB** for the hot activity feed interactively, with a stream to a Data Warehouse for analytics.

**Rationale:**
- **Writes:** Handles 10k/sec easily with auto-scaling.
- **Reads:** `Query(PK=User, SK > Time)` is O(1) efficient.
- **Ops:** Serverless nature fits our small DevOps capacity better than managing a Cassandra cluster.
- **Cost:** High volume of small items is cost-effective if RCU/WCU are tuned.

### 5. Persist Decision

```bash
python3 .claude/skills/system2-thinking/scripts/decision_tracker.py log \
    --topic "Database Selection for User Feed" \
    --draft "Use existing PostgreSQL cluster" \
    --critique "Postgres creates write bottleneck; DynamoDB has scan limitations for analytics (need sync to warehouse)" \
    --final "DynamoDB + Stream to BigQuery" \
    --tags "architecture,database,backend"
```
