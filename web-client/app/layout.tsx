import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../styles/globals.css";
import ChatWindow from "@/components/chat_window";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "E-commerce website",
  description: "HCMC UTE students capstone project.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
        <ChatWindow />
      </body>
    </html>
  );
}