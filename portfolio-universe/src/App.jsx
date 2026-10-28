import { useEffect, useState } from 'react'
import { defaultPortfolio, defaultPreferences } from './data/portfolio.js'
import { portfolioKey, readStored, savePortfolio, savePreferences } from './lib/storage.js'

const sections = [
  { id: 'overview', label: 'Home', icon: '⌂' },
  { id: 'skills', label: 'Skills', icon: '✳' },
  { id: 'projects', label: 'Work', icon: '◈' },
  { id: 'timeline', label: 'Timeline', icon: '⌁' },
  { id: 'journal', label: 'Notes', icon: '▤' },
]
const copy = (value) => JSON.parse(JSON.stringify(value))

function validateArchive(value) {
  if (!value || typeof value !== 'object' || !value.profile || typeof value.profile !== 'object') {
    throw new Error('Add a profile object before saving.')
  }
  for (const key of ['skills', 'projects', 'milestones', 'journal']) {
    if (!Array.isArray(value[key])) throw new Error('The "' + key + '" section must be a list.')
  }
  return value
}

function MapArt({ small = false }) {
  return <div className={'map-art ' + (small ? 'map-art-small' : '')} aria-hidden="true">
    <div className="map-halftone" />
    <svg viewBox="0 0 360 250" role="presentation">
      <path className="map-route" d="M30 202 C65 189 66 165 98 167 S130 195 155 164 S194 136 207 112 S240 85 267 99 S295 145 333 43" />
      <path className="map-route-shadow" d="M30 202 C65 189 66 165 98 167 S130 195 155 164 S194 136 207 112 S240 85 267 99 S295 145 333 43" />
      <path className="map-slash" d="M249 29 L328 3" /><path className="map-slash thin" d="M276 43 L344 20" />
      <circle className="map-point point-a" cx="98" cy="167" r="7" /><circle className="map-point point-b" cx="207" cy="112" r="7" /><circle className="map-point point-c" cx="333" cy="43" r="9" />
      <path className="map-asterisk" d="M53 71 L53 96 M41 83 L65 83 M45 75 L61 91 M61 75 L45 91" />
      <text x="26" y="225">START WHERE YOU ARE</text><text x="214" y="132">NEXT THING</text><text x="273" y="68">IN PROGRESS</text>
    </svg>
    <span className="map-stamp">01<span>FIELD MAP</span></span>
  </div>
}


function OpeningSequence({ effects, onComplete }) {
  const [phase, setPhase] = useState('charge')

  useEffect(() => {
    if (!effects || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      onComplete()
      return undefined
    }
    const strike = window.setTimeout(() => setPhase('strike'), 840)
    const transform = window.setTimeout(() => setPhase('transform'), 1510)
    const reveal = window.setTimeout(() => setPhase('reveal'), 2220)
    const finish = window.setTimeout(onComplete, 4050)
    return () => {
      window.clearTimeout(strike)
      window.clearTimeout(transform)
      window.clearTimeout(reveal)
      window.clearTimeout(finish)
    }
  }, [effects, onComplete])

  return <div className={'opening-sequence phase-' + phase} role="region" aria-label="Animated opening sequence">
    <div className="opening-speedlines" aria-hidden="true" />
    <div className="opening-aura" aria-hidden="true" />
    <div className="opening-rings" aria-hidden="true"><i /><i /><i /><i /></div>
    <div className="opening-particles" aria-hidden="true">{Array.from({ length: 14 }, (_, index) => <i key={index} />)}</div>
    <svg className="ichigo-art" viewBox="0 0 420 520" role="presentation" aria-hidden="true">
      <g className="ichigo-bankai">
        <path className="ichigo-coat" d="M164 182 L232 177 L269 251 L324 341 L279 359 L250 317 L259 485 L119 485 L137 321 L99 371 L56 344 L133 244 Z" />
        <path className="ichigo-coat-fold" d="M165 190 L188 285 L157 321 L175 484 L131 484 L141 321 L116 349 L138 252 Z" />
        <path className="ichigo-neck" d="M169 139 L231 139 L231 193 L202 220 L169 190 Z" />
        <path className="ichigo-face" d="M159 72 Q201 43 244 75 L239 139 Q220 173 196 172 Q170 159 160 131 Z" />
        <path className="ichigo-hair" d="M158 104 L125 87 L151 81 L127 55 L164 69 L160 30 L187 62 L205 17 L218 61 L250 37 L239 75 L273 73 L244 102 L238 124 L222 96 L207 115 L191 92 L175 116 L163 95 Z" />
        <path className="ichigo-brow" d="M212 111 L238 105" />
        <path className="ichigo-eye" d="M219 122 L235 119" />
        <path className="ichigo-blade" d="M246 229 L350 55 L372 65 L277 251 Z" />
        <path className="ichigo-blade-edge" d="M350 55 L372 65 L365 78 L343 68 Z" />
        <path className="ichigo-hilt" d="M232 244 L254 210 L272 221 L250 255 Z" />
      </g>
      <g className="ichigo-salvation">
        <path className="salvation-horn" d="M226 114 C269 84 301 47 307 7 C281 35 255 49 232 50 C249 71 241 92 226 114 Z" />
        <path className="salvation-mask" d="M218 92 Q249 104 241 138 Q231 161 204 169 L218 141 L199 150 L205 126 L188 135 L199 111 Z" />
        <path className="salvation-ridge" d="M150 70 L165 48 L180 69 L192 43 L207 69 L220 42 L233 68 L251 54 L246 93 L230 84 L215 103 L198 84 L181 104 L166 83 Z" />
        <path className="salvation-cross" d="M164 236 L220 221 L246 326 L187 344 Z" />
        <path className="salvation-stripe" d="M204 118 L231 112" />
        <path className="salvation-eye" d="M213 121 L236 114" />
      </g>
    </svg>
    <div className="opening-blade-trail" aria-hidden="true" />
    <div className="opening-impact" aria-hidden="true" />
    <button className="opening-skip" onClick={onComplete} aria-label="Skip opening animation"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19" /></svg></button>
  </div>
}

function Intro({ siteName, effects, onEnter }) {
  return <main className={'intro-screen ' + (!effects ? 'no-effects' : '')}>
    <div className="intro-topline"><span className="wordmark">{String(siteName || 'A').slice(0, 1).toUpperCase()}<span>·</span></span><span>PERSONAL ARCHIVE / VOL. 01</span><span className="online"><i /> OPEN FILE</span></div>
    <div className="intro-layout">
      <section className="intro-copy">
        <p className="eyebrow"><i /> CHAPTER 01 / IN PROGRESS</p>
        <h1>Welcome to<br /><em>{siteName}.</em></h1>
        <p className="intro-description">Things I’m learning. Things I’ve made. Notes I want to keep. A personal archive that gets to change as I do.</p>
        <button className="primary-button enter-button" onClick={onEnter}><span>OPEN THE FILE</span><b>↗</b></button>
        <div className="intro-footnote"><span>VOL. 01</span><span>START WHERE YOU ARE</span></div>
      </section>
      <section className="portal-stage" aria-label="Original route illustration">
        <MapArt />
        <div className="portal-caption"><span>FIELD MAP / 001</span><span>NO FINISH LINE</span></div>
      </section>
    </div>
    <div className="intro-bottom"><span>WORK IN PROGRESS, BY DESIGN.</span><span>MADE FOR MY OWN CURIOSITY.</span></div>
  </main>
}

function Sidebar({ active, onSelect, profile, siteName }) {
  return <aside className="sidebar">
    <a href="#home" className="brand" onClick={(event) => { event.preventDefault(); onSelect('overview') }}>
      <span className="brand-emblem">{String(siteName || 'A').slice(0, 1).toUpperCase()}</span><span className="brand-name">{siteName.toUpperCase()}<small>PERSONAL ARCHIVE</small></span>
    </a>
    <nav className="side-nav" aria-label="Main navigation">{sections.map((section) =>
      <button key={section.id} className={'nav-item ' + (active === section.id ? 'active' : '')} onClick={() => onSelect(section.id)}>
        <span className="nav-icon">{section.icon}</span>{section.label}
      </button>)}
    </nav>
    <div className="sidebar-spacer" />
    <div className="side-quest"><span className="quest-orbit">✳</span><div className="nav-label">RIGHT NOW</div><strong>{profile.status}</strong><small>LEVEL {profile.level} · SAVE FILE 01</small></div>
    <div className="sidebar-profile"><div className="avatar">{(profile.name || 'Y').trim().slice(0, 1).toUpperCase()}</div>
      <div><strong>{profile.name}</strong><small>MY CORNER OF THE INTERNET</small></div>
    </div>
  </aside>
}

function Topbar({ active, onEdit, onPrefs, onReplay }) {
  const current = sections.find((section) => section.id === active)
  return <header className="topbar">
    <div className="breadcrumb"><span>FILE 001</span><b>/</b><strong>{current?.label.toUpperCase()}</strong></div>
    <div className="topbar-actions"><span className="save-indicator"><i /> SAVED ON THIS DEVICE</span>
      <button className="icon-button" onClick={onReplay} aria-label="Replay opening page" title="Replay opening">↺</button>
      <button className="icon-button" onClick={onPrefs} aria-label="Preferences" title="Preferences">⚙</button>
      <button className="edit-button" onClick={onEdit}><span>✎</span> EDIT FILE</button>
    </div>
  </header>
}

function SectionHeading({ eyebrow, title, subtitle }) {
  return <div className="section-heading"><p className="eyebrow">{eyebrow}</p><h2>{title}</h2><p className="section-subtitle">{subtitle}</p></div>
}

function Overview({ data, setActive }) {
  const { profile } = data
  const xpPercent = Math.min(100, Math.round((profile.xp / Math.max(1, profile.nextLevelXp)) * 100))
  const focusSkill = data.skills[0]
  const latestProject = data.projects[0]
  const latestNote = data.journal[0]
  return <>
    <section className="hero-card">
      <div className="hero-copy">{profile.status && <div className="hero-status"><i /> {profile.status}</div>}
        <h1>{profile.title}</h1><p className="hero-bio">{profile.bio}</p>
        <div className="hero-meta">{profile.location && <span>⌖ {profile.location}</span>}<span>LEVEL {profile.level}</span></div>
      </div>
      <div className="hero-art"><div className="hero-art-label">A MAP THAT CAN CHANGE <span>↗</span></div><MapArt small />
        <div className="hero-art-coord">THE NEXT THING<br />IS UP TO YOU</div><div className="hero-art-stamp">{String(profile.level).padStart(2, '0')}<small>LVL</small></div>
      </div>
    </section>
    <section className="dashboard-grid">
      <article className="panel level-panel"><div className="panel-heading"><div><p className="eyebrow">SAVE FILE / GROWTH</p><h3>Level {profile.level} <span>·</span> In progress</h3></div><span className="panel-symbol">↗</span></div>
        <div className="level-meta"><span>EXPERIENCE POINTS</span><span>{profile.xp} <i>/</i> {profile.nextLevelXp} XP</span></div>
        <div className="xp-track"><i style={{ width: xpPercent + '%' }} /></div>
        <div className="level-footer"><span>THE NEXT LEVEL IS {profile.level + 1}</span><span>{Math.max(0, profile.nextLevelXp - profile.xp)} XP TO GO</span></div>
      </article>
      <article className="panel stat-panel"><span className="stat-symbol">✳</span><span className="stat-label">ON THE SKILL TREE</span><strong className="stat-name">{focusSkill?.name || 'Add your first skill'}</strong><button onClick={() => setActive('skills')}>SEE SKILLS <b>↗</b></button></article>
      <article className="panel stat-panel mint"><span className="stat-symbol">◈</span><span className="stat-label">ON THE WORKBENCH</span><strong className="stat-name">{latestProject?.name || 'Add your first project'}</strong><button onClick={() => setActive('projects')}>SEE PROJECTS <b>↗</b></button></article>
    </section>
    <section className="overview-lower">
      <article className="panel skills-preview"><div className="panel-heading"><div><p className="eyebrow">CURRENTLY LEARNING</p><h3>Skills on my mind</h3></div><button className="text-link" onClick={() => setActive('skills')}>ALL SKILLS ↗</button></div>
        <div className="mini-skills">{data.skills.length ? data.skills.slice(0, 3).map((skill) => <div className="mini-skill" key={skill.id}><span className="skill-glyph">{skill.icon}</span><div className="mini-skill-main"><div><strong>{skill.name}</strong><small>{skill.rank}</small></div><div className="mini-track"><i style={{ width: skill.progress + '%' }} /></div></div></div>) : <p className="inline-empty">Your board is clear. Add a skill when you’re ready.</p>}</div>
      </article>
      <article className="panel active-quest"><div className="panel-heading"><div><p className="eyebrow">LATEST NOTE</p><h3>{latestNote?.title || 'Nothing written yet'}</h3></div><button className="text-link" onClick={() => setActive('journal')}>OPEN NOTES ↗</button></div>
        <p className="latest-note">{latestNote?.text || 'Keep a thought here when there’s one you want to return to.'}</p><div className="quest-author"><i /> {latestNote?.mood || 'YOUR LOGBOOK'}</div>
      </article>
    </section>
  </>
}
function SkillsView({ skills }) {
  return <><SectionHeading eyebrow="THINGS I’M LEARNING" title="Skill tree" subtitle="A progress board for skills I want to keep growing." />
    {skills.length ? <div className="skills-grid">{skills.map((skill, index) => <article className="panel skill-card" key={skill.id}>
      <div className="skill-card-top"><span className="skill-glyph large">{skill.icon}</span><span className="tag">{skill.category}</span><span className="skill-index">0{index + 1}</span></div>
      <h3>{skill.name}</h3><p>{skill.detail}</p><div className="skill-rank"><span>{skill.rank}</span><span>{skill.progress}%</span></div>
      <div className="xp-track"><i style={{ width: skill.progress + '%' }} /></div><div className="skill-foot"><span>PROGRESS</span><span>{skill.progress < 30 ? 'STARTING' : skill.progress < 70 ? 'IN PRACTICE' : 'GROWING'}</span></div>
    </article>)}</div> : <EmptyState text="Add your first skill in Edit File." />}
  </>
}

function ProjectsView({ projects }) {
  return <><SectionHeading eyebrow="THINGS I’VE MADE OR WANT TO MAKE" title="The workbench" subtitle="Projects, experiments, and ideas worth keeping." />
    {projects.length ? <div className="projects-grid">{projects.map((project, index) => <article className={'project-card project-' + (project.color || 'violet')} key={project.id}>
      <div className="project-art"><div className="project-art-grid" /><span className="project-glyph">{['◈', '⌁', '✳', '◇'][index % 4]}</span>
        <span className="project-art-number">FILE {String(index + 1).padStart(2, '0')}</span><span className="tag">{project.status}</span></div>
      <div className="project-copy"><p className="eyebrow">{project.type}</p><h3>{project.name}</h3><p>{project.description}</p>
        <div className="project-tags">{project.tags.map((tag) => <span className="tag" key={tag}>{tag}</span>)}</div>
        {project.link && <a className="project-link" href={project.link} target="_blank" rel="noreferrer">OPEN PROJECT ↗</a>}
      </div>
    </article>)}</div> : <EmptyState text="Add a project to the workbench in Edit File." />}
  </>
}

function TimelineView({ milestones }) {
  return <><SectionHeading eyebrow="SAVE POINTS" title="Timeline" subtitle="Small beginnings count. Leave room for what happens next." />
    {milestones.length ? <div className="timeline">{milestones.map((milestone, index) => <article className="timeline-entry" key={milestone.id}>
      <div className="timeline-rail"><span className={'timeline-node ' + (milestone.kind || '')}>{index === 0 ? '✦' : String(index + 1).padStart(2, '0')}</span>{index < milestones.length - 1 && <i />}</div>
      <div className="panel timeline-card"><div className="timeline-date">{milestone.date}<span> / NOTE {String(index + 1).padStart(2, '0')}</span></div><h3>{milestone.title}</h3><p>{milestone.detail}</p></div>
    </article>)}</div> : <EmptyState text="Add a memory or future save point in Edit File." />}
  </>
}
function JournalView({ entries }) {
  return <><SectionHeading eyebrow="PRIVATE, LOCAL NOTES" title="Personal log" subtitle="Things I want to remember. Kept on this device." />
    {entries.length ? <div className="journal-list">{entries.map((entry, index) => <article className="panel journal-entry" key={entry.id}>
      <div className="journal-index">{String(index + 1).padStart(2, '0')}<span>LOG</span></div>
      <div className="journal-body"><div className="journal-meta"><span>{entry.date}</span><span className="tag">{entry.mood}</span></div><h3>{entry.title}</h3><p>{entry.text}</p></div><span className="journal-mark">↗</span>
    </article>)}</div> : <EmptyState text="Add a note in Edit File. Notes stay on this device." />}
  </>
}
function EmptyState({ text }) { return <div className="panel empty-state"><span>✧</span><p>{text}</p></div> }

function EditorModal({ data, onClose, onSave }) {
  const [draft, setDraft] = useState(JSON.stringify(data, null, 2))
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const handleSave = () => {
    try { onSave(validateArchive(JSON.parse(draft))); setError(''); setNotice('File saved in this browser.') }
    catch (reason) { setError(reason instanceof SyntaxError ? 'There is a formatting issue in the JSON. Check commas, quotes, and brackets.' : reason.message); setNotice('') }
  }
  const handleExport = () => {
    const file = new Blob([draft], { type: 'application/json' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(file)
    link.download = 'personal-archive.json'
    link.click()
    URL.revokeObjectURL(link.href)
  }
  const handleAdd = (key) => {
    try {
      const next = JSON.parse(draft)
      const templates = {
        skills: { id: 'skill-' + Date.now(), name: 'New skill', category: 'LEARN', rank: 'Starting', progress: 0, icon: '✳', detail: 'Write a short note about this skill.' },
        projects: { id: 'project-' + Date.now(), name: 'New project', type: 'PERSONAL PROJECT', status: 'In progress', color: 'orange', description: 'Write what this project is about.', tags: [], link: '' },
        milestones: { id: 'milestone-' + Date.now(), date: 'NEW SAVE POINT', title: 'A moment worth keeping', detail: 'Write a sentence about it.', kind: 'quest' },
        journal: { id: 'note-' + Date.now(), date: 'NEW NOTE', title: 'A note to myself', text: 'Write what you want to remember.', mood: 'Curious' },
      }
      next[key].push(templates[key])
      setDraft(JSON.stringify(next, null, 2))
      setNotice('Added a starter entry. Edit its fields, then save.')
      setError('')
    } catch {
      setError('Save or fix the JSON before adding an entry.')
      setNotice('')
    }
  }
  const handleReset = () => {
    const fresh = copy(defaultPortfolio)
    setDraft(JSON.stringify(fresh, null, 2))
    onSave(fresh)
    setError('')
    setNotice('Starter archive restored and saved.')
  }
  return <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose() }}>
    <section className="editor-modal" role="dialog" aria-modal="true" aria-labelledby="editor-title">
      <div className="modal-head"><div><p className="eyebrow">MAKE IT YOURS</p><h2 id="editor-title">Edit file</h2></div><button className="icon-button close-button" onClick={onClose} aria-label="Close editor">×</button></div>
      <p className="modal-intro">Edit your profile, skills, projects, timeline, and notes as JSON. Changes are saved in this browser.</p>
      <div className="editor-toolbar"><span><i /> {portfolioKey()}</span><button className="subtle-button" onClick={handleExport}>↓ EXPORT JSON</button></div>
      <div className="editor-add-row"><span>ADD A NEW ENTRY</span><div><button className="subtle-button" onClick={() => handleAdd('skills')}>+ SKILL</button><button className="subtle-button" onClick={() => handleAdd('projects')}>+ PROJECT</button><button className="subtle-button" onClick={() => handleAdd('milestones')}>+ MILESTONE</button><button className="subtle-button" onClick={() => handleAdd('journal')}>+ NOTE</button></div></div>
      <textarea className="json-editor" spellCheck="false" value={draft} onChange={(event) => { setDraft(event.target.value); setError(''); setNotice('') }} aria-label="Portfolio data JSON" />
      {error && <p className="editor-message error">{error}</p>}{notice && <p className="editor-message success">{notice}</p>}
      <div className="modal-actions"><button className="subtle-button reset-button" onClick={handleReset}>RESTORE STARTER</button><div><button className="subtle-button" onClick={onClose}>CLOSE</button><button className="primary-button save-button" onClick={handleSave}>SAVE CHANGES <span>↗</span></button></div></div>
    </section>
  </div>
}

function PreferencesModal({ preferences, onUpdate, onClose }) {
  return <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose() }}>
    <section className="preferences-modal" role="dialog" aria-modal="true" aria-labelledby="preferences-title">
      <div className="modal-head"><div><p className="eyebrow">TUNE THE PAGE</p><h2 id="preferences-title">Preferences</h2></div><button className="icon-button close-button" onClick={onClose} aria-label="Close preferences">×</button></div>
      <div className="preference-row"><div><strong>Ambient motion</strong><p>Small movement in the route illustration.</p></div><button className={'toggle ' + (preferences.effects ? 'on' : '')} onClick={() => onUpdate({ ...preferences, effects: !preferences.effects })} role="switch" aria-checked={preferences.effects} aria-label="Toggle ambient motion"><i /></button></div>
      <div className="preference-row"><div><strong>Accent color</strong><p>Choose the small flash of color.</p></div><div className="accent-options">{['orange', 'violet', 'teal'].map((accent) => <button key={accent} className={'accent-swatch ' + accent + ' ' + (preferences.accent === accent ? 'selected' : '')} onClick={() => onUpdate({ ...preferences, accent })} aria-label={'Set ' + accent + ' accent'} aria-pressed={preferences.accent === accent} />)}</div></div>
      <div className="preference-row"><div><strong>Replay the opening</strong><p>Return to the first page.</p></div><button className="subtle-button" onClick={() => { onUpdate({ ...preferences, hasEntered: false }); onClose() }}>REPLAY ↗</button></div>
      <div className="preferences-note"><span>◉</span> Your preferences stay on this device.</div>
    </section>
  </div>
}

function isOldStarter(value) {
  return value?.profile?.name === 'Your Name'
    && value?.profile?.title === 'Collecting skills. Building worlds.'
    && value?.projects?.some((project) => project.name === 'Lumen Atlas')
}

function loadArchive() {
  const saved = readStored('elsewhere:portfolio:v1', null)
  return saved && !isOldStarter(saved) ? saved : copy(defaultPortfolio)
}

function loadPreferences() {
  const saved = readStored('elsewhere:preferences:v1', null)
  if (!saved) return copy(defaultPreferences)
  const previousArchive = readStored('elsewhere:portfolio:v1', null)
  return isOldStarter(previousArchive) && saved.accent === 'violet' ? { ...saved, accent: 'orange' } : saved
}
export default function App() {
  const [data, setData] = useState(loadArchive)
  const [preferences, setPreferences] = useState(loadPreferences)
  const [loading, setLoading] = useState(true)
  const [active, setActive] = useState('overview')
  const [editorOpen, setEditorOpen] = useState(false)
  const [preferencesOpen, setPreferencesOpen] = useState(false)
  const accent = ['orange', 'violet', 'teal', 'amber'].includes(preferences.accent) ? preferences.accent : 'orange'
  const siteName = data.siteName || 'Afterimage'

  useEffect(() => { savePortfolio(data) }, [data])
  useEffect(() => { savePreferences(preferences) }, [preferences])
  useEffect(() => { document.title = siteName + ' — Personal Archive' }, [siteName])

  if (!preferences.hasEntered) return <>{loading && <OpeningSequence effects={preferences.effects} onComplete={() => setLoading(false)} />}<div className={'app-shell accent-' + accent}><Intro siteName={siteName} effects={preferences.effects} onEnter={() => setPreferences((current) => ({ ...current, hasEntered: true }))} /></div></>

  return <>{loading && <OpeningSequence effects={preferences.effects} onComplete={() => setLoading(false)} />}<div className={'app-shell accent-' + accent + (!preferences.effects ? ' no-effects' : '')}>
    <div className="ambient ambient-one" /><div className="ambient ambient-two" /><div className="site-grid" />
    <div className="app-layout"><Sidebar active={active} onSelect={setActive} profile={data.profile} siteName={siteName} /><main className="main-area">
      <Topbar active={active} onEdit={() => setEditorOpen(true)} onPrefs={() => setPreferencesOpen(true)} onReplay={() => setPreferences((current) => ({ ...current, hasEntered: false }))} />
      <div className="content-area">{active === 'overview' && <Overview data={data} setActive={setActive} />}{active === 'skills' && <SkillsView skills={data.skills} />}{active === 'projects' && <ProjectsView projects={data.projects} />}{active === 'timeline' && <TimelineView milestones={data.milestones} />}{active === 'journal' && <JournalView entries={data.journal} />}</div>
      <footer className="site-footer"><span>{siteName.toUpperCase()} <i>·</i> WORK IN PROGRESS, BY DESIGN</span><span>{data.profile.location && data.profile.location + ' · '}LOCAL FILE</span></footer>
    </main></div>
    {editorOpen && <EditorModal data={data} onClose={() => setEditorOpen(false)} onSave={(next) => setData(copy(next))} />}
    {preferencesOpen && <PreferencesModal preferences={preferences} onUpdate={setPreferences} onClose={() => setPreferencesOpen(false)} />}
  </div></>
}


