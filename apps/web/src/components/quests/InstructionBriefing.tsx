import React, { useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { BriefingCard, BriefingCardVariant } from './BriefingCard';

interface InstructionBriefingProps {
    md: string;
    onPasteCode?: (code: string) => void;
    components?: any;
    remarkPlugins?: any[];
}

interface Section {
    title: string;
    content: string;
    variant: BriefingCardVariant;
}

export function InstructionBriefing({ md, onPasteCode, components, remarkPlugins }: InstructionBriefingProps) {
    const sections = useMemo(() => {
        if (!md) return [];

        // Split by H1 or H2 headers
        // Matches: # Title, ## Title, ### Title
        const parts = md.split(/\n?(?=#{1,3}\s)/);
        
        const result: Section[] = [];
        let currentIntro = "";

        parts.forEach((part, index) => {
            const lines = part.trim().split('\n');
            const firstLine = lines[0] || "";
            
            if (firstLine.startsWith('#')) {
                const title = firstLine.replace(/^#{1,3}\s+/, '').trim();
                const content = lines.slice(1).join('\n').trim();
                
                if (!content && index === 0) {
                     // Just an intro title without content yet
                     return;
                }

                result.push({
                    title,
                    content,
                    variant: mapTitleToVariant(title)
                });
            } else if (index === 0) {
                currentIntro = part.trim();
            }
        });

        // Handle case where there are no headers or first block is text
        if (currentIntro && result.length === 0) {
            result.push({
                title: "Overview",
                content: currentIntro,
                variant: 'overview'
            });
        } else if (currentIntro) {
            // Prepend intro as overview if it's substantial
            result.unshift({
                title: "Overview",
                content: currentIntro,
                variant: 'overview'
            });
        }

        return result;
    }, [md]);

    if (sections.length === 0) {
        return (
            <div className="prose prose-invert prose-sm max-w-none opacity-50 italic">
                No instructions available.
            </div>
        );
    }

    return (
        <div className="instruction-briefing space-y-6 pb-20">
            {sections.map((section, idx) => (
                <BriefingCard 
                    key={`${section.title}-${idx}`}
                    variant={section.variant}
                    title={section.title}
                >
                    <ReactMarkdown 
                        remarkPlugins={remarkPlugins || [remarkGfm]}
                        components={components}
                    >
                        {section.content}
                    </ReactMarkdown>
                </BriefingCard>
            ))}
        </div>
    );
}

function mapTitleToVariant(title: string): BriefingCardVariant {
    const t = title.toLowerCase();
    
    if (t.includes('mission') || t.includes('goal') || t.includes('objective')) {
        return 'mission';
    }
    
    if (t.includes('requirement') || t.includes('criteria') || t.includes('checklist')) {
        return 'requirements';
    }
    
    if (t.includes('workflow') || t.includes('steps') || t.includes('process') || t.includes('guide')) {
        return 'workflow';
    }
    
    if (t.includes('watch') || t.includes('warning') || t.includes('caution') || t.includes('important')) {
        return 'watch';
    }
    
    return 'overview';
}
