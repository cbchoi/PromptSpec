import type { Metadata } from "next";
import "./styles.css";

export const metadata: Metadata = {
  title: "PromptSpec",
  description: "Slot-based prompt architecture studio"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

