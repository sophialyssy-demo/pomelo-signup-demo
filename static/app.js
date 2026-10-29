(function () {
  const I = window.ICONS;
  const X = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M4 4l12 12M16 4L4 16"/></svg>';
  const RADIO = '<svg class="radio" viewBox="0 0 20 20"><circle cx="10" cy="10" fill="rgba(252, 252, 250, 0.4)" r="9.75" stroke="#675d6c" stroke-width="0.5"></circle></svg>';
  const state = JSON.parse(sessionStorage.getItem('pomelo-demo') || '{}');
  const save = () => sessionStorage.setItem('pomelo-demo', JSON.stringify(state));

  const REASONS = [
    ['pregnant', "I'm pregnant"],
    ['postpartum', 'I had a baby within the last year'],
    ['ttc', "I'm trying to conceive"],
    ['loss', 'I experienced the loss of a pregnancy within the last year'],
    ['family', "I'm looking for support for my partner or family member"],
    ['menopause', "I'm experiencing perimenopause or menopause symptoms"],
  ];
  const COPY = {
    pregnant: ['Pomelo is here to support your pregnancy journey', [
      ['virtual', '24/7 virtual care', "from pregnancy through your baby's first birthday"],
      ['spec', 'Access to specialists', 'including therapists, dietitians, lactation consultants, and more'],
      ['third', 'Birth planning', 'guidance to set your labor & delivery preferences']]],
    postpartum: ['Pomelo is here to help you and your baby have a healthy, happy start', [
      ['virtual', '24/7 virtual care', "for you and your baby through their first birthday"],
      ['spec', 'Access to specialists', 'including therapists, dietitians, lactation consultants, and more'],
      ['third', 'Feeding guidance', 'support with breastfeeding, pumping, and formula']]],
    ttc: ['Pomelo is here to support you through every step of growing your family', [
      ['virtual', '24/7 virtual care', 'from preconception through pregnancy'],
      ['spec', 'Access to specialists', 'including therapists, dietitians, and more'],
      ['third', 'Expert guidance', 'on fertility, nutrition, and preparing for pregnancy']]],
    loss: ['Pomelo is here for you', [
      ['virtual', '24/7 virtual care', 'whenever you need support'],
      ['spec', 'Mental and emotional support', 'from therapists and care specialists'],
      ['third', 'Articles to help', 'navigate your physical and emotional recovery']]],
    family: ['We’d love to support your partner or family member', [
      ['virtual', '24/7 virtual care', 'for pregnancy, postpartum, and beyond'],
      ['spec', 'Access to specialists', 'including therapists, dietitians, lactation consultants, and more'],
      ['third', 'Partner resources', 'to help you support your loved one']]],
    menopause: ['Pomelo is here to support you through perimenopause and menopause', [
      ['virtual', '24/7 virtual care', 'from clinicians who specialize in midlife health'],
      ['spec', 'Access to specialists', 'including OB-GYNs, dietitians, and therapists'],
      ['third', 'Symptom relief', 'personalized plans for hot flashes, sleep, and more']]],
  };
  const PAYERS = [
    ['bcbstx', 'Blue Cross Blue Shield of Texas', '#0b5ca8', 'BCBS'],
    ['aetna', 'Aetna', '#7d3f98', 'AET'],
    ['uhc', 'UnitedHealthcare', '#002677', 'UHC'],
    ['cigna', 'Cigna Healthcare', '#0a7ec2', 'CI'],
    ['humana', 'Humana', '#3a8e1f', 'HUM'],
    ['medicaid_tx', 'Texas Medicaid', '#5e5e5e', 'TX'],
  ];
  const FOOTER = `<footer><p>All clinical services are provided by licensed physicians and clinicians practicing within an independently owned and operated medical practice, Pomelo, P.C. Pomelo Care, Inc. does not provide any medical, nursing, or other healthcare provider services.</p>
    <div class="links"><a href="#">Privacy Policy</a><a href="#">Terms of Service</a><a href="#">Accessibility</a><a href="#">Your Privacy Choices</a></div>
    <p>© 2026 Pomelo Care, Inc. All rights reserved.</p></footer>`;

  const esc = (s) => String(s || '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmtPhone = (d) => d.length < 4 ? d : d.length < 7 ? `(${d.slice(0, 3)}) ${d.slice(3)}` : `(${d.slice(0, 3)}) ${d.slice(3, 6)}-${d.slice(6, 10)}`;
  const app = document.getElementById('app');
  const go = (path) => { history.pushState({}, '', path); render(); window.scrollTo(0, 0); };
  window.addEventListener('popstate', render);

  async function api(path, body) {
    const r = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    let data = {};
    try { data = await r.json(); } catch (e) { /* non-JSON body */ }
    return { ok: r.ok, status: r.status, data };
  }

  const homeHeader = (back) => `<header class="hdr"><div class="hdr-left">${back ? `<button class="glass-btn" aria-label="Back" data-back>${I.back}</button>` : ''}<a class="logo" href="/signup/reason-for-care">Pomelo</a></div>
    <button class="lang" aria-label="Select language: English">EN ${I.globe}</button></header>`;
  const flowHeader = (pct) => `<header class="hdr flow-hdr"><button class="glass-btn lg" aria-label="Back" data-back>${I.back}</button>
    <button class="glass-btn lg" aria-label="Close" data-close>${X}</button></header>
    <div class="progress" role="progressbar" aria-valuenow="${pct}"><i style="width:${pct}%"></i></div>`;

  function shell(kind, header, body) {
    app.innerHTML = `<div class="page ${kind}">${header}${body}</div>`;
    app.querySelectorAll('[data-back]').forEach((b) => b.onclick = () => history.back());
    app.querySelectorAll('[data-close]').forEach((b) => b.onclick = () => go('/signup/reason-for-care'));
  }

  const views = {
    'reason-for-care'() {
      document.title = 'What brings you to Pomelo? | Pomelo Care';
      shell('home', homeHeader(false), `<main><h1>What brings you to Pomelo?</h1>
        <p class="sub">Choose your primary reason for seeking care with us. You can change this later if needed.</p>
        <div class="options">${REASONS.map(([k, t]) => `<button class="opt" data-r="${k}">${RADIO}<span>${esc(t)}</span></button>`).join('')}</div>
        <button class="textlink" data-none>None of these apply to me</button></main>`);
      app.querySelectorAll('[data-r]').forEach((b) => b.onclick = () => { state.reason = b.dataset.r; save(); go('/signup/phone-number'); });
      app.querySelector('[data-none]').onclick = () => go('/signup/unsupported-reason');
    },

    'phone-number'() {
      const [title, cards] = COPY[state.reason || 'pregnant'];
      document.title = 'Sign up | Pomelo Care';
      shell('home', homeHeader(true), `<main><h1>${esc(title)}</h1><p class="sub dark">Enter your number to sign up</p>
        <form id="f" novalidate><div class="field" id="pf"><label for="phone">Phone number</label>
          <input class="inp" id="phone" name="phoneNumber" type="tel" inputmode="tel" autocomplete="tel" value="${esc(state.phone ? fmtPhone(state.phone) : '')}">
          <div class="help" hidden id="perr">Not a valid phone number.</div></div>
        <p class="fine">By providing your phone number, you agree to receive account updates, notifications, and other text messages from Pomelo Care, including messages sent using automated technology, understanding that texts are not secure.</p>
        <p class="fine">Message frequency may vary and standard message and data rates may apply. You can opt out of receiving texts at any time by replying “STOP.” For help, reply “HELP.” See our <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.</p>
        <h2>How Pomelo supports you</h2>
        <div class="cards">${cards.map(([ic, h, p]) => `<div class="card">${I[ic]}<h3>${esc(h)}</h3><p>${esc(p)}</p></div>`).join('')}</div>
        <div class="cta-wrap"><button class="cta" type="submit">Get started</button></div></form></main>${FOOTER}`);
      const inp = app.querySelector('#phone');
      inp.oninput = () => { inp.value = fmtPhone(inp.value.replace(/\D/g, '').slice(0, 10)); };
      app.querySelector('#f').onsubmit = async (e) => {
        e.preventDefault();
        const d = inp.value.replace(/\D/g, '');
        const bad = d.length !== 10 || /^[01]/.test(d);
        app.querySelector('#pf').classList.toggle('err', bad);
        app.querySelector('#perr').hidden = !bad;
        if (bad) return;
        state.phone = d; save();
        await api('/api/otp/send', { phone: d });
        go('/signup/verify');
      };
    },

    verify() {
      document.title = 'Enter the code we sent you | Pomelo Care';
      shell('flow', flowHeader(10), `<main><h1>Enter the code we sent you</h1><p class="sub">We sent it to ${esc(fmtPhone(state.phone || '5126573630'))}</p>
        <form id="f" novalidate><div class="field" id="cf"><label for="code">Verification code</label>
          <input class="inp" id="code" inputmode="numeric" autocomplete="one-time-code" maxlength="6" placeholder="">
          <div class="help" hidden id="cerr">Please enter the 6-digit code.</div></div>
        <p class="resend">Didn't receive a code? <a href="#" id="resend">Request another one</a></p>
        <div class="cta-wrap"><button class="cta" type="submit">Next</button></div></form></main>`);
      const inp = app.querySelector('#code');
      inp.oninput = () => { inp.value = inp.value.replace(/\D/g, '').slice(0, 6); };
      app.querySelector('#resend').onclick = (e) => { e.preventDefault(); api('/api/otp/send', { phone: state.phone }); };
      app.querySelector('#f').onsubmit = async (e) => {
        e.preventDefault();
        const ok = /^\d{6}$/.test(inp.value) && (await api('/api/otp/verify', { phone: state.phone, code: inp.value })).ok;
        app.querySelector('#cf').classList.toggle('err', !ok);
        app.querySelector('#cerr').hidden = ok;
        if (ok) go('/signup/membership');
      };
    },

    membership() {
      const m = state.member || {};
      document.title = 'Let’s find your Pomelo membership | Pomelo Care';
      shell('flow', flowHeader(20), `<main><h1>Let’s find your Pomelo membership</h1>
        <p class="sub">Enter your details exactly as they appear on your insurance card so we can pull up your membership.</p>
        <form id="f" novalidate>
          <div class="row2"><div class="field" data-k="first"><label for="first">First name</label><input class="inp" id="first" autocomplete="given-name" value="${esc(m.first)}"><div class="help" hidden>First name is required</div></div>
          <div class="field" data-k="last"><label for="last">Last name</label><input class="inp" id="last" autocomplete="family-name" value="${esc(m.last)}"><div class="help" hidden>Last name is required</div></div></div>
          <div class="field" data-k="dob"><label for="dob">Date of birth</label><input class="inp" id="dob" inputmode="numeric" autocomplete="bday" value="${esc(m.dob)}"><div class="help">mm/dd/yyyy</div><div class="help" hidden>Please enter a valid date.</div></div>
          <div class="field" data-k="email"><label for="email">Email</label><input class="inp" id="email" type="email" autocomplete="email" value="${esc(m.email)}"><div class="help" hidden>Email is required</div></div>
          <p class="fine left">By providing your email, you agree to receive health, service and account-related communication through email, understanding that email may not be secure.</p>
          <div class="cta-wrap"><button class="cta" type="submit">Next</button></div></form></main>`);
      const dob = app.querySelector('#dob');
      dob.oninput = () => { const d = dob.value.replace(/\D/g, '').slice(0, 8); dob.value = [d.slice(0, 2), d.slice(2, 4), d.slice(4)].filter(Boolean).join('/'); };
      app.querySelector('#f').onsubmit = async (e) => {
        e.preventDefault();
        const v = (id) => app.querySelector('#' + id).value.trim();
        const val = { first: v('first'), last: v('last'), dob: v('dob'), email: v('email') };
        const dm = val.dob.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
        const dobOk = dm && +dm[1] >= 1 && +dm[1] <= 12 && +dm[2] >= 1 && +dm[2] <= 31 && +dm[3] > 1900 && new Date(`${dm[3]}-${dm[1]}-${dm[2]}`) < new Date();
        const errs = { first: !val.first, last: !val.last, dob: !dobOk, email: !/^\S+@\S+\.\S+$/.test(val.email) };
        app.querySelectorAll('[data-k]').forEach((f) => {
          const bad = errs[f.dataset.k]; f.classList.toggle('err', bad);
          const helps = f.querySelectorAll('.help'); helps[helps.length - 1].hidden = !bad;
        });
        if (Object.values(errs).some(Boolean)) return;
        state.member = val; save();
        const r = await api('/api/membership/lookup', { ...val, phone: state.phone });
        if (r.ok) { state.memberId = r.data.member_id; save(); go('/signup/insurance'); }
      };
    },

    insurance() {
      const ins = state.insurance || {};
      document.title = 'Connect your insurance | Pomelo Care';
      shell('flow', flowHeader(35), `<main><h1>Connect your insurance</h1>
        <p class="sub">We’ll check your coverage so you can start care with Pomelo at no cost to you.</p>
        <form id="f" novalidate><div class="field" id="payf"><label>Insurance provider</label></div>
          <div class="payers">${PAYERS.map(([k, n, c, ab]) => `<button type="button" class="opt ${ins.payer === k ? 'sel' : ''}" data-p="${k}"><span class="payer-logo" style="background:${c}">${ab}</span><span>${esc(n)}</span></button>`).join('')}</div>
          <div class="field" data-k="mid"><label for="mid">Member ID</label><input class="inp" id="mid" autocomplete="off" placeholder="e.g. XOJ123456789" value="${esc(ins.memberId)}"><div class="help">Found on the front of your insurance card</div><div class="help" hidden>Member ID is required</div></div>
          <div class="field"><label for="grp">Group number (optional)</label><input class="inp" id="grp" autocomplete="off" value="${esc(ins.group)}"></div>
          <div class="cta-wrap"><button class="cta" type="submit">Connect insurance</button></div></form></main>`);
      let payer = ins.payer || '';
      app.querySelectorAll('[data-p]').forEach((b) => b.onclick = () => {
        payer = b.dataset.p; app.querySelectorAll('[data-p]').forEach((x) => x.classList.toggle('sel', x === b));
        app.querySelector('#payf').classList.remove('err');
      });
      app.querySelector('#f').onsubmit = (e) => {
        e.preventDefault();
        const mid = app.querySelector('#mid').value.trim();
        const mf = app.querySelector('[data-k=mid]'); const helps = mf.querySelectorAll('.help');
        mf.classList.toggle('err', !mid); helps[1].hidden = !!mid;
        app.querySelector('#payf').classList.toggle('err', !payer);
        if (!mid || !payer) return;
        state.insurance = { payer, memberId: mid, group: app.querySelector('#grp').value.trim() }; save();
        go('/signup/insurance/connecting');
      };
    },

    'insurance/connecting'() {
      document.title = 'Connecting to your insurance | Pomelo Care';
      const steps = ['Securely connecting to your insurer', 'Verifying your eligibility', 'Confirming your Pomelo benefits'];
      shell('flow', flowHeader(50), `<main><div class="spinner-wrap"><div class="spinner"></div><h1>Connecting to your insurance</h1>
        <p class="sub">This usually takes less than a minute. Please don’t close this page.</p>
        <ul class="steps">${steps.map((s) => `<li><span class="dot"></span>${s}</li>`).join('')}</ul></div></main>`);
      const lis = [...app.querySelectorAll('.steps li')];
      const mark = (i) => lis.forEach((li, j) => { li.className = j < i ? 'done' : j === i ? 'active' : ''; li.querySelector('.dot').textContent = j < i ? '✓' : ''; });
      mark(0);
      const t1 = setTimeout(() => mark(1), 1400);
      const started = Date.now();
      api('/api/insurance/connect', { ...state.insurance, member: state.member, phone: state.phone, reason: state.reason }).then((r) => {
        const wait = Math.max(0, 2600 - (Date.now() - started));
        setTimeout(() => {
          clearTimeout(t1);
          if (location.pathname !== '/signup/insurance/connecting') return;
          if (r.ok) { mark(3); setTimeout(() => go('/signup/insurance/connected'), 600); }
          else { state.lastError = { ref: r.data.error_ref || 'unknown', status: r.status }; save(); go('/signup/insurance/error'); }
        }, wait);
      });
    },

    'insurance/error'() {
      const e = state.lastError || {};
      document.title = 'We couldn’t connect to your insurance | Pomelo Care';
      shell('flow', flowHeader(50), `<main><div class="err-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M12 7v6M12 16.5v.5"/></svg></div>
        <h1>We couldn’t connect to your insurance</h1>
        <p class="sub">Something went wrong on our end while verifying your coverage. Our team has been notified and is looking into it.</p>
        <div class="notice"><b>What you can do</b><br>Try again in a few minutes, or contact our care team at <b>(888) 990-5051</b> and we’ll finish setting up your membership.<br><br>Reference ID: <span class="ref">${esc(e.ref)}</span></div>
        <div class="cta-wrap"><button class="cta" id="retry">Try again</button><button class="cta secondary" id="edit">Edit insurance details</button></div></main>`);
      app.querySelector('#retry').onclick = () => go('/signup/insurance/connecting');
      app.querySelector('#edit').onclick = () => go('/signup/insurance');
    },

    'insurance/connected'() {
      shell('flow', flowHeader(70), `<main><h1>You’re covered!</h1><p class="sub">Your Pomelo membership is active. We’ll text you next steps.</p>
        <div class="cta-wrap"><button class="cta" data-close>Continue</button></div></main>`);
    },

    'unsupported-reason'() {
      document.title = 'Pomelo Care';
      shell('home', homeHeader(true), `<main><img class="uns-img" src="/static/img/exploring.png" alt=""><h1>It sounds like Pomelo isn’t the right fit at the moment.</h1>
        <p class="sub dark">Check back regularly to see if our services have changed, or if your situation has changed.</p>
        <div class="notice"><b>Remember, Pomelo may be able to support you if:</b><ul class="checklist">
          <li>You or your partner are pregnant or had a baby within the last year</li>
          <li>You're pregnant or postpartum and interested in doula support</li>
          <li>You're trying to conceive</li>
          <li>You're experiencing perimenopause or menopause symptoms, or want support for midlife health concerns</li></ul></div></main>${FOOTER}`);
    },
  };

  function render() {
    const route = location.pathname.replace(/^\/signup\/?/, '').replace(/\/$/, '');
    (views[route] || views['reason-for-care'])();
  }
  if (!location.pathname.startsWith('/signup/')) history.replaceState({}, '', '/signup/reason-for-care');
  render();
})();
