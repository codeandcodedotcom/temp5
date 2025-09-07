**Endpoint**  
```
POST /api/generation/ask
Content-Type: application/json
Authorization: Bearer <JWT or API_KEY>   # (auth method TBD)
```

---

## Request (frontend -> backend)

```json
{
  "project_name": "CRM Upgrade Initiative",
  "sponsor": "Alice Smith",
  "metadata": {
    "department": "Sales",
    "submission_date": "2025-09-07T12:00:00Z"
  },
  "answers": [
    {
      "id": "q1",
      "question": "Do you have approved budget?",
      "answer": "Yes",
      "score": 5
    },
    {
      "id": "q2",
      "question": "Project type",
      "answer": "Infrastructure",
      "score": 3
    },
    {
      "id": "q3",
      "question": "Expected budget",
      "answer": "Between 11-100 million",
      "score": 3
    }
  ],
  "additional_context": "This project is high-priority for Q4 deliveries."
}
```


---

## Response (backend -? frontend)

```json
{
  "project_title": "CRM Upgrade Initiative",
  "project_description": "Migration of legacy CRM to Salesforce to improve scalability and customer data management.",
  "project_budget": "Estimated 50 million USD",
  "complexity_score": 3,
  "recommended_pm_count": 2,
  "key_risks": [
    "Data migration challenges",
    "Integration delays"
  ],
  "supporting_documents": [
    {
      "id": "doc-001",
      "source": "Policies/Procurement.pdf",
      "excerpt": "Procurement approval required for >$1M",
      "score": 0.95
    }
  ],
  "diagnostics": {
    "used_top_k": 3,
    "retrieval_time_ms": 120,
    "generation_time_ms": 890
  }
}
```
