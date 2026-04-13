# Design System: AgaShop Premium

Ce document définit l'identité visuelle professionnelle de l'application AgaShop, suivant les standards de design SaaS modernes.

## 1. Visual Theme & Atmosphere
- **Mood:** Professionnel, Robuste, de Confiance.
- **Aesthetic:** Minimalisme moderne, typographie forte, espacement généreux.
- **Vibe:** "Business-ready", orienté efficacité.

## 2. Color Palette & Roles
- **Primary Deep** (#0F172A) – Couleur de marque principale, utilisée pour le texte fort et les bases sombres.
- **Primary Active** (#2563EB) – Couleur d'action, boutons principaux, états actifs.
- **Secondary Orange** (#F97316) – Alertes constructives, points d'attention.
- **Background Light** (#F8FAFC) – Fond de page principal.
- **Surface White** (#FFFFFF) – Cartes, barres de navigation.
- **Border Soft** (rgba(0, 0, 0, 0.05)) – Délimitations discrètes.

## 3. Typography Rules
- **Headings:** `Outfit`, sans-serif. Poids : 600 ou 700.
- **Body:** `Inter`, sans-serif. Poids : 400 ou 500.
- **Monospace:** `JetBrains Mono` (pour les codes ou données techniques).

## 4. Component Stylings
- **Buttons:** Coins arrondis (12px), ombre portée subtile lors du survol.
- **Cards:** Fond blanc, coins arrondis (16px), bordure fine (1px solid #E2E8F0), ombre douce.
- **Inputs:** Fond neutre (#F1F5F9), bordure au focus (#2563EB), coins (10px).

## 5. Layout Principles
- **Margins:** Multiples de 8px (Grille de 8).
- **Glassmorphism:** Appliqué sur le Header et les éléments flottants (backdrop-filter: blur(12px)).
- **Transitions:** Bézier cubique doux (0.4s, cubic-bezier(0.4, 0, 0.2, 1)).

## 6. Design System Notes for Stitch Generation
**DESIGN SYSTEM (REQUIRED):**
- Platform: Mobile (Ionic/Vue), Mobile-first.
- Theme: Light/Clean, Premium Business.
- Background: #F8FAFC
- Primary Accent: #2563EB
- Text Primary: #0F172A
- Font: Inter (Body), Outfit (Headings)
- Layout: Balanced, high density but breathable.
