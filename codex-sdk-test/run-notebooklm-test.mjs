import path from "node:path";
import { fileURLToPath } from "node:url";
import { Codex } from "@openai/codex-sdk";

const prompt = [
  "Use the notebooklm-patterns skill.",
  "Check auth with mcp__notebooklm__get_health.",
  "If not authenticated, run mcp__notebooklm__setup_auth and wait for login.",
  "Then add https://notebooklm.google.com/notebook/8e98a4d8-f778-4dfc-88e8-2d59e48b1069 via mcp__notebooklm__add_notebook with:",
  "name: \"NotebookLM Integration Test\",",
  "description: \"Test notebook for validating Codex + NotebookLM integration in this repository.\",",
  "topics: [\"notebooklm\", \"codex\", \"mcp\", \"integration\", \"authentication\"].",
  "Select it with mcp__notebooklm__select_notebook and confirm the active notebook.",
  "Proceed without asking for additional metadata.",
].join(" ");

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(scriptDir, "..");

const codex = new Codex();
const thread = codex.startThread({
  workingDirectory: repoRoot,
  sandboxMode: "workspace-write",
  approvalPolicy: "never",
});

try {
  const { events } = await thread.runStreamed(prompt);
  for await (const event of events) {
    if (event.type === "item.completed") {
      console.log(`Item completed: ${event.item?.type ?? "unknown"}`);
      if (event.item?.type === "agent_message") {
        console.log(event.item.text);
      } else if (event.item) {
        console.log(JSON.stringify(event.item, null, 2));
      }
      continue;
    }
    if (event.type === "turn.failed") {
      console.error("Codex turn failed:", event.error?.message ?? event.error);
      continue;
    }
    if (event.type === "turn.completed") {
      console.log("Turn completed.");
      continue;
    }
    console.log(`Event: ${event.type}`);
  }
} catch (error) {
  console.error("Codex SDK test failed:", error);
  process.exitCode = 1;
}
