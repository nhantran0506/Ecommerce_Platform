import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../../styles/globals.css";
import NavigationBar from "@/components/navigation_bar";
import ChatWindow from "@/components/chat_window";
import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";
import { notFound } from "next/navigation";
import { routing } from "@/i18n/routing";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "E-commerce website",
  description: "E-commerce website made by HCMUTE student",
};

export default async function LocaleLayout({
  children,
  params,
}: Readonly<{
  children: React.ReactNode;
  params: { locale: string };
}>) {
  const { locale } = await params;

  // Ensure that the incoming `locale` is valid
  if (!routing.locales.includes(locale as any)) {
    notFound();
  }

  // Providing all messages to the client
  // side is the easiest way to get started
  const messages = await getMessages();

  return (
    <html lang={locale}>
      <body className={inter.className}>
        <NextIntlClientProvider messages={messages}>
          <NavigationBar />
          {children}
          <ChatWindow />
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
