import * as React from "react"
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "GroBot - Mangrove Ecosystem Assistant",
  description: "Your AI assistant for mangrove ecosystems and ecology information",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen bg-gradient-to-br from-white via-green-50 to-blue-50 text-foreground`}>
        {children}
      </body>
    </html>
  );
} 