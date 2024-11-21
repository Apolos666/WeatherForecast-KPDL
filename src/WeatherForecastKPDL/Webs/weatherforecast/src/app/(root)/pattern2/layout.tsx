import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Trending Data',
};

export default async function Pattern2Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <main>{children}</main>;
}
