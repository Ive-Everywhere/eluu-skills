---
name: template-creator
description: Create or update a reusable personal artifact-template skill. Use when the user invokes the template-creator skill or asks in natural language to create a reusable template from a reference document, presentation, spreadsheet, Google Docs, Slides, or Sheets link, ImageGen or Product Design image, email, Slack message, or Site project, or explicitly asks to edit or update a passed artifact-template skill. Do not use for one-off creation from an existing template.
---

# Template Creator

**Announce at start:** "I'm using the template-creator skill to build this reusable template."

Create or update a reference-backed template. Keep the source file, Site project, or a canonical Google Workspace URL and rendered reference image inside the skill so later use can reproduce its structure, voice, and visual system precisely.

## Routing

- Manage only personal skills under `${CLAUDE_HOME:-~/.claude}/skills`.
- Create a new template by default. Use a numbered skill name instead of overwriting an existing template.
- Update only when the user explicitly asks to edit or update exactly one passed artifact-template skill. Treat that passed skill as the exact target; never choose a similarly named template.
- Do not modify a skill installed outside the personal skills directory. If the passed template lives outside it, explain that this skill can update only a personal template.
- If the request also asks to share the template with a workspace, explain that this skill only manages personal templates.
- A template exists only after `create-template-skill.mjs` succeeds. Never hand-author, rename, or copy a normal skill and report it as an artifact template.

## Create workflow

1. Require exactly one supported reference unless the user explicitly requests a batch. For a batch, complete this workflow separately for every reference:
   - Document: `.docx`
   - Presentation: `.pptx`
   - Spreadsheet: `.xlsx`
   - Google Workspace: one Google Docs, Google Slides, or Google Sheets URL
   - ImageGen or Product Design image: `.png`
   - Email or Slack message: `.txt`
   - Site: an existing Site project directory
   - When email or Slack content is pasted rather than attached, materialize the exact content as a temporary UTF-8 `reference.txt` without rewriting it.
2. Infer a concise display name and intended-use description from the reference and request. Infer document, presentation, spreadsheet, and image from the file extension. For a Site project directory, use `site`. Infer `google-docs`, `google-slides`, or `google-sheets` from the supplied Workspace URL; for a generic Drive share URL, use Google Drive metadata to identify the native file type and resolve its canonical `docs.google.com` URL. Ask only when the link is inaccessible or does not identify a supported native Workspace artifact. For an image, set its gallery kind to `product-design` when the request names Product Design; otherwise default to `imagegen`, including when the user provides only the image and this skill. Ask only when the request explicitly includes both Product Design and ImageGen and the intended target remains unclear. For `.txt`, determine whether the user requested `email` or `slack`; ask if the intended type is ambiguous.
3. For references other than Site projects, create `preview.png` before packaging:
   - DOCX: use Documents to render the reference and copy its first page PNG.
   - PPTX: use Presentations to render the reference and copy its first slide PNG.
   - XLSX: use Spreadsheets to render the used range of the first visible non-empty sheet.
   - Google Workspace: use the Drive integration to inspect the native artifact, then export it with the call below. Then:
     - Google Docs: export to PDF and render its first content page to `reference.png`. Normally this is PDF page 1. For a tabbed Doc, Google may prepend one or more synthetic pages that contain only a tab title; skip only those consecutive tab-title separator pages and use the first page containing the first tab's actual document body. Treat that page as the artifact's first page rather than as a later-page substitution. Do not skip a real content page merely to choose a more attractive preview, and stop if the export contains no representative content page.
     - Google Slides: export to PDF and render only its first slide to `reference.png`.
     - Google Sheets: identify the first visible non-empty sheet, export to XLSX, and use Spreadsheets to render that sheet's used range to `reference.png`.
   - PNG: copy the reference PNG unchanged.
   - Email or Slack: render a legible representative portion of the exact reference text on a neutral canvas. Do not paraphrase, decorate, or invent content.
   - For a Google Workspace template, copy the checked `reference.png` unchanged to `preview.png`.
   - A Google Workspace URL is sufficient to activate the Drive workflow; the user does not need to name the integration. If the Drive integration is not connected for this agent, say so and stop. Do not substitute a local file without asking.
   - For every Google Workspace export, use the Drive integration's export action. Do not download through a browser, open a Google `/export` URL, follow a `googleusercontent.com` download redirect, use a shell HTTP client, or request browser download permission. Browser inspection does not substitute for an authenticated export. If the Drive connection lacks access, or the export does not return the requested file, stop and explain the integration requirement instead of falling back to a browser download.

   Export Google Docs and Slides as PDF and Google Sheets as XLSX, then write the bytes into the task workspace:

```
mcp__integrations__call_tool({
  integration_slug: "drive",
  tool_name: "drive.files.export",
  arguments: {
    fileId: "<file-id-from-the-canonical-google-workspace-url>",
    mimeType: "<application/pdf-or-xlsx-mime-type>",
  },
})
```

Resolve the file ID from the canonical `docs.google.com` URL, including any `resourcekey` query parameter required for link access. Use `application/pdf` and an output ending in `.pdf` for Google Docs and Slides. Use `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` and an output ending in `.xlsx` for Google Sheets. Do not manually copy base64 export content into a command or file-editing tool.

4. Visually inspect the PNG when one was created. Stop if it is blank, clipped, corrupted, or not representative of the reference. Site templates use a bundled generic Sites PNG preview and do not require a screenshot.
5. Do not create an intermediary request file or use a file-editing tool for script inputs. Set `SKILL_DIR` to the directory containing this `SKILL.md` and pass the values directly. Before substituting real values into the command, shell-escape each value as one argument for the active shell. Never interpolate a raw path, display name, description, or skill name.

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --reference-path "/absolute/path/reference.docx" \
  --preview-path "/absolute/path/preview.png" \
  --display-name "Standup" \
  --description "Run a structured daily standup with updates, blockers, and owners."
```

Use the sandbox `node` for `NODE_BIN`.

Pass `--kind "image"` and `--gallery-kind "imagegen"` or `--gallery-kind "product-design"` for image templates. Pass `--kind "email"` or `--kind "slack"` for text templates, and `--kind "site"` for Site project directories. The script can infer the three Office kinds and image from their extensions, but Template Creator must pass the image gallery kind explicitly so ImageGen and Product Design templates remain separate. `.txt` always requires `--kind "email"` or `--kind "slack"`. Site templates never require `--preview-path`.

For a Google Workspace template, pass its exact kind, resolved `docs.google.com` link as `--source-url`, and the rendered PNG as both the reference and preview inputs. The script validates that the link matches the requested kind and stores a canonical file URL without account-routing or deep-link parameters while preserving a `resourcekey` required for link-based access.

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --kind "google-docs" \
  --source-url "https://docs.google.com/document/d/example/edit?usp=sharing" \
  --reference-path "/absolute/path/reference.png" \
  --preview-path "/absolute/path/reference.png" \
  --display-name "Project Brief" \
  --description "Create project briefs with this Google Doc's native structure and visual system."
```

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --kind "image" \
  --gallery-kind "product-design" \
  --reference-path "/absolute/path/reference.png" \
  --preview-path "/absolute/path/preview.png" \
  --display-name "Launch Visual" \
  --description "Create launch visuals with this product-design direction."
```

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --kind "email" \
  --reference-path "/absolute/path/reference.txt" \
  --preview-path "/absolute/path/preview.png" \
  --display-name "Launch Email" \
  --description "Draft launch emails with this structure, voice, and call to action."
```

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --kind "site" \
  --reference-path "/absolute/path/existing-site" \
  --display-name "Marketing Site" \
  --description "Create a marketing site with this layout and component system."
```

6. Read the JSON result. Verify that `skillName` begins with `artifact-template-` and that the generated directory contains `SKILL.md`, `artifact-template.json`, and `assets/preview.png`. For Site templates, verify that the project is retained in `assets/source` with the generic Sites preview. Read the original project's `.gitignore` when present, inspect `assets/source`, and remove ignored files, project-specific credentials, customer exports, runtime data, generated archives, and unnecessary large files from the generated copy without modifying the original project before reporting success. For all other templates, verify the retained canonical `assets/reference.<ext>`. For a Google Workspace template, also verify that the manifest contains the canonical `sourceUrl` and `assets/reference.png`. If any check fails, do not claim the template was created.

## Update workflow

1. Resolve the exact passed artifact-template skill and read its `SKILL.md`, `artifact-template.json`, retained reference, and preview. Stop if it is not a direct child of the personal skills directory or if more than one target was passed.
2. Preserve the skill folder name. For Sites, rebuild the entire template from the selected source; for other templates, preserve every file or behavior the user did not ask to change.
3. Apply the requested edit:
   - For reference content or visual changes, use the matching artifact, image, or text workflow to edit a temporary copy of the retained reference, render a new preview from it, and visually inspect the result. Never edit a linked Google Workspace source artifact; update its canonical URL and rendered reference image only when the user explicitly changes the template source.
   - For Site project changes, use the updated project directory as the reference without creating a preview.
   - For display-name or intended-use changes, preserve the current reference and, when applicable, preview unless the request also changes them. For Site metadata-only changes, use the existing template's `assets/source`, not the current project.
   - For instruction-only or other skill-owned text changes, edit only the requested files directly and keep the manifest and agent metadata consistent.
4. When the reference, preview, display name, or description changes, pass the existing kind and values for every unchanged field directly to the script. For an image template, also pass its existing `galleryKind` as `--gallery-kind`. For a Google Workspace template, pass its existing or explicitly updated `sourceUrl` as `--source-url`. For a Site template, pass the updated project directory or the existing template's `assets/source`, as selected above, as `--reference-path` without `--preview-path`. Do not create or edit a request file:

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --mode "update" \
  --skill-name "artifact-template-standup" \
  --kind "document" \
  --reference-path "/absolute/path/updated-reference.docx" \
  --preview-path "/absolute/path/updated-preview.png" \
  --display-name "Standup" \
  --description "Run a structured daily standup with updates, blockers, and owners."
```

5. The script validates the existing template kind, preserves additional skill-owned files, and replaces the package atomically without changing its skill name.
6. Verify every requested change in the target directory and confirm there are no staging or backup directories left behind.

## Response

After verification, replace the placeholders with the script result and respond with only the applicable content between the comment markers below. The markers delimit the response template; do not emit them.

<!-- TEMPLATE CREATOR RESPONSE START -->

Here's your {displayName} template.

### How to use a template

Invoke the {skillName} skill and describe what you want to build.

<File>{skillPath}/SKILL.md</File>

<!-- TEMPLATE CREATOR RESPONSE END -->

Formatting rules:

- Keep the paragraph wording and punctuation unchanged apart from replacing `{displayName}`, `{skillPath}`, `{skillName}`, and `{kind}`.
- Use the exact returned `skillName` and `skillPath` values, and the lowercase `kind`.
- Surface the generated `SKILL.md` with a `<File>` tag on its own line.
- For a batch, repeat the response block for each created or updated skill.

## Constraints

- Do not search for or fetch remote templates.
- Do not create or edit `request.json` or any other intermediary request file. Pass script inputs through command-line flags.
- Do not delete or sanitize retained artifact-reference files; the user chose reference retention for fidelity. For Site projects, retain application source, project configuration, package-manager metadata, static assets, migrations, and logical D1/R2 bindings. Use the project's `.gitignore` to guide cleanup of the generated source, and exclude environment files, credentials, private keys, symlinks, dependencies, caches, build outputs, databases, and runtime or customer data without modifying the original project. Remove the original `project_id` from `.openai/hosting.json`.
- Treat every linked Google Workspace source artifact as read-only. Generated template skills must copy the complete native artifact before making changes.
- Generated Site templates must use the existing Sites workflow with `assets/source`; do not scaffold a new project over the retained source.
- Do not send an email or post a Slack message merely because a template was created or invoked.
- Do not add Artifact.md package generation here. Template distillation and creation belong to the artifact skills.
- Do not modify global skill metadata or protocol files.

## Requirements

Python: none
System: `node` (Node standard library only). Rendering `preview.png` from a `.docx`, `.pptx`, or `.xlsx` reference inherits the matching skill's needs, that is LibreOffice (`soffice`) plus `pdftoppm` (poppler-utils).
Integrations: Drive (`drive.files.export`), for the Google Workspace reference path only.
