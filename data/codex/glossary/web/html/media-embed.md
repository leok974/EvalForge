---
id: web/html/media-embed
title: HTML Media and Embeds
category: html
tags: [html, media, video, audio, iframe]
---

# HTML Media and Embeds

Embedding media and external content in web pages.

## Video

```html
<video controls width="640" height="360">
  <source src="video.mp4" type="video/mp4">
  <source src="video.webm" type="video/webm">
  Your browser doesn't support video.
</video>
```

### Video Attributes

- **`controls`**: Show play/pause/volume controls
- **`autoplay`**: Start playing automatically (use sparingly)
- **`loop`**: Repeat video
- **`muted`**: Mute audio (required for autoplay)
- **`poster`**: Thumbnail image before play

## Audio

```html
<audio controls>
  <source src="audio.mp3" type="audio/mpeg">
  <source src="audio.ogg" type="audio/ogg">
  Your browser doesn't support audio.
</audio>
```

## Iframes

Embed external content:

```html
<iframe 
  src="https://example.com" 
  title="Description"
  width="600" 
  height="400"
  loading="lazy">
</iframe>
```

### Common Uses

- Embedded maps
- YouTube/Vimeo videos
- Third-party widgets
- External documents

### Security Attributes

```html
<iframe 
  src="..."
  sandbox="allow-scripts allow-same-origin"
  allow="autoplay; fullscreen">
</iframe>
```

## Best Practices

- Always provide fallback content
- Include multiple formats for compatibility
- Use `loading="lazy"` for performance
- Add `title` attribute to iframes
- Consider accessibility (captions, transcripts)
- Optimize file sizes
- Use appropriate `sandbox` restrictions for iframes

## Accessibility

```html
<video controls>
  <track kind="captions" src="captions.vtt" srclang="en" label="English">
  <source src="video.mp4">
</video>
```
