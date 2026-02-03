# Media & Embeds: Bring Content to Life

## Outcome

In this quest, you'll embed rich media (video, audio) and external content (iframes) into your pages, understanding controls, fallbacks, accessibility considerations, and performance best practices.

## Concept in 30 seconds

HTML5's `<video>` and `<audio>` elements provide native media playback with `controls` attribute for UI. The `<iframe>` element embeds external content like maps or YouTube videos. Always provide fallback content and consider accessibility (captions) and performance (lazy loading).

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/html-media-embed/terms.json) and linked to the Codex:

- **video** - Element for embedding video content with controls
- **audio** - Element for embedding sound content
- **iframe** - Inline frame for embedding external content
- **controls attribute** - Displays playback controls for media
- **fallback content** - Content displayed if media cannot be loaded

## Walkthrough

1. **Add video with controls**: `<video src="video.mp4" controls>`
2. **Provide multiple formats**: Use `<source>` for browser compatibility
3. **Include captions**: Add `<track>` with WebVTT subtitle file
4. **Embed audio**: Similar to video but usually smaller file sizes
5. **Use iframes responsibly**: Embed YouTube, Google Maps with security attributes
6. **Add lazy loading**: `loading="lazy"` to defer offscreen content

## Example implementation

```html
<!-- Video with multiple sources and captions -->
<video controls width="640" height="360" poster="thumbnail.jpg">
  <source src="video.mp4" type="video/mp4">
  <source src="video.webm" type="video/webm">
  <track 
    kind="captions" 
    src="captions.vtt" 
    srclang="en" 
    label="English"
  >
  <p>Your browser doesn't support HTML5 video. 
     <a href="video.mp4">Download the video</a>.
  </p>
</video>

<!-- Audio with controls -->
<audio controls>
  <source src="podcast.mp3" type="audio/mpeg">
  <source src="podcast.ogg" type="audio/ogg">
  <p>Your browser doesn't support HTML5 audio.</p>
</audio>

<!-- YouTube embed (secure iframe) -->
<iframe 
  width="560" 
  height="315" 
  src="https://www.youtube-nocookie.com/embed/VIDEO_ID" 
  title="Video title"
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
  allowfullscreen
  loading="lazy"
></iframe>

<!-- Google Maps embed -->
<iframe 
  src="https://www.google.com/maps/embed?pb=..." 
  width="600" 
  height="450" 
  style="border:0;" 
  allowfullscreen="" 
  loading="lazy" 
  referrerpolicy="no-referrer-when-downgrade"
  title="Office location map"
></iframe>
```

## Common mistakes

- **No fallback content**: Users with unsupported browsers see nothing
- **Missing captions**: Videos without captions exclude deaf/hard-of-hearing users
- **Autoplaying media**: Violates WCAG, annoys users, wastes mobile data
- **No iframe title**: Screen readers can't describe embedded content
- **Insecure iframes**: Missing `sandbox` attribute allows malicious scripts
- **Huge video files**: Not optimizing for web causes slow loading

## Deep dive

The `<track>` element links WebVTT (Web Video Text Tracks) caption files to video. Captions aren't just for deaf users—they help in noisy environments, during language learning, and improve SEO since search engines can index the text. The `kind` attribute supports `captions` (translations), `subtitles` (dialogue), `descriptions` (visual descriptions for blind users), and `chapters` (navigation markers).

The `poster` attribute on `<video>` displays an image before playback starts, improving perceived performance and giving users context about video content. Without it, browsers show the first frame, which might be black or mid-motion.

Iframe security requires careful attention. The sandbox attribute restricts what embedded content can do: `sandbox="allow-scripts allow-same-origin"` enables JavaScript and same-origin access,while omitting it blocks scripts, forms, popups, and more. For untrusted content, use restrictive sandboxing. The `loading="lazy"` attribute defers loading offscreen iframes, significantly improving initial page load performance.
