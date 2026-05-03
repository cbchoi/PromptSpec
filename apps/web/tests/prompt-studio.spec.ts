import { expect, test } from "@playwright/test";

test("prompt studio renders and validates slots", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "PromptSpec" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Run pipeline" })).toBeVisible();

  await page.getByRole("button", { name: "Run pipeline" }).click();

  await expect(page.getByLabel("Rendered prompt")).toContainText("Write for backend engineers.");
  await expect(page.getByLabel("Validation report")).toContainText("pass");

  await page.getByRole("button", { name: "Add slot" }).click();
  await expect(page.getByRole("button", { name: /slot_3/ })).toBeVisible();
});

test("test lab and trace views expose reports and traces", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Test Lab" }).click();
  await expect(page.getByLabel("Test cases")).toContainText("scenario_pass_case");

  await page.getByRole("button", { name: "Run" }).click();
  await expect(page.getByLabel("Report detail")).toContainText("pass");

  await page.getByRole("button", { name: "Trace" }).click();
  await expect(page.getByLabel("Trace list")).toContainText("trace_local_001");
  await expect(page.getByLabel("Trace detail")).toContainText("backend engineers");
});
