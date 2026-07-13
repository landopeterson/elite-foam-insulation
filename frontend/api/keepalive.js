// Pinged daily by a Vercel Cron Job to keep the Supabase free project from idling out
// (which would pause it and break the contact form). Harmless: it does a read that returns
// nothing (RLS blocks public reads), which still counts as Supabase activity.
// Vercel Cron has no "repo inactivity" rule, so this runs for as long as the site exists.

module.exports = async (req, res) => {
  const KEY = "sb_publishable_Sx0e9I__azKV40cqLycudw_nruWASEf"; // public publishable key (safe)
  try {
    const r = await fetch(
      "https://kvimcudxptpdnyemrrbk.supabase.co/rest/v1/leads?select=id&limit=1",
      { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } }
    );
    return res.status(200).json({ ok: true, supabase: r.status });
  } catch (e) {
    return res.status(200).json({ ok: false, error: String(e) });
  }
};
