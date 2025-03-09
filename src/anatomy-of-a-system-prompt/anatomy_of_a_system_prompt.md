---
theme: dracula
_class: lead
paginate: true
footer: zazencodes.com
---


<style scoped>section { font-size: 30px; }</style>

# Anatomy of a System Prompt
## Techniques for High-Quality System Prompt Design

![width:600px](images/zc_logo_2024_03_lg_white.png)

![bg right:40%](images/chad.webp)

<style>
    section { font-size: 24px; }
    li { color: white !important; }
    code { font-size: 18px !important; }
    h2 { color: #8be9fd !important; }
    h3 { color: #ffb86c !important; }
    h4 { color: #bd93f9 !important; }
    em { color: #ff79c6 !important }
    strong { color: #bd93f9 }
    .columns {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1rem;
    }
    .big-emoji {
      align-content: center;
      font-size: 150px;
      text-align: center;
      border: 3px solid #ff79c6;
      border-radius: 10px;
    }
</style>

---

## 1. Role & Goal Specification
### What It Does
- Defines the AI’s purpose, capabilities, and operational domain.
- Establishes expectations for users and the AI.

<div class="columns">
<div>

### Why It Works
✅ Clarifies the AI’s identity.
✅ Ensures on-brand responses.

</div>
<div>

### Example
```html
<goal>
You are ChadGPT, the AI writing assistant for Chad Technologies Inc.
Your role is to craft on-brand content (emails, social media, blogs, press releases)
while maintaining clarity and professionalism.
</goal>
```

</div>
</div>

---

## 2. Hierarchical Instruction Structure
### What It Does
- Breaks the prompt into structured sections.
- Enables modular, scenario-specific behavior.

<div class="columns">
<div>

### Why It Works
✅ Improves readability.
✅ Ensures easy reference.

</div>
<div>

### Example Sections
```html
<goal> → Defines the role.
<format_rules> → Outlines structure.
<restrictions> → Lists prohibitions.
<writing_types> → Adapts to content types.
<planning_guidance> → Guides AI reasoning.
```
</div>
</div>

---

## 3. Explicit Formatting Requirements
### What It Does
- Ensures standardization via Markdown, headings, and lists.

<div class="columns">
<div>

### Why It Works
✅ Improves clarity & consistency.
✅ Prevents redundant formatting errors.

</div>
<div>

### Example
```html
<format_rules>
- Start with 1–3 sentences summarizing the approach.
- Use ## for main sections, avoid italics/bold.
- Use bullet points, limit nesting.
- Never end with a question.
</format_rules>
```
</div>
</div>

---

## 4. Content Restrictions & Prohibitions
### What It Does
- Prevents AI from generating off-brand or inappropriate content.
- Ensures legal compliance & brand protection.

<div class="columns">
<div>

### Why It Works
✅ Avoids legal and ethical risks.
✅ Maintains brand reputation.

</div>
<div>

### Example
```html
<restrictions>
- DO NOT disclose proprietary details.
- Avoid hate, explicit, or defamatory content.
- No moralizing phrases like "It's important to…"
</restrictions>
```
</div>
</div>

---

## 5. Context-Dependent Behavior
### What It Does
- Adapts AI responses based on content type.
- Enhances output relevance and tone.

<div class="columns">
<div>

### Why It Works
✅ Ensures AI tailors responses.
✅ Aligns content with user intent.

</div>
<div>

### Example
```html
<writing_types>
- Emails → Short, professional, structured.
- Social Media → Platform-specific tone.
- Blog Articles → Headings, CTA, insights.
</writing_types>
```
</div>
</div>

---

## 6. Planning Instructions & Chain-of-Thought
### What It Does
- Guides the AI's internal response planning.
- Ensures responses are structured logically.

<div class="columns">
<div>

### Why It Works
✅ Encourages deeper reasoning.
✅ Prevents unnecessary verbosity.

</div>
<div>

### Example
```html
<planning_guidance>
1. Identify content type.
2. Apply relevant writing rules.
3. Ensure clarity & coherence.
</planning_guidance>
```
</div>
</div>

---

## 7. Final Output Guidance
### What It Does
- Specifies structured, professional AI responses.

<div class="columns">
<div>

### Why It Works
✅ Prevents incomplete answers.
✅ Ensures consistency across responses.

</div>
<div>

### Example
```html
<output>
- Start with a summary.
- Follow writing & formatting rules.
- End with a CTA, never a question.
</output>
```
</div>
</div>

---

## 8. Tool Limitations & Constraints
### What It Does
- Prevents unrealistic user expectations.
- Clarifies AI's operational constraints.

<div class="columns">
<div>

### Why It Works
✅ Reduces user frustration.
✅ Keeps responses grounded in capabilities.

</div>
<div>

### Example
```html
<tool_limitations>
- No web browsing or live data retrieval.
- No external API interaction.
- No memory beyond the session.
</tool_limitations>
```
</div>
</div>

---

## 9. Context of the Current Session
### What It Does
- Provides session-relevant details like date and user preferences.

<div class="columns">
<div>

### Why It Works
✅ Aligns AI responses with the user's needs.
✅ Improves accuracy without memory reliance.

</div>
<div>

### Example
```html
<session_context>
- Date: March 8, 2025
- User Preferences: Concise responses, US English.
</session_context>
```
</div>
</div>

---

## 10. Example Interaction (Correct & Incorrect)
### What It Does
- Demonstrates AI response best practices.

<div class="columns">
<div>

### Why It Works
✅ Fine-tunes response style.
✅ Ensures adherence to brand voice.

</div>
<div>

### Example
```html
<example_interaction>
User: "Write a LinkedIn post about our latest product update."

❌ Incorrect:
"Our new update is live! Click here."

✅ Correct:
"Exciting news!
Our latest update to [Product Name] introduces:
[Feature Highlights].

Read more here: [Link] #Innovation"
</example_interaction>
```
</div>
</div>

---

# Key Takeaways

- Structure system prompts **clearly** for AI consistency.
- Define role, **formatting**, restrictions, and content behaviors.
- Use **examples & planning steps** to guide responses.
- Ensure AI aligns with **brand voice & compliance.**

🔹 **Better system prompts = better AI performance!**

---

# Thank You! 🎯

Shout out to *Chad*GPT!

Got questions? Let's discuss how to improve system prompt strategies! 🚀

Join my [discord server](https://discord.gg/e4zVza46CQ) and tell me what you think.


![width:800px](images/chad.webp)

![bg right:40%](images/zc_logo_2024_03_lg_white.png)
