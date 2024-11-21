import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Correlation Matrix',
};

export default async function Pattern4Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <main>{children}</main>;
}
