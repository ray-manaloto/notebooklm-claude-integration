import path from "node:path";
import { fileURLToPath } from "node:url";
import { Codex } from "@openai/codex-sdk";

const prompt = [
  "Use the notebooklm-patterns skill.",
  "Ensure RPC auth is available (cookies saved via save_auth_tokens).",
  "List notebooks with mcp__notebooklm-rpc__notebook_list.",
  "Find the notebook titled \"NotebookLM Integration Test\"; if missing, stop and report.",
  "Ask it with mcp__notebooklm-rpc__notebook_query: \"What is this notebook about?\"",
  "Return a 3-bullet summary with citations.",
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
