## Google Sheets-targeted output
### New Creations

For a net-new Google Sheets request, create and verify a local `.xlsx` with this skill first. The native Google Sheets deliverable must then be produced by the Drive integration's upload action, `mcp__integrations__drive_upload_file`, with the local file as `sourcePath` and the Google Sheets MIME type so Drive converts on upload:

```
mcp__integrations__drive_upload_file({
  name: "<deliverable name>",
  sourcePath: "/absolute/path/to/output.xlsx",
  mimeType: "application/vnd.google-apps.spreadsheet",
})
```

This import path is verified to preserve freeze panes, fills, borders, font family and size, bold, wrap, horizontal alignment, number formats and column widths. Build the formatting into the local `.xlsx` rather than planning to repair it after import.

Do not use Computer Use, Browser Use, blank-Google-Sheets creation plus Google Sheets write APIs, or another direct-to-Sheets construction path for net-new Google Sheets unless the user explicitly asks for that alternate workflow. If they do, mention first that output quality is expected to be best when a local `.xlsx` is imported through the Drive integration.

If the Drive integration is not connected for this agent, say so and stop. Do not substitute a local file without asking.

After successful native import, the user-facing deliverable is the Google Sheets link. Treat the local `.xlsx` as a build artifact unless the user explicitly asks to keep or receive it.

### Edits

Use the Drive integration's Google Sheets tools for edits to existing Google Sheets. The local `.xlsx` creation and native import workflow above applies only to net-new Google Sheets deliverables.
