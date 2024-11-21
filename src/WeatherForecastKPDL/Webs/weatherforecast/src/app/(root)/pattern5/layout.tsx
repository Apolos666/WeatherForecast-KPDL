import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Spider Chart',
};

export default async function Pattern5Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <main>{children}</main>;
}
