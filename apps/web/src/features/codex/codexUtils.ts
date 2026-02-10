
export interface ParsedCodex {
    content: string;
    metadata: Record<string, any>;
}

export function parseCodexContent(markdown: string): ParsedCodex {
    if (!markdown) return { content: '', metadata: {} };

    let processedMd = markdown;
    const meta: Record<string, any> = {};

    // 1. YAML Frontmatter check
    const yamlRegex = /^---\n([\s\S]*?)\n---/;
    const yamlMatch = processedMd.match(yamlRegex);

    if (yamlMatch) {
        try {
            const yamlBlock = yamlMatch[1];
            yamlBlock.split('\n').forEach(line => {
                const [key, ...rest] = line.split(':');
                if (key && rest.length) {
                    const val = rest.join(':').trim();
                    // Handle generic arrays [a, b] - very basic parser
                    if (val.startsWith('[') && val.endsWith(']')) {
                        meta[key.trim()] = val.slice(1, -1).split(',').map(s => s.trim());
                    } else {
                        meta[key.trim()] = val;
                    }
                }
            });
            processedMd = processedMd.replace(yamlRegex, '').trim();
        } catch (e) {
            console.error("Failed to parse YAML frontmatter", e);
        }
    } else {
        // 2. Legacy "Key: Value" lines at top (First 10 lines max)
        const lines = processedMd.split('\n');
        const newLines = [];
        let inHeader = true;

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();

            // Stop heuristic if empty line or heading
            if (line === '' || line.startsWith('#')) {
                if (inHeader && i > 0) inHeader = false;
                // If immediate empty line, likely separator.
            }

            if (inHeader && i < 8 && line.includes(':')) {
                const [key, ...rest] = line.split(':');
                const cleanKey = key.trim().toLowerCase();
                // Whitelist common keys to avoid false positives
                if (['title', 'id', 'world', 'section', 'tags', 'level', 'related'].includes(cleanKey)) {
                    const val = rest.join(':').trim();
                    if (val.startsWith('[') && val.endsWith(']')) {
                        meta[cleanKey] = val.slice(1, -1).split(',').map(s => s.trim());
                    } else {
                        meta[cleanKey] = val;
                    }
                } else {
                    // Not a known key, verify if it looks like prose?
                    // If it's just "Definition: something", that's content.
                    // Assume if it matches whitelist it's meta, else content.
                    inHeader = false;
                    newLines.push(lines[i]); // Keep this line
                }
            } else {
                inHeader = false;
                newLines.push(lines[i]);
            }
        }
        processedMd = newLines.join('\n').trim();
    }

    return { content: processedMd, metadata: meta };
}
