# Task
Create a production-ready, complete project template following strict Clean Code, SOLID principles, and industry-standard project architecture using Python. The solution must include the backend structure, a normalized database schema, and a comprehensive, professional README.md. This project will be a core piece of my professional portfolio.

---

# Project Context
"HasMyIdeaBeenTaken" is a web application inspired by "HaveIBeenPwned", but designed for software ideas and repositories. 
The system consists of:
1. A background worker/script that actively fetches new open-source projects, repository IDs, usernames, and uses an LLM to generate a concise contextual summary of the project's core purpose.
2. A web interface with a simple search bar where users can describe their project idea in natural language.
3. A semantic/hybrid search mechanism: The AI processes the user's prompt and queries the database to find highly similar or overlapping existing repositories, returning a comparative table with matching details and descriptions.

The goal is to build a normalized, scalable, and maintainable database structure capable of handling high-frequency writes (from the scraper) and fast semantic reads (from the search engine).

---

# Table Purpose
To store indexed open-source repositories, developer metadata, and AI-generated semantic summaries/embeddings to allow fast, accurate similarity mapping against new user ideas.

---

# Columns & Schema Suggestions
The database should be designed with proper foreign keys and indexing. Suggested entities:
* **users/owners:** `id` (PK), `platform_username`, `platform_profile_url`
* **repositories:** `id` (PK), `owner_id` (FK), `repository_name`, `source_platform` (e.g., GitHub), `repository_url`, `created_at`, `updated_at`
* **project_context:** `id` (PK), `repository_id` (FK), `raw_description`, `ai_generated_summary`, `embedding_vector` (for semantic search tracking)

---

# Requirements
1. **Architecture:** Use a clean, modular architecture (e.g., Layered Architecture or Service-Repository Pattern) separating the Scraper, the AI Service, and the Web API.
2. **Database:** PostgreSQL (highly recommended due to `pgvector` support for the AI search component) or SQLite for the initial MVP setup.
3. **Frameworks:** Python with FastAPI or Flask for the API, SQLAlchemy or Tortoise-ORM for database mapping, and Pydantic for data validation.
4. **AI Integration:** Integration setup using LangChain, LlamaIndex, or direct OpenAI/Ollama API calls for generating embeddings and summaries.
5. **Documentation:** A complete `README.md` featuring architecture diagrams (ASCII/Mermaid), setup instructions via Docker/Virtualenv, API endpoints documentation, and a guide on how the semantic search works.

---

# Constraints
* **Language:** Python 3.11+
* **Code Quality:** Strict adherence to PEP 8, type hinting, and comprehensive error handling (robust retry mechanisms for third-party API rate limits). No errors or nonsense logic, always use the mmost optimized options.
* **Performance:** Queries must be optimized; the semantic search should not perform a full-table scan using heavy LLM processing per row.

---

# Output
Provide the following deliverables:
1. The recommended **Directory Structure tree** for a scalable Python project.
2. The **SQL DDL scripts** (or SQLAlchemy Models) reflecting the normalized database design.
3. A boilerplate implementation of the core components (The Repository pattern implementation, the Search service, and the Scraper worker).
4. A professional, structured markdown template for the `README.md`.
5. The ready to test program, try to do everything u can, even though i will do some repair soon, reduce, or try to, make me have not check anything, because the code is so good