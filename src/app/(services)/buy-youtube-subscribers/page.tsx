export const metadata = {{ title: "Buy YouTube Subscribers — Likes.io" }};

export default function Page() {{
  const packages = ["100", "500", "1,000", "2,500", "5,000"];
  return (
    <section className="container-balanced py-16">
      <h1 className="text-3xl font-bold">Buy YouTube Subscribers</h1>
      <p className="mt-2 text-slate-600 dark:text-slate-300">
        Grow your channel’s social proof.
      </p>
      <ul className="mt-6 grid gap-4 sm:grid-cols-2 md:grid-cols-3">
        {{packages.map((p) => (
          <li key={{p}} className="card p-5">
            <div className="font-semibold">{{p}} Package</div>
            <div className="text-sm text-slate-600 dark:text-slate-300 mt-1">Secure checkout • Instant start</div>
            <button className="mt-4 w-full rounded-xl bg-brand text-white py-2.5 font-semibold hover:bg-brand-dark">
              Buy Now
            </button>
          </li>
        ))}}
      </ul>
    </section>
  );
}}
