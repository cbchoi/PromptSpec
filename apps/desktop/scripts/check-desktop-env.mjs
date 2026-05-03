import { spawnSync } from "node:child_process";

function exists(command) {
  const result = spawnSync(command, ["--version"], { encoding: "utf8" });
  return result.status === 0;
}

const checks = [
  ["node", exists("node")],
  ["corepack", exists("corepack")],
  ["rustc", exists("rustc")],
  ["cargo", exists("cargo")]
];

let failed = false;
for (const [name, ok] of checks) {
  console.log(`${ok ? "pass" : "fail"} ${name}`);
  failed = failed || !ok;
}

process.exit(failed ? 1 : 0);

