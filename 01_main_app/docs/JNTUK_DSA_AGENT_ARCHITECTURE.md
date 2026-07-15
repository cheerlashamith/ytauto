# JNTUK R23 DSA Agent Architecture

The DSA syllabus is stored in:

```text
data/jntuk_r23_data_structures_syllabus.json
```

The agent should use this syllabus to decide:

- subject
- unit
- topic
- subtopic
- lab exercise
- visualization style
- course script
- Manim scene plan

## User interaction examples

User: "Generate video on linked list"

Agent should ask:

- Singly linked list?
- Doubly linked list?
- Circular linked list?
- Array vs linked list?
- Applications?

User: "Generate video on stack postfix evaluation"

Agent should directly generate:

- What is postfix?
- Why stack is used?
- Token scanning
- Operand push
- Operator pop two operands
- Compute result
- Example expression
- Summary

## Visual renderer

For DSA topics, use Manim Course Mode by default.

## Story Mode

Story mode is unrelated to JNTUK DSA syllabus. It is for kids stories.
