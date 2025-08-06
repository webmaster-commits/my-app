import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const data = await req.json();
  if (!data?.username || !data?.service || !data?.quantity) {
    return NextResponse.json({ ok: false, error: "Missing fields" }, { status: 400 });
  }
  return NextResponse.json({
    ok: true,
    orderId: `ORD-${Math.random().toString(36).slice(2, 8).toUpperCase()}`,
    received: data
  });
}
