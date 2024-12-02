import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Prediction Next Day',
};

export default async function Pattern5Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <main>{children}</main>;
}
