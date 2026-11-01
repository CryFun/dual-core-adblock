// FIClash subscription extension (Script mode) - CryFun/dual-core-adblock
const main = (config) => {
  const name = 'custom-ad-domain';
  config['rule-providers'] ||= {};
  config['rule-providers'][name] = {
    type: 'http', behavior: 'domain', format: 'mrs',
    url: 'https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/domain.mrs',
    path: './ruleset/custom-ad-domain.mrs', interval: 86400
  };
  const obsolete = new Set(['custom-ad-domain','custom-ad-ip','custom-ad-classical','reiji-adblock','anti-ad','awavenue']);
  const original = Array.isArray(config.rules) ? config.rules : [];
  const filtered = original.filter(r => typeof r !== 'string' || !(r.startsWith('RULE-SET,') && obsolete.has(r.split(',')[1])));
  config.rules = [`RULE-SET,${name},REJECT`, ...filtered];
  return config;
};
