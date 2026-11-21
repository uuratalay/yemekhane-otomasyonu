/* ===================================================================
   ortak.js — tüm sayfaların paylaştığı yardımcılar
   · Oturum token'ı localStorage'da; her istekte Authorization başlığı
   · istek(): fetch sarmalayıcı; sunucudan gelen {"hata": ...} mesajını fırlatır
   · koru(): korumalı sayfalarda token yoksa girişe yönlendirir
   · menuCiz(): role göre üst menü
   =================================================================== */
const API = "/api";

const Depo = {
  token: () => localStorage.getItem("oturum_token"),
  kullanici: () => JSON.parse(localStorage.getItem("kullanici") || "null"),
  kaydet: (token, kullanici) => {
    localStorage.setItem("oturum_token", token);
    localStorage.setItem("kullanici", JSON.stringify(kullanici));
  },
  temizle: () => {
    localStorage.removeItem("oturum_token");
    localStorage.removeItem("kullanici");
  },
};

async function istek(yol, { method = "GET", govde = null } = {}) {
  const baslik = { Accept: "application/json" };
  if (govde) baslik["Content-Type"] = "application/json";
  const t = Depo.token();
  if (t) baslik["Authorization"] = "Bearer " + t;

  const yanit = await fetch(API + yol, {
    method, headers: baslik, body: govde ? JSON.stringify(govde) : null,
  });

  let veri = null;
  try { veri = await yanit.json(); } catch (e) { /* gövdesiz yanıt */ }

  if (!yanit.ok) {
    if (yanit.status === 401) {
      Depo.temizle();
      if (!konumGiris()) location.href = "/index.html";
    }
    throw new Error((veri && veri.hata) || ("İstek başarısız (HTTP " + yanit.status + ")."));
  }
  return veri;
}

function konumGiris() {
  return location.pathname === "/" || location.pathname.endsWith("index.html");
}

function koru() {
  if (!Depo.token()) { location.href = "/index.html"; return false; }
  return true;
}

function paraYaz(n) {
  return Number(n).toLocaleString("tr-TR",
    { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " ₺";
}

function bildirim(hedefId, mesaj, tur = "hata") {
  const el = document.getElementById(hedefId);
  if (!el) return;
  el.textContent = mesaj;
  el.className = "bildirim " + (tur === "basari" ? "bildirim-basari" : "bildirim-hata");
  el.style.display = "block";
}

function menuCiz(aktif) {
  const k = Depo.kullanici();
  const nav = document.getElementById("ustmenu");
  if (!k || !nav) return;
  const linkler = [
    ["hafta.html", "Haftalık & Rezervasyon"],
    ["menu.html", "Günün Menüsü"],
    ["rezervasyonlarim.html", "Rezervasyonlarım"],
    ["bakiye.html", "Bakiye"],
    ["degerlendirme.html", "Değerlendirme"],
    ["profil.html", "Profil"],
  ];
  if (k.rol === "yonetici") linkler.push(["yonetim.html", "Yönetim"]);

  nav.innerHTML =
    '<div class="marka">🍽️ Yemekhane</div>' +
    '<div class="baglantilar">' +
      linkler.map(([h, a]) =>
        `<a href="/${h}"${h === aktif ? ' class="etkin"' : ""}>${a}</a>`).join("") +
    "</div>" +
    '<div class="kullanici"><span>' + k.ad + " " + k.soyad + " · " + k.rol + "</span>" +
    '<button class="dugme cikis" onclick="cikisYap()">Çıkış</button></div>';
}

async function cikisYap() {
  try { await istek("/cikis", { method: "POST" }); } catch (e) { /* yoksay */ }
  Depo.temizle();
  location.href = "/index.html";
}
