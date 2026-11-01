// Replace YOUR_GITHUB_USERNAME and YOUR_REPOSITORY before importing.
const main = (config) => {
  const base = 'https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY/rules/';
  const providers = config['rule-providers'] || {};
  const add = (name, behavior, format, file) => {
    providers[name] = {
      type: 'http', behavior, format,
      url: base + file,
      path: './ruleset/custom-' + file,
      interval: 86400
    };
  };
  add('custom-ad-domain', 'domain', 'mrs', 'domain.mrs');
  // Keep optional outputs conditional: missing remote files cause load errors.
  // Enable these only if corresponding files exist on the rules branch.
  // add('custom-ad-ip', 'ipcidr', 'mrs', 'ipcidr.mrs');
  // add('custom-ad-classical', 'classical', 'yaml', 'classical.yaml');
  config['rule-providers'] = providers;
  const names = ['custom-ad-domain', 'custom-ad-ip', 'custom-ad-classical'];
  const legacy = ['reiji-adblock', 'anti-ad', 'awavenue'];
  const old = Array.isArray(config.rules) ? config.rules : [];
  const filtered = old.filter(rule => ![...names, ...legacy].some(n => rule.startsWith('RULE-SET,' + n + ',')));
  config.rules = ['RULE-SET,custom-ad-domain,REJECT', ...filtered];
  return config;
};
