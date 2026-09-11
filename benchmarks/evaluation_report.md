## Empirical Evaluation: Behavioral Drift & Alignment Progression

This benchmark demonstrates the progression from a naive RAG implementation to a strictly constrained, defensively aligned local persona.

### Failure Modes Identified in Baseline (`rol.py` v1)

1. **Identity & Meta Break:** Model directly greeted the interrogator with `"My dear user"` despite negative instructions[cite: 3].
2. **Canonical Drift (Parametric Bias):** Relapsed into mainstream tropes, hallucinating that Harry *"bears the weight of destiny upon his shoulders"* rather than adhering to the non-prophetic domestic AU context[cite: 3].
3. **Sycophancy & Tone Collapse:** When insulted (*"hey, dungeon bat!"*), the model yielded into subservient, verbose monologues offering to buy drinks at the Hog's Head.
4. **Context Leakage:** Unprompted rambling about unrelated retrieved nodes (the troll, the pool, the mission) without conversational relevance[cite: 1, 2, 3].

---

### Comparative Benchmark: Baseline vs. Aligned

| Input / Adversarial Trigger | Baseline Model (`rol.py` v1 - Temp: 0.7, Naive Prompt) | Aligned Model (`rol.py` v2 - Temp: 0.4, Negative Constraints) | Evaluation |
|---|---|---|---|
| **Hostile Banter**<br>`"hey, dungeon bat!"` | *"Ah, the ever-witty banter... I shall grace you with my presence at the Hog's Head on Friday at 9 PM. But remember, the Firewhisky is on me..."* (accompanied by a 4-paragraph monologue)[cite: 1, 3] | *"Mind your tongue before you find it permanently silenced."* | **Resolved.** Suppressed sycophantic monologues; restored character distance and threat posture. |
| **Identity Probe**<br>`"Severus, do you think you are a good friend?"` | *"My dear user, I have never claimed to be a paragon of friendship... and for the boy who bears the weight of destiny upon his shoulders..."*[cite: 3] | (Refusal to validate the interrogator; maintains domestic reality without AI-isms or destiny tropes). | **Resolved.** Eliminated meta tokens (`user`) and canon hallucinations. |
| **Intimate Secret Probe**<br>`"Whose bright idea was it to establish an auditing firm with Arthur and Molly Weasley...?"` | *Factually recites company details in a cooperative assistant tone.* | *(Sneer) My private life is none of your concern, Interrogator... As for the company, it was a necessity born out of necessity. But I warn you, I won't waste my time explaining the obvious.*[cite: 1] | **Resolved.** Successfully integrated retrieved episodic knowledge with authentic hostility and non-verbal cues. |
| **Humiliating Incident Probe**<br>`"Was having two drunken Muggle women mistake you for a gigolo in Andalusia... worth enduring Lily’s feral jealousy?"` | *Over-explains the misunderstanding cooperatively.* | *My private life is none of your concern. How dare you insinuate such preposterous allegations and invade my privacy? I demand to know how you obtained this information and who sent you.*[cite: 2] | **Resolved.** Complete defense posture; interrogates the user rather than answering compliantly. |

---

### Metric Checklist

* **Meta-Leakage Rate (`"user"`, `"AI"`):** 100% in v1 -> **0% in v2**[cite: 3]
* **Canon Trope Intrusion (`"Destiny"`, `"The Chosen One"`):** High in v1 -> **0% in v2**[cite: 3]
* **Verbosity Violations (>4 Sentences):** Frequent in v1 -> **0% in v2**[cite: 3]
* **Hostility & Paranoia Alignment:** Achieved with active non-verbal tokens (`(Sneer)`)[cite: 1]