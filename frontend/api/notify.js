// Serverless function (Vercel): emails the owner when a new lead is inserted.
// Triggered by a Supabase Database Webhook on INSERT into `leads`.
// Secured with a shared secret so only our webhook can send mail.
// Env vars (set in Vercel → Settings → Environment Variables):
//   WEBHOOK_SECRET, RESEND_API_KEY, LEAD_NOTIFY_TO, LEAD_NOTIFY_FROM

module.exports = async (req, res) => {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const secret = process.env.WEBHOOK_SECRET || "";
  const auth = req.headers["authorization"] || "";
  if (!secret || auth !== `Bearer ${secret}`) return res.status(401).json({ error: "unauthorized" });

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  const lead = (body && body.record) || {};

  const RESEND = process.env.RESEND_API_KEY;
  const TO = process.env.LEAD_NOTIFY_TO;
  const FROM = process.env.LEAD_NOTIFY_FROM;
  if (!RESEND || !TO || !FROM) return res.status(500).json({ error: "email not configured" });

  const name = lead.name || "someone";
  const text =
    `New quote request from ${name}\n\n` +
    `Name:    ${lead.name || "—"}\n` +
    `Phone:   ${lead.phone || "—"}\n` +
    `Email:   ${lead.email || "—"}\n` +
    `Service: ${lead.service || "—"}\n\n` +
    `Message:\n${lead.message || "(none)"}\n\n` +
    `— Sent automatically from elitesprayinsulation.com`;

  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${RESEND}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: FROM,
        to: [TO],
        subject: `New quote request from ${name}`,
        text,
        reply_to: lead.email || undefined,
      }),
    });
    if (!r.ok) {
      const t = await r.text();
      console.error("resend failed", r.status, t);
      return res.status(502).json({ error: "email send failed" });
    }
  } catch (e) {
    console.error("resend error", e);
    return res.status(502).json({ error: "email send failed" });
  }
  return res.status(200).json({ ok: true });
};
