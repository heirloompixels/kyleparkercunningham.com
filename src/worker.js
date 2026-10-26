// The only code in front of the Zola build. GitHub Pages sent www and plain
// http to https://kyleparkercunningham.com; the zone does not (its
// always_use_https is off, and turning it on would change every subdomain), so
// the Worker does. Everything else goes to the static assets, where
// public/_redirects and the 404 page apply.
const APEX = 'kyleparkercunningham.com';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === `www.${APEX}` || (url.hostname === APEX && url.protocol === 'http:')) {
      url.hostname = APEX;
      url.protocol = 'https:';
      url.port = '';
      return Response.redirect(url.toString(), 301);
    }
    const res = await env.ASSETS.fetch(request);
    // _redirects lists only the trailing-slash form, and the asset handler adds
    // the slash only where a page exists, so /oeuvre/printmaking/2017 was a 404
    // while /oeuvre/printmaking/2017/ was a 301 (Search Console, 2026-10-26).
    // A slashless 404 tries the slash form and passes on a redirect it finds,
    // so it is still one hop.
    if (res.status === 404 && !url.pathname.endsWith('/') && !/\.[a-z0-9]+$/i.test(url.pathname)) {
      const slashed = new URL(url);
      slashed.pathname += '/';
      const alt = await env.ASSETS.fetch(new Request(slashed, request));
      if (alt.status === 301 || alt.status === 308) return alt;
    }
    return res;
  },
};
