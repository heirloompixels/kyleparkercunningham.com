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
    return env.ASSETS.fetch(request);
  },
};
