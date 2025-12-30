import path from "node:path";
import { fileURLToPath } from "node:url";
import { Codex } from "@openai/codex-sdk";

const prompt = [
  "Use the notebooklm-patterns skill.",
  "List notebooks and clean up duplicates for URL:",
  "https://notebooklm.google.com/notebook/8e98a4d8-f778-4dfc-88e8-2d59e48b1069.",
  "Keep the most recently added/used entry and remove older duplicates.",
  "Then select the remaining notebook as active.",
  "Finally, ask: 'What is this notebook about?' and return a 3-bullet summary with citations.",
  "The user has approved cleanup; do not ask for confirmation.",
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
      if (event.item?.type === "agent_message") {
        console.log(event.item.text);
        continue;
      }
      if (event.item?.type === "mcp_tool_call" || event.item?.type === "command_execution") {
        console.log(JSON.stringify(event.item, null, 2));
        continue;
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
  }
} catch (error) {
  console.error("Codex SDK cleanup/query failed:", error);
  process.exitCode = 1;
}
