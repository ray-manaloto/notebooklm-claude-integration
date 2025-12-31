import path from "node:path";
import { fileURLToPath } from "node:url";
import { Codex } from "@openai/codex-sdk";

const question = process.env.QUESTION ?? "How can we improve the Codex implementation in this repo?";

const prompt = [
  "Use the notebooklm-patterns skill.",
  "List all notebooks.",
  "If subagents or task parallelism are available, spawn one subagent per notebook.",
  `Each subagent should ask this question via notebook_id: '${question}'.`,
  "If subagents are unavailable, run the notebook queries sequentially.",
  "Aggregate responses labeled by notebook name and include citations.",
  "If any ask_question times out, retry once with browser_options timeout_ms=60000.",
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
  console.error("Codex SDK ask-all failed:", error);
  process.exitCode = 1;
}
