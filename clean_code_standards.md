# 🛠️ Core Coding Principles

1.  Always follow recognized code quality rules and best practices.
2.  Prioritize straightforward solutions—avoid needless complexity.
3.  Consistently improve the codebase in every interaction.
4.  Seek and resolve the true underlying causes of issues.

# 🎨 Design Fundamentals

1.  Define configuration at the highest reasonable abstraction.
2.  Prefer strategies and polymorphic design over repeated conditionals.
3.  Prevent excessive configurability from creeping into systems.
4.  Manage dependencies explicitly, ideally using dependency injection.
5.  Stick to the Principle of Least Knowledge; objects should talk to their immediate collaborators only.

# 🧠 Tips for Code Readability

1.  Maintain consistency in all coding approaches.
2.  Use descriptive variable names that clearly state intent.
3.  Use dedicated value objects where possible, rather than plain primitives.
4.  Prevent hidden dependencies between class methods.
5.  Rewrite negative conditions into positive, easily understood logic.

# 🔤 Naming Standards

1.  Select precise names that express intent and use.
2.  Make sure names highlight their distinctions from others.
3.  Opt for names that are simple to read and pronounce.
4.  Use identifier names that are easily searchable within the codebase.
5.  Replace magic numbers with meaningfully named constants.
6.  Do not include prefixes that describe types or roles (e.g., txt, str, arg).

# 🔧 Function Design Best Practices

1.  Functions should be concise and address a single responsibility.
2.  Each function must do only one thing.
3.  Function names must clearly describe their action or purpose.
4.  Minimize the number of parameters; avoid overloading function signatures.
5.  Functions should have transparent effects—no hidden side effects.
6.  Do not use boolean parameters to alter internal flow; instead, create distinct functions for different behaviors.

# 🧱 Guidelines for Source Organization

1.  Group logically related content vertically within files.
2.  Keep related functions and code blocks physically close together.
3.  Declare local variables right where they are first needed.
4.  Arrange dependent functions in proximity to each other.
5.  Collect similar-purpose functions together for discoverability.
6.  Order your functions so that dependencies flow from top to bottom.
7.  Write concise, legible lines; avoid cramming too much onto one.
8.  Don’t horizontally align variable assignments or code.
9.  Use blank lines to visually separate unrelated code and group what belongs together.
10. Indent for structure and clarity—avoid forced or convoluted indentation.

# 🧩 Object and Data Pattern Guidelines

1.  Shield internal state and logic—publicly expose only what’s essential.
2.  Use either pure data structures or pure behavior objects—do not blend the two.
3.  Keep objects streamlined and focused.
4.  An object should model a single, well-defined concept.
5.  Limit the number of instance variables within objects.
6.  Base classes must not presume details about their subclasses.
7.  Use explicit, specialized methods rather than control flags.
8.  Prefer instance methods for behaviors relating to object state.

# 🧪 Principles for Writing Tests

1.  Each test should verify only one thing.
2.  Strive for clarity, readability, and intention in your tests.
3.  Ensure independence between individual tests.
4.  Each test should yield the same outcome every time it runs.

# 🚨 Signs of Code Problems

1.  **Highly rigid** — changing one thing forces changes in many places.
2.  **Highly brittle** — minor alterations lead to unexpected breakage elsewhere.
3.  **Tightly coupled** — hard to use bits of code in isolation or another context.
4.  **Unnecessarily complex** — the solution is more intricate than needed.
5.  **Widespread duplication** — similar logic appears in multiple code areas.
6.  **Unclear purpose** — others will struggle to quickly grasp the code’s intent.
