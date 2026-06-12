pywindow.I18N = {};
let CURRENT_LANG = "zh";

async function loadLang(lang) {
    if (!window.I18N[lang]) {
        const res = await fetch(`/static/lang/${lang}.json`);
        window.I18N[lang] = await res.json();
    }
}

function applyLang(lang) {
    const dict = window.I18N[lang] || {};
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (dict[key]) {
            el.innerText = dict[key];
        }
    });
}

async function setLang(lang) {
    await loadLang(lang);
    CURRENT_LANG = lang;
    localStorage.setItem("lang", lang);
    applyLang(lang);
}

document.addEventListener("DOMContentLoaded", async () => {
    const lang = localStorage.getItem("lang") || "zh";
    await loadLang(lang);
    CURRENT_LANG = lang;
    applyLang(lang);
});
