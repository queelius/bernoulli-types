# Repository Guidelines

## Project Structure & Module Organization
- `include/bernoulli/`: Public headers (header‑only core). Include with `#include <bernoulli/...>`.
- `tests/`: GoogleTest unit tests (`test_*.cpp`). Integrated via CTest.
- `examples/`: Small, buildable demos; binaries land in `build/bin/examples/`.
- `benchmarks/`: Performance experiments (optional target).
- `docs/`, `papers/`: Reference material and LaTeX sources.
- `bernoulli_data_types/`: Snapshot of the legacy repo; reference for papers and potential migrations (not built by default).
- `cmake/`: Package/config helpers. Use out‑of‑tree builds (`build/`).

## Build, Test, and Development Commands
```bash
mkdir -p build && cd build
cmake -DBERNOULLI_BUILD_TESTS=ON -DBERNOULLI_BUILD_EXAMPLES=ON -DCMAKE_CXX_STANDARD=20 ..
cmake --build . -j
ctest --output-on-failure          # Run unit tests
cmake --build . --target check     # Alt: verbose tests
cmake --build . --target valgrind  # If Valgrind is available
```
Examples run from `build/bin/examples/`, e.g. `./bin/examples/basic_usage`.
Optional flags: `-DBERNOULLI_BUILD_BENCHMARKS=ON`, `-DBERNOULLI_BUILD_DOCS=ON`, `-DBERNOULLI_INSTALL=ON`.

## Coding Style & Naming Conventions
- Language: C++20/“C++21” with concepts; header‑only target `Bernoulli::Types`.
- Indentation: 4 spaces; no tabs. Prefer `#pragma once` include guards.
- Filenames: `lower_snake_case.hpp` (e.g., `observed_bool.hpp`).
- Types/aliases: `lower_snake_case` for simple structs (e.g., `observed_bool`, `rate_span`).
- Prefer const‑correctness, RAII, and small, composable headers. Document public APIs with concise Doxygen comments.
- Use concepts for template constraints (avoid SFINAE). Example:
  `template<class T> concept hashable = requires(T a){ { std::hash<T>{}(a) } -> std::convertible_to<size_t>; };`

## Testing Guidelines
- Framework: GoogleTest (fetched via CMake FetchContent).
- Test files: `tests/test_<feature>.cpp`; group related assertions in `TEST` cases.
- Run locally with `ctest`; ensure failures print context (`--output-on-failure`).
- Add coverage or property tests as appropriate; include edge cases and error‑propagation checks.

## Commit & Pull Request Guidelines
- Commits: Imperative mood, focused scope. Example: `add observed_bool XOR and XNOR`.
- Reference issues with `Fixes #123` where applicable. Keep diffs minimal and self‑contained.
- PRs: Include a clear description, rationale, links to issues, and before/after notes (numbers or example output for perf/behavioral changes). Add tests and docs for new APIs.
- Build must pass (`ctest`) and examples compile. Align CMake lists with added/removed files (tests/examples).

## Notes
- First configure will download GoogleTest; offline builds need it vendored/cached.
- Until `CMakeLists.txt` is updated, pass `-DCMAKE_CXX_STANDARD=20` to enable concepts.
- If you add new headers, ensure they live under `include/bernoulli/` and are included via the public path.
