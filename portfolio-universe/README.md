# Afterimage — Personal Archive

A React + Vite personal portfolio with a high-contrast manga-inspired art direction: ink, paper, orange accents, and original route illustrations. On startup, an original SVG/CSS fan-art sequence depicts Ichigo changing from Bankai to Horn of Salvation. It uses no source frames, official logos, or music. Starter portfolio content is intentionally blank so the site does not invent your story.

## Run locally

Install Node.js 20.19+ or 22.12+, then from this folder run:

1. npm install
2. npm run dev
3. Open the local address printed by Vite.

To create a production build, run npm run build. To preview the build, run npm run preview.

## Customize the archive

- Edit src/data/portfolio.js to change the starter profile, skills, projects, milestones, and journal entries.
- Choose Edit File in the website to edit the archive as JSON. Quick-add buttons create starter entries for skills, projects, milestones, and notes. Save stores changes in this browser. Export downloads a JSON backup; Restore Starter clears your content and returns to the blank setup.
- Choose the gear icon for ambient motion, accent color, and the cinematic intro. The startup sequence respects the motion preference and can be skipped.
- The archive and preferences are saved in this browser local storage. They are not sent to a server.

If you edit the starter data module after already saving in the browser, use Restore Starter to load the new defaults.

## Project structure

src/data/portfolio.js   Starter content and preference defaults
src/lib/storage.js      Local storage helpers
src/App.jsx             Screens, navigation, and edit/preferences panels
src/styles.css          Responsive visual system and motion
src/main.jsx            React entry point



