import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Seasonal Data',
};

export default async function Pattern3Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <main>{children}</main>;
}
