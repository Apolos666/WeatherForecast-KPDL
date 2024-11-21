import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Prediction date',
};

export default async function Pattern6Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <main>{children}</main>;
}
