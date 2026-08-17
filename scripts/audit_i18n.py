import re
import glob

def audit_i18n():
    with open('src/web/js/i18n.js', 'r', encoding='utf-8') as fp:
        i18n_content = fp.read()

    uk_keys = set(re.findall(r'^\s*([a-zA-Z0-9_]+)\s*:', i18n_content, re.MULTILINE))
    print(f"Total keys in i18n.js: {len(uk_keys)}")

    # Parameterized keys
    param_keys = {}
    for line in i18n_content.splitlines():
        m = re.search(r'^\s*([a-zA-Z0-9_]+)\s*:\s*["\']([^"\']+)["\']', line)
        if m:
            key, text = m.group(1), m.group(2)
            params = re.findall(r'\{([a-zA-Z0-9_]+)\}', text)
            if params:
                param_keys[key] = set(params)

    print(f"Parameterized keys in i18n: {len(param_keys)}")
    for k, p in sorted(param_keys.items()):
        print(f"  {k}: {sorted(list(p))}")

    print("\nAuditing call sites across JS files:")
    for path in glob.glob('src/web/js/*.js'):
        with open(path, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
        for i, line in enumerate(lines):
            for k in param_keys:
                if f'"{k}"' in line or f"'{k}'" in line:
                    print(f"  {path}:{i+1} -> {line.strip()}")

if __name__ == '__main__':
    audit_i18n()
