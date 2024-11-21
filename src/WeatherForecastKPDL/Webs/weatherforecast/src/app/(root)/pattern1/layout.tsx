import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Data over time',
};

export default async function Pattern1Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <main>{children}</main>;
}
