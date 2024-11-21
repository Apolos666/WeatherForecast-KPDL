import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Prediction Tomorrow',
};

export default async function Pattern7Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <main>{children}</main>;
}
