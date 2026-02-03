# Colors & Backgrounds: Visual Hierarchy

## Outcome

In this quest, you'll master CSS color formats (hex, rgb, hsl) and background properties to create accessible, visually appealing designs with proper contrast, gradients, and layered backgrounds.

## Concept in 30 seconds

Colors can be specified as **hex** (#FF0000), **rgb** (255, 0, 0), or **hsl** (0, 100%, 50%). Always ensure 4.5:1 contrast ratio for accessibility. Backgrounds support colors, images, gradients, and multiple layers with control over size, position, and repeat.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/css-colors-backgrounds/terms.json) and linked to the Codex:

- **hex color** - Hexadecimal color format like #FF0000
- **rgb** - Red, green, blue color values
- **contrast** - Difference between text and background for readability
- **background-image** - Property for adding image backgrounds
- **background-size** - Controls how background image scales

## Walkthrough

1. **Use semantic color variables**: Define colors in `:root` with CSS custom properties
2. **Check contrast**: Ensure 4.5:1 minimum for text (WCAG AA)
3. **Apply gradients**: `linear-gradient()` or `radial-gradient()`
4. **Layer backgrounds**: Multiple images/gradients with comma separation
5. **Control background size**: `cover` fills area, `contain` fits fully
6. **Set background position**: `center`, `top left`, or precise values

## Example implementation

```css
/* Color system with CSS variables */
:root {
  --primary: #3498db;
  --secondary: #2ecc71;
  --accent: #e74c3c;
  --text: #2c3e50;
  --background: #ecf0f1;
  --surface: #ffffff;
}

body {
  background-color: var(--background);
  color: var(--text);
}

/* Color formats */
.hex { color: #3498db; }
.rgb { color: rgb(52, 152, 219); }
.rgba { color: rgba(52, 152, 219, 0.8); }  /* Alpha for opacity */
.hsl { color: hsl(204, 70%, 53%); }
.hsla { color: hsla(204, 70%, 53%, 0.8); }

/* Background images */
.hero {
  background-image: url('/images/hero.jpg');
  background-size: cover;       /* Fill entire area */
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed; /* Parallax effect */
}

/* Gradients */
.gradient-linear {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.gradient-radial {
  background: radial-gradient(circle at center, #fff 0%, #000 100%);
}

/* Multiple backgrounds (front to back) */
.layered {
  background: 
    linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),  /* Dark overlay */
    url('/images/pattern.svg') repeat,                    /* Pattern */
    linear-gradient(to bottom, #4e54c8, #8f94fb);        /* Base gradient */
}

/* Shorthand */
.shorthand {
  background: var(--primary) url('/image.jpg') center/cover no-repeat;
}
```

**Accessible color contrast:**
- Normal text: 4.5:1 minimum
- Large text (18pt+): 3:1 minimum
- Use contrast checkers: WebAIM, Chrome DevTools

## Common mistakes

- **Poor contrast**: Gray text on white background fails accessibility
- **Not using variables**: Hardcoding colors makes theme changes difficult
- **Background without fallback**: Images fail to load, text becomes unreadable
- **Fixed backgrounds on mobile**: `background-attachment: fixed` performs poorly
- **Forgetting alpha channels**: Not using rgba/hsla when opacity needed

## Deep dive

HSL (Hue, Saturation, Lightness) is often more intuitive than RGB. Hue is a degree on the color wheel (0=red, 120=green, 240=blue), saturation is intensity (0%=gray, 100%=vivid), and lightness is brightness (0%=black, 50%=pure color, 100%=white). Adjusting lightness creates tints and shades while preserving hue.

CSS custom properties (variables) centralize color management: `--primary: #3498db` defined once, used everywhere with `var(--primary)`. Changing one variable updates the entire theme. You can even switch themes with JavaScript: `document.documentElement.style.setProperty('--primary', '#newColor')`.

The `background` shorthand packs many properties: `background: color image position/size repeat attachment`. Note the `/` between position and size: `center/cover` means "center positioned, cover sized."

Multiple backgrounds layer front-to-back: the first listed appears on top. This enables sophisticated effects like overlays on images: `linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('/image.jpg')` darkens the image without editing the file.

`background-size: cover` scales the image to cover the entire area (may crop), while `contain` scales to fit entirely within (may show empty space). For responsive hero images, `cover` is usually correct.

## Check yourself

Before moving on, verify you can:
- Explain the core concepts covered in this quest
- Identify common mistakes and how to avoid them
- Apply the techniques in your own projects
- Debug issues when things don't work as expected

