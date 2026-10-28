# Homepage Refresh Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement these tasks in order.

**Goal:** Apply the approved refined academic design, highlight 2027 opportunities, and add verified research resources without changing publication order or restoring removed profile links.

**Architecture:** A homepage-only Jekyll layout and stylesheet isolate the design from the existing AcademicPages layouts. Publications remain in the existing YAML data and shared include; the overview and two experience entries remain in the homepage source.

**Tech Stack:** Jekyll 3.9, Liquid, YAML, HTML, CSS; Python unittest and lxml for built-page checks; browser screenshots for responsive verification.

## Approved Design

- White background, charcoal text, blue links, and a restrained green opportunities notice immediately below the name.
- Keep the portrait and email, LinkedIn, and Google Scholar in a left profile column on desktop. Stack the profile and main content on mobile.
- No eyebrow above the name. Display the company as Snowflake AI Research in both the overview and Experience.
- Use the latest CV's Snowflake dates, February to September 2026.
- Preserve all nine publications, with HybridResearcher first and HybridDeepResearch second. Do not restore the removed One-Shot paper.
- Add short summaries, readable publication metadata, two verified Snowflake technical write-ups, and the benchmark leaderboard.
- No CV, Instagram, or GitHub in the profile. Do not replace or publish the supplied CV.
- No unsupported HealthResearchBench entry; its public source is not yet verified.

## Tasks

### 1. Regression Checks

**Create:** `tests/test_homepage.py`

- [x] Build the current site to `/private/tmp/peiranxu-modern-check`.
- [x] Check the nine publication titles and order, absence of removed content, profile links, resources, local image dimensions, accessibility anchors, and the new opportunity text before the introduction.
- [x] Run the test against the existing build and confirm the new-design assertions fail (eight expected failures; publication order already passes).

### 2. Homepage Layout and Content

**Create:** `_layouts/home.html`, `assets/css/homepage.css`
**Modify:** `_pages/about.md`, `_config.yml`

- [x] Select `layout: home` for the homepage only. Reuse the site's existing head/SEO includes and config-driven profile data.
- [x] Add the portrait/profile column, in-page section navigation, a skip link, and a compact footer. No new JavaScript is required.
- [x] Place `Seeking 2027 full-time and internship opportunities` directly after the H1, without the mockup eyebrow or comparison toolbar.
- [x] Render Snowflake AI Research and Alibaba with their existing logos, dates, locations, and concise CV-grounded summaries.
- [x] Implement the approved A layout with a 1136px maximum width, 192px desktop sidebar, 40px name heading, and 210px publication figures. Stack at 620px and reduce column widths at 850px; use fixed font sizes per breakpoint, never viewport-scaled type.
- [x] Exclude the development plan and tests from the published site.

### 3. Publication Resources

**Modify:** `_data/homepage_publications.yml`, `_includes/publication-list.html`

- [x] Keep every title, author, paper URL, image, figure source, and ordering, except clearly labeled publication metadata.
- [x] Add two `Technical write-up` links and one `Leaderboard` link from the verified CV resources.
- [x] Add short summaries for the four papers previewed in the approved design. Label the remaining publications by their existing venues; label the Hawkeye Hugging Face link `Model`.
- [x] Render links as wrapping text links and figures at their original aspect ratios. Keep text-only papers aligned with the other information columns on desktop.

### 4. Verification and Delivery

- [x] Rebuild with the working Ruby environment and run the regression checks (nine pass).
- [x] Check desktop, intermediate, and mobile widths for overflow, clipping, unloaded images, navigation, and opportunity visibility. Verify keyboard focus and link destinations (320, 390, 768, 953 and 1280px checked).
- [x] Run `git diff --check`, review only scoped changes, and leave unrelated `.DS_Store` files untouched. Independent read-only review found no actionable issues.
- [x] Open the updated local homepage for review; keep the redesign unpushed until the user approves the actual page.

## Approved Follow-Up Changes

- Rename the top-left navigation label to `Homepage` and both technical write-up links to `Blog`.
- Rename the publication section and navigation link to `Selected Publications`; remove both ISMRM entries, leaving seven papers in the same order.
- Change the introduction and page description from `AI4S` to `AI for Healthcare`, preserving the user's two-paragraph introduction and bold research interests.
- The user approved committing and pushing the reviewed homepage on October 27, 2026.

## Commands

Build:

```sh
env JEKYLL_NO_BUNDLER_REQUIRE=true GEM_HOME=/Users/xup2/.bundle/peiranxu-github-pages GEM_PATH=/Users/xup2/.bundle/peiranxu-github-pages:/Library/Ruby/Gems/2.6.0 JEKYLL_ENV=production /Users/xup2/.bundle/peiranxu-github-pages/bin/jekyll build --destination /private/tmp/peiranxu-modern-check --trace
```

Regression checks:

```sh
/Users/xup2/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tests/test_homepage.py /private/tmp/peiranxu-modern-check
```

Preview: run the same Jekyll environment with `serve --host 127.0.0.1 --port 4000 --destination /private/tmp/peiranxu-modern-preview` after checking port availability.
