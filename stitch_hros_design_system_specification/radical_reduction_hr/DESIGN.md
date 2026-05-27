---
name: Radical Reduction HR
colors:
  surface: '#fcf8fa'
  surface-dim: '#ddd9db'
  surface-bright: '#fcf8fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f2f4'
  surface-container: '#f1edef'
  surface-container-high: '#ebe7e9'
  surface-container-highest: '#e5e1e3'
  on-surface: '#1c1b1d'
  on-surface-variant: '#47464c'
  inverse-surface: '#313032'
  inverse-on-surface: '#f4f0f2'
  outline: '#78767d'
  outline-variant: '#c8c5cd'
  surface-tint: '#5d5c74'
  primary: '#00000b'
  on-primary: '#ffffff'
  primary-container: '#1a1a2e'
  on-primary-container: '#83829b'
  inverse-primary: '#c6c4df'
  secondary: '#585f6c'
  on-secondary: '#ffffff'
  secondary-container: '#dce2f3'
  on-secondary-container: '#5e6572'
  tertiary: '#695d3c'
  on-tertiary: '#ffffff'
  tertiary-container: '#b9aa83'
  on-tertiary-container: '#493f20'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2e0fc'
  primary-fixed-dim: '#c6c4df'
  on-primary-fixed: '#1a1a2e'
  on-primary-fixed-variant: '#45455b'
  secondary-fixed: '#dce2f3'
  secondary-fixed-dim: '#c0c7d6'
  on-secondary-fixed: '#151c27'
  on-secondary-fixed-variant: '#404754'
  tertiary-fixed: '#f2e1b7'
  tertiary-fixed-dim: '#d5c59d'
  on-tertiary-fixed: '#231b02'
  on-tertiary-fixed-variant: '#514627'
  background: '#fcf8fa'
  on-background: '#1c1b1d'
  surface-variant: '#e5e1e3'
typography:
  display:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-md-bold:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '600'
    lineHeight: '1.5'
  label-sm:
    fontFamily: Geist
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.4'
  label-sm-bold:
    fontFamily: Geist
    fontSize: 13px
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: 0.01em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  huge: 64px
  mobile-margin: 24px
  touch-target-min: 44px
---

## Brand & Style
The design system is built on the principle of **Radical Reduction**. It serves as a calm, confident, and AI-native operating system for Indian enterprises. The goal is to strip away the traditional complexity of HR software, replacing it with a mobile-first, intentional interface that prioritizes progressive disclosure.

The aesthetic is **Minimalist-Professional**. It avoids decorative flourishes like gradients or heavy shadows in favor of structural clarity, precise hairline borders, and expansive whitespace. The emotional response should be one of "quiet efficiency"—the system feels like a dependable partner rather than a bureaucratic hurdle.

## Colors
The palette is restricted and functional. 
- **Primary (Deep Indigo):** Used for primary actions and brand anchoring. It conveys institutional trust.
- **Surface & Background:** A subtle distinction between `#F8F9FA` (app background) and `#FFFFFF` (interactive cards) creates depth without needing shadows.
- **Text:** High-contrast `#0D0D0D` for readability, with `#6B7280` reserved for metadata and secondary labels.
- **Semantic Colors:** Green, Amber, and Red are used strictly for status and "Readiness Signals," providing immediate visual orientation for task urgency.

## Typography
The design system utilizes **Geist** for its technical precision and geometric clarity, essential for a data-driven HR environment. 

The scale is intentionally stepped:
- **Display & Headlines:** Used for onboarding milestones and section titles.
- **Body:** Set at 16px to ensure accessibility on mobile devices (375px viewport).
- **Labels:** 13px for metadata, status pills, and micro-copy. 

We avoid "Medium" weights; use **Regular** for standard information and **Semibold** for hierarchy and emphasis.

## Layout & Spacing
This is a **Mobile-First** system optimized for a 375px base width. 
- **Grid:** A standard 4-column mobile grid with 24px side margins.
- **Spacing Rhythm:** Based on a 4px modular scale. Use `lg (24px)` for primary content padding and `md (16px)` for internal card spacing.
- **Touch Targets:** All interactive elements (buttons, inputs, checkboxes) must maintain a minimum height/width of `44px` to ensure usability in "on-the-go" enterprise scenarios.
- **Progressive Disclosure:** Layouts should start with essential info and expand using accordions or bottom sheets to prevent cognitive overload.

## Elevation & Depth
In line with the "Radical Reduction" philosophy, this design system avoids traditional shadows. 
- **Hairline Borders:** Use 1px borders in a slightly darker neutral than the background (e.g., `#E5E7EB`) to define containers.
- **Tonal Elevation:** Depth is communicated by placing `#FFFFFF` surfaces on the `#F8F9FA` background. 
- **Interactive States:** On tap/click, elements can shift slightly in background color (e.g., a subtle grey tint) rather than lifting off the page.
- **AI Concierge:** This is the only element permitted a subtle, highly diffused "Ambient Shadow" to signify it exists on a separate, persistent interaction plane.

## Shapes
The shape language is **Rounded**, balancing the technical nature of the font with a sense of approachability. 
- **Cards & Inputs:** 0.5rem (8px) corner radius.
- **Status Pills:** Fully pill-shaped (rounded-full) to distinguish them from interactive buttons.
- **Selection Indicators:** Use soft circular shapes for progress rings and radio buttons.

## Components
- **Task Card:** The central unit. White surface, hairline border. Contains: Title (Body-Bold), Purpose (Label-SM), Deadline (Label-SM + Icon), and a Status Pill. 
- **Status Pill:** Small, 13px text, semibold. Backgrounds are low-opacity versions of semantic colors (e.g., 10% Green for "Verified") with high-contrast text.
- **Readiness Signal:** A 12px circular dot placed next to section headers. Green (Ready), Amber (Action Needed), Red (Blocked).
- **Upload Zone:** Large touch-friendly area. Icons for "Camera" and "File" are clearly separated. Primary action triggers the native mobile camera.
- **AI Concierge Trigger:** A floating button at the bottom-right. It should be distinctive—either using the Primary color or a unique icon—to signal it is the "intelligent layer" of the OS.
- **DPDP Consent Block:** High-density text area for Indian DPDP compliance. Requires a clear border and a mandatory checkbox. Use `Label-SM` for legal text to keep it readable but secondary.
- **Declaration Confirm:** A fixed bottom-bar containing a Checkbox and a full-width Primary CTA button (44px height).
- **Section Progress:** A thin horizontal bar at the top of the viewport or a small ring inside cards to show completion percentage.