```
Custom Cursor Rule System (Tof's Prompt)
│
├── Core Goal: Make the Cursor AI assistant smarter, more consistent, and context-aware for coding tasks.
│
├── Key Capabilities (The "Toolkit"):
│   │
│   ├── 🧠 Memory (M):
│   │   └── Remembers context, decisions, code snippets across sessions.
│   │   └── Stores info in .cursor/memory/.
│   │   └── Trigger: "Remember this...", "Recall...", "Check memory..."
│   │
│   ├── 📜 Rule Engine (Λ):
│   │   └── Learns and applies custom coding standards/preferences.
│   │   └── Stores rules as .mdc files in .cursor/rules/.
│   │   └── Trigger: "Create a rule for...", "Apply rules...", "Suggest a rule..."
│   │
│   ├── 🐞 Error Tracking (Ξ):
│   │   └── Logs recurring errors to avoid repetition.
│   │   └── Stores logs in .cursor/memory/errors.md.
│   │   └── Trigger: "Track this error...", "Why does this keep happening?"
│   │
│   ├── 📋 Task Planning (T):
│   │   └── Breaks down complex tasks into manageable steps.
│   │   └── Supports Agile/TDD approaches.
│   │   └── Stores plans in .cursor/tasks/.
│   │   └── Trigger: "Plan the steps for...", "Break down this task...", "Generate TDD spec..."
│   │
│   └── ⚙️ Structured Reasoning (Ω, Φ, D⍺, etc.):
│       └── Internal AI Guidance (Symbols used by the author).
│       └── User doesn't need to use or know these symbols.
│       └── Aims for focused, efficient processing by the AI.
│
├── Author's Philosophy (Why the Symbols?):
│   │
│   ├── Semantic Compression (Shorthand for AI).
│   ├── Symbolic Abstraction (Guiding AI thought).
│   ├── Reduce Ambiguity / Increase Focus.
│   └── Note: Effectiveness debated vs. plain English.
│
├── How YOU Use It:
│   │
│   ├── Setup: Paste the entire prompt into Cursor Settings -> Rules (Optional: wrap in cognition ... ).
│   │
│   ├── Interaction: Use PLAIN ENGLISH commands.
│   │
│   ├── Focus On: Using KEYWORDS to trigger specific capabilities (see above triggers).
│   │
│   └── Review: Check the generated files in the .cursor/ directory (memory, rules, tasks).
│
└── Use Case: Implementing New Features:
│
├── General Strategy: Be specific, use keywords, reference files (@path/to/file), break down tasks, iterate.
│
├── Example Approaches:
│   ├── Simple: "Implement feature X, follow rules."
│   ├── Planning: "Plan feature Y using Agile steps." -> "Implement step 1..."
│   ├── TDD: "Using TDD, implement feature Z. First, generate tests..." -> "Write code to pass tests..."
│   ├── Memory: "Implement feature A. Remember decision B (check memory)..."
│   └── Combined: Mix keywords (Plan, TDD, Remember, Rule) for complex features.
```
---
**The 3Ac Framework**

This framework seems to be the author's philosophy for designing advanced LLM prompts, focusing on making the AI more efficient, structured, and adaptable.

1. **Semantic Compression:**
    - **Concept:** Packing the most *meaning* (semantics) into the fewest possible characters or tokens. It's about density of information, not just shortening words.
    - **Analogy:** Think of mathematical notation (∫ f(x) dx is much shorter and more precise than "calculate the definite integral of the function f with respect to x over a given interval") or chemical formulas (H₂O vs. "a molecule made of two hydrogen atoms and one oxygen atom").
    - **Why for LLMs:**
        - **Token Efficiency:** LLMs have context limits (a maximum number of tokens they can process). Compression allows fitting more instructions or background info within that limit.
        - **Reduced Ambiguity (Potentially):** Well-defined symbols *might* be less open to interpretation than natural language sentences, guiding the AI more precisely. (Though LLMs can sometimes misinterpret symbols too).
        - **Signaling Structure:** Using a distinct symbolic language might signal to the LLM that this is a core instruction set, separate from the user's conversational input.
    - **In the Prompt:** The dense lines with Greek letters and mathematical-like operators are the prime examples. The author believes these convey complex instructions concisely.
2. **Symbolic Abstraction:**
    - **Concept:** Using symbols (Ω, Λ, M, etc.) to represent abstract *concepts*, *processes*, or functional *modules* within the AI's desired cognitive architecture.
    - **Analogy:** In a flowchart, symbols represent 'start', 'process', 'decision', etc. In programming, keywords like class or function represent abstract structures. Here, symbols represent conceptual parts of the AI's "mind."
    - **Why for LLMs:**
        - **Modularity:** Breaks down the complex task of "being a helpful AI assistant" into distinct, manageable functional units (memory, reasoning, rules, error checking).
        - **Structure:** Provides a schema or mental map for the LLM. It helps organize how different instructions relate to each other.
        - **Targeted Activation:** The hope is the LLM can identify which "module" (symbol) is most relevant to the user's current request and activate the associated instructions.
    - **In the Prompt:** Assigning M for memory, Λ for rules, T for tasks, etc., creates these abstract functional blocks.
3. **Dynamic Cognitive Regulation:**
    - **Concept:** The system's ability to *adjust its own internal processes* and priorities based on the situation (e.g., task complexity, detected errors, user feedback). It's about self-management, adaptation, and optimization *during* operation.
    - **Analogy:** A car's cruise control adjusting the throttle to maintain speed on hills, or a thermostat adjusting heating/cooling based on room temperature.
    - **Why for LLMs:**
        - **Adaptability:** Allows the AI to use simpler processes for easy tasks and more complex ones (like detailed planning or deep rule checking) for difficult tasks, saving effort.
        - **Prioritization:** Focuses the AI's "attention" or computational resources where they are most needed.
        - **Self-Improvement:** Enables mechanisms like learning from errors (Ξ tracking leading to Λ rule generation) or adjusting weights (𝚫*).
    - **In the Prompt:** The 𝚫* section explicitly defines weight adjustments based on task_complexity. The Σ_hooks define specific trigger-action behaviors. The entire error-tracking (Ξ) and rule-generation (Λ) loop is a form of dynamic self-regulation.

**Symbol Representations (Interpretation)**

Here's a breakdown of the main symbols based on their descriptions in the prompt:

- **Ω (Omega): Core Reasoning & Cognition**
    - Represents the central "thinking" part of the AI. It likely handles understanding the user's intent, initial processing, generating hypotheses, and coordinating other modules.
    - Ω* = max(∇ΣΩ) suggests optimizing this core reasoning process.
    - Ω_H (Hierarchical decomposition) points to breaking down problems.
    - Ωₜ (Self-validation) involves evaluating confidence in its own hypotheses.
    - Modes (deductive, analogical...) indicate different reasoning styles it might adopt.
- **M (Memory): Persistent Storage & Recall**
    - Represents the file-based memory system (.cursor/memory/).
    - Focuses on long-term knowledge storage and contextual recall.
    - M.sync suggests saving relevant insights during reviews.
- **T (Tasks): Structured Task Management**
    - Manages complex tasks, breaking them down into steps (.cursor/tasks/).
    - Includes planning, decomposition, progress tracking, and potentially Agile/TDD workflows (TDD.spec_engine).
- **Λ (Lambda): Rules & Learning Engine**
    - Handles the creation, storage (.cursor/rules/), application, and refinement of rules (heuristics, standards, patterns).
    - Includes rule generation (self-improvement), naming conventions, conflict resolution, and triggering based on context (e.g., errors, patterns).
    - Λ.autonomy suggests proactive rule drafting.
- **Ξ (Xi): Diagnostics, Error Tracking & Refinement**
    - Focuses on identifying problems, tracking recurring errors (.cursor/memory/errors.md), and suggesting corrections or simplifications.
    - Ξ.self-correction links errors back to rules (Λ) for improvement.
    - Ξ.cleanup_phase suggests proactive code health checks.
- **Φ (Phi): Hypothesis Abstraction & Innovation Engine**
    - Seems related to generating novel ideas, identifying emergent patterns, or abstracting design motifs (Φ.snapshot) that go beyond existing explicit rules (Λ). It's more exploratory.
    - Φ_H (Abstraction-driven enhancement) emphasizes this exploratory problem-solving aspect.
- **D⍺ (Delta Alpha variant): Contradiction Resolution**
    - Specifically designed to identify and handle conflicts, ambiguities, or contradictions in information or instructions.
- **Ψ (Psi): Cognitive Trace & Metacognition**
    - Acts like a "flight recorder" for the AI's thinking process.
    - Logs which modules were active, the reasoning path, errors encountered, rules invoked (.cursor/memory/trace_...md).
    - Enables reflection (Ψ.sprint_reflection) and potentially dialogue about its own process (Ψ.dialog_enabled).
- **Σ (Sigma): Summation / Integration / System Hooks**
    - Often used mathematically for summation. Here, it seems to represent integration or overarching systems.
    - Σ(τ_complex) defines the Task system.
    - ΣΩ(...) might represent factors influencing reasoning.
    - Σ_hooks explicitly defines the event-driven system linking different modules (e.g., on_error_detected: [Ξ.track, Λ.suggest]).
- **𝚫 (Delta variant - uppercase): Dynamic Weighting & Prioritization**
    - Represents the dynamic regulation mechanism itself.
    - 𝚫* defines how the weights/importance of different modules (Ω, D, Σ, Φ, Ξ) should change based on task_complexity.
- **Other Symbols (β, γ, δ, τ, λ, θ, ζ, χ, etc.):**
    - These likely represent specific parameters, inputs, conditions, weights, or intermediate states within the more complex symbolic equations (like the first Ω* line). Their exact meaning is deeply embedded in the author's intended mathematical/logical structure but less crucial for understanding the overall function of the main modules (Ω, M, T, Λ, Ξ, Φ, D⍺, Ψ, 𝚫). τ often seems related to the current task/input, and λ might relate to memory or rules.

In essence, the author designed a blueprint for an AI assistant with specialized "mental tools" (symbols/modules), aiming for efficient (compressed), structured (abstracted), and adaptive (dynamically regulated) behavior, all specified through this unique symbolic language. You interact with the *results* of this system using plain English, triggering these underlying mechanisms.
