import { remarkTermLinker } from '../remark-term-linker';
import { describe, it, expect } from 'vitest';
import { unified } from 'unified';
import remarkParse from 'remark-parse';

// Simple mock compiler to just traverse and return parts of tree
const compileAndFind = async (md: string, keyTerms: any[]) => {
    let matches: any[] = [];

    // We use .run() instead of .process() to identify nodes without compiling to string
    const processor = unified()
        .use(remarkParse)
        .use(remarkTermLinker, { keyTerms });

    const tree = processor.parse(md);
    const transformedTree = await processor.run(tree);

    const visit = (node: any) => {
        if (node.type === 'termLink') matches.push(node);
        if (node.children) node.children.forEach(visit);
    };
    visit(transformedTree);

    return matches;
}

describe('remark-term-linker', () => {
    it('links simple terms', async () => {
        const terms = [{ id: '1', term: 'foo', codex_ref: 'mod/foo' }];
        const matches = await compileAndFind('Hello foo bar', terms);
        expect(matches).toHaveLength(1);
        expect(matches[0].term).toBe('foo');
        expect(matches[0].codexRef).toBe('mod/foo');
    });

    it('is case insensitive', async () => {
        const terms = [{ id: '1', term: 'Foo', codex_ref: 'mod/foo' }];
        const matches = await compileAndFind('hello foo bar', terms);
        expect(matches).toHaveLength(1);
    });

    it('matches plural', async () => {
        const terms = [{ id: '1', term: 'term', codex_ref: 'mod/term' }];
        const matches = await compileAndFind('two terms here', terms);
        expect(matches).toHaveLength(1);
        expect(matches[0].children[0].value).toBe('terms');
    });

    it('ignores inside code', async () => {
        const terms = [{ id: '1', term: 'foo', codex_ref: 'mod/foo' }];
        // "foo" in code block
        const matches = await compileAndFind('`foo` and foo', terms);
        expect(matches).toHaveLength(1);
    });

    it('links multiple terms in same node', async () => {
        const terms = [
            { id: '1', term: 'foo', codex_ref: 'mod/foo' },
            { id: '2', term: 'bar', codex_ref: 'mod/bar' }
        ];
        const matches = await compileAndFind('hello foo and bar here', terms);
        expect(matches).toHaveLength(2);
        expect(matches[0].term).toBe('foo');
        expect(matches[1].term).toBe('bar');
    });

    it('ignores inside headings', async () => {
        const terms = [{ id: '1', term: 'foo', codex_ref: 'mod/foo' }];
        const matches = await compileAndFind('# Header with foo\n\nBody with foo', terms);
        expect(matches).toHaveLength(1);
        // Should catch the one in body, but not header
        // Note: compileAndFind flattens matches. We rely on length check. 
        // Logic: # Header -> Heading(Text(foo)) -> Skip. Body -> Paragraph(Text(foo)) -> Link.
    });
});
